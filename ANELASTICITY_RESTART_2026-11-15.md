# Anelasticity restart, 2026-11-15

Read first: this file, then `INPROGRESS.md`, `ANELASTICITY_TODO.md` (T23–T25, RC1) and summary §5m. The previous restart is `ANELASTICITY_RESTART_2026-10-16.md`.

## 1. State
All jobs submitted through 10-15 finished between 10-15 and 10-17. None are running. No new jobs were submitted today; every proposal below waits for RC (INPROGRESS §3).

## 2. Analyses done today (details: summary §5m)

| item | result | write-up |
|---|---|---|
| D1/D1b edge dislocation (4593708–11, 4602367/8) | B = (1.755 ± 0.027) × 10⁻⁴ Pa s, linear in τ from 0.15 to 0.5 GPa, no threshold, same for the 63 Å and 262 Å lines; no kink pairs | `results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md` §8, `edge_vtau_core.{pdf,png,txt}` |
| **Bug: top block in `disl_drive.lammps`** | `fix aveforce` with unequal masses: the block's Mg and O sublattices slid apart (30.3 vs 46.0 Å in 150 ps), so block-based v were 21 % low (also in job 4452807, §5k). Stress transmission was fine. Now `fix rigid/nve single` (untested on the GPU; check the first run) | same, §8.1 |
| Bug: `disl_core_track.py` plane pair | it used the two halves of one plane; fixed (planes at y_g − a/2 and y_g) | tool docstring |
| PBE single points (4520046) | MgO-only model is PBE-trained (P within 0.3–1.0 GPa of PBE, constant energy offset). Its ΔG_f error vs PBE is 0.5–0.9 eV; PBEsol − PBE only 0.05–0.16 eV | `results_dft/MGO_DFT_MODEL_COMPARISON.md` §8 |
| G-diff MgO Σ5, 5 states (4612246) | frozen in 1 ns at 27/2200, 30/2000, 90/2500, 120/2800 (δD_b < 10⁻²³ m³/s); at 60/2300 stick–slip sliding + migration, β_x = 7.4 × 10⁶ Pa s/m | `results_cordier2023/CORDIER2023_COMPARISON.md` §5 |
| dt test (4620528) | 2 fs fine for production (ΔP ≤ 0.3 GPa); Bdg fails at 3 fs (ΔP 0.75) and blows up at 5 fs; keep 1 fs for activated rates | `DengStates/README.md` |
| polycrystal (4612253) | runs on P100; no grain growth in 300 ps | `DengStates/README.md` |
| Bdg lowf sweeps (4446443/4) | G″ unresolved at 20–50 GHz (Q ≥ 65–280) vs MgO Schottky Q 9.7/3.7 | `results_Tdep/T_DEPENDENCE_RESULTS.md` §2.3 |
| Bdg γ | energy-only γ_E 2.49/2.57/1.77 J/m²; still 1.8× van Driel | `DengStates/README.md` |
| RC1 talk trajectories | 6 VMD movies | `/groups/carnegie_poc/rcohen/LAMMPS/TalkTrajectories/README.md` |

Note: RC wrote RC1 into `/resnick/home/recohen/Claude/Resnick/Anelasticity/ANELASTICITY_TODO.md` (and an identical `Claude/WSDA/Anelasticity/`), which are stale 10-07 copies of this directory. It was copied into the real TODO; the stale copies were not touched.

## 3. Tools changed or added today
`disl_core_track.py` (plane fix, v ± err, B, line-shape kymograph), `disl_drive.lammps` (rigid top block), `disl_vtau_plot.py` (new), `gb_diff.py` (β, `gb_u.dat`), `dt_test.py` (blow-ups, block errors), `bdg_gb_energy.py` (γ_E), `traj_for_vmd.py` and `vmd_movie.tcl` (new).

## 4. RC question 11-15: "Can we get lower frequencies using kinetic Monte Carlo? Or can we extract some effective activation energies?"

Answer given (short form):
- **Effective activation energies: yes, and we have several already.** O-vacancy hops in bridgmanite: 2.36 ± 0.12 eV, consistent with a single E (3000–5000 K). MgO vacancy hops: curved, E_loc 3.6 → 2.1 eV (Mg) and 4.6 → 2.1 eV (O) from 3500 to 5000 K. Σ5 sliding (MgO-only, 18 GPa): ≈ 2 eV, noisy. Missing: the activation energy of the loss itself (MgO Schottky 20 GHz loss known only at 5000 K) and of the 60 GPa stick–slip.
- **Lattice kMC is not the bottleneck.** A rate model, Q⁻¹(ω) = Σ Δ_i ωτ_i/(1 + ω²τ_i²), reaches any frequency once τ_i(T) and Δ_i are known; kMC only adds value when events are correlated. Two pieces of evidence argue against a vacancy kMC now: (i) the orientational (Zener) strength of the bound pair is ≈ 100× too small to give the loss we see (§5c), so a hop-catalogue kMC would miss the mechanism; (ii) MD O-hop rates are 2–3× faster than NEB-TST, so the catalogue is incomplete (§5b).
- **Scale argument.** With E = 2.4 eV, a process at 20 GHz at 5000 K moves to ≈ 80 MHz at 2500 K and ≈ 5 MHz at 2000 K. A single-site process with a 10¹³ s⁻¹ prefactor needs E ≈ 6 eV to sit at 1 Hz at 2500 K. Seismic-band loss therefore needs a length scale (grain size, dislocation segment) or a very high E (formation + migration). Both enter through mesoscale models: Nabarro–Herring/Coble (τ ∝ d²/D or d³/δD_b) and Raj–Ashby sliding with diffusional accommodation. Sliding with β = 7 × 10⁶ Pa s/m and d = 1 mm relaxes at ≈ MHz (τ ≈ βd/G); diffusional accommodation with δD_b < 10⁻²³ m³/s is far below 1 Hz; the seismic band lies between them.
- **Decisive cheap test proposed:** if the MgO Schottky 20 GHz loss is diffusional on the cell scale, its τ scales as L², which maps directly to grain size. A cell-size test (e.g. a smaller cell, peak should move up by (L₁/L₂)²) tells whether that mapping holds.
- **Proposed runs** (INPROGRESS §3): Σ5 sliding T series at 60 GPa (≈ 20 P100-h); MgO Schottky 20 GHz at 4000/4500 K (≈ 24 P100-h); optionally the cell-size test.

