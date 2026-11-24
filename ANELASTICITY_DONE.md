# Anelasticity DONE

## 2026-10-05

- Read the user's notebooks, LAMMPS inputs and submit scripts for runs 54671682 (xz shear) and x/R1A1/2267049 (x uniaxial) at 8000 K. Listed six problems in the notebooks (restart doc §2).
- Wrote `tools/anelastic_lockin.py`. Validated on synthetic data with flips, duplicates and bin averaging (exact recovery of $G'=20$, $G''=60$ GPa). Reanalysed both 8000 K runs: $\eta'(1\,\mathrm{THz})=0.0068\pm0.0008$ Pa s; $\zeta+\frac43\eta=0.0142\pm0.0001$ Pa s.
- Calibrated the fluctuation–dissipation noise model ($C\approx8$) on run 54671682.
- Wrote `tools/anelastic_sweep.lammps` (restartable, `units box`, flips allowed) and `tools/anelastic_sweep_setup.py` (cost table, tasks, array job).
- Flip test on an LJ liquid (job 4014216): passed. Found that `fix deform` defaults to lattice units.
- `dp --tf compress` of `graph.pb` succeeded (job 4014215, 26 s).
- Timing of uncompressed `graph.pb` with the conda env: 3.86 s/step (job cancelled after 100 steps). Cause open (TODO T1).
- Cancelled before start: H200 and L40S timing jobs (4013744, 4013745), first P100 jobs with a non-standard header (4013850, 4014111), 512-atom job (4014009).
- Wrote `ANELASTICITY_PLAN.md` and these restart docs.

## 2026-10-06

- **GPU DeePMD fixed.** The conda CPU TensorFlow libs shadowed the pip CUDA TensorFlow in `deepmd_py311`; moved them to a backup dir and rebuilt deepmd-kit v3.2.0 against the pip TF with CUDA for sm_60 (`deepmd-kit/source/build_gpu`). TF now creates the P100 device. (T1 done.)
- Measured on P100, 4096 atoms: `graph.pb` 8.1 steps/s, `graph_c.pb` 22.8 steps/s; step-0 energy and pressure agree.
- Sweep cost re-derived (T3): shear sweep 0.6 M steps, about 0.3 P100-days with the compressed model.
- Added uniaxial mode to `anelastic_sweep.lammps`, `anelastic_sweep_setup.py` and `anelastic_lockin.py`; wrote `sweep_watch.sh`.
- Fixed two input bugs (`pe` in thermo_style, `elif` syntax) and added start-from-`eq.data`. Tested all three start paths on a P100 (T5 done).
- Submitted the shear sweep (4113924) and the uniaxial x sweep (4115169) at 8000 K. Cancelled/failed attempts: 4109686 (uncompressed, cancelled), 4112680 (`pe`), 4113591 (`elif`).
- First sweep result, xz shear at 5 THz: $G'=87.2\pm5.6$, $G''=98.0\pm5.6$ GPa, $\eta'=3.12\pm0.18$ mPa s.
- Shear sweep (4113924) complete: $\eta'$ plateaus at ≈ 8 mPa s for f ≤ 200 GHz. Linearity repeat at 50 GHz (4115423, γ₀ = 0.095) agrees with γ₀ = 0.32 within $0.6\pm1.0$ mPa s. Uniaxial P0.2, P1, P5, P20 done.

## 2026-10-07

- **T2 done.** `tools/compare_dp_models.py` (job 4146365, CPU): `graph_c.pb` vs `graph.pb` on four 8000 K configurations: force difference 1 µeV/Å rms, 12 µeV/Å max (forces 5.0 eV/Å rms); energy < 10⁻⁷ eV/atom; virial/V < 10⁻⁴ GPa.
- **Thermostat test** (4145234, uniaxial, P = 1 ps, ε₀ = 0.03, from `FreqSweep_x/P1ps_r0/eq.data`, dir `FreqSweep_x_tauT`): $M'$ = 684, 540, 609 GPa and $M''$ = 61, 93, 73 GPa for $\tau_T$ = 1.0, 0.1, 0.02 ps. Confirms the thermal-relaxation artefact (restart §3). Added optional `-var TDAMP` to `anelastic_sweep.lammps` (default 0.1).
- **Green–Kubo set up.** `tools/gk_stress.lammps` (NVT equilibration, then NVE; pressure tensor every 2 fs; MSD; restartable) and `tools/gk_viscosity.py` (Eqs. 1–8 of its docstring). The analysis tool was validated on synthetic Maxwell data ($\eta=10$ mPa s exact; recovered $9.7\pm0.4$). LAMMPS input tested on P100 (4146366; `min()` is not a LAMMPS formula function, so it uses `ternary`), 24.4 steps/s.
- Submitted GK production: 4146463 (8000 K) and 4146464 (7000 K), 1.5 ns NVE each, both started from `8000K/FreqSweep/P1ps_r0/eq.data`.

## 2026-10-07: 8000 K frequency sweeps complete
- Shear xz (4113924) 5 THz–10 GHz: $\eta'$ plateau $\eta_0\approx8$ mPa s for f ≤ 200 GHz; linearity confirmed at 50 GHz (γ₀ 0.095 vs 0.32 agree, 4115423).
- Uniaxial x (4115169, τ_T = 0.1 ps) finished: $M'=581.9\pm1.0$, $M''=1.16\pm0.64$ GPa at 10 GHz. $M'$ ≤ 200 GHz gives $K_T\approx582$ GPa; $M''$ is thermostat-contaminated at all frequencies (restart 10-07 §3, §5), so no ζ from this sweep. Rerun: 4147331 (`FreqSweep_x2`).

## 2026-10-08
- Sent RC fig_vs_T and fig_Q. Wrote `ANELASTICITY_METHODS.md` (methods, tools, pitfalls, porting checklist).
- Aged Schottky sweep 4230009 had failed (write_data needs a pair style); fixed `restart2data.lammps` (pair_style zero) and resubmitted as 4233462.
- `anelastic_collect.py --cases`: case tables moved to `tools/anelastic_cases_MgO_V6.6868.py` (output unchanged) and `..._V9.6397.py`.
- Trajectory dumps (`DUMPN`, `DUMPSTEPS`) in `anelastic_sweep.lammps`; generic `sweep_array.sh`, `gk_job.sh`, `launch_after_eq.sh`.
- `build_defect_crystals.py`: rcut defaults to 0.3185 a (fixed 1.2 Å gave 1.35 Å contacts at a = 4.256 Å).
- Submitted sample trajectories (4233485) and the V9.6397 GK runs 4233549–54; sweeps auto-launch on eq.data.

## 2026-10-09 (see ANELASTICITY_RESTART_2026-10-09.md §1)
- Results summary doc; final collects for both volumes (crystallized V9.6397 4000 K tasks excluded).
- New figures: fig_vs_T revised, fig_kk, fig_effective_viscosity; collect calls the effective-viscosity plot.
- OCTP built as a plugin (CMake) and tested: equivalent to GK, no gain at long lags.
- T17 vacancies: hop statistics, NEB barriers and TST, elastic dipoles. Bound-pair Zener loss is negligible; the THz defect loss is dynamic.
- T18 grain boundaries: equilibrium sliding friction at both volumes, static γ-lines, provisional grain-scale Q model; size test running (job 4283403).
- Watcher fix (N ≥ M completion).

## 2026-10-10
- GB sliding size test (4283403, all 4 tasks complete) analysed: results summary §5f, `results/fig_gb_size`. At V9.6397 3000 K, β_x = 2–10×10⁶ Pa s/m for 1×–9× area with no trend, so the mechanism is local and β is transferable. At V6.6868 5000 K the 9× cell is still locked in both directions (β ≥ 1.5–3.7×10⁹).
- 140 GPa driven GB motion (4330883) and zero-stress quench and NEB (4334633–36, 4335408–10, 4335884–88): shear-coupled migration at τ ≥ 2–3 GPa. The 1× cell NEB barriers are collective (14–28 eV, 0.25–0.5 J/m²), so not transferable. Summary §5g. A 3×1 driven run (4336984) tests for disconnections.

## 2026-10-11
- 3×1 driven runs (4336984_1–6) analysed (summary §5h, `GBslide/drive/analysis_3x1`). The onset is unchanged at 5000 K (1.5–2 GPa). At 4000 K there was one step at 2 GPa and none at 2.5 GPa (stochastic).
- LAMMPS quench of 5000 K / 2 GPa frames 9–17 (job 4346903, `tools/gb_quench.lammps`, `drive/gb_quench_job.sh`). Frames 10 and 12–16 are symmetry-equivalent minima one coupled-migration period apart (Δu = 1.18 Å, ΔE = 0). z_b is uniform in x, so there is no localized disconnection. ASE quench fails at 11 760 atoms (nlist), jobs 4346889 and 4346900.
- New tool `tools/gb_quench_u.py`: energy, u, and slab-resolved z_b of the quenched frames. It fixes the stale-image-flag unwrap.
- 3×1 NEB (frames 10 → 12) submitted as 4359736. `gb_event_neb.py` now uses ASE neighbour lists.
- MgSiO3 started (restart 10-11 §3): model compressed and checked; a 1 THz test sweep on 1280-atom bridgmanite at 100 GPa and 2000 K gave G′ = 239 GPa (Q ≈ 240) and M′ = 803 GPa (Q ≈ 190). The sweep tools are generalized with MASSES and FPARAM.

## 2026-10-12
- All MgSiO3 GPU jobs complete (4364278–4364297). Lock-in run on all 62 sweep tasks. GK analysed: no crystallization down to 4000 K (D still 3×10⁻¹⁰ m²/s at 4000 K), and η₀ = 7.5 / 12.8 / 23.2 / 220 mPa s at 7000 / 6000 / 5000 / 4000 K. The sweep slopes agree at ≥ 5000 K. Collected into `results_MgSiO3_V6.5669/`; summary §5i compares with MgO.
- `anelastic_collect.py`: per-case GK cutoff (`GKTC`), crystal branch (`XTAL`) drawn as separate lines in `fig_vs_T`, optional `SOLID_SPAN`/`SOLID_LABEL`, KK check keyed on the "solid" label. Fixed a ternary bug that truncated crystal rows of the GK spectrum table. The MgO collect was regenerated.
- New case file `tools/anelastic_cases_MgSiO3_V6.5669.py`.
- 4000 K MgSiO3 shear points at 10 and 50 GHz are nonlinear (γ₀ = 0.5 and 0.32). Linearity test submitted (4406967). Methods §1.4: amplitude rule for supercooled liquids.
- Bridgmanite crystal: 5 THz internal-strain resonance (M′ falls, M″ rises, KK fails), absent in B1 MgO (summary Eq. 14).
- MgO 3×1 NEB (4359736) analysed. Stage-1 barrier ≈ 29.5 eV (0.175 J/m²); the climbing stage diverged. `gb_event_neb.py` gained a stage-1 save, a guarded small-step climbing stage, checkpoints, `--from-band`, an x-localization report and a per-image result cache. Smoke test 4406805 passed; rerun 4407041.
- New `tools/build_vacancy_pairs.py`: bridgmanite V_Mg + V_O cells (6 pairs in 1280 atoms, the MgO Schottky density) at 4000 and 5000 K with identical sites; aging jobs 4407170 and 4407171.
- T dependence (RC question: single activation energy or T-independent?): new `tools/T_dependence.py`; `anelastic_collect.py` writes `results_gk.csv`; all three collects regenerated. Summary §5j: the liquids are super-Arrhenius (MgSiO₃ η E_loc 1.6 → 3.6 eV, VFT T₀ ≈ 2800 K; MgO 1.3 → 1.8 eV). Crystal THz loss is not activated (perfect bridgmanite Q⁻¹ ∝ T¹·⁰; melt-grown MgO at 18 GPa T-independent).
- Submitted (RC approved): MgO perfect-B1 T series at V6.6868, ladder 4407426 and sweeps 4407427 (4000 K) and 4407428 (3000 K), recorded in `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/B1perfect_Ladder/README.md`. Added to the MgO case file. `T_dependence.py` takes repeated `--crystal-dir`; `results_Tdep/README.md` holds the command. MgSiO₃ V_Mg + V_O 3000 K cell built (same sites), aging 4407370.
- MgSiO₃ V_Mg + V_O aging done at 4000 and 5000 K (4407170, 4407171): stable, vacancies mobile. Production submitted: GK 4407925/4407927 and sweeps 4407926/4407928. Record: `V6.5669/crystal_VMgO/README.md`. Case file updated (keys '<T> VMgO').
- MgSiO₃ V_Mg + V_O 3000 K aging done (4407370, stable); production GK 4408168 and sweep 4408169 submitted.

## 2026-10-13

- All 10-12 jobs finished: NEB rerun 4407041 (2 h 40 min, analysis pending), 4000 K MgSiO₃ linearity test 4406967, MgO perfect-B1 ladder and sweeps 4407426–8, bridgmanite V_Mg + V_O GK and sweeps at 3000/4000/5000 K (4407925–8, 4408168–9). Lock-ins run (`sweep_watch.sh`), both collectors rerun.
- 4000 K MgSiO₃ linearity test: η′ = 114 ± 2 mPa s at 50 GHz (γ₀ = 0.05) and 202 ± 5 mPa s at 10 GHz (γ₀ = 0.1), against 110 and 220 expected from GK. Confirms that the earlier halved η′ was nonlinearity. Summary §5i not yet updated.
- `tools/T_dependence.py`: new `--series` (per-case crystal series by path substring) and `--defect-gk` (crystal D from GK MSD). Rerun with every new series; written results in `results_Tdep/T_DEPENDENCE_RESULTS.md`; summary §5j item 4 updated. Key results: perfect-B1 MgO uniaxial $Q^{-1}\propto T^{1.2}$ at 1 THz and T-independent at 0.2 THz; bridgmanite vacancy THz excess unresolved (about 1σ); O vacancies in bridgmanite single-E 2.36 ± 0.12 eV; Mg vacancies frozen below 5000 K; Si mobile at 5000 K.
- Submitted (RC approved): bridgmanite V_Mg + V_O shear sweeps at 50 and 20 GHz, 4000 K (4446443) and 5000 K (4446444); γ₀ = 0.02, from the 1.5 ns GK end state. Record: `V6.5669/crystal_VMgO/README.md`. The case file gets `FreqSweep_lowf` rows (added once lockin_results.txt exists).
- Read Ita & Cohen 1997 (PRL) and 1998 (GRL), Cordier et al. 2023, Guan et al. 2026 and Perez et al. 2025 (`Papers/`). Wrote `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` (free energies, diffusion, dislocations; costs; decisions). Checked the build: `fix ti/spring`, `fix plumed` (libplumed linked), centro/CNA available; colvars, ovito and atomsk are not. Deng MgSiO₃ model training covers bridgmanite and MgO at 20–160 GPa.
- Found: Cordier Table 1 $E_0=0.4\times10^{-19}$ J is a typo for 9.4×10⁻¹⁹ J; their Table 2 D values are reproduced within 5 % with the latter.
- Correction added to summary §5c and the `crystal_VMgO` README: the fixed-V "formation energies" (2.44 eV MgO, ≈ 1.9 eV bridgmanite) leave out $P\,v_f$ (≈ 9–16 eV at 110–190 GPa). Thermal Schottky pairs are not expected in our MD; the extra vacancies above 4500 K in fixed-N MD are Frenkel pairs.
- Free-energy machinery (T20): `tools/build_b1_vacancy.py`, `tools/ti_einstein.lammps`, `tools/ti_array.sh`, `tools/ti_einstein_analyze.py`. Smoke test 4452700 passed (after fixing ave/atom of xu). A0 submitted as 4452757 (`LAMMPS/FreeEnergy/A0_MgO_Deng`).
- MgO dislocations for the Perez comparison (T21): `tools/build_mgo_edge_slab.py`, `tools/npt_lattice.lammps`, `tools/disl_drive.lammps`, `tools/disl_job.sh`, `tools/disl_velocity.py`. Smoke test 4452709 passed (after switching to centroid/stress/atom): a = 3.7037 Å at 175 GPa / 3500 K, MgO-only model. Production 4452807 (`LAMMPS/MgO/Dislocations/edge_P175_T3500`).

## 2026-10-13 (later)
- **A0 TI 4452757 finished; preliminary analysis** (`A0_MgO_Deng/README.md`). Bound-pair ΔG_f:
  - 5.15 ± 0.21 eV at 20 GPa / 2000 K;
  - 11.90 ± 0.24 eV (switching 40 ps) and 12.68 ± 0.31 eV (20 ps) at 140 GPa / 3000 K;
  - Ita & Cohen: 7.51 and 15.79 eV.

  No hops. The P·ΔV term is not yet converged.
- **Bridgmanite low-frequency vacancy sweeps 4446443 and 4446444 finished** (not yet analysed).
- **DFT spot check started** (RC request; `/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck/README.md`):
  - Settings: Deng's training INCAR (PBEsol, 800 eV, SIGMA = kT).
  - Snapshot MD 4480280 done: 4 states × 8 frames.
  - VASP 1-frame test 4482343 submitted.
  - New tools: `dft_snapshots.lammps`, `dft_snapshots_poscar.py`, `vasp_array.sh`, `dft_compare.py`.
- Restart written: `ANELASTICITY_RESTART_2026-10-13.md`.
- **MgO edge dislocation 4452807 analysed** (175 GPa, 3500 K):
  - B = 2.2e-4 Pa s, from v ∝ τ at 0.5–1 GPa;
  - η_eff = B/(ρb²) = 330 down to 0.33 Pa s for ρ = 1e13 to 1e16 m⁻², consistent with Perez's η ≤ 1e2 Pa s for ρ ≳ 3e13;
  - no steady glide at τ ≤ 0.25 GPa.

  Plot: `edge_velocity.pdf`. `disl_velocity.py` now has `--plot`.
- **Write-up:** `results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md` and summary §5k (RC: "Please write this up").

## 2026-10-14
- **DFT spot check, part 1, done** (VASP array 4487158 plus test 4486053; PBEsol, Deng training settings; 8 snapshots × 4 cells):
  - DeePMD pressure within 0.3 GPa of DFT, so the EOS is fine;
  - force RMSE 0.07 eV/Å;
  - bound-pair ΔG_f model error +0.95 ± 0.08 eV (20 GPa / 2000 K) and +1.27 ± 0.09 eV (140 GPa / 3000 K);
  - corrected ΔG_f = 6.10 and 13.2–14.0 eV, against Ita & Cohen 7.51 and 15.79;
  - the vacancy pair has electronic entropy (gap states): T S_el = 0.17 and 0.80 eV.
- **VASP launch fix:** `~/bin/vasp_gam` needs oneAPI 2025.3 plus `~/lib` (HDF5), and Intel `mpirun`. srun ranks lose the oneAPI environment. Four failed tests: 4482343, 4484497, 4485052, 4485862.
- **Model comparison against DFT and experiment** (RC: "What is the DFT comparison with my MgO model…", "Please write up the comparisons"):
  - The MgO-only model was re-scored on the same DFT frames (`tools/dp_rescore.py`; `dft_compare.py --tag`).
  - It gives +5 to +9 GPa relative to PBEsol at fixed V, and +7 to +13 GPa relative to the Tange 2009 EOS (probably PBE).
  - Force RMSE 0.054–0.074 eV/Å; bound-pair δΔG_f +0.72 and +0.96 eV.
  - VIB EOS: −1 and −10 GPa relative to Tange; VIB ΔG_f is 1.0–2.6 eV above DFT.
  - Write-up: `results_dft/MGO_DFT_MODEL_COMPARISON.md` (figure `mgo_dft_model_comparison.pdf/png`, `tools/plot_dft_model_comparison.py`) and summary §5l.

## 2026-10-15
- Discussed kinetic Monte Carlo for frequencies between NEMD and diffusion. RC chose driven discovery of collective events, focused on dislocations and grain boundaries with a grain-size model. Wrote `ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md`.
- Analysed 3×1 boundary NEB 4407041: barrier 28.3 eV (0.168 J/m²), not converged; the saddle is collective (uniform over x-slabs). Recorded in summary §5h.
- `disl_drive.lammps` / `disl_job.sh`: optional `DUMPN` trajectory dump of the mobile atoms. D1 submitted (4593708–4593711).
- PBE spot check 4520046 submitted 10-14 (MgO-only model functional test); waiting in the queue.
- **Read the papers RC added** (van Driel thesis and PCM 2020, Cordier 2012 + SI, Carrez 2009, Ferré 2007, Fei 2023, Ritterbex 2020, and two Cordier mineral papers). Notes with numbers and comparisons: `LITERATURE_NOTES_2026-10-15.md`. Plan revised (`ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md` §5: D0, D1b, G0, G4 emphasis, the T20 link).
- New tool `tools/disl_core_track.py`: core position x_c(z, t) per line slice from the glide-plane disregistry (kymograph). Tested on the first D1 frames.
- **Fei et al. 2023 compared in detail** (`results_fei2023/FEI2023_COMPARISON.md`; tool `tools/fei2023_model.py` re-implements their growth and creep model).
  - Their printed climb Eq. 3 is dimensionally wrong; their figure needs ×3.3 on the Nabarro form. The k-fit signs are inverted in the text.
  - MgO vs Bdg in their framework: the viscosity ratio spans 10⁷ depending on periclase transport.
- **Cordier et al. 2023 compared in detail** (RC: the intended paper; `results_cordier2023/CORDIER2023_COMPARISON.md`).
  - E₀ = 9.4×10⁻¹⁹ J verified numerically against their Table 2.
  - Our VIB→DFT ΔG_f correction speeds D_O by ×8–1900 (Eq. 2 there), which cuts their 10³–10⁷ contrast by 1–3 orders. Near 800 km "periclase slower" is no longer secure.
  - A grain-boundary O path in MgO (our Σ5 δD_b, upper bound) could reverse the contrast (lever about 10⁷). New high-priority item G-diff.
- D1b long-line runs submitted (4602367/8). RC approved: bridgmanite boundaries (van Driel [100] tilts) and the long runs.
- **New builders (10-15):**
  - `tools/build_mgo_polycrystal.py`: periodic Voronoi MgO; `.grains` atom→grain map plus an orientation JSON. Tests in `Downloads/mgo_poly_test/`: 26.5 k atoms with 8 grains of about 3.7 nm, about 19 % boundary atoms.
  - `tools/build_bdg_tilt_gb.py`: symmetric [100]-tilt Pbnm bicrystals (van Driel planes) with `--scan` rigid shifts. Tests (021)/(013)/(011) with 6.6–7.5 k atoms in `Downloads/bdg_gb_test/`. Interiors match bulk; ambient fractional coordinates; a, b, c should come from the Deng NPT cell (`--abc` / `--ref-data`).
  - Neither has been minimised yet.
- OCTP open item in the results summary §7 marked done (it was finished 10-09).
- **Deng-model state runs set up and submitted** (RC 10-15; `LAMMPS/DengStates/README.md`): new tools `build_bdg_bulk.py`, `state_lattice_array.sh`, `gb_min.lammps`, `bdg_gb_scan_job.sh`, `bdg_gb_energy.py`, `gb_diff.lammps`, `gb_diff_job.sh`, `poly_anneal.lammps`, `poly_anneal_job.sh`; `npt_lattice.lammps` extended (NA NB NC, BARO, FPARAM; backward compatible).
- New tool `tools/gb_diff.py` (G-diff): boundary-resolved in-plane D(s) and δD_b with grain sliding removed. Synthetic test recovers δD_b to 2 %; a linear-ramp sliding correction overestimates it by 60 % when sliding is a step, so the step correction is the default.
- r-RESPA with DeePMD assessed (answer to RC; see restart 10-15 item 9).
- RC 10-15: r-RESPA is not worth 2–3×; time-step test 1–5 fs submitted instead (4620528; tools `dt_test_job.sh`, `dt_test.lammps`, `dt_test.py`).

## 2026-11-15
- D1/D1b (4593708–11, 4602367/8) analysed: glide-plane core tracking (tool fixed: wrong plane pair), B = (1.755 ± 0.027)e-4 Pa s, no threshold, no length dependence. Found and fixed the non-rigid top block in `disl_drive.lammps` (aveforce on unequal masses → `fix rigid/nve single`). `results_dislocations/` §8, figure `edge_vtau_core`. New tool `disl_vtau_plot.py`; `disl_core_track.py` now prints v ± err and B and plots the line shape.
- PBE single points (4520046) analysed: MgO-only model is PBE-trained; ΔG_f model error 0.5–0.9 eV vs PBE. `results_dft/` §8.
- G-diff MgO Σ5 (4612246_1–5) analysed; `gb_diff.py` now also gives β (Eq. 4) and writes `gb_u.dat`. Cordier doc §5.
- Time-step test (4620528) analysed; `dt_test.py` handles blow-ups and gives block errors. 2 fs recommended for production.
- MgO polycrystal (4612253) checked: no grain growth in 300 ps.
- Bdg lowf sweeps (4446443/4) analysed: no resolved loss at 20–50 GHz. T-dependence doc §2.3. MgSiO₃ collect rerun.
- `bdg_gb_energy.py`: energy-only γ_E column (Eq. 3).
- RC1 talk trajectories: `LAMMPS/TalkTrajectories` (6 movies), tools `traj_for_vmd.py`, `vmd_movie.tcl`.

## 2026-11-16
- A1 (6930969/70) and A2 (6931057) analysed: `results_freeenergy/MGO_VACANCY_FREE_ENERGIES.md` (formation, migration, Ita & Cohen comparison, D vs Cordier). `vac_mig_analyze.py` generalised (saddle = max G, barrier from the minimum; full paths; hop skipping).
- Matched-(P, T) liquids (6931065) analysed: `LIQUID_SE_ODENSITY.md` §6, new tool `liquid_pt.py`, figure `results_Tdep/liquid_pt.{pdf,png}`.
- Schottky 20 GHz at 4000/4500 K (6929639/40) and cell-size test (6929874) analysed: `T_DEPENDENCE_RESULTS.md` §2.4.
- Σ5 60 GPa T series (6929623) analysed: Cordier doc §5.1.
- A3 bridgmanite set up and submitted (RC 11-16): TI 6957232/6957233, hops 6957279/80, migration 6957324, smoke 6957192–4, 6957247/8, 6957282. New tools `build_bdg_vacancy.py`, `bdg_schottky_analyze.py`, `vac_mig_indep.lammps`, `site_hops.lammps`, `site_hops.py`, `hops_array.sh`.
- A3 perfect TI (6957232) finished; A3 direct-MD hops at V6.5669 (6957279_1–2) analysed: isolated V_O Γ_v = 6.0×10¹⁰ (3021 K), 3.1×10¹¹ s⁻¹ (4020 K), E ≈ 1.7 ± 0.4 eV, 10–12× the MD-cell rate (A3 README).
- RC 11-16 "Yes do 1 2 3 4 5": submitted (1) separated-pair DFT check 6963424 → 6963519 (VASP stage 2); (2) Schottky 20 GHz reruns 6963124 (8×8×8, 2 ns), 6965639_2 (same at γ₀ = 0.01, linearity) and 6963125 (6×6×6, 1.5 ns ageing); (3) Σ5 at 90/120 GPa 6963084; (4) MgO TST check 6963299/6963300 (`FreeEnergy/A2b_MgO_TSTcheck`); (5) liquid g(r) for Rosenfeld scaling 6963196. New tools `liquid_rdf.lammps`, `rosenfeld.py`; `VASP/MgO_vacancy_DFTcheck/sep/{build_sep.py,relax_dp.lammps,make_vasp_relax.py,stage2.sh}`.

## 2026-11-16, evening
- A3 analysed (6957233, 6957324, 6957280_3): `results_freeenergy/BDG_VACANCY_A3.md` (+ `A3_analysis.txt`). O-vacancy barriers 0.9–1.9 eV, TST vs MD κ ≈ 0.6; V_Mg 4.7–6.0 eV; formation runs compromised by O hops (hop-free subset provisional); Si migration unusable. New options `--maxdr` in `ti_einstein_analyze.py` and `bdg_schottky_analyze.py`.
- MgO TST check (A2b, 6963299/6963300) analysed: κ = 0.5–1.6 (mean 1.0) for free vacancies; `MGO_VACANCY_FREE_ENERGIES.md` §6. `site_hops.py` now tracks the cation–O vacancy distance (vac_pair.dat) and splits bound/free rates.
- Σ5 at 90/120 GPa (6963084) analysed: locked at all 6 states up to 3400/3800 K; `CORDIER2023_COMPARISON.md` §5.2.
- Rosenfeld g(r) job 6963196 produced no data (fix ave/time Nfreq vs timestep); `liquid_rdf.lammps` fixed, rerun 6999519.
- Rosenfeld g(r) rerun 6999519 analysed: both melts collapse on s₂ (D*_O 8 % rms, η* 10 %); `LIQUID_SE_ODENSITY.md` §7 (also repaired the corrupted Eq. 2 there), `results_Tdep/rosenfeld.{pdf,png,txt}`.
- A3 redo (A3b) set up and submitted (RC "Yes, run the A3 redo"): smoke 7000244 (FL with fixed fparam) and 7000291 (ladder; 7000245 failed on `$(pe)` after reset_timestep, fixed) passed; production 7000466 (16 FL), 7000467 (8 ladders), 7000468 (8 migration). New tools `tint_energy.lammps`, `tint_array.sh`, `bdg_tint_analyze.py`, `bdg_mig_plot.py`; `build_bdg_vacancy.py` kinds vmg/vsi/vo1/vo2; `ti_einstein.lammps` FPARAM fixed/FPVAL; `ti_array.sh` FPVAL column and absolute BOXFROM.

- 11-17: session logs (RC request): `sessions/<date_time>_<id>.md` for all 7 Anelasticity sessions (2026-10-05 → now) + index README; new `tools/session_log_md.py`; Stop/SessionEnd hooks in `Anelasticity/.claude/settings.json` keep them current.

## 2026-11-17
- Session logs for all Anelasticity sessions in `sessions/` (new `tools/session_log_md.py`; Stop/SessionEnd hooks in `Anelasticity/.claude/settings.json`).
- A3b analysed (7000466/7/8, all 32 COMPLETED): hop-free; Schottky energies at 4 states (Table 2 of BDG_VACANCY_A3.md §5), V_Mg migration 3.9–6.1 eV, Si migration still unresolved (cooperative); intrinsic c and D in bridgmanite (§6): D_O ≈ 10⁵ × periclase. Ladder vs direct F_I differ by 0.4–0.8 eV (does not enter ΔG).
- Schottky reruns (6963124, 6963125) analysed: loss reproducible in 8×8×8 (27 ± 2 GPa), absent in 6×6×6 after 1.5 ns ageing; all vacancies in one nanovoid in both cells → void anelasticity (T_DEPENDENCE §2.5). New `tools/b1_vacancy_clusters.py`.
- A3b follow-ups submitted (RC "Yes do a and b"): TS 80 Frenkel–Ladd 7045833, V_Si MD 7045834, NEB tool `bdg_vac_neb.py` (smoke 7045934). Optional (c) added to TODO. Repaired corrupted LaTeX in restart 2026-10-07.
- γ₀ = 0.01 Schottky run (6965639) analysed: G″ 25 ± 5 vs 27 ± 2 GPa at γ₀ = 0.02 → linear; same nanovoid (T_DEPENDENCE §2.5).
- 2026-11-17 hcp-Fe set-up: VASP 6.6.1 built (std/gam/ncl, `VASP/VASP/vasp.6.6.1`); CPU LAMMPS with ML-VASP (`LAMMPS_VASP/lammps/build_cpu`, `~/bin/lmp_mpi_vasp`, 6.6.1 VASPml); GPU plugin `LAMMPS_VASP/plugin/vaspplugin.so` for the production lmp (works, = CPU to 1e-7 eV/Å; P100 0.31 steps/s, profile: unified-memory ping-pong). Fe training set analysed: bcc + liquid only, no hcp. Docs: `tools/vasp_lammps/README.md`, restart 11-17 §7.


## Archive: INPROGRESS §3 as of 2026-11-19 (open items now in QUESTIONS.md)

### (old) Waiting for RC (proposals, with costs; nothing submitted)

- **Fe Q and effective viscosity plan (RC 11-18): `ANELASTICITY_PLAN_FE.md`.** Phases A (hcp training + validation, gate), B (Q sweeps), C (vacancy/dislocation/boundary viscosity); ≈ 1110–1340 node-h full, ≈ 520 reduced (11-18 RC: training hcp + fcc 0–350 GPa, 300 K–T_m, ≤ 64 atoms, non-magnetic; A0 revised to 64-atom cells, ≈ 3–5 node-h) (11-18: fcc added to training after RC's question: ML_AB has no fcc or hcp crystal, `tools/mlab_structure.py`); first step A0 (≈ 15 node-h). Decisions for RC in its §8. Nothing submitted.
- **hcp Fe at inner-core conditions (RC 11-17), 300–350 GPa, 5000–7000 K, VASP MLFF (`pair_style vasp`):**
  - **Training set checked 11-17** (refit dir `/groups/carnegie_poc/rcohen/VASP/Fe/bcc/ML/Orthogonal/P300GPa`, ML_FF md5-identical to the sample): 913 × 128-atom bcc/liquid configurations, V/atom 6.6–7.5 Å³, static P 250–320 GPa; **no hcp**, and 350 GPa at or beyond the edge → on-the-fly training with hcp cells (VASP 6.6.1) needed before production; proposal with costs to RC.
  - **11-17 10:00: RC approved both builds (now in §1).** Found: an older ML-VASP CPU build exists (`LAMMPS_VASP/lammps/build/lmp`, 2026-03-31, minimal packages); the sample's start cell (`end.pos.start`, 8192 atoms, cubic 38.296 Å) is **not an hcp crystal** but a crystallized quench (12-NN q6 = 0.48, q4 = 0.13: mixed close-packed with defects), so the 5300–5600 K volume drop may be annealing/grain growth, not a phase change.
  - The old CPU binary `~/bin/lmp_mpi_vasp` is gone, so a LAMMPS build is needed: vasp-dev/lammps branch `vasp-mlff-6.6.0`, CMake, `-DPKG_ML-VASP=yes -DVASPML_DIR=...`.
  - VASPml 6.6.0 contains an undocumented NVIDIA GPU path for prediction (`PredictorGPU.cpp`, `DescriptorSHS*GPU.cpp`; NVHPC `-stdpar=gpu -acc -gpu=mem:managed,cc60`; commented out in `arch/makefile.include.nvhpc`); the current library was built with Intel (CPU only). The nvhpc/23.9 module exists.
  - Sample run (8192 atoms, 300 GPa, 80 → 8000 K ramp in 100 ps, 64 CPU cores): 6.5 steps/s. The V/atom kink near 5300–5600 K (−0.15 %) is worth a structure check; melting in the ramp (superheated) by ≈ 7800 K.
  - Plan proposed to RC: (1) CPU build; (2) GPU test build with NVHPC on P100, checked against the CPU forces and timed; (3) check that the ML_FF training set covers 300–350 GPa and 5000–7000 K; (4) hcp cells and the same anelastic protocol as MgO.

- A3b follow-ups (a), (b): approved and submitted 11-17 (§1). (c) DFT correction of the bridgmanite vacancy energies: optional, in TODO.

- ~~**A3 redo**~~ approved and submitted 11-16 (§1, A3b). Was (≈ 60 P100-h): O-vacancy hops spoil the Frenkel–Ladd runs of every bridgmanite cell with V_O, and the Si (and 30/60 GPa Mg) migration. Proposal: single-vacancy cells (V_Mg, V_Si, V_O1, V_O2) at the 4 states; formation by Frenkel–Ladd at T₀ ≈ 800–1000 K (fparam fixed at the target k_BT) plus ⟨E⟩(T) integration at fixed box (Eq. 5 there, immune to hops); Mg and Si migration in cells without V_O.
- **Σ5 follow-up (11-16):** why the unlocking T jumps between 60 and 90 GPa — static γ(u) scan or NEB of one event at 60 and 90 GPa (≈ 2–4 P100-h).

- **RC question 11-15: kMC for lower frequencies / effective activation energies.** Answer in restart 11-15 §4. Proposed runs:
  1. ~~Σ5 T series~~ and 2. ~~Schottky 20 GHz at 4000/4500 K~~: approved and submitted 11-15 (§1).
  3. ~~Cell-size test~~: submitted 11-15 (6929874).
- **D1 follow-up:** B(T) at 2000 and 5000 K with the rigid-block fix (≈ 40 P100-h); does a threshold appear at 2000 K?
- **Bdg γ:** anneal + quench (≈ 4 P100-h) and zoff scan.
- **Bridgmanite talk trajectory** (5000 K, V_Mg + V_O, short dump): ≈ 1 P100-h, if wanted for the talk.
- T26 liquids, A1/A2: done and analysed 11-16. A3: submitted 11-16 (§1).
- **11-16 proposals (a)–(e): all approved and submitted 11-16 (§1b).** Were: (a) DFT check of the MgO *separated* pair (VASP, 216/512 atoms; decides D_O vs Cordier, `results_freeenergy/MGO_VACANCY_FREE_ENERGIES.md` §4); (b) Schottky 20 GHz: 8×8×8 rerun 2 ns (≈ 22 P100-h) and 6×6×6 with 1.5 ns ageing (≈ 13 P100-h) (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.4); (c) Σ5 unlocking T at 90 and 120 GPa (replicas, ≈ 7 P100-h per run); (d) MgO direct hop rates vs A2 TST; (e) Rosenfeld scaling of the liquids (≈ 1 P100-h).
- Older: optional MgO liquid 7500/6500 K points; bridgmanite boundaries (RC literature check).


## 2026-11-19: bridgmanite talk trajectory (RC "Do the Bridgmanite talk trajectory")

- Job 7279725 (P100, 39 min, 87 steps/s): 6 V_Mg + V_O pairs, 1268 atoms, V6.5669, Deng model, 5000 K NVT, 200 ps from the aged `5000K/GK/restart.gk`; run dir `MgSiO3/1280atoms/V6.5669/crystal_VMgO/5000K/TalkTraj` (README).
- Movies (`traj_for_vmd.py --color disp`): `TalkTrajectories/Bdg_vacancy_hops_5000K` (401 × 0.5 ps) and `_first50ps` (251 × 0.2 ps); `vmd -e movie.vmd` tested in text mode.
- In 200 ps, 103 of 762 O, 12 of 250 Mg and 14 of 256 Si moved more than 2 Å from their start sites.

- 2026-11-19, **Fe A0c2 true shifted 2×2×2 k-mesh** (RC: "We should test a real shifted 2x2x2, and it should not include -k"): job 7279850_1–6 (debug), 4 explicit k-points (¼,¼,¼), (−¼,¼,¼), (¼,−¼,¼), (¼,¼,−¼) with KBLOWUP = .FALSE. (NKPTS = 4 checked in OUTCAR). Errors against 3³ at $k_BT$: 0.008–0.015 eV/Å, ≤ 0.1 GPa; against 4³ at 300 K: 0.026–0.087 eV/Å, 0.01 GPa at fcc 330 GPa (Γ-centred 2×2×2: 12.4 GPa). Wall 160–310 s vs 250–720 s for Γ-centred 2×2×2. Table `results_Fe/A0c_summary.txt`; recommendation in QUESTIONS item 2.
