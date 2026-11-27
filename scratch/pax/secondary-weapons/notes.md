# Secondary weapons (grenade key, shoulder, jetpack slot)

Later sections replace earlier ones where they say so. Shared goal and rules: [`../common.md`](../common.md). Effects and costs in the table are from the Gemini draft and **unverified**.

## Shoulder weapons (hotkey)

| Module | Needs | Effect (from draft) | Draft cost or fuel | Check notes | Keep? | My notes |
|---|---|---|---|---|---|---|
| Sentry Cluster Mortar | Shoulder mount | Micro-missile salvo | 2 missiles or 5mm rounds, 15 s | All four: script, F4SE for the hotkey, new meshes that may not render |  |  |
| Assaultron Focus Beam | Shoulder mount | Sustained laser | 3 fusion cells, 20 s | As above |  |  |
| Voltaic Arc Discharge | Tesla Coils (torso) | Chain lightning, up to 4 targets | 2 fusion cells, 20 s | As above, mesh not stated |  |  |
| Corrosive Acid Sprayer | Shoulder mount | Armor-stripping cone | 1 acid, 12 s | As above |  |  |

## Grenade / secondary launcher in the jetpack slot (owner, 2026-11-27)
- The launcher should take the jetpack's slot. The two would likely conflict on models anyway.
- Note: [`concept-spec.md`](../concept-spec.md) lists Jet Pack among the torso mods, so the launcher would probably also exclude the other mods in that slot *(inferred, unverified)*.
- Related: "Shoulder weapons (hotkey)" above.

## Launchers on X-01 and firing them (2026-11-27)

- Owner: tie X-01 to sentry bot gear and allow the backpack launcher there: the base missile pack with Automatron, Nuka launchers from Nuka-World.
- Read: sentry missile and shoulder launcher mods in `DLCRobot.esm`; sentry shoulder Nuka launcher mods in `DLCNukaWorld.esm`.
- No F4SE rules out a custom hotkey. Assistant suggestion, untested: make the launcher a grenade type, so the grenade key fires it and the backpack is the visual; a throwing motion would probably show. The same trick could cover a Tesla lobber.
