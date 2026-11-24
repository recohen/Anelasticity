# Anelasticity restart, 2026-11-17 (06:30 PST; updated 10:50 PST: hcp-Fe / VASP MLFF builds, §7)

Read first: this file, then `INPROGRESS.md` (§1 running, §3 proposals), `ANELASTICITY_TODO.md` (last lines) and summary §5n–§5p. Previous restart: `ANELASTICITY_RESTART_2026-11-16.md` (A3, the five 11-16 items, Rosenfeld, the A3b set-up). Session logs: `sessions/` (one Markdown file per session; `tools/session_log_md.py`; Stop/SessionEnd hooks in `.claude/settings.json`).

## 1. RC requests since the 11-16 restart
1. "Please update restarts" (11-16 19:45) → done.
2. "Can you please put sessions logs … in sessions" → `sessions/` with all 7 sessions since 2026-10-05, index `sessions/README.md`, hooks for future sessions (§5).
3. "Analyse the finished A3b jobs" → done (§2).
4. "Yes do a and b, and analyse the Schottky runs and put c as optional in the TODO list" → (a) and (b) running (§4); Schottky analysed (§3); (c) in TODO.

5. "So I also want to run similar solid runs for hcp iron … Can these force fields now run on GPUs?" → answered (§7).
6. "Go ahead and build both with 6.6.0 now … it could be added to what we have, as we need PLUMED DEEPMD etc" → CPU build + GPU plugin for the production lmp (§7).
7. "There is training data at … I just got 6.6.1 ! … It should be built in …/vasp.6.6.1" → training set analysed, VASP 6.6.1 built (§7).
8. "I wonder if it is really running on the GPU. Did you try nvidia-smi -l 60?" → yes (dmon every 2 s + nsys), §7.
9. "Yes, let's do a H200 test." → 7058548 queued (§7).
10. "please write restarts" (10:50) → this update.

