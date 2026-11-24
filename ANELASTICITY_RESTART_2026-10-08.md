# Anelasticity restart 2026-10-08

Read first: `ANELASTICITY_METHODS.md`, the self-contained guide to methods, tools, pitfalls and porting. Read it with `REQUIREMENTS.md`, `ANELASTICITY_TODO.md` and `ANELASTICITY_DONE.md`. `ANELASTICITY_RESTART_2026-10-07.md` §7–7h has the V6.6868 history.

Paths:
- `R6` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom`
- `R9` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V9.6397/4096atom` (new). RC's earlier NEMD runs at this volume are in `.../V9.6397/Viscosity/<T>K` and are left untouched.

## 0. What to check FIRST

`squeue -u recohen`, then work through the table.

| job | what | dir | action when done |
|---|---|---|---|
| 4163822 | GK perfect B1 5000 K (V6.6868) | `R6/5000K/GK_B1perfect` | resubmit `sbatch gk.sh` if it stopped before `PRODUCTION_STEP 1500000` |
| 4230008 (2 tasks) | bicrystal γ₀ = 0.03, P = 20 and 50 ps | `R6/5000K/FreqSweep_bicrystal_g3` | watcher bhcnwtat7 writes `lockin_results.txt` |
| 4233462 (3 tasks) | aged Schottky P = 5, 20, 50 ps, γ₀ = 0.02 | `R6/5000K/FreqSweep_Schottky_aged` | watcher bcsnblllp; check PE is stationary (`stress.dat` column 8, by quarters) |
| 4233485 (8 tasks) | sample trajectories (§2) | `R6/Trajectories` | check `traj.lammpstrj` frame counts |
| 4233549–54 | V9.6397 GK runs (§3) | `R9/...` | resubmit any that stopped at 24 h: `sbatch -J NAME --export=ALL,TEMP=..,DATA=..,NEQ=.. gk_job.sh` in the same dir (restart.gk is picked up) |
| (auto) | V9.6397 sweeps, submitted by `launch_after_eq.sh` when each GK `eq.data` appears | `R9/<T>K/FreqSweep*` | if the session died before launch, run `tools/launch_after_eq.sh ROOT NAME` by hand for each root that has no `slurm-*` files |

**Aged Schottky failure, now fixed.** The first submission (4230009) died after 13 s. `write_data` in `restart2data.lammps` needs a pair style; it now uses `pair_style zero 6.0`. Logs are in `failed_4230009/`.

**Final V6.6868 collect.** The waiter brgveib9t runs it only once no `GK*` or `MgO*` job is queued, which now includes the V9.6397 jobs. When the V6.6868 jobs are done, run it by hand:
`python tools/anelastic_collect.py` (the default case file is V6.6868).

## 1. Collect script refactor

`anelastic_collect.py` takes `--cases FILE`. All paths, labels, colours, box volumes, GK cut/skip values, the liquid set, the defect T and the plot ranges live in that file:
- `tools/anelastic_cases_MgO_V6.6868.py` (default; reproduces the 10-07 output exactly, checked by diff);
- `tools/anelastic_cases_MgO_V9.6397.py` (writes `Anelasticity/results_V9.6397/`).

Backup of the previous version: `Downloads/anelastic_collect.py.bak_2026-10-08`.

## 2. Trajectories (RC request 10-08)

`anelastic_sweep.lammps` now takes `-var DUMPN n -var DUMPSTEPS m`. It writes `traj.lammpstrj` (`id type x y z ix iy iz`, tilted box) every n steps during the first m production steps. Backup: `Downloads/anelastic_sweep.lammps.bak_2026-10-08`.

Sample runs, `R6/Trajectories` (job 4233485, generic `sweep_array.sh`):

| dir | system | drive | frames |
|---|---|---|---|
| liq8000_xz_P20_g0.32 | liquid 8000 K | shear P = 20 ps, γ₀ = 0.32, 3 cycles | 301 (every 0.2 ps) |
| liq8000_xz_P1_g0.016 | liquid 8000 K | shear P = 1 ps, 5 cycles | 501 (every 10 fs) |
| liq8000_x_P5_e0.02 | liquid 8000 K | uniaxial P = 5 ps, ε₀ = 0.02, 3 cycles | 601 |
| B1perfect5000_xz_P20_g0.03 | perfect B1 5000 K | shear P = 20 ps | 301 |
| Schottky5000aged_xz_P20_g0.02 | aged Schottky 5000 K (GK end state + 20 ps NVT) | shear P = 20 ps | 301 |
| bicrystal5000_xz_P20_g0.03 | Σ5 bicrystal | shear P = 20 ps | 301 |
| bicrystal5000_xz_P20_g0.10_visual | Σ5 bicrystal | γ₀ = 0.10 (nonlinear; for viewing) | 301 |
| bicrystal5000_xz_P1_g0.01_resonance | Σ5 bicrystal | P = 1 ps (slab resonance, Eq. 13 of the methods doc) | 501 |

Viewing these in OVITO is covered in §5 of the methods doc.

