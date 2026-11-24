# Anelasticity restart, 2026-11-16 (rewritten 19:10 PST; job states updated 19:45) — superseded by ANELASTICITY_RESTART_2026-11-17.md

Read first: this file, then `INPROGRESS.md` (§1 running, §3 proposals), `ANELASTICITY_TODO.md` (T20, T25, T26) and summary §5n–§5o. Previous restart: `ANELASTICITY_RESTART_2026-11-15.md`.

## 0. Update 2026-11-17 06:10
- **Session logs** (RC 11-17): `Anelasticity/sessions/` (one Markdown file per session; `tools/session_log_md.py`; Stop/SessionEnd hooks; open `/hooks` once or restart for the hook to start firing in the session where it was added).
- **A3b analysed** (RC "Analyse the finished A3b jobs"): `results_freeenergy/BDG_VACANCY_A3.md` §5–6, summary §5p.
  - Hop-free.
  - Formation energies, 30 → 120 GPa: MgO partial 6.2 → 12.2 eV, SiO₂ partial 12.3 → 22.6 eV, full Schottky 18.5 → 34.8 eV.
  - V_Mg migration 3.9–6.1 eV. Si migration unresolved (cooperative jump).
  - Intrinsic D_O in bridgmanite ≈ 10⁵ × periclase.
  - Ladder vs direct F_I: −0.4 to −0.8 eV (does not enter ΔG).
  - Follow-ups (a)–(c) in INPROGRESS §3.
- **Still running / pending:**
  - item 1: VASP relaxations 6998279 still PENDING.
  - item 2: 6963124_1 (8×8×8, γ₀ 0.02; output in the run root) and 6963125_1 (6×6×6 aged) COMPLETED 11-17, not analysed. 6965639_2 (γ₀ 0.01) is RUNNING at 21.8 h, near its 24 h limit; it is restartable with `sbatch --array=2 sweep.sh` in `FreqSweep_Schottky_aged_2ns`.

## 0b. Update 2026-11-17, later (RC: "Yes do a and b, and analyse the Schottky runs and put c as optional in the TODO list")
- **Schottky reruns analysed** (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.5):
  - 8×8×8: G″ = 27.3 ± 2.4 GPa at 20 GHz (reproduces 38 ± 9). 6×6×6 aged 1.5 ns: 2.3 ± 0.5 GPa.
  - **In both cells all vacancies form one nanovoid** (40 and 16 sites; new `tools/b1_vacancy_clusters.py`). The sub-50 GHz "Schottky" loss is void anelasticity (Debye τ ≈ 7.6 ps vs 0.5 ps), not point-defect relaxation, and is not a mantle mechanism.
  - The γ₀ = 0.01 run (6965639_2) is still running.
- **(a) Si vacancy path:**
  - static NEB with the new `tools/bdg_vac_neb.py` (ASE + DeepPot with fparam). Smoke 7045831 failed (wrong python: `python` was cohen_env); fixed in `neb_job.sh`, resmoke 7045934 pending. The production array **7045971** (afterok 7045934; 12 distinct Si candidates per state, Mg calibration at 30 and 120 GPa) is queued; if the smoke fails, fix it and resubmit the array.
  - V_Si MD at high T: 7045834 (4).
- **(b) TS 80 ps direct Frenkel–Ladd:** 7045833 (6).
- **Correction:** the "3N − 3 kinetic convention" explanation of the ladder offset was wrong. The convention is consistent, and the offset is unexplained until (b).
- **(c) DFT correction for bridgmanite:** optional, in TODO.
- Also repaired escape-sequence corruption of the LaTeX in `ANELASTICITY_RESTART_2026-10-07.md` (Eqs. 6–7) and in the new T_DEPENDENCE Eq. 8. Lesson: write LaTeX through raw strings or heredocs, never through plain Python strings.

## 1. RC requests today, in order
1. "Go ahead with A3 for bridgmanite too" → A3 run and analysed (§3).
2. "Yes do 1 2 3 4 5" (the 11-16 proposals) and "Also run the γ₀ = 0.01 linearity check" → items 3–5 analysed (§4); items 1 and 2 running (§5).
3. "Analyse the finished A3 and item 3–5 jobs" → done (§3, §4).
4. "Yes, run the A3 redo" → A3b running (§5).
5. "Analyse the finished A3b jobs" (19:10) → none had finished; status check only (A3b README, "Status check").

## 2. Results from the 11-15 jobs (analysed this morning; summary §5n)

