# aoirint Agent Skills

These skills are packaged and installed with
[APM](https://github.com/microsoft/apm) for use with
[OpenAI Codex](https://openai.com/codex/).

## Install

Install APM first.

### Install all skills globally

To install the complete collection into your user scope, run:

```shell
apm install --global "aoirint/skills#main"
```

### Update skills globally

If you initially installed the skills from the `main` branch (using `#main`), you can update them by running:

```shell
apm update --global
```

## Skills

| Skill | Purpose |
| --- | --- |
| [apm-usage](.apm/skills/apm-usage/README.md) | Safely set up, pin, deploy, audit, and update APM-managed agent dependencies. |
| [bws-workflow](.apm/skills/bws-workflow/README.md) | Use the Bitwarden Secrets Manager CLI safely with OS-backed access-token storage. |
| [bepinex-mono-mod-quality-check](.apm/skills/bepinex-mono-mod-quality-check/README.md) | Review BepInEx Mono repositories for structure, family alignment, dependencies, CI, package readiness, release, and Thunderstore quality. |
| [changelog-workflow](.apm/skills/changelog-workflow/README.md) | Maintain canonical developer changelogs and release history. |
| [code-quality-check](.apm/skills/code-quality-check/README.md) | Review implementation changes for readability, maintainability, and verification. |
| [commit-message-quality-check](.apm/skills/commit-message-quality-check/README.md) | Draft and review accurate Conventional Commit messages. |
| [docker-quality-check](.apm/skills/docker-quality-check/README.md) | Review Dockerfiles, Compose configurations, and container runtime changes. |
| [flet-project-quality-check](.apm/skills/flet-project-quality-check/README.md) | Create and review production-quality Python Flet projects. |
| [git-worktree-workflow](.apm/skills/git-worktree-workflow/README.md) | Set up and use isolated Git worktrees for repository work. |
| [github-workflow](.apm/skills/github-workflow/README.md) | Create and review GitHub Actions workflows, issues, and pull requests. |
| [gitignore-workflow](.apm/skills/gitignore-workflow/README.md) | Create and maintain repository `.gitignore` rules. |
| [hugo-quality-check](.apm/skills/hugo-quality-check/README.md) | Review pnpm-managed Hugo sites, local build assets, and CI. |
| [lethal-company-analyze](.apm/skills/lethal-company-analyze/README.md) | Investigate version-specific Lethal Company mechanics with reproducible evidence. |
| [node-quality-check](.apm/skills/node-quality-check/README.md) | Review pnpm-managed Node.js source, dependencies, runtime, CI, configuration, and validation changes. |
| [prose-quality-check](.apm/skills/prose-quality-check/README.md) | Review explanatory prose for readability, local structure, and preserved nuance. |
| [python-quality-check](.apm/skills/python-quality-check/README.md) | Create and review strict, reproducible uv-managed Python projects. |
| [release-note-workflow](.apm/skills/release-note-workflow/README.md) | Create, update, and review channel-specific release notes, and assess publication readiness. |
| [rollout-workflow](.apm/skills/rollout-workflow/README.md) | Roll out a validated canonical change to compatible repositories. |
| [security-check](.apm/skills/security-check/README.md) | Review repository changes for practical security and supply-chain risks. |
| [skill-quality-check](.apm/skills/skill-quality-check/README.md) | Review Agent Skills for clear triggers, focused scope, and validation readiness. |
| [software-documentation-maintenance](.apm/skills/software-documentation-maintenance/README.md) | Design and maintain coherent software documentation systems. |
| [unity-game-analyze](.apm/skills/unity-game-analyze/README.md) | Trace Unity game behavior through decompiled code and serialized assets. |

## License

Unless otherwise specified, repository content is licensed under the
[MIT License](LICENSE). Third-party skills may carry their own licenses; their
licenses and notices are recorded in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