## 3. Second volume V = 9.6397 Å³/atom (RC request 10-08)

Cell and model:
- L = 34.051872 Å; B1 a = L/8 = 4.256484 Å.
- Same DeePMD model as V6.6868 (graph.pb md5 81f3fc48), so `graph_c.pb` is reused.

RC's earlier NEMD runs at this volume (thermo of `Viscosity/<T>K`):

| T (K) | p (GPa) | state |
|---|---|---|
| 8000 | ≈ 60 | liquid |
| 6000 | ≈ 50 | liquid |
| 5000 | ≈ 44 | liquid |
| 4000 | ≈ 38 | liquid; stayed liquid for 1 ns (etot −18260 ± 50 eV) |
| 3000 | ≈ 18 | the liquid start crystallized: same etot as the solid start, −21180 eV |

RC's choice: liquid at 6000 and 4000 K (no 8000 K); crystal at 3000 K (melt-grown, perfect, Schottky, bicrystal) and at 2000 K (melt-grown).

| dir | job | start | NEQ | then |
|---|---|---|---|---|
| `6000K/GK` | 4233549 | RC's `Viscosity/8000K/MgO4096_Liq8000.in.pos` | 20 ps NVT | 1.5 ns NVE |
| `4000K/GK` | 4233550 | RC's `Viscosity/4000K/55439625/end.pos` (1 ns liquid) | 20 ps | 1.5 ns NVE |
| `3000K/GK` (melt-grown) | 4233551 | same 4000 K `end.pos` | **300 ps** NVT, to crystallize | 1.5 ns NVE |
| `3000K/GK_B1perfect` | 4233552 | `B1_8x8x8.data` (`build_defect_crystals.py schottky --npair 0 --a 4.256484`) | 20 ps | 1.5 ns NVE |
| `3000K/GK_Schottky` | 4233553 | `B1_schottky20.data` (20 pairs, dmin 6.8 Å, N = 4056) | 50 ps | 1.5 ns NVE |
| `3000K/GK_bicrystal` | 4233554 | `B1_S5_310.data` (normal z; N = 3920; box 33.6505 × 17.0259 × 67.3009 Å) | 50 ps | 1.5 ns NVE |
| `2000K/GK` | **not yet** | `3000K/GK/eq.data` once it is confirmed crystalline | 100 ps | 1.5 ns NVE |

The bicrystal overlap cutoff must scale with a:
- At 1.2 Å the cell had N = 4000 atoms with a 1.35 Å closest pair.
- At rcut = 0.3185 a = 1.356 Å it has the same 3920-atom topology as V6.6868, with a 2.128 Å minimum distance.
- This is now the tool's default.

Sweeps: task tables were written for all roots. They keep the V6.6868 γ₀ and ε₀ and τ_T rules, with amplitudes scaled to L (bicrystal: to $L_z$ for shear and $L_x$ for uniaxial).

| root | tasks | M steps | launch |
|---|---|---|---|
| 6000K/FreqSweep, 4000K/FreqSweep (shear) | 5 each | 0.64 each | auto (b0cqzne4g) |
| 6000K/FreqSweep_x, 4000K/FreqSweep_x (uniaxial, adiabatic τ_T) | 5 each | 1.58 each | auto |
| 3000K/FreqSweep_B1perfect | 6 | 1.20 | auto |
| 3000K/FreqSweep_Schottky (6 + P20 and P50, γ₀ = 0.02) | 8 | 3.00 | auto |
| 3000K/FreqSweep_bicrystal (6 + P20 and P50, γ₀ = 0.03) | 8 | 3.45 | auto |
| 3000K/FreqSweep_solid (melt-grown) | 6 | 1.20 | **manual**, after the crystallization check |
| 2000K/FreqSweep_solid | 6 | 1.20 | **manual**, after `2000K/GK/eq.data` exists |

Trajectory dumps are in the P20 shear tasks (liquid, Schottky and bicrystal; 60 ps every 0.2 ps) and the P5 shear tasks of the perfect and melt-grown solids.

Total cost:
- GK: 7 × 1.5 M steps.
- Sweeps: 14.5 M steps.
- Overall ≈ 25.6 M steps.
- Measured speed at V9.6397 is ≈ 32 steps/s (6000 K NVT, `cpuremain`), against 24 at V6.6868, because of the lower density. So the total is ≈ 220 P100-h ≈ 9 P100-days, and a 1.5 ns GK run takes ≈ 13 h.

**Melt-grown check (background b61gk8gwb).** When `3000K/GK/eq.data` appears, the script prints PE every 20 ps of the NVT stage. Before launching the solid sweep and the 2000 K GK, confirm:
1. PE dropped by ≈ 0.4 eV/atom and is flat.
2. `xtal_check.py` shows Bragg peaks.

If PE is not flat, the NVE stage may crystallize and heat the cell. In that case cancel 4233551 and run a longer NVT.

Analysis: `python tools/anelastic_collect.py --cases tools/anelastic_cases_MgO_V9.6397.py`.
