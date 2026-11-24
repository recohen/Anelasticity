# Anelasticity restart 2026-10-05 (written 17:20 PDT)

Read with `REQUIREMENTS.md`, `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md` and the physics/plan document `ANELASTICITY_PLAN.md` (equations, noise model, sweep design). All in `/resnick/home/recohen/Claude/Anelasticity`.

## 0. What to check FIRST (in order)

1. **Speed of DeePMD on the P100 is unresolved (T1).** The timing test (job 4014215, cancelled after 100 steps) ran `~/bin/lmp` with the conda env `deepmd_py311` and took **3.86 s/step** for 4096 atoms with the uncompressed `graph.pb`. Old 4096-atom logs run at 7–19 steps/s (0.05–0.14 s/step), about 30–75× faster.
   - Facts: LAMMPS 22Jul2025 build has `PKG_GPU=yes, GPU_API=cuda, GPU_ARCH=sm_60` (P100). The deepmd-kit summary in the run log says `build variant: cpu`; `libdeepmd_cc.so`, `libdeepmd_op.so`, `libdeepmd_c.so` in the env contain no CUDA symbols; `libtensorflow_cc.so.2` does. No TensorFlow "Created device ... GPU" line appeared in the log.
   - RC (17:15): "It is gpu build and so is lmp!!" — the LAMMPS part is confirmed GPU. Whether DeePMD's network actually ran on the GPU in that job is **not established**. The LAMMPS GPU package does not accelerate `pair_style deepmd`.
   - The job script set `PATH` and `LD_LIBRARY_PATH` to the conda env only. It did **not** `module load cuda` and did not set the CUDNN path that the old scripts set. This is the first suspect.
   - Next step: a 15-minute P100 diagnostic with `TF_CPP_MIN_LOG_LEVEL=0`, `module load cuda`, and `nvidia-smi` sampling during the run (T1).
2. The old GPU deepmd-kit still exists: `/groups/carnegie_poc/rcohen/deepmd-kit/bin/lmp` (Aug 2025, has `libdeepmd_op_cuda.so`). It has no `dp` binary.
3. `squeue -u recohen`: no anelasticity jobs should be running. Nothing from the sweep has been submitted.

## 0b. Which lmp did the old runs use? (added 17:50)

- The R1A1 log (2026-09-02) reports **LAMMPS 29 Aug 2024 - Update 4** and **deepmd-kit v3.0.0, build variant cuda**, installed at `/central/groups/carnegie_poc/rcohen/deepmd-kit`, with TensorFlow from `deepmd_venv` (python 3.9). TensorFlow created the GPU device (Tesla P100).
- `/groups/carnegie_poc/rcohen/deepmd-kit/bin/lmp` links `/resnick/home/recohen/lib/liblammps.so.0` (29 Aug 2024, md5 f035fa6b…, identical to `deepmd-kit/lib/liblammps.so.0`) and that deepmd-kit (`libdeepmd_op_cuda.so`). This matches the old log, so the overwritten `~/bin/lmp` was almost certainly this binary or a copy. Not proven byte-for-byte.
- `deepmd_venv/bin/lmp` and `deepmd_venv/bin/dp` are pip Python wrappers, not that binary.
- `/central/groups/carnegie_poc/rcohen/deepmd-kit` is a git tree now at **v3.2.0** (source), but its `bin/ lib/ lib64/ include/ etc/` are **untracked leftovers of the old install**: `lib/libdeepmd_cc.so` reports v3.0.0, commit e695a91c (2024-11-23), exactly as in the R1A1 log. So the old CUDA stack survives there; 3.2.0 was built in `build3.2.0b/` and the conda env `deepmd_py311`.
- Timing jobs, both from RC's R1A1 script with minimal diffs:
  - **4021504** `timing/p100_env`: new `~/bin/lmp`, env swapped to `conda activate deepmd_py311`.
  - **4021610** `timing/p100_old`: script unchanged except `EXE=/groups/carnegie_poc/rcohen/deepmd-kit/bin/lmp`.
  - Each times `graph.pb` then `graph_c.pb` (compressed by deepmd 3.2.0; may not load in v3.0.0).

## 0c. Timing results so far (added 18:40)

