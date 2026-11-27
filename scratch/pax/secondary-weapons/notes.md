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

## Launcher power budget (owner, 2026-11-27)
- The launcher replaces the jetpack **and** the grenade option; scale the launchers to that.
- Assistant notes, untested: as a grenade type, the player could swap back to normal grenades from the Pip-Boy, so the grenade cost holds only for what is equipped. Nothing in a torso mod stops the launcher grenade being used without the pack; that likely needs a script check on equip.

## Launcher ammo and limits (owner, 2026-11-27; replaces the crafted launcher round idea)
- The pack consumes **frag grenades** and launches them like a launcher.
- Also considered: a longish cooldown so it cannot be spammed.
- The test it has to pass: why mount it instead of a jetpack and a pile of grenades?
- Assistant proposal: per frag it must beat a thrown one (impact detonation, long flat range, more damage or blast); numbers and cooldown open.
- Leads (offline CK wiki, untested): `Weapon.Fire(source, ammo)` fires a weapon from a reference; a script would take a frag and start the cooldown. Detecting the grenade key press is the hard part: `OnPlayerFireWeapon` is documented as out of combat and timer limited; animation events (`RegisterForAnimationEvent`) are the next lead.

## Sentry shoulder cluster launcher and ammo (2026-11-27)
Records read (`Fallout4.esm`; field meanings decoded by the assistant, not seen in game):
- `SentryBotLeftShoulderClusterLauncher` `00134271` / `...Right...` `00134272`, ammo `AmmoSentryShoulder` `0018844F`.
- Shell `SentryShoulderCluster` `00188450`: arcs (gravity 2.5, speed 1700). Its explosion `00216362` spawns **5** small missiles `001ACAC6` in a **30 degree** spread; each explodes for 30 base damage. A value of 0.8 on the shell is likely the time to burst (inferred). For scale, base explosion damage: missile 135, frag grenade 150.
- Indoor variants (`0021635F`, `00216360`) also carry a lobbed shell with a frag grenade explosion.
- Owner: if the launcher needs ammo and not a grenade, use grenade launcher ammo.
- That ammo is Creation Club only (`ccsbjfo4003-grenade.esl`, installed on the Deck): 40mm frag `xx000F9E`, MIRV, Nuka, pulse, cryo, plasma, incendiary and others. The plugin has vendor and loot lists and no 40mm ammo recipe was seen. Using it makes that plugin a requirement.

- Owner (2026-11-27): Creation Club as a requirement is acceptable; ammo cost to be decided later.
- Assistant suggestion, not agreed: the sentry cluster shell for the basic shot; 40mm round types as pack tiers.
