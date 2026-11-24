# Anelasticity restart 2026-10-13

Read first:
- `INPROGRESS.md`: running jobs and what to do when each finishes.
- `ANELASTICITY_PLAN_FE_DISLOCATIONS.md`: the new plan for free energies, diffusion and dislocations, written 10-13.
- `results_Tdep/T_DEPENDENCE_RESULTS.md`.
- `ANELASTICITY_RESULTS_SUMMARY.md` (§5h–§5j).
- `ANELASTICITY_TODO.md` (T20–T22), `ANELASTICITY_DONE.md`, `ANELASTICITY_METHODS.md`, `REQUIREMENTS.md`.
- The 10-12 restart for earlier detail.

**Python:** `source ~/cohen_env/bin/activate`. System python3 has no numpy.

Paths:
- `V` = `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3/1280atoms/V6.5669`
- `A0` = `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A0_MgO_Deng`
- `ED` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/Dislocations/edge_P175_T3500`
- `DFT` = `/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck`
- Tools: `/resnick/home/recohen/Claude/tools`

## 0. RC requests and decisions (10-13)

1. Run `T_dependence.py` and write a results file. Done: `results_Tdep/T_DEPENDENCE_RESULTS.md`.
2. Bridgmanite V_Mg + V_O shear sweeps at 50 and 20 GHz. Submitted 4446443 and 4446444; both have finished.
3. After reading Cordier 2023 (Nature, s41586-022-05410-9), Ita & Cohen (PRL 1997, GRL 1998), Guan et al. 2026 and Perez 2025 (all in `Papers/`):
   - Ita & Cohen–style free-energy integrations for vacancy formation free energies and diffusion rates.
   - Dislocations, using Guan's slip change at about 1800 K from [010](100) to [100](010) in bridgmanite.
   - Compare every result with previous work (plan §6 table; references still to collect are marked †).
   - "Pursue the comparison with Perez on MgO."
4. AskUserQuestion answers:
   - Ita grid plus Cordier geotherm points.
   - All three bridgmanite Schottky types.
   - The Deng model for both minerals (it is trained on MgO B1 and MgO melt).
   - Bridgmanite dislocations at 25 GPa plus V6.5669.
5. **New 10-13:** "The Ita and Cohen was also a model--not full DFT. Even the equation of state (so V at PT) may be different. We should do a DFT spot check. We have vasp and QE." DFT check started (§2.4).
6. Cordier Table 1 has a typo: E₀ = 0.4e-19 J should be 9.4e-19 J. Verified: with 9.4e-19 J their D is reproduced within 5 %.

## 1. Done 10-13

1. **T-dependence results file:** `results_Tdep/T_DEPENDENCE_RESULTS.md`; the README has the exact command.
   - `T_dependence.py` gained `--series` and `--defect-gk`.
   - MgO perfect B1: uniaxial 1 THz Q⁻¹ ∝ T^1.22±0.11; 0.2 THz is T-independent (Q⁻¹ ≈ 0.014).
   - Bridgmanite V_O hop rate Γ ≈ 5e9 to 2e11 s⁻¹, with E = 2.36 ± 0.12 eV. V_Mg is frozen below 5000 K.
2. **The 4000 K MgSiO₃ liquid linearity test (4406967) confirms nonlinearity.**
   - η′ = 114 ± 2 mPa s at 50 GHz and 202 ± 5 mPa s at 10 GHz, against GK 220.
   - **Still to do:** replace the 4000 K sweep slope in summary §5i.
3. **Phase A0, Frenkel–Ladd TI of the MgO bound Schottky pair (Deng model), job 4452757, done.** Preliminary results:

   | state | ΔG_f (eV), switching 40 ps | ΔG_f (eV), switching 20 ps | Ita & Cohen (eV) |
   |---|---|---|---|
   | 20 GPa, 2000 K | 5.15 ± 0.21 | — | 7.51 |
   | 140 GPa, 3000 K | 11.90 ± 0.24 | 12.68 ± 0.31 | 15.79 |

   - No hops occurred.
   - The 20 and 40 ps runs differ mainly in the P·ΔV term (formation volume 0.97 vs 1.09 Ω), so V_D − V_I needs longer NPT averaging.
   - Record: `A0/README.md`.
   - New tools: `build_b1_vacancy.py`, `ti_einstein.lammps`, `ti_array.sh`, `ti_einstein_analyze.py`. The command is `--gf <perfect> <bound> --L 2`; note the ts20 directories are named `P140_T3000_perfect_ts20`.
4. **MgO edge dislocation for the Perez comparison, job 4452807 (running).**
   - Setup: ½[110](001) edge in an 8232-atom slab, MgO-only model, 175 GPa / 3500 K, a = 3.7044 Å; τ = 0.1, 0.25, 0.5, 1.0 GPa for 30 ps each.
   - Speed: about 13 steps/s; finishes about 3.5 h after start.
   - Preliminary, τ = 0.1 GPa: v ≈ 320 ± 80 m/s and B ≈ 8e-5 Pa s, giving η_eff ≈ 120 down to 0.1 Pa s for ρ = 1e13 to 1e16 m⁻².
   - Problem: σ_yy averages about 168 GPa, not 175. Check the piston force (−P·A/n_top) against the stress-per-atom volume estimate.
   - New tools: `build_mgo_edge_slab.py`, `npt_lattice.lammps`, `disl_drive.lammps`, `disl_job.sh`, `disl_velocity.py`.
5. **DFT spot check set up** (§2.4).
   - New tools: `dft_snapshots.lammps`, `dft_snapshots_poscar.py`, `vasp_array.sh`, `dft_compare.py`.
   - Deng's training DFT, from `/groups/carnegie_poc/rcohen/LAMMPS/XDeng/MgSiO/MLP/inputs/MgO/inputs_*/INCAR`:
     - VASP with PBEsol (`GGA = PS`);
     - PAW_PBE Mg (13Apr2007) and O (08Apr2002);
     - ENCUT 800 eV, EDIFF 1e-6, LREAL A, ALGO VeryFast;
     - Fermi smearing with SIGMA = k_BT;
     - 128 atoms on a 2×2×2 Γ mesh.
6. Corrections recorded:
   - Summary §5c and the crystal_VMgO README: the fixed-V 2.44 eV leaves out P·v_f (≈ 12 eV at 140 GPa).
   - So thermal Schottky pairs are not expected; the extra vacancies are Frenkel pairs.

## 2. Next steps (in this order)

1. **Bridgmanite low-frequency vacancy sweeps 4446443 (4000 K) and 4446444 (5000 K): finished, not yet analysed.**
   - Run `sweep_watch.sh V/crystal_VMgO/4000K/FreqSweep_lowf:4446443:shear V/crystal_VMgO/5000K/FreqSweep_lowf:4446444:shear`, or collect directly with `anelastic_collect.py --cases tools/anelastic_cases_MgSiO3_V6.5669.py` (the lowf rows switch on automatically).
   - Compare with perfect bridgmanite and with MgO aged Schottky (Q 9.7 at 50 GHz, 3.7 at 20 GHz).
   - Update `T_DEPENDENCE_RESULTS.md` §2.3 and summary §5i/§5j.
2. **Edge dislocation 4452807: DONE, analysed and written up 10-13 (`results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md`, summary §5k; README there: B = 2.2e-4 Pa s; τ ≤ 0.25 GPa is not steady). Remaining:**
   - Run `python tools/disl_velocity.py $ED` for v(τ), B, η_eff(ρ) and the flow stress at 1e6 and 1e7 s⁻¹. Compare with Perez: η ≤ 1e2 Pa s, yield ≲ 1 GPa.
   - Check that the top block moves in the +x sense, that T_mob ≈ 3500 K, and the 168 vs 175 GPa issue.
   - Then: screw dislocation, T = 2000 and 5000 K, and an NX = 48 size check.
3. **A0 follow-up:**
   - separated pair;
   - longer NPT averaging for V_D − V_I;
   - the MgO-only model against the Deng model;
   - then A1 (Ita grid plus Cordier geotherm).
4. **DFT spot check (`$DFT`, README there). PART 1 DONE 10-14:** δΔG_f = +0.95 (20 GPa) and +1.27 eV (140 GPa); EOS fine (ΔP ≤ 0.3 GPa); corrected ΔG_f 6.10 and 13.2–14.0 eV, against Ita & Cohen 7.51 and 15.79. Next is part 2 (static). **Model comparison written up 10-14** (`results_dft/MGO_DFT_MODEL_COMPARISON.md`, summary §5l). The MgO-only model's pressure is 7–13 GPa above experiment (probably PBE; RC to confirm its training settings), and its δΔG_f is +0.72/+0.96 eV. VIB is 1–2.6 eV above DFT. Open items: relabel the MgO-only pressures; run a PBE check once the settings are known. Older detail:
   - Snapshots: MD 4480280 is done (4 states × 8 frames). The VASP dirs `$DFT/<state>/fNN` are built.
   - Pressures: DeePMD virial P (no kinetic part) is ≈ 17 GPa for P20 and 134 GPa for P140.
   - **VASP test 4486053 OK (7 min/frame; ΔP = +0.28 GPa, force RMSE 0.07 eV/Å); **production array 4487158 (31 frames)**** (1 frame, `P140_T3000_bound/f00`, 32 ranks, 2 h; `vasp_gam` from `~/bin`) is pending.
   - When it finishes:
     - check `slurm-4486053_1.out`, the elapsed time and MaxRSS;
     - check that the TOTEN is near the DeePMD pe (−2607.0 eV for f00) and that it converged in fewer than 200 SCF steps.
     - **If it is OK**, submit the array from `$DFT`: `sbatch -J MgOdft --array=1-32 vasp_array.sh`. tasks.txt has 32 lines, including f00, which could be skipped.
     - **If it is not OK** (e.g. it timed out at 32 ranks), adjust the time or the NCORE setting.
   - Analysis:
     - `python tools/dft_compare.py --gf $DFT/P140_T3000_perfect $DFT/P140_T3000_bound --L 2 --temp 3000` and the same for P20 with `--temp 2000`;
     - Eq. 1: ΔE = E_DFT − E_DP; Eq. 2: ΔP at fixed V (the EOS error); Eqs. 3–4: the FEP estimate of the model error in ΔG_f.
   - Part 2: static relaxed ΔH_f (64- and 216-atom cells, bound and separated) at 0, 20 and 140 GPa, DFT against DeePMD. Compare with Karki & Khanduja 2006 and with Ita & Cohen.
   - QE cross-check only if needed.
5. **MgO 3×1 NEB rerun 4407041: finished 10-12, analysis still pending** (summary §5h; see the 10-12 restart §2.1).
6. **Later:**
   - migration free energies via PLUMED (`fix plumed` is available; colvars is not);
   - all three bridgmanite Schottky types;
   - B2: bridgmanite slip systems at 25 GPa (1400–2500 K across Guan's 1800 K transition) and V6.5669;
   - collect the † references.
