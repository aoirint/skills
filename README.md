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
| [analyze-lethal-company](.apm/skills/analyze-lethal-company/README.md) | Investigate version-specific Lethal Company mechanics with reproducible evidence. |
| [changelog-workflow](.apm/skills/changelog-workflow/README.md) | Maintain canonical developer changelogs and release history. |
| [code-quality-check](.apm/skills/code-quality-check/README.md) | Review implementation changes for readability, maintainability, and verification. |
| [commit-message-quality-check](.apm/skills/commit-message-quality-check/README.md) | Draft and review accurate Conventional Commit messages. |
| [document-quality-check](.apm/skills/document-quality-check/README.md) | Review explanatory prose for readability, structure, and preserved nuance. |
| [git-worktree-workflow](.apm/skills/git-worktree-workflow/README.md) | Set up and use isolated Git worktrees for repository work. |
| [github-actions-quality-check](.apm/skills/github-actions-quality-check/README.md) | Review GitHub Actions workflows and composite actions. |
| [gitignore-workflow](.apm/skills/gitignore-workflow/README.md) | Create and maintain repository `.gitignore` rules. |
| [issue-quality-check](.apm/skills/issue-quality-check/README.md) | Review GitHub issue titles, bodies, comments, and updates. |
| [maintain-mod-documentation](.apm/skills/maintain-mod-documentation/README.md) | Maintain developer documentation for software mods and plugins. |
| [manage-apm](.apm/skills/manage-apm/README.md) | Safely set up, pin, deploy, audit, and update APM-managed agent dependencies. |
| [minimal-primary-rollout](.apm/skills/minimal-primary-rollout/README.md) | Roll out a validated canonical change to compatible repositories. |
| [pull-request-quality-check](.apm/skills/pull-request-quality-check/README.md) | Review pull requests and PR-thread communication. |
| [release-note-workflow](.apm/skills/release-note-workflow/README.md) | Create, update, and review user-facing release notes. |
| [security-check](.apm/skills/security-check/README.md) | Review repository changes for practical security and supply-chain risks. |
| [skill-quality-check](.apm/skills/skill-quality-check/README.md) | Review Agent Skills for clear triggers, focused scope, and validation readiness. |

## License

Unless otherwise specified, repository content is licensed under the
[MIT License](LICENSE). Third-party skills may carry their own licenses; their
licenses and notices are recorded in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
