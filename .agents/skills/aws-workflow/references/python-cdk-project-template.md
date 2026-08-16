# Python CDK Project Template

Use this template contract to create or substantially restructure a Python AWS CDK repository. It
defines responsibilities and validation, not fixed business resources. Pair it with
`python-quality-check`, `github-actions-quality-check`, `domain-architecture-docs-workflow`,
`test-quality-check`, and `security-check`; use their stricter current assets and checks instead of
copying stale duplicates into this Skill.

## Template map

```text
<repository>/
├── .github/
│   ├── actions/
│   │   ├── setup-python-locked/
│   │   └── check-python-cdk/
│   └── workflows/
│       ├── pull-request.yml
│       └── main.yml
├── docs/
│   ├── README.md
│   ├── architecture/README.md
│   ├── domain/README.md
│   └── operations/README.md
├── src/<package>/
│   ├── __init__.py
│   ├── app.py
│   ├── settings.py
│   ├── constructs/
│   └── stacks/
├── tests/
├── .python-version
├── AGENTS.md
├── README.md
├── cdk.json
├── pyproject.toml
└── uv.lock
```

Start with one installable package and one deployable stack. Add a `constructs/` module only when a
logical unit contains multiple resources or has an independently useful contract. Add another stack
only when its resources need a different deployment, rollback, ownership, or deletion lifecycle.

## Compose the repository baseline

1. Use `python-quality-check` to create the PEP 621 package, `src/` layout, exact Python minor,
   uv lock, Ruff, strict mypy, pytest, statement and branch coverage, build, and distribution checks.
2. Add `aws-cdk-lib` and `constructs` as direct runtime dependencies. Keep test and quality tools in
   the development dependency group.
3. Select and record one reviewed CDK CLI version. Keep the CLI invocation reproducible and under
   `security-check` cooldown and provenance rules. If a committed Node toolchain owns the CLI, also
   use `node-quality-check`; otherwise document the exact reviewed package-runner command.
4. Use `github-actions-quality-check` event templates and the Python setup asset. Put repository
   commands in a local `check-python-cdk` Composite Action so local documentation and both workflows
   share one validation contract.
5. Create the required domain, architecture, and operations indexes. Document the resource boundary,
   bootstrap contract, deployment and teardown procedure, retained dependencies, and irreversible
   effects.
6. Add repository-specific `AGENTS.md` rules for the intended account/region, authorized stack
   boundary, external resources, secret handling, and required checks.

## Keep the entry point thin

Limit machine-dependent input to `app.py`. Parse and validate it into an immutable settings object,
then pass explicit values into stacks and constructs.

```python
from aws_cdk import App, Environment

from example.settings import StackSettings
from example.stacks.application import ApplicationStack


def build_app(*, settings: StackSettings) -> App:
    app = App()
    ApplicationStack(
        scope=app,
        construct_id=settings.stack_name,
        env=Environment(account=settings.account, region=settings.region),
        settings=settings,
    )
    return app
```

- Use a frozen, keyword-only dataclass or an equivalent typed model for settings.
- Validate missing, empty, malformed, and mutually inconsistent values before construct creation.
- Never read environment variables inside a construct or stack. This keeps synthesis deterministic
  and tests independent of the developer machine.
- Repository-specific Profile, expected account, and region may be tracked as non-secret routing
  metadata when the owner approves. Credentials, session tokens, raw responses, and unnecessary
  physical identifiers remain outside source control.

## Model with constructs and deploy with stacks

- Prefer L2 or L3 constructs for new resources because they supply intent-oriented APIs and safer
  defaults. Use L1 `Cfn*` constructs when import parity, an unsupported property, or an exact
  CloudFormation contract requires them; document that reason.
- Group one logical unit into a construct and expose only the values consumers need. Keep stack
  classes focused on composition, environment, dependencies, and lifecycle.
- Keep names generated unless a stable physical name is an external contract. A fixed name reduces
  replacement and multi-environment flexibility.