| item | result | write-up |
|---|---|---|
| A1 MgO formation (Deng, 7 states) | bound pair 5.27 → 12.45 eV, separated 6.50 → 15.30 eV (20/2000 → 140/3000); binding 1.2–2.8 eV | `results_freeenergy/MGO_VACANCY_FREE_ENERGIES.md` §2 |
| A2 MgO migration | ΔG_m Mg 2.19 → 3.85, O 2.39 → 4.54 eV; agrees with Ita & Cohen within 0.15 eV except O at 140 GPa | same §2–3 |
| D_O (MgO) | 10⁴–7×10⁴ × Cordier's Table 2, driven by the separated-pair ΔG_f (no DFT check yet: item 1) | same §4 |
| Liquids at matched (P, T) | η₀ within 5–13 %; D_O 1.2–1.4× faster in MgSiO₃; D_O not a function of n_O | `results_Tdep/LIQUID_SE_ODENSITY.md` §6 |
| Schottky 20 GHz T series, cell-size test | E_app = 3.2 ± 0.6 eV; the 6×6×6 cell contradicts both τ ∝ L² and a local mechanism (reruns: item 2) | `results_Tdep/T_DEPENDENCE_RESULTS.md` §2.4 |
| Σ5 at 60 GPa | locked at 2000 K, shear-coupled migration at ≥ 2300 K | `results_cordier2023/CORDIER2023_COMPARISON.md` §5.1 |

## 3. A3, bridgmanite vacancies (analysed this evening; `results_freeenergy/BDG_VACANCY_A3.md`, figure `bdg_migration.{pdf,png}`)
Run dir `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A3_Bdg_Deng` (README; raw `A3_analysis.txt`).
- **O vacancy is very mobile.**
  - Edge-jump barriers: 0.87 / 1.26 / 1.61 / 1.92 eV at 30 / 60 / 90 / 120 GPa.
  - Per-vacancy rate 3×10¹⁰–5×10¹¹ s⁻¹, ≈ 10⁴ × periclase.
  - The O1 and O2 sites are within 0.07 eV.
  - TST vs direct MD: κ = 0.63 ± 0.18 (V6.5669 / 3021 K) and 0.54 ± 0.24 (120 / 2800).
- **V_Mg is slow:** 5.5–6.0 eV at 90–120 GPa (4.65 eV at 60 GPa, less reliable).
- **The formation runs are compromised** for every cell containing V_O.
  - O hops occur at λ ≈ 0, and some tether sites were averaged over hops.
  - At 30 GPa the defects rearranged: V_O clustered with V_Si, and the "bound" pair dissociated.
  - The hop-free replicas (new `--maxdr 1.5`) give only provisional values (±0.5 eV) at 60–120 GPa. All Si migration is unusable.
  - This is why A3b exists (§5).

## 4. Items 3–5 (analysed this evening)
- **Item 3, Σ5 at 90 / 120 GPa** (`DengStates/MgO_S5_P90P120_Tseries`, Cordier doc §5.2):
  - locked at all 6 states, up to 3400 K (90 GPa) and 3800 K (120 GPa);
  - so the unlocking temperature rises by more than 1100 K between 60 and 90 GPa (proposal in INPROGRESS §3: γ(u) scan or NEB).
- **Item 4, MgO TST check** (`FreeEnergy/A2b_MgO_TSTcheck`, MGO doc §6):
  - κ = 0.5–1.6 (mean 1.0) for free vacancies, so the A2 barriers are good to ≈ 0.1 eV;
  - in the MD the separated pair binds within 0.5 ns (new pair tracking in `site_hops.py`).
- **Item 5, Rosenfeld** (`LiquidPT_Deng`, `LIQUID_SE_ODENSITY.md` §7, `results_Tdep/rosenfeld.{pdf,png}`):
  - both melts collapse on the two-body excess entropy s₂: D*_O within 8 % rms, η* within 10 %;
  - at equal n_O they were 4× apart;
  - η*·D*_O = 0.13–0.16.

## 5. Running (states at 19:45)

| what | jobs | state | dir (README) | when done |
|---|---|---|---|---|
| **A3b, A3 redo:** single-vacancy cells (V_Mg, V_Si, V_O2). V_Mg and V_Si by Frenkel–Ladd at T. Perfect and V_O2 by Frenkel–Ladd at T₁ = 800 / 1200 / 1500 / 1800 K (fparam fixed at k_B T), then a 7-point ⟨E⟩(T) ladder to T (Eq. 1 of the README). Mg and Si migration without V_O | 7000466 (16, Frenkel–Ladd), 7000467 (8, ladders), 7000468 (8, migration) | 19:45: **Frenkel–Ladd** 1–3 of 6 replicas done per task (done ≈ 21:00); every replica so far is hop-free (max \|dr\| 0.48–0.61 Å at T₁, 0.71–0.91 Å for V_Mg / V_Si at T). **Ladders** all 8 running, 1–2 of 7 temperatures done (done ≈ 21:30–22:00); errors 0.09–0.21 eV per point. **Migration** 7000468_1 running, 2–8 pending | `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A3b_Bdg_single` | `python ~/Claude/tools/bdg_tint_analyze.py`. **Check first:** the ladder F_I(T) must equal the direct A3 F_I(T) (Eq. 2), within ≈ 0.1–0.2 eV. Then the hop column of the V_Mg and V_Si runs (if they hop, add ladders), and `vac_mig_analyze.py P*_Mg_single P*_Si_single`. Compare with Table 1 of BDG_VACANCY_A3.md |
| **Item 1, DFT check of the separated MgO pair** | DeePMD relaxations 6997697 done; VASP relaxations **6998279_1–10** PENDING (12 h each); snapshot single points 6966033 done | | `/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck` (README Part 3), `sep/` | (a) FEP now: `python ~/Claude/tools/dft_compare.py --gf P20_T2000_perfect P20_T2000_sep --L 2 --temp 2000` and the same for 140/3000, against δ^bound = +0.95 / +1.27 eV. (b) After 6998279: E_b(d), DFT vs DeePMD, and the long-range fit |
| **Item 2, Schottky 20 GHz reruns** | 6963124_1 (8×8×8, γ₀ 0.02, 2 ns; **output in the run root**, see README), 6965639_2 (γ₀ 0.01), 6963125_1 (6×6×6, 1.5 ns ageing) | RUNNING 12–12.5 h at 19:45 (≈ 18–22 h total) | `MgO/4096atoms/V6.6868/4096atom/5000K/FreqSweep_Schottky_{aged_2ns,L6_aged}` | `ONESHOT=1 ~/Claude/tools/sweep_watch.sh <dir>:<job>:shear`; G″ vs 38 ± 9 (reference) and vs 1.1 ± 1.5 GPa (6×6×6, 300 ps ageing); linearity between γ₀ 0.01 and 0.02; stress events vs vacancy moves (trajectory every 10 ps) |

