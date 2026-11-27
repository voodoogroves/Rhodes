# PAX: goal and rules shared by every piece

Edit freely: **Keep?** (yes / no / maybe) and **My notes**, or change any cell. Everything in the effect and cost columns is from the Gemini draft and **unverified**. The draft itself is in `concept-spec.md`.

## Goal (owner, 2026-11-25)

A framework that lets someone who plays in power armor keep investing in it and turn it into a walking tank. Not tuned to one character.

So far: Locksmith and Hacker yes; carry weight is a low priority (other equipment mods cover it); Action Boy/Girl style perk of interest.

## Vision and framework (owner, 2026-11-25)

- Mostly expertise and engineering capabilities that let a player who leans into power armor turn it into a Swiss Army knife.
- A few are add-ons; be careful with those, as they may conflict with other mods.
- **Built** augments cost the perk cost and materials (locks). **Trained** augments cost the perk cost only.

## Categories (owner, 2026-11-25)

1. Perk replacers: skip the SPECIAL requirement, power armor only. **Working on now.**
2. New suit-only abilities bought with the perk cost (e.g. Stagger Dampeners). **Working on now.**
3. Overclocks: make existing pieces stronger.
4. Grenade replacers: mounted system fired with the grenade key (parked).
5. Condition triggers: passive, fire on low health and similar.

Draft sensor toggles and companion support are not in these.

## Rules so far (owner, 2026-11-25; costs updated 2026-11-27)

- **The aim is balance** (owner, 2026-11-27). Every upgrade has a cost:
  - If it **takes the place** of something the game already offers (a module slot, say), giving that up is cost enough.
  - If it comes **on top** of what the game offers, it needs a SPECIAL or perk cost. The price is delayed progress: points spent here are levels not spent toward other perks.
- Materials count as a cost only when they are rare or hard to find: the price is the time to find them, or using up a rare or single item. Steel is easy; super mutant gauntlets from a few locations, or several officer swords, are a hunt.
- The perk cost is paid in SPECIAL: lower a named base stat by 1 per rank, which the player rebuys with a perk point (see [`perks/notes.md`](perks/notes.md), "Perk cost mechanism"). Replaces "must spend a real perk point": a script cannot subtract one. Without a real cost it is free power with a small build barrier.
- Overclocks sit on top of a vanilla mod, so they cost SPECIAL. Shields follow the same research and cost rule as claws.
- Upgrades **stack** on top of vanilla mods.
- Do not change existing records, so other power armor mods don't conflict.
- Example: a perk that overclocks Motion-Assist Servos, +1 Strength per perk spent up to a maximum, only in power armor.

## Next session (owner request, 2026-11-25)

- Owner wants to be told how to install the Creation Kit (seen on Steam) on the Deck alongside Mod Organizer 2, or whether to use a different compiler.
- Facts so far: Steam app `1946160`; reports of running it under Proton were mixed and mostly old; Caprica is an alternative compiler that still needs the vanilla base script sources. The loose sources in the game folder looked like F4SE's set only. Back up `Data/Scripts` before installing.
- Then: compile a trivial script, test a stat change from script, detection test for overclocks, Stagger Compensation end to end.
- Still unchecked from the stat test: owned perks, health, save and reload, behaviour at 11.

## Suit themes and packaging (owner, 2026-11-27, in progress)

- Tie each option to the content it needs and to a suit that fits it.
- Skills go with any suit. Hacking is not one: Suit Intrusion is a helmet module made only for the Automatron-related suits, T-60 and the sentry suit (X-01).
- Hardware (claws, shields, launchers, overclock variants) belongs to a suit theme.

| Suit | Theme | Notes |
|---|---|---|
| T-45 | Kit-bashed, ad hoc, such as the shield | Lowest tier |
| Raider | Machete (ritual) blades, Tessa's Fist | |
| T-51 | Far Harbor and Nuka-World | Owner (not checked): two Vim! T-51 sets and heavy synth and Children of Atom things in Far Harbor; a T-51 in Nuka-World |
| T-60 | Automatron: Tesla and robot things, Assaultron blades | Rust Devil boss wears the Tesla T-60 (records read). Start here |
| X-01 | Sentry bot gear, backpack launcher; Nuka launchers | Owner (not checked): an X-01 set in Nuka-World |
| Overboss, Hellfire, X-02 | None | Strong enough already |

Open:
- Assistant suggestion, not agreed: a core with no DLC plus one add-on each for Automatron, Far Harbor and Nuka-World. T-60 and X-01 without those would get only base game pieces.
- For other suit-themed effects: which piece decides when suits are mixed (torso or helmet likely)?
- The owner's last message on suit themes ended "In the base game"; the rest of that thought is not recorded.

## Creation Club content and first suit (owner, 2026-11-27)
- Creation Club requirements are not a concern: the owner believes the current Anniversary Edition includes them and many players have them (not checked).
- First suit to work through in detail: **Raider**. Brief: [`attachments/notes.md`](attachments/notes.md), "Raider: first suit".
