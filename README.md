# Alludium Brain

Install the plugin from this marketplace, or download [brain.zip](downloads/brain.zip)
for manual import. It contains both Claude and OpenAI manifests, skills and the hosted MCP
connection. Sign in with your own work account after installation.

In Codex, run `codex plugin marketplace add alludium/brain-plugin`, then install
**Alludium Brain** from that marketplace in the plugin browser and start a new chat.
Marketplace approval is not required for this private distribution route.

## CLI 0.29.113

Download [alludium_brain_cli-0.29.113-py3-none-any.whl](downloads/alludium_brain_cli-0.29.113-py3-none-any.whl), then run:

```sh
uv tool install ./alludium_brain_cli-0.29.113-py3-none-any.whl
brain login
brain tools
```

Python 3.12+ and an OS keyring are required; uv can install Python. Upgrade by downloading the
new wheel and running the same command with `--upgrade`.
[CLI source and usage guide](downloads/alludium_brain_cli-0.29.113.tar.gz) · [SHA-256 checksums](downloads/SHA256SUMS)

The CLI calls the same MCP tools as your AI, without a model in the transfer path. Folder uploads
are private by default and additive: changed files become additional snapshots, not replacements.
Use `brain upload /path/to/vault --namespace research-vault --dry-run` to preview the selection.
[Detailed help](https://app.brain.alludium.ai/help/feed/cli.md)