## 4a. Submitted after RC's OK (11-15): "Go ahead with the Σ5 T series and Schottky runs"
| job | what | record |
|---|---|---|
| 6929623_1–3 | Σ5 MgO, 60 GPa, 2000/2600/2900 K, 1 ns each (Deng) | `/groups/carnegie_poc/rcohen/LAMMPS/DengStates/MgO_S5_P60_Tseries/README.md` |
| 6929639 / 6929640 | MgO aged Schottky, shear 20 GHz, 4000 / 4500 K (V6.6868) | `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/{4000K,4500K}/FreqSweep_Schottky_aged/README.md` |

| 6929874_1–2 | Schottky cell-size test: 6×6×6, 8 pairs, 5000 K, 50 and 20 GHz, 2 ns each | `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/5000K/FreqSweep_Schottky_L6/README.md` |

Exact commands: `sbatch sweep.sh` in `FreqSweep_Schottky_L6`; `sbatch --array=1-3 gb_diff_job.sh` in `MgO_S5_P60_Tseries`; `sbatch sweep.sh` in each `FreqSweep_Schottky_aged`.

RC asked (11-15) what "O vacancies in bridgmanite" meant: the MgSiO₃ bridgmanite cell (Deng model, V = 6.5669 Å³/atom, 1280 − 12 atoms) with 6 neutral V_Mg + V_O pairs (an Mg and its nearest O removed; no Si vacancies); no charged defects and no charge correction (the DeePMD cell is neutral). The 2.36 eV is the apparent energy of O tracer diffusion in that cell at fixed vacancy number and fixed V: migration only, no formation term.

## 4b. Submitted later on 11-15 (RC: "Yes please start A1/A2" and "Yes please do" the matched-pressure liquids)
| job | what | record |
|---|---|---|
| 6930969 / 6930970 | A1 MgO formation free energies, 7 states (perfect, then defects at the perfect box) | `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A1_MgO_Deng/README.md` |
| 6931057 | A2 MgO migration (Mg, O), umbrella integration, 7 states (afterok A1 perfect) | `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A2_MgO_Deng_mig/README.md` |
| 6931065 | Liquids at matched (P, T), Deng model, MgO and MgSiO₃ | `/groups/carnegie_poc/rcohen/LAMMPS/LiquidPT_Deng/README.md` |

New/changed tools: `ti_einstein.lammps` (FIXBOX), `ti_array.sh` (BOXFROM, TLIM), `ti_einstein_analyze.py` (Eq. 3b), `vac_mig.lammps`, `vac_mig_analyze.py`, `mig_array.sh`, `liq_state_job.sh`, `gk_stress.lammps` (empty-type guard), `liquid_se.py`.

## 5. Priorities for the next session
1. RC's decisions on §4 and INPROGRESS §3.
2. First GPU run with the rigid-block drive: check `fix rigid/nve single` runs and dx_top now equals the glide-plane slip.
3. Polycrystal grain-ID / G-diff tool; Bdg γ anneal+quench.
4. Open older items: 3×1 NEB (4407041), summary §5i slope.

## 6. References for the rate model (RC asked 11-15)
Q⁻¹(ω) = Σ Δᵢ ωτᵢ/(1 + ω²τᵢ²) with thermally activated τᵢ: Nowick & Berry, *Anelastic Relaxation in Crystalline Solids* (Academic Press, 1972), chs. 3–4 (standard anelastic solid, relaxation spectra, point-defect relaxations, activation analysis); Zener, *Elasticity and Anelasticity of Metals* (1948). Mineral physics/seismic: Cooper (2002), Rev. Mineral. Geochem. 51, 253; Jackson & Faul (2010), PEPI 183, 151. Mechanisms: Raj & Ashby (1971), Metall. Trans. 2, 1113 (boundary sliding + diffusional accommodation); Granato & Lücke (1956), J. Appl. Phys. 27, 583 (dislocation string). Absorption band: Anderson & Minster (1979), GJRAS 58, 431.
