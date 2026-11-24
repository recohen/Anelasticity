# Anelasticity restart 2026-10-11

Read first: `INPROGRESS.md` (running jobs and their next actions), `ANELASTICITY_RESULTS_SUMMARY.md` (§5g and the new §5h), `ANELASTICITY_METHODS.md`, `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md`, `REQUIREMENTS.md`. The 10-10 restart describes the driven-boundary set-up.

Paths: `M` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms`, `G` = `M/GBslide`, `DR` = `G/drive`. Tools are in `/resnick/home/recohen/Claude/tools`.

The 10-10 session was lost after it submitted the quench job. This restart rebuilds its state from the files on disk.

## 0. Status

4336984_1–6 and the quench job 4346903 are complete. Running:

| job | what | dir | action when done |
|---|---|---|---|
| 4359736 | ASE CI-NEB of the 3×1 cell, quenched frames 10 → 12 (9 images, P100, ASE neighbour lists), 24 h limit | `DR/V6.6868_3x1_5000K_tau2/neb_10_12.{json,log,traj}`, `DR/slurm-4359736.out` | Compare E_b per area with the 1× values (0.25–0.5 J/m²). If it is about 3× the 1× barrier, the step is collective, so go to the disconnection dipole (§2.2). |

## 1. Done 10-11

1. **3×1 driven runs analysed** (summary §5h).
   - Scan: `gb_event_neb.py scan DR/V6.6868_3x1_* --out DR/analysis_3x1`.
   - u_x at the end of each run: 4000 K gives 0.06 / 1.50 / 0.37 Å at τ = 1.5 / 2 / 2.5 GPa; 5000 K gives 0.21 / 0.03 / 4.95 Å at τ = 1 / 1.5 / 2 GPa.
   - The 5000 K onset is unchanged (1.5–2 GPa). The 4000 K motion is stochastic: one step at 2 GPa, none at 2.5 GPa.
2. **LAMMPS quench of `V6.6868_3x1_5000K_tau2`, frames 9–17** (job 4346903).
   - Script `DR/gb_quench_job.sh` (`RUN`, `F0`, `F1`) runs `tools/gb_quench.lammps`.
   - Output: `RUN/quench/{quench.dat,quench_<k>.data,quench_u.txt}`.
   - Frames 10 and 12–16 have identical energy. Frame 10 → 12 is one coupled-migration period (Δu_x = 1.18 Å, Δz_b ≈ 2–3 Å).
   - Frame 9 is 14.2 eV lower and has a different structure. Frames 11 and 17 carry local defects (+27.7 and +12.9 eV).
   - **z_b is uniform in x, so the step is still collective.** No localized disconnection appears at L_x = 89 Å.
3. **ASE quench fails for 11 760 atoms** (DeePMD "cannot allocate mem for nlist", jobs 4346889 and 4346900). Cause: GPU memory. With no external neighbour list, DeePMD's TF op builds a dense n_loc × n_all buffer on the GPU (n_all rounded up to a power of 2, here 65 536 for rc = 7 Å), about 9 GB, plus the previous 4.6 GB buffer held while it grows. The 4096-atom 1× cell needs only 0.8 GB. Host RSS was 2 GB of 18 GB, so the task memory limit is not the issue. Fix: pass `neighbor_list=NewPrimitiveNeighborList(...)` to `deepmd.calculator.DP` (memory ∝ n_loc × max_nbor), or use a larger-memory GPU. The empty `quench_9_17.{log,traj}` left by those jobs were removed.
4. **New tool `tools/gb_quench_u.py RUN [--nx 6]`.** It reports E, u, and slab-resolved z_b for the quenched frames.
   - `quench_<k>.data` carries stale image flags (read_dump `replace yes`), so the tool rebuilds positions as MD frame + minimum-image displacement.
   - MD-frame slab profiles at 5000 K are noisy, so judge localization from the quenched states.
5. **`gb_event_neb.py` now uses ASE neighbour lists by default** (`make_calc`; `--native-nlist` restores the old behaviour). Each NEB image keeps its own list.
   - Test (job 4359632, `/resnick/groups/carnegie_poc/rcohen/Downloads/nlist_test`): identical to the native list (ΔE = 0, max ΔF = 5×10⁻¹³ eV/Å).
   - 11 760 atoms on a P100: first call 36 s (list build), then 0.65 s per call.
   - An H200 (`--gres=gpu:nvidia_h200:1`) also works (the pip op library includes sm_90), but it is not needed.

## 2. Next steps

1. **NEB of the elementary step in the 3×1 cell**, quenched frames 10 → 12 (ΔE = 0, Δu = 1.18 Å). Running as job 4359736 (§0), with the ASE neighbour list on one P100. The result is the barrier per area, to compare with the 1× values (14–28 eV, 0.25–0.5 J/m²) and to test whether the barrier scales with area (collective).
2. **If it is collective:** build an explicit disconnection dipole, i.e. a step of height ≈ 2 Å and Burgers vector ≈ 1.2 Å along x, in a cell with L_x ≥ 90 Å. Relax it and NEB the glide of the disconnection by one period. Alternatively, drive at τ = 1.5–2 GPa for longer times (ns) to look for nucleation.
3. **Stress dependence of the MD rate / activation volume.** Use thicker forced groups, or forces applied far from both boundaries, so the force stays on the grains.
4. **Longer (ns) equilibrium runs at V9.6397** to test whether D_u(t) converges, which gives the low-frequency β.
5. **Still open from 10-09:** grain model with the transferable β, boundary-resolved δD_b, dynamic vacancy loss, T6, T8.

## 3. MgSiO3 started (11 Oct)

Base directory: `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3`.

**Model.** X. Deng's `MLP.pb` was copied to `graph.pb` and compressed to `graph_c.pb` (job 4360074). The compressed model matches the original to within 2 µeV/Å in force, with no measurable energy or virial difference. Model details:
- se_e2_a descriptor, rc = 6 Å;
- type map Mg, Si, O;
- one frame parameter, fparam = k_BT in eV.

**Test sweep** (`1280atoms/V6.5669/2000K/SweepTest`, array job 4360075):
- Cell: 1280-atom Pbnm bridgmanite from the old run at 100 GPa and 2000 K.
- Protocol: P = 1 ps, 20 ps NVT + 40 ps driven, γ₀ = ε₀ = 0.01.
- Speed: 94.5 steps/s on a P100, against 13 steps/s for the old 32-process run.

Results at 1 THz, after the one-step lag correction (Eq. 6):

| channel | storage modulus | loss modulus | Q |
|---|---|---|---|
| shear | G′ = 238.6 ± 1.0 GPa | G″ = 1.0 ± 0.8 GPa | ≈ 240 |
| uniaxial | M′ = 803.0 ± 0.7 GPa | M″ = 4.3 ± 1.4 GPa | ≈ 190 |

Harmonics are below 0.7%.

**Tool changes.**
- `anelastic_sweep.lammps`: new options `MASSES` (`MgO` or `data`) and `FPARAM` (`none`, `kT`, or a number).
- `sweep_array.sh`: sources `ROOT/sweep.env`, if present, for `LMPEXTRA`.
- `compare_dp_models.py`: new `--fparam` option.

**Still to port before the full program.**
- `gk_stress.lammps` (masses and fparam).
- A bridgmanite defect and grain-boundary builder; `build_defect_crystals.py` is B1 only.
- The uniaxial τ_T rule (Eq. 11).
- A case file.
- The production cell: 1280 atoms, or larger (6×6×4 = 2880).
- The state points: liquid first and cool down, as for MgO, or bridgmanite at 100 GPa. **RC to decide.**

## 4. MgSiO3 production: liquid cooling and crystal heating at V = 6.5669 Å³/atom (RC, 10-11)

Root: `V` = `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3/1280atoms/V6.5669`. The run options are set in `V/sweep.env`: `-var MASSES data -var FPARAM kT -var NTYPES 3`.

**Temperature ladders** (`tools/T_ladder.lammps` and `T_ladder_job.sh`; jobs 4361369 and 4361370). Each step is NVT starting from the previous state. Output: `V/{liquid,crystal}/Ladder/eq_<T>.data`.

| branch | T (K) | ⟨p⟩ (GPa) | MSD at end of step (Å²) | note |
|---|---|---|---|---|
| liquid (melted from bridgmanite in 30 ps) | 8000 | 171.0 | 275 | above the 160 GPa training range; used only for melting |
| | 7000 | 159.8 | 134 | |
| | 6000 | 150.0 | 78 | |
| | 5000 | 139.2 | 30 | |
| | 4000 | 128.4 | 5 | nearly glassy |
| crystal (Pbnm, heated) | 2000 | 100.0 | 0.07 | |
| | 3000 | 107.7 | 0.09 | |
| | 4000 | 115.1 | 0.13 | |
| | 5000 | 123.0 | 0.18 | still crystalline |

- Steps are 20 ps for the liquid and 30 ps for the crystal.
- At 4000 K the PE difference between liquid and crystal is 0.45 eV/atom.

**Production** (`tools/stage_T_series.py`; about 76 P100-h). Each `V/<branch>/<T>K/` has:
- `GK/`: 10 ps NVT and 1.5 ns NVE.
- **Liquid:** `FreqSweep/` (shear at P = 0.2–100 ps) and `FreqSweep_x/` (uniaxial; τ_T table from MgO, §1.5).
- **Crystal:** `FreqSweep_solid/` (6 tasks).

Every task starts from the ladder state, so there is no re-equilibration. The shear amplitude is γ₀ ≤ 0.5 for liquids at ≤ 6000 K.

| T (K) | GK | shear | uniaxial / solid |
|---|---|---|---|
| liquid 7000 | 4364278 | 4364279 | 4364280 |
| liquid 6000 | 4364281 | 4364282 | 4364283 |
| liquid 5000 | 4364284 | 4364285 | 4364286 |
| liquid 4000 | 4364287 | 4364288 | 4364289 |
| crystal 2000 | 4364290 | – | 4364291 |
| crystal 3000 | 4364292 | – | 4364293 |
| crystal 4000 | 4364294 | – | 4364295 |
| crystal 5000 | 4364296 | – | 4364297 |

**Checks when the jobs are done:**
- **Liquids:** look at PE over the whole GK run for crystallization, especially at 5000 and 4000 K. Use `msd.dat` (columns Mg, Si, O) to tell glass from liquid at 4000 K.
- **GK cutoff:** check t_c from the G(t) decay, which will be slow at 4000 K.
- **Uniaxial τ_T:** check against K_S − K_T for MgSiO3 (Eq. 11).
- **Crystal:** check `xtal_check.py` at 5000 K for superheating.
- **Then:** write `anelastic_cases_MgSiO3_V6.5669.py` and collect into a new results directory.