- Pass cross-construct values directly. Use exports, parameters, SSM, or lookups only when the
  ownership and deployment boundary requires them.
- Apply least privilege at the action, resource, condition, and trust boundaries. Avoid wildcard
  permissions and direct manipulation of service-managed identities.
- Choose `RemovalPolicy` and update-replacement behavior per resource and environment. Production
  data normally needs retention and recovery controls; an ephemeral experiment can use destruction
  only with explicit authorization and documented irreversibility.

## Keep synthesis deterministic

- Use the implicit `DefaultStackSynthesizer` unless a reviewed organization bootstrap contract
  requires another synthesizer. Bootstrap every target account-region separately and keep bootstrap
  lifecycle independent from application stacks.
- Synthesize before diff or deploy. Inspect the CloudFormation template and asset manifest, not only
  the source constructs.
- Avoid network lookups during unit tests and routine synthesis. When CDK lookup context is required,
  generate it deliberately, review it, and commit `cdk.context.json` because it is application state.
  Do not edit cached lookup keys manually.
- Put stable non-cached app context under the `context` key in `cdk.json`. Do not use context or
  environment variables as a secret store.
- Keep `cdk.json` small. Its `app` command must use the locked Python environment; add feature flags
  only from the current CDK contract and review their effect during upgrades.

## Test behavior at three layers

1. **Settings tests** prove valid normalization and every failure boundary without reading live AWS.
2. **Template tests** use `aws_cdk.assertions.Template` for resource counts, security properties,
   IAM scopes, retention/deletion behavior, dependencies, and absence of forbidden properties.
3. **Assembly checks** run the real locked `cdk synth` with non-sensitive example configuration and
   inspect expected stacks and warnings.

Prefer focused assertions over broad snapshots. A snapshot can supplement review of a stable small
template, but it must not replace semantic assertions about security and lifecycle. Use live canaries
only after unit/synthesis checks and only with explicit authorization, exact scope, cleanup, and
post-change read-back.

## Deployment contract

Run the following order with the exact intended Profile, account, and region:

1. verify CLI/library versions and `sts get-caller-identity`;
2. verify or bootstrap the account-region and read back the bootstrap stack;
3. run the complete locked source, test, coverage, build, and artifact checks;
4. run `cdk synth` and inspect the assembly;
5. run `cdk diff` and classify every IAM, replacement, removal, and data effect;
6. obtain approval required by the change boundary;
7. deploy the exact reviewed stack and wait for completion;
8. read back CloudFormation and service state, then run bounded behavioral checks;
9. record rollback, retained resources, cost ownership, and untested behavior.

CI should synthesize with examples but must not receive deployment credentials or deploy from an
ordinary pull-request validation job. Add deployment automation only after defining protected
environments, identity federation, approvals, concurrency, rollback, and artifact provenance.

## Completion checklist

- Package, app, constructs, stacks, settings, and tests have distinct responsibilities.
- Account, region, configuration, physical-name, lookup-context, and secret boundaries are explicit.
- Bootstrap and synthesizer contracts match and remain separate from application lifecycle.
- L2/L3 versus L1 choices and every destructive policy have recorded reasons.
- Fine-grained assertions cover security, lifecycle, dependencies, and forbidden behavior.
- Local and CI checks use the locked environment and synthesize deterministically.
- Deployments require identity verification, diff review, authorization, read-back, and cleanup.

Recheck the current AWS documentation when applying this template:

- [AWS CDK best practices](https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html)
- [AWS CDK constructs](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html)
- [AWS CDK testing](https://docs.aws.amazon.com/cdk/v2/guide/testing.html)
- [AWS CDK context](https://docs.aws.amazon.com/cdk/v2/guide/context.html)
- [AWS CDK bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-env.html)
- [AWS CDK synthesis](https://docs.aws.amazon.com/cdk/v2/guide/configure-synth.html)
