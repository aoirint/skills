# aoirint Agent Skills

These skills are packaged and installed with
[APM](https://github.com/microsoft/apm) for use with
[OpenAI Codex](https://openai.com/codex/).

## Install

Install APM first.

### All skills (global)

To install the complete collection into your user scope, run:

```shell
apm install --global aoirint/skills
```

## Skills

| Skill | Purpose |
| --- | --- |
| [apm-usage](.apm/skills/apm-usage/README.md) | Safely set up, pin, deploy, audit, and update APM-managed agent dependencies. |
| [bepinex-mono-mod-quality-check](.apm/skills/bepinex-mono-mod-quality-check/README.md) | Review BepInEx Mono repositories for structure, dependencies, CI, release, and Thunderstore quality. |
| [changelog-workflow](.apm/skills/changelog-workflow/README.md) | Maintain canonical developer changelogs and release history. |
| [code-quality-check](.apm/skills/code-quality-check/README.md) | Review implementation changes for readability, maintainability, and verification. |
| [commit-message-quality-check](.apm/skills/commit-message-quality-check/README.md) | Draft and review accurate Conventional Commit messages. |
| [git-worktree-workflow](.apm/skills/git-worktree-workflow/README.md) | Set up and use isolated Git worktrees for repository work. |
| [github-actions-quality-check](.apm/skills/github-actions-quality-check/README.md) | Review GitHub Actions workflows and composite actions. |
| [gitignore-workflow](.apm/skills/gitignore-workflow/README.md) | Create and maintain repository `.gitignore` rules. |
| [issue-quality-check](.apm/skills/issue-quality-check/README.md) | Review GitHub issue titles, bodies, comments, and updates. |
| [lethal-company-analyze](.apm/skills/lethal-company-analyze/README.md) | Investigate version-specific Lethal Company mechanics with reproducible evidence. |
| [pull-request-quality-check](.apm/skills/pull-request-quality-check/README.md) | Review pull requests and PR-thread communication. |
| [prose-quality-check](.apm/skills/prose-quality-check/README.md) | Review explanatory prose for readability, local structure, and preserved nuance. |
| [release-note-workflow](.apm/skills/release-note-workflow/README.md) | Create, update, and review user-facing release notes. |
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