- **4021504, new stack** (`~/bin/lmp`, conda `deepmd_py311`, RC's R1A1 script with `conda activate`): **3.73 s/step**, `build variant: cpu`, and `nvidia.out` shows **no process on the GPU** for the whole job. The conda deepmd-kit 3.2.0 does not use the P100. Not an environment mistake this time.
- **4021610, old stack**: failed at start, `libmkl_intel_lp64.so.2` not found. Cause: `~/.bashrc` line 77 now aliases `load_intel` to `~/intel/oneapi` (2026.1, MKL `.so.3`); the old lmp needs the group oneAPI `/central/groups/carnegie_poc/rcohen/intel/oneapi` (MKL 2025.3, `.so.2`). The 54671682 script sources that `setvars.sh` explicitly.
- **4024866, old stack resubmitted** with that one `setvars.sh` line added after `load_intel`. `.bashrc` left untouched.
- 4024866 then failed: `deepmd_venv/lib/libmpi.so.12` (replaced **2026-09-22**, after the R1A1 run) needs `FABRIC_1.9`; the group Intel MPI 2021.17 libfabric has only 1.8.
- **4025085, old stack**: also `export LD_LIBRARY_PATH=<group oneAPI>/mpi/2021.17/lib:$LD_LIBRARY_PATH` after the venv activate, and Intel's `mpirun`. All libraries resolve on the login node (`ldd`). Diff vs R1A1 script is in `timing/p100_old/1submit_lammps.sh`.
- Summary: since 2026-09-02 three things changed under the old scripts: `~/bin/lmp` overwritten, `load_intel` repointed to `~/intel/oneapi` 2026.1 (MKL `.so.3`), `deepmd_venv` MPI replaced.

## 0d. Why there is no working GPU DeePMD right now (added 19:30) — DECISION NEEDED from RC

- **4025085 old stack**: libraries now load and report `build variant: cuda`, then die: `libdeepmd_cc.so: undefined symbol _ZN10tensorflow8GraphDefC1EPN6google8protobuf5ArenaEb`. The v3.0.0 libs were built against an older TensorFlow; `deepmd_venv` TensorFlow was upgraded to **2.20.0 on 2026-09-22**. The old stack cannot run without reinstalling the old TensorFlow.
- **New stack is CPU-only on both levels**: the 3.2.0 C++ build (`deepmd-kit/source/build`, 2026-09-24, installed into conda `deepmd_py311`) has no `USE_CUDA_TOOLKIT`, and the conda TensorFlow 2.21.0 reports `is_built_with_cuda() = False`.
- `deepmd_venv` TensorFlow 2.20.0 **is** CUDA (12.5, cuDNN 9) with `sm_60` (P100) support.
- Options put to RC:
  A. Configure the same source tree in a second build directory with `-DUSE_CUDA_TOOLKIT=TRUE -DCMAKE_CUDA_ARCHITECTURES=60` against `deepmd_venv` TensorFlow 2.20, install to a new prefix, load via `LAMMPS_PLUGIN_PATH`. Touches no existing install. (Recommended.)
  B. Put CUDA TensorFlow into conda `deepmd_py311` and rebuild deepmd there with CUDA.
  C. Reinstall the old TensorFlow into `deepmd_venv` to revive the v3.0.0 stack.

## 1. Results in hand

- Lock-in reanalysis of the existing 8000 K runs at 1 THz (period 1 ps):

| run | strain amp | result | $\delta$ | loss$/\omega$ (Pa s) |
|---|---|---|---|---|
| 54671682, xz shear, 0.2 Å | 0.0066 | $G'=15.5\pm3.6$, $G''=42.9\pm4.9$ GPa | 70° | $\eta'=0.0068\pm0.0008$ |
| x/R1A1/2267049, x uniaxial, 1 Å | 0.033 | $M'=537.5\pm1.6$, $M''=89.1\pm0.9$ GPa | 9.4° | $\zeta+\frac43\eta=0.0142\pm0.0001$ |

- Maxwell estimate at 8000 K: $G_\infty\approx135$ GPa, $\tau\approx0.057$ ps, $\eta_0\approx7.7$ mPa s.
- The fluctuation–dissipation noise model (plan Eq. 7, $C\approx8$) reproduces the measured shear error bar.
- Model compression works: `dp --tf compress` (deepmd 3.2.0) made `graph_c.pb` in 26 s, in `.../8000K/FreqSweep/timing/p100/`. Its speed was never measured.
- Box flips with `fix deform xz wiggle ... flip yes`: CERTIFIED on an LJ liquid (job 4014216, 16 flips, unwrapped tilt matches $A\sin\omega t$ to $5\times10^{-5}$). Note that `fix deform` defaults to **lattice units**; production input now has `units box`.

## 2. Problems found in the user's notebooks (`stressstrain*.py`)

1. The frequency conversion assumes 10 fs per sample. Actual spacing is 1 fs (R1A1) and 5 fs (54671682).
2. The shear notebook uses the raw xz tilt (Å) as strain. It must be divided by $L_z$.
3. The viscosity formula leaves out the strain amplitude, the $2\pi$ and $\sin\delta$. Correct form: $\eta'=G''/\omega$.
4. Phase from the correlation coefficient is biased toward 90° by noise.
5. A uniaxial x wiggle measures $M=K+\frac43G$, not shear.
6. `54671682/stressstrain.dat` stops at step 246400 although the run finished 500000 steps.

## 3. Tools (in `/resnick/home/recohen/Claude/tools`)

- `anelastic_lockin.py`: lock-in fit at the known drive frequency, harmonics, block errors, box-car correction, flip unwrap, restart-duplicate removal. Validated on synthetic data (exact recovery) and on both 8000 K runs. Usage:
  `anelastic_lockin.py <thermo file | run dir> --period PS [--mode shear|uniaxial] [--cols ...] [--L0 Å]`
- `anelastic_sweep.lammps`: restartable xz-wiggle input, outputs `stress.dat` (bin-averaged) and `strain.dat` (instantaneous). **Not yet run on MgO.**
- `anelastic_sweep_setup.py`: writes task directories, `tasks.txt`, and a SLURM array `sweep.sh` with the user's P100 header. Defaults: periods 0.2, 1, 5, 20, 100 ps; $\dot\gamma_0=10^{11}$ s$^{-1}$; 10% error; at least 3 cycles and 20 ps per point; 20-ps chunks.

## 4. Decisions by RC (2026-10-05)

- Constant volume, 6.6868 Å$^3$/atom. On cooling the liquid supercools, then crystallizes all at once.
- 4096 atoms.
- Cheap Tesla P100 only, with the header of `8000K/Viscosity/x/R1A1/2267049/1submit_lammps.sh`.
- Green–Kubo already run by RC. It is noisy at low frequency but will be compared.
- Goal: 4–5 decades in frequency for extrapolation toward MHz.
- The first cost estimate (41 P100-days) was rejected as far too much. The revised 8000 K sweep is about 0.6 M steps in total. Cost must be re-derived from a **measured** speed before anything is submitted.

## 5. Directories

- Project and docs: `/resnick/home/recohen/Claude/Anelasticity`
- Existing runs: `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/<T>/Viscosity`
- New sweep root (only `timing/` exists): `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/8000K/FreqSweep`
- Scratch tests: `/resnick/groups/carnegie_poc/rcohen/Downloads/{fliptest,lockin_synth,sweep_dry}`

## 0e. RESOLVED 2026-10-06 18:00: DeePMD now runs on the P100 (conda deepmd_py311)

- Cause: `deepmd_py311` had both pip TensorFlow 2.21.0 (CUDA 12, abseil lts_20250814) and conda-forge CPU TF 2.21.0 C++ libs in `$CONDA_PREFIX/lib` (abseil lts_20260107). The env's `activate.d/env_vars.sh` prepends `$CONDA_PREFIX/lib` to `LD_LIBRARY_PATH`, so the CPU libs were loaded; deepmd 3.2.0 (`build variant: cuda`) had also been compiled against conda's TF/abseil headers.
- Fix: conda CPU `libtensorflow*.so*` moved to `/groups/carnegie_poc/rcohen/anaconda2/deepmd_py311_condaCPUtf_backup_2026-10-06/lib` (previous deepmd install tarred in `prev_install/`). deepmd-kit v3.2.0 rebuilt in `/groups/carnegie_poc/rcohen/deepmd-kit/source/build_gpu` (`configure_gpu.sh`, `make_gpu.sh`): TENSORFLOW_ROOT = pip TF, conda CXXFLAGS stripped, `CMAKE_CUDA_ARCHITECTURES=60`, installed into `deepmd_py311`.
- Measured: 4096 atoms, 200 steps, 4 OMP threads, P100 on hpc-21-19: **8.10 steps/s (0.123 s/step)**, TF "Created device ... Tesla P100", GPU util 70–98 %. Test dir `/resnick/groups/carnegie_poc/rcohen/Downloads/gputest`.
- Next: re-derive sweep cost from this speed (T1).

## 0f. Sweep cost at the measured 8.1 steps/s (2026-10-06, T3)

`anelastic_sweep_setup.py --sec-per-step 0.1235` (dry runs in `Downloads/sweep_cost_8p1{,_lin}`), 20k-step NVT equilibration per task included:

| P (ps) | $\gamma_0$ | run (ps) | cycles | steps | wall (h) |
|---|---|---|---|---|---|
| 0.2 | 0.010 | 20 | 100 | 40 k | 1.4 |
| 1 | 0.016 | 60 | 60 | 80 k | 2.7 |
| 5 | 0.080 | 60 | 12 | 80 k | 2.7 |
| 20 | 0.32 | 60 | 3 | 80 k | 2.7 |
| 100 | 1.59 | 300 | 3 | 320 k | 11.0 |
| 20, $\dot\gamma_0=3\times10^{10}$ (linearity) | 0.095 | 480 | 24 | 500 k | 17.1 |

Total 1.1 M steps = 37.7 P100-hours = 1.6 P100-days; as a 6-task array the wall time is ~17 h (11 h without the linearity check). Awaiting RC approval (T4).

## 0g. 8000 K sweep submitted 2026-10-06 18:11 (T4, without linearity check)

- Array **4109686** (tasks 1–5 = P 0.2, 1, 5, 20, 100 ps), root `8000K/FreqSweep`, 24 h limit, TIMEOUT 86100. `anelastic_sweep_setup.py` template now uses `$CONDA_PREFIX/bin/lmp`, `LAMMPS_PLUGIN_PATH`, no `load_intel`, mail ALL, `nvidia-smi -l 300`.
- All five: TF "Created device ... Tesla P100"; production speed during NVT equilibration **8.26 steps/s (0.121 s/step)** with 9 OMP threads, identical across tasks. Expected finish: P0.2 ~1.3 h, P1/P5/P20 ~2.7 h, P100 ~10.8 h.
- `log.lammps.<jobid>` is written in large buffered blocks; follow progress in `slurm-4109686_<i>.out`.
- Still to check: speed in the wiggle (sllod + deform) phase, first box flip in P20/P100, then lock-in analysis.

## 0h. Switched the sweep to the compressed model (2026-10-06 18:45)

- `graph_c.pb` (md5 6357206b, `dp --tf compress` of graph.pb md5 81f3fc48) timed on P100, 4 threads, 200 steps: **22.8 steps/s** vs 8.10 uncompressed (2.8×). Step-0 PE −10404.604 eV and P 2148762.2 bar identical; TotEng differs by 3e-4 eV.
- Array 4109686 (uncompressed) cancelled during equilibration (step ~13000/20000, no restart written); its logs are in `FreqSweep/cancelled_4109686_uncompressed/`.
- Resubmitted as **4112680** (tasks 1–5 = P 0.2, 1, 5, 20, 100 ps) with `MODEL=$ROOT/graph_c.pb`, 24 h limit. Expected wall time at ~23 steps/s: P100 ≈ 4 h, others ≤ 1 h. Total sweep ≈ 0.3 P100-days.
- 4112680 running 18:39: all 5 tasks report TF "Created device ... Tesla P100"; ~21–22 steps/s (9 threads) in equilibration.

## 0i. Input bug fixed, shear resubmitted, uniaxial sweep set up (2026-10-06 19:05)

- 4112680 failed at the start of production in all 5 tasks: `Thermo keyword pe in variable requires thermo to use/init potential energy` (v_pe in fix SAV; thermo_style lacked pe). Fixed in `tools/anelastic_sweep.lammps` (pe added to thermo_style). Input also now starts production from `eq.data` when it exists and `restart.mgo` does not, so the equilibration was not repeated. Failed outputs in `FreqSweep/failed_4112680_pe/`.
- Shear resubmitted as **4113591** from the existing `eq.data` files.
- `anelastic_sweep.lammps` has `-var MODE shear|uniaxial` (uniaxial: `fix deform 1 x wiggle AMP PERIOD remap v units box`). `anelastic_lockin.py <dir> --mode uniaxial` uses ε = ln(lx/<lx>) and pxx. `anelastic_sweep_setup.py --mode uniaxial --eps0 0.03 --dM 281e9 [--tmax-ps]`, C = 1 (R1A1 error bar gives 0.74). Uniaxial short test (2 periods of 0.2 ps, GPU node) OK: Lx 29.24–31.05 Å.
- Uniaxial sweep generated, NOT submitted: `8000K/FreqSweep_x` (ε₀ = 0.03, tmax 1 ns): P 0.2/1/5 ps 20 ps each, P20 0.3 ns (10 %), P100 1.1 ns (25 % on M″; 10 % would need 7.1 ns = 3.7 P100-days). Total 1.6 M steps = 0.8 P100-days; P100 task ≈ 14 h.
- 19:05 shear resubmitted as **4113924** after an `elif` syntax fix (4113591 failed at line 26; outputs in `FreqSweep/failed_4113591_elif/`). Production running from eq.data at ~22.7 steps/s.
- 19:15 uniaxial sweep submitted as **4115169** (`FreqSweep_x`, as generated above). It uses the same seeds and start file as the shear sweep, so the equilibrations are near-identical; harmless for separate observables.
- 19:21 **First sweep point, shear P = 0.2 ps (5 THz)**, 4113924_1, 98 cycles, γ₀ = 0.010: $G'=87.2\pm5.6$, $G''=98.0\pm5.6$ GPa, δ = 48.4°, $\eta'=G''/\omega=3.12\pm0.18$ mPa s; |σ₂/σ₁| = 0.010, |σ₃/σ₁| = 0.057 (at the noise level, 5.7 %). Single-Maxwell guess (135 GPa, 0.057 ps) predicts G′ = 103, G″ = 58: G″ is well above it, so the spectrum is broader than one Maxwell time.
