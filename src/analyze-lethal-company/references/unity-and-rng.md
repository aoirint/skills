# Unity and RNG analysis

## Serialization

Search scene YAML, prefabs, ScriptableObjects, addressable/bundle extracts, and build scene lists. Join a `MonoBehaviour` to its class through the script `.meta` GUID and join other assets by GUID/fileID rather than filename guesses. Before calling a serialized value effective, verify the component is enabled, its GameObject is active, the scene is in the build/load path, and no later code assignment replaces it. Record whether a value is a code default, serialized override, or runtime mutation.

## RNG streams

Inventory every RNG constructor and seed offset. Record draw order, conditional draws, `Next` exclusive maxima, float32 versus float64 arithmetic, casts, clamps, retries, and fallback branches. Treat two streams with related seeds as separate but not automatically statistically independent.

For Mono legacy `System.Random`, verify against a C# oracle or frozen vectors. In weighted selection, reproduce the game's accumulator precision and comparison direction exactly.

## Runtime consumption hazards

Static item-list generation does not imply exact realized values when the same RNG later drives spawn-point selection, NavMesh sampling, retry loops, or failures before value draws. Model such paths only after reproducing the generated interior and candidate objects, or label a fixed-consumption implementation counterfactual.

`FindObjectsOfType` order is runtime state. Noneligible objects can change a global array index without consuming endpoint-specific RNG. A fixed offset is a scenario, not a bound, unless monotonicity is proved.

## Networking and observation windows

Trace who computes the value, who owns the authoritative state, when RPC synchronization occurs, and whether the UI queries the server or reads local objects. Define a snapshot protocol such as post-sync, pre-movement, pre-dynamic-spawn. Pair predictors and targets on the same object set and frame.
