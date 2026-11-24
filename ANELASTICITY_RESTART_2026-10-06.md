# Anelasticity restart 2026-10-06 (written 19:35 PDT)

Read with `REQUIREMENTS.md`, `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md` and `ANELASTICITY_PLAN.md` (equations, noise model, sweep design), all in `/resnick/home/recohen/Claude/Anelasticity`. The 2026-10-05 restart file holds the full history of the GPU debugging (§0–0i). This file supersedes it.

## 0. What to check FIRST

1. `squeue -u recohen` and the two sweep arrays:
   - **4113924** shear (xz), `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/8000K/FreqSweep`
   - **4115169** uniaxial (x), same path with `FreqSweep_x`
   - **4115423** linearity repeat (xz, P = 20 ps, $\dot\gamma_0=3\times10^{10}$ s⁻¹, γ₀ = 0.095, 480 ps, ~6 h), `FreqSweep_lin20`, started from `FreqSweep/P20ps_r0/eq.data`
2. `lockin_results.txt` in each sweep root. `tools/sweep_watch.sh` appends one line per finished task (lock-in result), or a FAILED / INCOMPLETE line with the resubmit command.
3. If the watcher is not running, restart it (it skips tasks already in `lockin_results.txt`):
   `tools/sweep_watch.sh <FreqSweep>:4113924:shear <FreqSweep_x>:4115169:uniaxial <FreqSweep_lin20>:4115423:shear`
4. A task stopped by the 24 h limit resumes from `restart.mgo`: `sbatch --array=<i> sweep.sh` in its root. A task with `eq.data` but no `restart.mgo` starts production without re-equilibrating.

## 1. GPU DeePMD: working (resolved 2026-10-06)

