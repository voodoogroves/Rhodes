# PAX: goal and rules shared by every piece

Edit freely: **Keep?** (yes / no / maybe) and **My notes**, or change any cell. Everything in the effect and cost columns is from the Gemini draft and **unverified**. The draft itself is in `concept-spec.md`.

## Goal (owner, 2026-11-25)

A framework that lets someone who plays in power armor keep investing in it and turn it into a walking tank. Not tuned to one character.

So far: Locksmith and Hacker yes; carry weight is a low priority (other equipment mods cover it); Action Boy/Girl style perk of interest.

## Vision and framework (owner, 2026-11-25)

- Mostly expertise and engineering capabilities that let a player who leans into power armor turn it into a Swiss Army knife.
- A few are add-ons; be careful with those, as they may conflict with other mods.
- **Built** augments cost a perk point and materials (locks). **Trained** augments cost a perk point only.

## Categories (owner, 2026-11-25)

1. Perk replacers: skip the SPECIAL requirement, power armor only. **Working on now.**
2. New suit-only abilities bought with a perk point (e.g. Stagger Dampeners). **Working on now.**
3. Overclocks: make existing pieces stronger.
4. Grenade replacers: mounted system fired with the grenade key (parked).
5. Condition triggers: passive, fire on low health and similar.

Draft sensor toggles and companion support are not in these.

## Rules so far (owner, 2026-11-25)

- Every upgrade has a cost or a drawback.
- Perk upgrades must spend a real perk point (firm). Without that it is free power with a small build barrier.
- Upgrades **stack** on top of vanilla mods.
- Do not change existing records, so other power armor mods don't conflict.
- Example: a perk that overclocks Motion-Assist Servos, +1 Strength per perk spent up to a maximum, only in power armor.

## Next session (owner request, 2026-11-25)

- Owner wants to be told how to install the Creation Kit (seen on Steam) on the Deck alongside Mod Organizer 2, or whether to use a different compiler.
- Facts so far: Steam app `1946160`; reports of running it under Proton were mixed and mostly old; Caprica is an alternative compiler that still needs the vanilla base script sources. The loose sources in the game folder looked like F4SE's set only. Back up `Data/Scripts` before installing.
- Then: compile a trivial script, test a stat change from script, detection test for overclocks, Stagger Compensation end to end.
- Still unchecked from the stat test: owned perks, health, save and reload, behaviour at 11.
