# Idea (parked): the Eye of Ra grants the three herbal effects (2026-11-24)

**Verdict: parked. Too complicated for what it gives.** Not needed for 0.1.

**The idea:** while the Eye is worn, the player carries the three vanilla Survival herbal effects, which together counter all six diseases, so disease risk drops.

**Why parked**
- Survival Mode only; no effect otherwise.
- The three herbal effects (`HC_Herbal_Anodyne/Stimulant/Antimicrobial_Effect`, `00249F9C/9B/9A`) are Fire and Forget with a 1 hour duration *(casting type read from the record layout; unverified)*, so a worn-item enchantment cannot hold them. It would need a small Papyrus script that applies them on equip and every hour while worn.
- The vanilla manager script tests those exact effect records, so we cannot use our own copies, and editing the vanilla quest costs compatibility.
- The payoff is modest: a reduction, not immunity (see the numbers below). Antibiotics are still needed once sick.

**What was found (kept so it need not be re-derived)**
- Herbal to disease: Anodyne counters Insomnia and Weakness; Stimulant counters Lethargy and Fatigue; Antimicrobial counters Hunger ("Parasites") and Infection. Read from `HC_Manager`'s `DiseaseEffects` property.
- Mechanism (script `hardcore/hc_managerscript.pex`): risky actions add to a risk pool (standard food or chem +0.07, high-risk food +0.12, cannibalism or faction hit +0.05, rain or swimming +0.03, cola +0.02, immunodeficiency +0.05); the pool drains 0.01 per 8 game hours; rolls start at 0.25; 1 game day grace after catching one. Per the script's text, a disease needs `herbal threshold (0.2) <= roll <= pool` while a herbal is active. If the roll is uniform *(unverified)*, that cuts the chance about 40 to 57% at pools of 0.35 to 0.5 and removes it at 0.2 or below. Hunger and thirst states clamp the pool (floors 0.05 to 0.3+), so a starving player is hard to protect.
- Cures and sources: Antibiotics (craft at the Chemistry Station with Chemist rank 1), the three craftable herbals (Survival only). Lead Belly affects radiation only.
- Check in game, if ever revived: `player.hasmagiceffect 00249F9A` (and `9B`, `9C`) *(command unverified)*.

**How it was read:** `esmdump` and `scripts/fo76utils/esmrec.py` for records; the script's variable defaults from the compiled `.pex` (little-endian; string table then variable entries); the quest's properties by parsing its `VMAD` blob. The `VMAD` parser was a throwaway and was not kept.
