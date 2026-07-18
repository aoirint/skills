# aoirint Agent Skills

## Install for Codex

```shell
ln -s ~/git/skills/src ~/.codex/skills/user
```

## Markdown lint

Markdown is checked with `markdownlint-cli2`. The pinned Docker image below is
the documented local command; another installation method is acceptable when it
uses the same version and this repository's configuration.

On Windows with PowerShell:

```powershell
docker run --rm --network none --user 1000:1000 -v ".:/workdir" davidanson/markdownlint-cli2:v0.22.1@sha256:0ed9a5f4c77ef447da2a2ac6e67caf74b214a7f80288819565e8b7d2ac148fe5
```

On Linux:

```bash
sudo docker run --rm --network none --user "$(id -u):$(id -g)" -v ".:/workdir" davidanson/markdownlint-cli2:v0.22.1@sha256:0ed9a5f4c77ef447da2a2ac6e67caf74b214a7f80288819565e8b7d2ac148fe5
```
