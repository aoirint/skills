# Guest Feature Authorization and Global Gates

Use this reference when a BepInEx mod exposes a practice, debug, cheat-like,
or other feature that a non-host player could use to materially change shared
gameplay, game balance, progression, challenge, or another player's session.

## 1. Classify the feature

Treat a feature as host-authorized by default when a guest can use it to:

- mutate shared game state, spawn or remove resources, bypass progression, or
  change movement, damage, inventory, physics, AI, objectives, or saves;
- reveal information that normally gates play or materially changes challenge;
- run a practice, rollback, rewind, teleport, debug, or test action that can
  affect a shared session; or
- trigger a server RPC or equivalent authoritative action whose effect is not
  purely local and cosmetic.

Do not use the feature's label as the classification. A feature called
"diagnostic" can still require authorization when its information or controls
materially change play. A purely local, cosmetic presentation that cannot affect
or reveal balance-relevant state may use a documented client-only policy.

When classification is uncertain, use host authorization until game evidence
shows the feature is local and non-material.

## 2. State the policy before choosing transport

Document these facts in the mod architecture before implementing a handshake:

| Question | Required answer |
| --- | --- |
| Protected capability | Which guest action or information is gated? |
| Host decision | Which host-controlled setting or policy grants it? |
| Default | Is guest use denied or allowed before authorization, and why? |
| Failure behavior | What happens on no host mod, no reply, deny, disconnect, or reset? |
| Lifetime | When does authorization expire and reset? |
| Scope | Which feature paths does the decision gate? |

For balance-changing guest features, use fail-closed behavior: no response,
denial, unavailable network state, or expired session authorization disables the
guest capability.

## 3. Implement an authoritative authorization path

Use an authoritative host-to-client path, normally a targeted response to a
guest request, when the game has no verified general mod-list or authorization
protocol.

- Validate the execution role before sending, receiving, or applying a request.
- Let the host read its own current policy and return an explicit allow/deny
  value. Mod presence alone is not permission.
- Target the response to the requesting client unless every recipient needs the
  same result.
- Keep the client-side result connection-scoped. Clear it on disconnect,
  network despawn, lobby replacement, or another proven session boundary.
- Bound requests and retries. Do not send authorization traffic from a per-frame
  update loop. State the initial delay, retry interval, maximum attempts, and
  reason for each timing choice.
- Treat an unmodded host, an unknown RPC, a timeout, and a denied response as
  unavailable authorization. The guest feature must remain disabled without
  breaking normal game callbacks.
- Do not describe a presence handshake as authentication, anti-cheat, exact
  version negotiation, or a general mod-list unless separately implemented and
  verified.

Keep Unity, Netcode, BepInEx configuration, and RPC code in Interop. Pass Core
only the plain authorization result or an explicit policy value.

## 4. Provide a coherent global gate

Give the mod a global `Enabled` configuration setting by default. It controls
the mod's declared functionality; it does not unload the BepInEx plugin.

- Apply the gate before expensive observation, mutation, rendering, and network
  sends. Hide or clean up mod-owned presentation when disabling it.
- Keep lifecycle cleanup, error containment, and required passive callbacks
  safe while the gate is off.
- Combine the global gate with narrower feature settings rather than replacing
  them. A useful order is global enablement, host/guest authorization, then
  presentation or feature-specific controls.
- Describe settings by responsibility. For example, put plugin-wide operation
  and host guest-policy settings in `General`, and local presentation choices in
  an `Overlay` or feature-specific category when that matches the repository.

An exception is valid only when a coherent gate cannot be applied because of a
specific scale, lifecycle, or implementation constraint. Document the affected
paths, why a gate would be unsafe or misleading, and the narrower controls that
remain available. "This mod is large" alone is not enough.

## 5. Verify policy, not only RPC reachability

Cover the applicable rows below with the real Interop boundary or a faithful
harness. Use distinct values so an incorrect role, stale authorization, or
wrong recipient cannot pass by coincidence.

| Host state | Guest state | Expected result |
| --- | --- | --- |
| Mod absent or no response | Feature requested | Guest feature stays disabled. |
| Mod present, host denies | Feature requested | Guest feature stays disabled. |
| Mod present, host allows | Feature requested | Only the authorized guest capability enables. |
| Host policy changes or session ends | Previously allowed guest | Authorization resets at the documented boundary. |
| Global gate disabled | Host or guest | Declared mod functionality is disabled without plugin unload. |
| Guest lacks the mod | Shared session | Normal game callbacks and other clients remain safe. |

Also verify that requests are bounded, host policy is authoritative, and a guest
cannot enable the protected path by editing only local configuration.