- Env: `conda activate deepmd_py311` + `module load cuda`, `EXE=$CONDA_PREFIX/bin/lmp` (LAMMPS 22Jul2025 + deepmd-kit **v3.2.0, cuda**), `LAMMPS_PLUGIN_PATH=$CONDA_PREFIX/lib`.
- Cause of the CPU-only runs: the conda-forge CPU TensorFlow 2.21 C++ libs in `$CONDA_PREFIX/lib` shadowed the pip CUDA TensorFlow 2.21 (the env's `activate.d` prepends `$CONDA_PREFIX/lib` to `LD_LIBRARY_PATH`, and the deepmd libs carry an RPATH to it). deepmd had also been compiled against conda's abseil (`lts_20260107`); pip TF uses `lts_20250814`.
- Fix: conda CPU `libtensorflow*.so*` moved to `/groups/carnegie_poc/rcohen/anaconda2/deepmd_py311_condaCPUtf_backup_2026-10-06/lib` (old deepmd install tarred in `prev_install/`). deepmd rebuilt from `/groups/carnegie_poc/rcohen/deepmd-kit` (v3.2.0) in `source/build_gpu` with `configure_gpu.sh` / `make_gpu.sh`: pip TF root, conda CXXFLAGS stripped, `CMAKE_CUDA_ARCHITECTURES=60`, installed into `deepmd_py311`. `source/build` (conda TF) no longer builds.
- Check GPU use by the TensorFlow log line `Created device ... Tesla P100` and by `nvidia-smi`, not by `build variant: cuda`.
- Speeds, 4096 atoms, one P100:

| model | md5 | steps/s |
|---|---|---|
| `graph.pb` | 81f3fc48 | 8.1 (4 thr), 8.3 (9 thr) |
| `graph_c.pb` (`dp --tf compress -i graph.pb -o graph_c.pb`) | 6357206b | 22.8 (4 thr), ~22.7 in production |

  Compressed vs uncompressed, step 0: PE −10404.604 eV and P 2148762.2 bar in both; total energy differs by 3×10⁻⁴ eV. Production uses `graph_c.pb`.
- Quick tests on the user's interactive GPU job: `srun --jobid=<job> --overlap -n1 -c4 <script>`. Test dir `/groups/carnegie_poc/rcohen/Downloads/gputest`.

## 2. Sweeps at 8000 K (V = 6.6868 Å³/atom, 4096 atoms)

Both use `tools/anelastic_sweep.lammps` (`-var MODE shear|uniaxial`), 20 ps NVT equilibration from `MgO4096_Liq12000.in.pos`, then `nvt/sllod` + `fix deform ... wiggle` in whole-period chunks, restart after each chunk; 24 h limit, `TIMEOUT 86100`.

**Shear, xz** (4113924; $\gamma_0=\dot\gamma_0/\omega$, $\dot\gamma_0=10^{11}$ s⁻¹, plan Eq. 1):

| P (ps) | f | $\gamma_0$ | run (ps) | expected err | status |
|---|---|---|---|---|---|
| 0.2 | 5 THz | 0.010 | 20 | 9 % | **done** |
| 1 | 1 THz | 0.016 | 60 | 9 % | **done** |
| 5 | 200 GHz | 0.080 | 60 | 8 % | **done** |
| 20 | 50 GHz | 0.32 | 60 | 8 % | **done** (|σ₃/σ₁| = 0.17) |
| 100 | 10 GHz | 1.59 | 300 | 4 % | **done** |

**Uniaxial, x** (4115169; fixed $\varepsilon_0=0.03$, Maxwell guess $\Delta M=281$ GPa, $\tau=0.057$ ps; $C=1$):

| P (ps) | run (ps) | expected err on $M''$ | status |
|---|---|---|---|
| 0.2, 1, 5 | 20 each | 1, 2, 9 % | P0.2, P5 **done**; P1 running |
| 20 | 300 | 10 % | **done** |
| 100 | 1100 (capped) | 25 % | **done** |

Linearity repeat (shear, P = 20 ps, $\dot\gamma_0=3\times10^{10}$ s⁻¹, γ₀ = 0.095, 480 ps, expected 10 % on $G''$): array 4115423, submitted 19:45.

## 3. Results so far (lock-in, `anelastic_lockin.py`)

| run | f | $G'$ (GPa) | $G''$ (GPa) | δ | $\eta'=G''/\omega$ (mPa s) |
|---|---|---|---|---|---|
| sweep P0.2, xz, γ₀ = 0.010 | 5 THz | 87.2 ± 5.6 | 98.0 ± 5.6 | 48.4° | 3.12 ± 0.18 |
| sweep P20, xz, γ₀ = 0.32 (skip 0.25 cyc, 2.7 cyc) | 50 GHz | 0.1 ± 0.5 | 2.38 ± 0.29 | 87.7° | 7.6 ± 0.9 |
| sweep P5, xz, γ₀ = 0.080 | 200 GHz | 1.59 ± 0.94 | 9.96 ± 0.17 | 81.0° | 7.92 ± 0.13 |
| sweep P100, xz, γ₀ = 1.59 (skip 0.25 cyc, 2.7 cyc) | 10 GHz | −0.024 ± 0.003 | 0.503 ± 0.027 | 92.7° | 8.00 ± 0.42 |
| lin20, xz, γ₀ = 0.095 (22 cyc) | 50 GHz | 0.11 ± 0.25 | 2.57 ± 0.11 | 87.5° | 8.19 ± 0.36 |
| sweep P1, xz, γ₀ = 0.016 | 1 THz | 16.7 ± 2.7 | 44.8 ± 1.1 | 69.6° | 7.14 ± 0.17 |
| 54671682, xz, γ₀ = 0.0066 | 1 THz | 15.5 ± 3.6 | 42.9 ± 4.9 | 70° | 6.8 ± 0.8 |

- **Linearity at 50 GHz (lin20 done 01:00, 10-07):** $\eta'=8.19\pm0.36$ at γ₀ = 0.095 vs $7.58\pm0.94$ at γ₀ = 0.32; difference $0.6\pm1.0$ mPa s, so the sweep's P20 point is in the linear regime. |σ₃/σ₁| = 0.097 at the smaller amplitude (vs 0.17), i.e. the harmonic ratios are at the noise floor, not real nonlinearity. Best 50 GHz value: weighted mean $\eta'=8.13\pm0.34$ mPa s.
- **Shear sweep complete (22:43).** $\eta'$ plateaus at ≈ 8 mPa s for f ≤ 200 GHz (7.9, 7.6, 8.0): $\eta_0\approx8$ mPa s. P100 $G'$ is slightly negative (unphysical; 3 blocks of ~1 cycle underestimate the error, and a 2.7-cycle fit leaks drift into the in-phase part); read it as $G'\approx0$. Harmonics at P100: |σ₂/σ₁| = 0.084, |σ₃/σ₁| = 0.031, so γ₀ = 1.59 is still linear in the viscous regime.
- **sweep_x P0.2 (uniaxial, ε₀ = 0.03, 5 THz):** $M'=769.4\pm2.6$, $M''=109.6\pm2.0$ GPa, δ = 8.1°, $M''/\omega=3.49\pm0.06$ mPa s, |σ₂/σ₁| = 0.146. From 1 THz (R1A1) to 5 THz $M'$ rises by 232 GPa; shear accounts for $\frac43\Delta G'\approx94$ GPa, leaving ≈138 GPa in the bulk part, the size expected for $K_S-K_T$ (§7).
- **sweep_x P5 (uniaxial, 200 GHz, 3.7 cycles):** $M'=579.6\pm1.9$, $M''=13.5\pm10.5$ GPa (77 % error vs 9 % predicted: C = 1 is too optimistic, or 3 blocks of ~1 cycle are too few). $M'$ is non-monotonic: 769 (5 THz) > 537.5 (1 THz, R1A1) < 580 (200 GHz). Check against the sweep's own 1 THz point before interpreting.
- **sweep_x P20 (uniaxial, 50 GHz, 13 cycles, done 23:05):** $M'=582.0\pm1.1$, $M''=3.9\pm1.0$ GPa, δ = 0.39°, $M''/\omega=\zeta+\frac43\eta=12.5\pm3.0$ mPa s; with $\eta_0\approx8$ mPa s this gives $\zeta\approx1.8\pm3$ mPa s. T amplitude at ω only 0.4 K, so no thermostat contamination. $M'$ at 200 and 50 GHz agree (580, 582 GPa): relaxed $M_0=K_0\approx581$ GPa (G′ ≈ 0). The 1 THz value (540 GPa, both the sweep and R1A1) lies **below** this relaxed value, which a passive viscoelastic response cannot do; it supports the thermostat artefact of §7 at 1 THz.
- **sweep_x P100 (uniaxial, 10 GHz, 9 cycles, done 10-07 ~08:30, 13.2 h):** $M'=581.9\pm1.0$, $M''=1.16\pm0.64$ GPa, $M''/\omega=18\pm10$ mPa s (55 % error vs 25 % predicted; $C=1$ is optimistic by ~2–5×). Weighted with P20: $\zeta+\frac43\eta=13.0\pm2.9$ mPa s, so $\zeta\approx2.3\pm2.9$ mPa s (Eq. 3 with $\eta_0=8$). Relaxed $M_0=K_0=581.9\pm0.7$ GPa (P5, P20, P100 agree). **Both 8000 K sweeps complete.** ⚠ Superseded by restart 10-07 §3/§5: with τ_T = 0.1 ps every uniaxial $M''$ here (and the ζ estimate) carries thermostat loss (Eq. 6 there); $M'$ at ≤ 200 GHz is $K_T$. Use the rerun `FreqSweep_x2` (4147331).
- x/R1A1/2267049 (uniaxial, ε₀ = 0.033, 1 THz): $M'=537.5\pm1.6$, $M''=89.1\pm0.9$ GPa, $\zeta+\frac43\eta=14.2\pm0.1$ mPa s.
- At 5 THz the single-Maxwell guess (135 GPa, 0.057 ps) gives $G'=103$, $G''=58$ GPa. The measured $G''$ is well above it: the relaxation spectrum is broader than one Maxwell time.
- Harmonics at 5 THz: $|\sigma_3/\sigma_1|=0.057$, the size of the noise.

## 4. Bugs found and fixed today in `anelastic_sweep.lammps`

1. `v_pe` in `fix ave/time` needs `pe` in `thermo_style` (4112680 died at production start).
2. LAMMPS `elif` takes no `then` (4113591 died at line 26).
Now tested on the GPU node for all three start paths: fresh, from `eq.data`, from `restart.mgo`. Failed outputs kept in `FreqSweep/failed_4112680_pe/` and `failed_4113591_elif/`; the cancelled uncompressed run in `cancelled_4109686_uncompressed/`.

## 5. Tools (`/resnick/home/recohen/Claude/tools`)

- `anelastic_lockin.py <file|dir> --period PS --mode shear|uniaxial`: uniaxial sweep dirs use $\varepsilon=\ln(L_x/\langle L_x\rangle)$ and $p_{xx}$.
- `anelastic_sweep_setup.py --mode shear|uniaxial [--eps0 0.03 --dM 281e9 --tmax-ps]`: writes tasks, `sweep.sh` (job name `MgOshear`/`MgOuniax`), and a cost table with expected error per point.
- `anelastic_sweep.lammps`: as above.
- `sweep_watch.sh ROOT:JOB:MODE ...`: lock-in on each finished task into `ROOT/lockin_results.txt`.
- Backups of the tools before today's MODE edits: `/groups/carnegie_poc/rcohen/Downloads/anelastic_*.bak`.

## 6. Paths

Write LAMMPS paths as `/groups/carnegie_poc/rcohen/LAMMPS/...` (RC's form; `/groups` is a symlink to `/resnick/groups`).

## 7. Open concern: thermostat loss in the uniaxial runs (found 19:50)

Lock-in of the temperature (`v_tt` in `stress.dat`) against strain:

| run | T amp at ω (K) | at 2ω (K) |
|---|---|---|
| uniaxial P0.2 | 432 | 1024 |
| uniaxial P1 | 294 | 1 |
| uniaxial P5 | 6 | 1 |
| shear P0.2 | 6 | 119 |
| shear P1 | 4 | 20 |

Uniaxial strain changes T adiabatically (Grüneisen ≈ 1.2–1.8). With Nosé–Hoover $\tau_T=0.1$ ps the thermostat adds a thermal-relaxation loss to $M''$ of strength $\Delta M\approx\rho C_v\gamma^2T\approx75$–$160$ GPa (Eq. 7), peaking near $1/(2\pi\tau_T)\approx1.6$ THz; R1A1's $M''=89$ GPa at 1 THz may be partly this. Shear is not affected (T at ω only 4–6 K). Proposed test, awaiting RC: rerun uniaxial P1 from its `eq.data` with $\tau_T$ = 1 and 0.02 ps. Viscous heating at P0.2, ε₀ = 0.03 is ≈340 K/ps, so weak thermostats need smaller ε₀ at high frequency.

## 8. Lock-in on short runs

Runs with < 10 cycles (P20, P100 shear; P5 uniaxial; lin20) must use `--skip-cycles 0.25 --nblock 3`; the default skip of 2 cycles leaves 1 cycle and no error bar. `sweep_watch.sh` now does this automatically.
