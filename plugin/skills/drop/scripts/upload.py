#!/usr/bin/env python3
"""Upload files to VC Brain without reading them into the conversation.

Standard library only, so it runs in any Claude code-execution sandbox. It prints file names,
sizes, MIME types and hashes, never file content.

  upload.py --list [DIR ...]       list files that look attached to this chat or task
  upload.py --prepare PATH ...     name, MIME type, size and SHA-256 for each file's request_upload call
  upload.py --check UPLOAD_URL     test that the sandbox can reach the upload host (egress)
  upload.py --put PLAN.json        PUT each file to its upload_url; the plan is a JSON list of
                                   {"path", "upload_url", "upload_headers"} ("-" reads stdin);
                                   the plan file is deleted afterwards
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

# Where attached files usually land. Neither path is officially documented: claude.ai and Cowork
# cloud sandboxes are reported to use /mnt/user-data/uploads, Cowork desktop an uploads/ folder in
# the session's working directory. Claude Code works in the current directory.
DEFAULT_DIRS = ["/mnt/user-data/uploads", "uploads", "."]
SKIP_NAMES = {".DS_Store", "desktop.ini", "Thumbs.db"}
# The types request_upload accepts (server/src/vcbrain/extract.py).
ACCEPTED = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".html": "text/html",
    ".htm": "text/html",
}
MAX_LISTED = 50
TIMEOUT = 120


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:,.0f} {unit}" if unit == "B" else f"{n:,.1f} {unit}"
        n /= 1024
    return str(n)


def walk(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw).expanduser()
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for root, dirs, names in os.walk(p):
                dirs[:] = sorted(d for d in dirs if not d.startswith("."))
                files += [
                    Path(root) / n for n in sorted(names) if not n.startswith((".", "~$")) and n not in SKIP_NAMES
                ]
        else:
            print(f"SKIP  {raw}: not found", file=sys.stderr)
    return files


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def content_type(path: Path) -> str | None:
    return ACCEPTED.get(path.suffix.lower())


def explain(exc: Exception) -> str:
    """Turn a network failure into a hint about the org's egress setting."""
    text = str(exc)
    if isinstance(exc, urllib.error.HTTPError):
        body = exc.read(300).decode(errors="replace").strip().replace("\n", " ")
        text = f"HTTP {exc.code} {exc.reason}: {body}"
        if exc.code == 403 and "<Error>" not in body:
            text += "  -> looks like the sandbox egress proxy refused the host (see network egress settings)"
        elif exc.code == 403:
            text += "  -> storage refused the upload (the URL expired or the file differs from the hash sent)"
    elif "Tunnel connection failed" in text:
        text += "  -> the sandbox egress proxy refused the host (see network egress settings)"
    elif isinstance(exc, urllib.error.URLError):
        text += "  -> host unreachable from this sandbox (egress blocked, DNS, or the server is down)"
    return text


def cmd_list(dirs: list[str]) -> int:
    seen = 0
    for d in dirs or DEFAULT_DIRS:
        p = Path(d).expanduser()
        if not p.is_dir():
            continue
        files = walk([str(p)])
        print(f"{p.resolve()}: {len(files)} file(s)")
        for f in files[:MAX_LISTED]:
            print(f"  {f.relative_to(p)}  {human(f.stat().st_size)}")
        if len(files) > MAX_LISTED:
            print(f"  ... and {len(files) - MAX_LISTED} more")
        seen += len(files)
    if not seen:
        print("No files found in: " + ", ".join(dirs or DEFAULT_DIRS))
    return 0


def cmd_prepare(paths: list[str]) -> int:
    files = walk(paths)
    rows, skipped = [], 0
    for f in files:
        ctype = content_type(f)
        if not ctype:
            skipped += 1
            print(f"SKIP  {f}: type not accepted (PDF, docx, pptx, xlsx, txt, md only)")
            continue
        rows.append(
            {"path": str(f), "filename": f.name, "content_type": ctype, "size": f.stat().st_size, "sha256": sha256(f)}
        )
    for r in rows:
        print(json.dumps(r))
    print(f"{len(rows)} file(s) ready, {skipped} skipped.")
    return 0 if rows else 1


def cmd_check(url: str) -> int:
    parts = urlsplit(url)
    probe = f"{parts.scheme}://{parts.netloc}/"
    proxies = [k for k in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY") if os.environ.get(k)]
    print("proxy env: " + (", ".join(proxies) or "none"))
    try:
        with urllib.request.urlopen(probe, timeout=20) as r:
            print(f"EGRESS OK  {parts.netloc} answered HTTP {r.status}")
            return 0
    except urllib.error.HTTPError as exc:
        # Storage answers an unsigned request with an S3 error document: the host is reachable.
        body = exc.read(300).decode(errors="replace")
        if "<Error>" in body or exc.code in (400, 404, 405):
            print(f"EGRESS OK  {parts.netloc} answered HTTP {exc.code}")
            return 0
        print(f"EGRESS FAIL  {parts.netloc}: HTTP {exc.code}: {body.strip()[:200]}")
        return 2
    except Exception as exc:
        print(f"EGRESS FAIL  {parts.netloc}: {explain(exc)}")
        return 2


def put(item: dict) -> int:
    path = Path(item["path"]).expanduser()
    size = path.stat().st_size
    headers = {**item.get("upload_headers", {}), "Content-Length": str(size)}
    with path.open("rb") as f:
        req = urllib.request.Request(item["upload_url"], data=f, method="PUT", headers=headers)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            r.read()
    return size


def cmd_put(plan_path: str) -> int:
    try:
        plan = json.loads(sys.stdin.read() if plan_path == "-" else Path(plan_path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read the plan {plan_path}: {exc}")
        return 1
    ok = failed = total = 0
    for i, item in enumerate(plan):
        name = Path(item.get("path", "?")).name
        try:
            size = put(item)
            total += size
            ok += 1
            if i < MAX_LISTED:
                print(f"OK    {name}  {human(size)}")
        except Exception as exc:
            failed += 1
            print(f"FAIL  {name}: {explain(exc)}")
    if len(plan) > MAX_LISTED:
        print(f"... {len(plan) - MAX_LISTED} more not listed")
    print(f"Uploaded {ok} of {len(plan)} file(s), {human(total)}; {failed} failed.")
    if plan_path != "-":
        Path(plan_path).unlink(missing_ok=True)  # it holds signed upload URLs
    return 0 if not failed else 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="list candidate files")
    ap.add_argument("--prepare", action="store_true", help="hash and type the files named")
    ap.add_argument("--check", metavar="UPLOAD_URL", help="egress check against the upload host")
    ap.add_argument("--put", metavar="PLAN", help="upload the files in this JSON plan")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    if args.list:
        return cmd_list(args.paths)
    if args.prepare:
        if not args.paths:
            ap.error("name the files or directory to prepare")
        return cmd_prepare(args.paths)
    if args.check:
        return cmd_check(args.check)
    if args.put:
        return cmd_put(args.put)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