## 2. A3b: bridgmanite vacancies redone (`results_freeenergy/BDG_VACANCY_A3.md` §5–6; summary §5p)
Runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A3b_Bdg_single` (README). Single-vacancy cells. V_Mg and V_Si by Frenkel–Ladd at T. Perfect and V_O2 by Frenkel–Ladd at T₁ (800–1800 K, fparam fixed at k_B T) plus a 7-point ⟨E⟩(T) ladder. All 96 replicas are hop-free.

| P, T | MgO partial (eV) | SiO₂ partial (eV) | full Schottky (eV) | V_Mg ΔG_m (eV) |
|---|---|---|---|---|
| 30 / 2000 | 6.22 ± 0.32 | 12.32 ± 0.54 | 18.54 ± 0.81 | 3.86 |
| 60 / 2300 | 8.40 ± 0.37 | 16.15 ± 0.70 | 24.55 ± 1.04 | 4.77 |
| 90 / 2500 | 10.25 ± 0.33 | 19.53 ± 0.55 | 29.78 ± 0.81 | 5.47 |
| 120 / 2800 | 12.17 ± 0.32 | 22.64 ± 0.51 | 34.81 ± 0.75 | 6.07 |

- **Formation:** agrees with the hop-free A3 subset within 0.2–0.4 eV. The MgO partial Schottky is 1.4–1.9 eV cheaper than in periclase.
- **Intrinsic diffusion:** the defects are MgO partial Schottky; D_O is 2×10⁻²¹–4×10⁻¹⁷ m²/s, ≈ 10⁵ × periclase; D_Mg is 10⁷–10⁹ × slower than D_O. Raw Deng values; real bridgmanite is extrinsic.
- **Si migration is unresolved:** the straight jump is cooperative (O neighbours move 2–3 Å). Follow-up (a).
- **Open check:** the ladder F_I(T) of the perfect crystal is 0.83 / 0.77 / 0.46 / 0.37 eV below the direct A3 value. It is unexplained: the "3N − 3 convention" explanation was withdrawn, because the convention is consistent. It does not enter the ΔG (same-route differences). Follow-up (b).

## 3. MgO Schottky reruns (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.5; summary §5p item 4)

| run | G′ (GPa) | G″ at 20 GHz (GPa) |
|---|---|---|
| 8×8×8, γ₀ 0.02, new seed, 2 ns (6963124; output in the run root) | 143.7 ± 3.5 | **27.3 ± 2.4** (reference 38 ± 9) |
| 8×8×8, **γ₀ 0.01** (6965639_2) | 127 ± 5 | **25.2 ± 5.0** (linear: ratio 0.92 ± 0.20) |
| 6×6×6 aged 1.5 ns (6963125) | 118.6 ± 0.7 | **2.3 ± 0.5** |

- **In every run all vacancies form one nanovoid**: 40 sites in the 8×8×8 cell, 16 in the 6×6×6 cell (`tools/b1_vacancy_clusters.py`, `vac_clusters.txt`). There is no slip.
- **Debye fit:** with G_R ≈ 119 and G_U ≈ 171 GPa, τ ≈ 7.6 ps (40-site void) and ≈ 0.5 ps (16-site void).
- **Conclusion:** the "Schottky" loss below 50 GHz (and its E_app = 3.2 eV) is void anelasticity from a 10⁶-fold vacancy supersaturation, not a point-defect or grain-size mechanism. Item 2 is closed.

## 4. Jobs (status at 10:50)

| what | jobs | state | dir | to do |
|---|---|---|---|---|
| (b) direct Frenkel–Ladd with TS 80 ps: 4 perfect cells + V_Mg, V_Si at 30 GPa | 7045833_1–6 | **all COMPLETED, not analysed** | `A3b_Bdg_single/P*_TS80` | `ti_einstein_analyze.py P*_TS80` against the A3 direct values (TS 40) and the ladder. If F_I moves toward the ladder and D_Mg, D_Si (30 GPa) stay put, Table 2 stands; if they move, add ladders for V_Mg, V_Si |
| (a) static NEB, Si → V_Si (12 distinct candidates per state, l < 5 Å) + Mg calibration at 30, 120 GPa | 7045971_1–6 | **all COMPLETED, not analysed** | `A3b_Bdg_single/neb/neb_<state>_<kind>.txt`, `saddle_*.xyz` | lowest converged Si barrier per state; check the saddle geometry (cooperative O motion?); compare the Mg calibration (static 6.03 vs umbrella 6.07 eV at 120 GPa); then D_Si and a comparison with Cordier's bridgmanite (Si-controlled) |
| (a) V_Si cell MD: 30 GPa 2600, 3000 K; 120 GPa 3600, 4200 K; 500 ps | 7045834_1–4 | **all COMPLETED, not analysed** | `A3b_Bdg_single/hopsSi_*` | `site_hops.py hopsSi_* --ref ../A3_Bdg_Deng/build/<state>_perfect.data --pbnm --dt-dump 0.2` |
| item 1: DFT check of the separated MgO pair, VASP relaxations | 6998279_1–10 | 1, 2, 3, 6 done; 4, 5, 7, 8 running; 9, 10 pending | `VASP/MgO_vacancy_DFTcheck/sep/relax` | E_b(d) DFT vs DeePMD (DeePMD: −1.38 / −0.47 / −0.13 / −0.06 eV at 2.1 / 4.6 / 6.9 / 9.5 Å, 20 GPa) and the long-range fit. **The FEP snapshots (6966033) are done and not yet analysed:** `dft_compare.py --gf P20_T2000_perfect P20_T2000_sep --L 2 --temp 2000` (and 140/3000) |
| hcp Fe: CPU check of the new CPU LAMMPS (6.6.1 VASPml) | 7058477 | pending | `LAMMPS/VASP/Fe/plugin_test` (`log.cpu`, `forces_cpu.dump`) | step 0 vs GPU-plugin numbers (PE −49224.521559 eV, P 2945569.013 bar) and forces; steps/s vs 6.47 (2025) |
| hcp Fe: H200 test of the GPU plugin | 7058548 | pending | same dir (`log.h200`, `log.h200off`, `dmon_h200.txt`) | steps/s on H200 vs P100 0.31 and the node's CPU path (16 ranks); SM% and memory from dmon |

## 5. Tools and fixes since the 11-16 restart
- **New tools:** `session_log_md.py` (session logs), `b1_vacancy_clusters.py` (vacancy clusters and slip in B1 trajectories, drift removed), `bdg_vac_neb.py` + `A3b_Bdg_single/neb_job.sh` (static NEB with ASE + DeepPot and fparam; the job must call the deepmd_py311 python explicitly).
- **Corrected:**
  - the ladder-offset explanation (BDG doc §5, A3b README, summary);
  - LaTeX corrupted by Python escape sequences in `ANELASTICITY_RESTART_2026-10-07.md` (Eqs. 6–7) and the new T_DEPENDENCE Eq. 8. Write LaTeX through raw strings or heredocs only.

## 6. Priorities for the next session
1. hcp Fe: read 7058477 (CPU check) and 7058548 (H200). Choose the production route: the CPU build, unless the H200 is competitive. Then write the **hcp training proposal** (VASP 6.6.1 on-the-fly, hcp cells at 300–350 GPa, 5000–7000 K, plus liquid) with costs for RC (§7).
2. A3b (b) TS 80 analysis (all 6 done).
3. A3b (a) NEB and V_Si MD analysis (all done) → Si migration barrier, D_Si, Cordier's bridgmanite side.
4. Item 1: FEP of the separated MgO pair (ready), DFT binding curve when 6998279 ends.
5. Waiting for RC (INPROGRESS §3): Σ5 60-vs-90 GPa follow-up, D1 B(T), Bdg γ anneal, talk trajectory; optional (c) in TODO.

## 7. hcp Fe with the VASP MLFF (11-17, 09:30–10:50)
Everything is documented in `/resnick/home/recohen/Claude/tools/vasp_lammps/README.md` (read first: build recipe, fixes, run recipe, results log). Scripts there: `build_cpu_lmp.sh`, `build_gpu_plugin.sh`, `build_vasp661.sh`, `makefile.include.gpu`, `vaspml_palgo.cpp`, `vaspplugin.cpp`.

### 7.1 Builds (all done)
- **VASP 6.6.1** (from `~/Downloads/vasp.6.6.1.tgz`): std, gam and ncl in `/groups/carnegie_poc/rcohen/VASP/VASP/vasp.6.6.1/bin`, built by 7057228 (std) and 7057874 (gam, ncl).
  - makefile.include copied from 6.6.0 (Intel 2025.3, `-xicelake`, `-Dlibvaspml`).
  - Under `make -j` the lib/ Fortran modules race (preclib.mod), so the script builds one version at a time and retries.
  - VASPml 6.6.1 differs from 6.6.0 only in the GRACE files. The LAMMPS branch is still `vasp-mlff-6.6.0`.
- **CPU LAMMPS** with `pair_style vasp`:
  - vasp-dev tree `/groups/carnegie_poc/rcohen/LAMMPS_VASP/lammps` (branch vasp-mlff-6.6.0, commit 6bf2cf4901), dir `build_cpu`, built by 7058476.
  - Intel 2025.3 + Intel MPI 2021.17 + MKL, linked to `vasp.6.6.1/build/std/vaspml/lib/libvaspml.a` (icelake-only).
  - Packages: ML-VASP, PLUGIN, MANYBODY, EXTRA-FIX, EXTRA-COMPUTE, RIGID, MOLECULE, MISC, REPLICA, OPENMP.
  - `~/bin/lmp_mpi_vasp` is a symlink to it. Run environment as in `plugin_test/cpu_check.sh`.
  - The older `build/` (2026-03-31) is untouched.
- **GPU plugin** for the production deepmd_py311 lmp (LAMMPS 22Jul2025 with DEEPMD, PLUMED, GPU, PLUGIN): `/groups/carnegie_poc/rcohen/LAMMPS_VASP/plugin/vaspplugin.so`.
  - VASPml compiled with nvc++ 23.9 (`-stdpar=gpu -acc -gpu=managed,cc60,cc70,cc80,cc90,cuda12.2 -D__NVCOMPILER_STDPAR_GPU=1`; build root `LAMMPS_VASP/vaspml_gpu`, currently from the **6.6.0** source).
  - `pair_vasp.cpp` (vasp-dev) and `vaspplugin.cpp` compiled with the conda g++; linked with nvc++ `-shared -fortranlibs`.
  - VASPml's LAMMPS interface never calls `global::parallel.init()`. The plugin does it through a shim, from `$VASPML_PALGO` (off | serial | gpu).
  - **Run recipe:**
    - `VASPML_PALGO=gpu env LD_PRELOAD=$NVHPC/compilers/lib/libnvhpcmanaux.so:/groups/carnegie_poc/rcohen/LAMMPS_VASP/plugin/vaspplugin.so lmp ...`
    - with `plugin load …/vaspplugin.so` in the input; `NVHPC=/central/software9/external/nvhpc/23.9/Linux_x86_64/23.9`.
    - Without the preload the job aborts with `free(): invalid pointer` (gdb: managed memory freed by glibc in the InterfaceLAMMPS static initializer).
    - Keep the plugin out of `$LAMMPS_PLUGIN_PATH`.
  - **To do:** rebuild from 6.6.1 (`build_gpu_plugin.sh`, default `VASPVER=6.6.1`). The run recipe stays the same.

### 7.2 Checks (`/groups/carnegie_poc/rcohen/LAMMPS/VASP/Fe/plugin_test`, input `fe_check.lammps`, 8192-atom start cell of the 2025 sample, 300 GPa, 80 K)

| run | step-0 PE (eV) | P (bar) | H (eV) | steps/s |
|---|---|---|---|---|
| 2025 log (old binary, older VASPml; 32 × 2 icelake) | — | 2945557.3 | 54113.194 | 6.47 |
| plugin, GPU path, 1 P100 (7057847) | −49224.521559 | 2945569.013 | 54113.684 | **0.31** |
| plugin, CPU path, 8 Broadwell ranks (7057847) | −49224.521557 | 2945569.013 | 54113.684 | 0.98 |
| CPU build, 32 × 2 icelake (7058477) | pending | | | |
| plugin, GPU path, 1 H200 (7058548) | pending | | | |

- **Agreement:**
  - GPU vs CPU path: forces max |ΔF| = 1e-7 eV/Å (rms |F| 0.94).
  - Against the 2025 log: ΔP = 4 ppm, ΔH = 0.06 meV/atom.
  - NVE: energy conserved to 1.5 meV over 100 steps.
- **Profile (7058218, P100):**
  - `nvidia-smi dmon`: SM 20 % on average (0–100 %), device memory up to 15.5 of 16 GB.
  - nsys, per force call:
    - ≈ 1 s of stdpar kernels;
    - ≈ 5 GB of unified-memory migration in ≈ 1e5 small transfers;
    - ≈ 24 600 cuBLAS axpy launches;
    - ≈ 1 400 managed alloc/free calls.
  - So it does run on the GPU, but the host/device ping-pong dominates. On P100 it is ≈ 20× slower than one CPU node.
  - Files: `dmon.txt`, `nsys_stats.txt`, `prof_gpu.nsys-rep`.

### 7.3 The force field and the training set (argue with RC: the current ML_FF is not an hcp potential)
- **Sample run** `LAMMPS/VASP/Fe/ML/Orthogonal/P300GPa/8192atoms/.../aniso`: its start cell `end.pos.start` is a crystallized quench (12-NN q6 0.48, q4 0.13), not an hcp crystal. The 5300–5600 K volume drop is probably annealing or grain growth; melting appeared at ≈ 7800 K in a fast, superheated ramp.
- **Training set** (refit dir `/groups/carnegie_poc/rcohen/VASP/Fe/bcc/ML/Orthogonal/P300GPa`; ML_FF md5 d63190a7… = the sample's; ML_AB 913 configurations):
  - All configurations are 128-atom cells.
  - V/atom 6.6–7.5 Å³; static DFT pressure 250–320 GPa (≈ 265–335 GPa with the kinetic part at 6000 K).
  - Local order: low-force configurations are bcc (14-NN q4 0.037, q6 0.510); the rest are hot bcc and liquid. **No hcp was sampled.**
  - 350 GPa is at or beyond the edge.
  - Training runs: `1024atoms/10000Kto200K10000eachTNVT` (ML_MODE=run, vasp 6.4.3), 10000 → 200 K NVT steps. INCAR.train: 10 → 2500 K, ISIF 3, 128-atom bcc. Refit: ML_IALGO_LINREG 4, ENCUT 900, ISPIN 1.
- **Next (proposal to RC, with costs):** on-the-fly training in VASP 6.6.1 with hcp cells:
  - orthogonal hcp, e.g. 4×4×3 or 6×4×4 cells, ≈ 128–192 atoms, at 300, 325, 350 GPa and 4000–7000 K, plus liquid and bcc at the same P;
  - then refit, and validate on held-out DFT;
  - then the production anelastic protocol: NPT box, then shear sweeps as for MgO.