**DeePMD side of item 1 (already available, 6997697).** These are the static relaxed energies at fixed box, ΔE(d) − ΔE(d_max):

| state | separation d (Å) | ΔE(d) − ΔE(d_max) (eV) |
|---|---|---|
| 20 GPa | 2.08 | −1.38 |
| 20 GPa | 4.64 | −0.47 |
| 20 GPa | 6.89 | −0.13 |
| 20 GPa | 9.51 | −0.06 |
| 20 GPa | 13.29 | 0 |
| 140 GPa | 1.87 | −2.59 |
| 140 GPa | 6.21 | −0.18 |
| 140 GPa | 11.98 | 0 |

The binding vanishes beyond the 6 Å cutoff, as expected. The DFT values at the same geometries come from 6998279.

**Single-vacancy energies, not a bug.** Removing an atom changes the DeePMD energy by +43.8 eV (Mg), +89.5 eV (Si) and −28.9 eV (O). These are the model's per-species references. Only stoichiometric sums are physical: Mg + O = +14.9 eV against the A3 mgo_sep cell's +14.5 eV. `bdg_tint_analyze.py` reports only sums with μ.

## 6. Bugs found and fixed today (all documented in the READMEs)
- **Item 1 relaxations:**
  - `relax_dp.lammps` printed a compute that was not current, and the ERROR was hidden by the grep in `gpu_job.sh`. Fixed and rerun.
  - The first stage 2 then submitted an empty relaxation array. `stage2.sh` now counts only `relax/` lines.
- **Schottky `sweep.sh`:** it had no `mkdir`, so 6963124_1 writes to the run root. Fixed for later runs; before any restart of that task, move its files to `P50ps_xz/`.
- **`liquid_rdf.lammps`:** fix ave/time never reached Nfreq. Added `reset_timestep 0`.
- **`tint_energy.lammps`:** `$(pe)` was used after `reset_timestep`. Fixed.
- **`LIQUID_SE_ODENSITY.md` Eq. 2:** corrupted by an earlier edit (backslash escapes). Repaired.
- **Dates:** entries I had dated 11-17 were corrected to 11-16.

## 7. Tools added or changed today
- **New:**
  - `build_bdg_vacancy.py` (with the single-vacancy kinds vmg / vsi / vo1 / vo2 added this evening);
  - `bdg_schottky_analyze.py` (`--maxdr`);
  - `vac_mig_indep.lammps`;
  - `site_hops.lammps`, `site_hops.py` (vacancy-pair tracking, bound/free rates);
  - `hops_array.sh`, `liquid_pt.py`, `liquid_rdf.lammps`, `rosenfeld.py`;
  - `tint_energy.lammps`, `tint_array.sh`, `bdg_tint_analyze.py`, `bdg_mig_plot.py`.
- **Changed:**
  - `ti_einstein.lammps`: `FPARAM fixed` with `FPVAL`;
  - `ti_einstein_analyze.py`: `--maxdr`; the replica dissipation is now written to ti_result.txt;
  - `ti_array.sh`: optional column 15 FPVAL, absolute BOXFROM;
  - `vac_mig_analyze.py`: general saddle rule, full paths, hop-window skipping;
  - `mig_array.sh`: MIGIN, MIGVARS.

## 8. Priorities for the next session
1. A3b as it finishes (§5; nothing finished at 19:45): Eq. 2 check first, then the Schottky sums and Mg / Si migration. Then a bridgmanite D (plan Eq. 8) and an update of BDG_VACANCY_A3.md.
2. Item 1 FEP (snapshots ready), then the DFT binding curve when 6998279 ends. This decides the MgO D_O against Cordier.
3. Item 2 lock-in analyses when the three Schottky runs end (about 6–10 h after 19:10).
4. Waiting for RC (INPROGRESS §3): the Σ5 60-vs-90 GPa follow-up, D1 B(T), Bdg γ anneal, talk trajectory.
