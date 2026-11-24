# Anelasticity restart, 2026-11-19 (16:00 PST, evening update 21:00 in §10): Fe DFT settings decided, first DeePMD recalculation batch running, speed test pending

**Start with §10** (evening): 26 of the 38 R1 tasks in 7286822 timed out at 10–20× the normal time per SCF step (rank placement under Intel mpirun on scattered grants), srun + PMI2 works, and RC: the debug job was far too big.

Read first: this file, then `INPROGRESS.md` (jobs), `QUESTIONS.md` (open decisions for RC, new 11-19), `ANELASTICITY_PLAN_FE.md` (§3.1: the DeePMD route and X. Deng's workflow) and `ANELASTICITY_TODO.md` (last lines). Previous restart: `ANELASTICITY_RESTART_2026-11-18.md`. Its §9 items 2–4 and the 11-17 items (A3b analyses, MgO separated pair) are still open. Tables: `results_Fe/A0b_summary.txt`, `results_Fe/A0c_summary.txt`. Session log: `sessions/2026-11-19_0325_04107a7c.md`.

Coordination: another Claude session (WSDA) owns `~/Claude/WSDA` and `~/Claude/Resnick`. This session owns `~/Claude/Anelasticity` and the Fe tools. File rules (RC 11-19): docs, summaries and tables in `~/Claude/Anelasticity` (`results_<topic>/`), tools in `~/Claude/tools`, run dirs only job I/O + README. Jobs ≤ 30 min go in `-q debug -t 30:00` (standing rule; one running at a time).

## 1. RC requests and decisions this session (11-19)
1. "Continue training Fe vasp ML potential" → A1 smoke, then A0b analysis (§3).
2. "You should put short 30 minute jobs in debug queue" … "this goes back to the beginning" → memory note + REQUIREMENTS item 13.
3. "Do the k-mesh test in debug" → A0c (§3).
4. **"Yes recomputing configs for deepmd is a good idea. I actually have a whole bunch of tools …"** → DeePMD with fparam $=k_BT$ (one model for all T, since SIGMA must equal $k_BT$), X. Deng's mldp workflow (plan §3.1). "My lammps and deepmd and plumed installations work" → dp/lmp/plumed from RC's `deepmd_py311`; only the mldp data scripts use Xin's env.
5. **"A1. Use PBE"**. **A2: "use vasp_gam for MD trajectories and selection, and then recalculation using MP2x2x2"** → agreed (Γ-only VASP on-the-fly MLFF as the sampler).
6. "MP2x2x2 cannot give 16 k-points" / "It should not apply symmetry with ISYM=0!" / **"We should test a real shifted 2x2x2, and it should not include -k"** → KBLOWUP found and A0c2 run (§3).
7. "Do the Bridgmanite talk trajectory (5000 K, V_Mg + V_O, short dump)" → done (§6). "Maybe make a new file QUESTIONS" → `QUESTIONS.md` (proposals no longer in INPROGRESS).
8. **"Go ahead and stage the first recalculation batch and submit"** → R1 (§4) and A1 sampling (§5). **"Submit"** → FPS configs 101–150 too.
9. "Why so much memory? Can it be reduced via INCAR?" → measured 0.54–0.60 GB/rank; job script now 2 × 32 at 3 GB/task (§4).
10. **"That seems way too slow"** → pending R1 tasks held, speed test 7302962 (§4). "Are you using KPAR" → yes, KPAR 4 (= number of k-points), NCORE 4; the slowness came partly from ranks spread over 7–9 nodes.
11. "Write restarts" → this file.

## 2. DFT settings for the Fe training labels (decided)
PBE, Fe_sv (PAW_PBE Fe_sv 23Jul2007; Fe_pv spheres overlap at 330 GPa), ISPIN 1, ENCUT 700, SIGMA = $k_BT$ (ISMEAR −1), **true shifted 2×2×2 mesh: 4 k-points listed explicitly, (¼,¼,¼), (−¼,¼,¼), (¼,−¼,¼), (¼,¼,−¼), with `KBLOWUP = .FALSE.`**, NBANDS = 8/atom + (0.25 + 5σ[eV])/atom (rounded up to 16). ALGO/EDIFF/PREC/LREAL pending the speed test (§4).

## 3. A0b / A0c results (`/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/A0`)
- **A0b** (`results_Fe/A0b_summary.txt`): Γ-only in 64-atom cells is not converged (forces 0.15–0.53 eV/Å, P 1–7 GPa off); ENCUT 700 enough (700→900: 0.5–0.8 GPa); SIGMA must equal $k_BT$ (0.2588 eV at 330 GPa/5600 K: 0.22 eV/Å, −8.5 GPa). So the old 913-config ML_AB (Γ, SIGMA 0.2588 at all T) has wrong labels → recompute.
- **KBLOWUP:** VASP (default `KBLOWUP = .TRUE.`) completes a generated k-mesh with the Bravais-lattice point group even with ISYM = 0 (`mkpoints.F`, IBZKPT "blow-up"). "Monkhorst 2 2 2" on the 64-atom fcc primitive cell became 32 points (16 ±k pairs). Only ISYM < 0 or `KBLOWUP = .FALSE.` stops it.
- **A0c/A0c2** (`results_Fe/A0c_summary.txt`; 500 eV, against 3³ at $k_BT$ / 4³ at 300 K smearing; wall on 64 ranks):

  | mesh | force rms, $k_BT$ (eV/Å) | force rms, 300 K (eV/Å) | ΔP (GPa) | wall (s) |
  |---|---|---|---|---|
  | Γ | 0.14–0.25 | 0.19–0.46 | 1–7 | 23–45 |
  | one k (¼,¼,¼) | 0.06–0.17 | 0.09–0.36 | 0.3–2 | 52–124 |
  | Γ-centred 2×2×2 | 0.011–0.025 | 0.036–0.11 | 12.4 at fcc 330 GPa / 300 K | 250–720 |
  | **true shifted 2×2×2 (4 k)** | **0.008–0.015** | **0.026–0.087** | **≤ 0.1** | **160–310** |
  | VASP-blown-up 16 pairs | — | 0.005–0.018 | ≤ 0.01 | 790–1090 |

  For 0 K static checks ($C_{ij}$, stacking faults) use 4×4×4.

## 4. R1: recalculating the old ML_AB (`/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/R1`, README)
- Old ML_AB: 913 configs, all 128 atoms, 344 bcc + 569 liquid/disordered, 266–300 GPa, no hcp/fcc.
- **T of each config** (`old/configs.txt`, `fe_r1_old.py prep`): configs map one-to-one onto the DFT steps of the old MD logs (12 + 631 [`log.out.85728`, 10→7000 K] + 271 [`PRE.42968496/log.out`, 7000→10000 K]); T = kinetic T ±50 steps. Check: ⟨|F|²⟩/(3k_BT) = 43–48 eV/Å² in every segment.
- **Selection:** `soap_fps.py` (dscribe SOAP c 6, n 6, l 6, σ 0.44, frame average + FPS), because asaplib in Xin's mambaforge fails with its dscribe (`SOAP(rcut=)` TypeError). `old/fps-n-150.index` in FPS order; 1–100 → `old/`, 101–150 → `old_b/`. 500 K bands; per band `deepmd/` + `inputs/old_T<T>/`, dirs made by Xin's `recal_dpdata.py -rv no` → `<set>/T<T>/recal/<n>/`.
- **Jobs:**
  - 7286822 (tasks 1–11, 13–38; `--ntasks=64`, 4–6 GB/task, spread over 3–9 nodes): running/done; 11 finished at 16:00. Task 12 was OOM-killed (5.75 GB summed over 4 ranks on one node; cause unclear).
  - **7297693** (old tasks 12, 39–100) and **7297695** (old_b 1–50): 2 × 32 ranks, 3 GB/task, **HELD** (`scontrol release` after the INCAR update).
- **Memory:** finished tasks peak at 0.54–0.60 GB per rank (OUTCAR); VASP's count on rank 0 0.26 GB (wavefunctions 0.17).
- **Speed:** 300 K configs took 2600–3640 s: 35–45 SCF steps × 68–78 s, ±0.1–0.4 eV energy oscillation in steps 6–24. Xin's pure-Fe recalc INCAR uses ALGO VeryFast, EDIFF 1e-5, PREC Normal, LREAL F.
- **Speed test 7302962_1–10** (`R1/speed`, `tasks_speed.txt`, 2 × 32 ranks, 3 h): configs old/T300/recal/1 (reference already done at 2596 s on 7 nodes) and old/T7500/recal/1, variants ref, fast (ALGO Fast + EDIFF 1e-5), vfast (VeryFast), fastN (+PREC Normal), fastR (+LREAL Auto). Analyse with `python ~/Claude/tools/fe_r1_speed.py R1/speed -o ~/Claude/Anelasticity/results_Fe/R1_speed.txt`. Choose the fastest variant within ≈ 0.01 eV/Å and 0.1 GPa of ref; edit the INCARs of the held, not-started dirs (`old/T*/recal/*`, `old_b/T*/recal/*` without OUTCAR, and `inputs/`); `scontrol release 7297693 7297695`. Possible extra variant: NCORE 8/16.
- **After R1:** per band in `recal/`: `post_recal.py`, `check_nbands_nelm.py -ip all -v` (top-band occupation), `merge_out.py -o OUTCAR -r y`, `extract_deepmd.py -d deepmd -ttr 10000` (fparam from SIGMA). Note the configs already done with ref settings (ALGO Normal, EDIFF 1e-6) are equally valid labels.

## 5. A1 sampling for hcp/fcc frames (`.../ML/A1/bands`, A1 README)
- `fe_a1_setup.py --mode bands`: hcp (orthohexagonal) and fcc, 64 atoms, P = 0, 100, 200, 300, 360 GPa × T = 300 K, 0.4, 0.7, 0.95 T_m (provisional T_m 1800, 4000, 5000, 6000, 6500 K); Langevin NPT 8 ps; vasp_gam, 500 eV, SIGMA = $k_BT$; MLFF on-the-fly from scratch (sampler only).
- **Job 7286841_1–40** (32 ranks, 8 GB/task, 6 h): 18 running at 16:00. 8 GB came from the smoke OOM with the old 913×128 ML_AB; fresh runs probably need much less: check the first finished run, lower for any resubmission.
- **Next (R1b):** XDATCAR frames → `soap_fps.py` → recalculation with the §2 settings (64-atom cells), a few hundred frames.

## 6. Bridgmanite talk trajectory (done)
Job 7279725 (P100, 39 min). 1268 atoms, 6 V_Mg + V_O pairs, ≈ 120 GPa, 5000 K, Deng model, 200 ps. Movies `/groups/carnegie_poc/rcohen/LAMMPS/TalkTrajectories/Bdg_vacancy_hops_5000K` (401 frames × 0.5 ps) and `_first50ps` (251 × 0.2 ps); `vmd -e movie.vmd`. Hops > 2 Å in 200 ps: O 103/762, Mg 12/250, Si 14/256 ("slow Mg", not frozen). Reported to RC.

## 7. Tools added or changed today (`~/Claude/tools`)
| tool | purpose |
|---|---|
| `fe_a1_setup.py` | A1 staging: smoke, ramps, **bands** (constant T, fresh MLFF, `--nbands 0` = R1 rule) |
| `vasp_mlab.py` | ML_AB info/block/append/check (6.6 CTIFOR header; PSTRESS·V removed) |
| `fe_a0b_analyze.py`, `fe_a0c_setup.py`, `fe_a0c_analyze.py` | A0b/A0c analysis and staging (MP2x mesh with KBLOWUP = .FALSE.) |
| `fe_r1_old.py` | R1: prep (T per old config, extxyz), stage (bands, deepmd/npy, inputs; `--set old_b`) |
| `soap_fps.py` | SOAP + FPS (replaces asap gen_desc + select_frames.py) |
| `fe_r1_speed.py` | speed-test comparison |
| `R1/fe_r1_job.sh` | R1 array job, one recal dir per task, 2 × 32, 3 GB/task |

## 8. Jobs (16:00)
| job | what | state |
|---|---|---|
| 7286822 | R1 old 1–11, 13–38 | 26 running, 11 done |
| 7297693 | R1 old 12, 39–100 | HELD |
| 7297695 | R1 old_b 1–50 | HELD |
| 7302962_1–10 | R1 speed test | PENDING |
| 7286841_1–40 | A1 sampling | 18 running, rest pending |

## 9. Priorities for the next session
1. Speed test → choose INCAR → update held dirs → release 7297693/7297695 (§4). Report the speedup and accuracy to RC.
2. Rerun any 7286822 task that failed (same index with `TASKS=tasks_old.txt`; finished dirs are skipped).
3. A1 sampling: check memory/time of finished runs; XDATCAR → FPS → R1b staging.
4. mldp post-processing of finished R1 bands; then the first DeePMD training (fparam = $k_BT$; RC's `deepmd_py311`, P100).
5. Open RC questions in `QUESTIONS.md` (budget, pressure, phases, light elements; MgO/MgSiO₃ items 8–13).

## 10. Evening update (21:00 PST)
RC messages after 16:00, in order: "What is the speed result?"; "Speed tests should be done in debug and last less than 30 minutes. A lot shorter for a simple speed test."; "I always use srun with PMI2"; "Debug jobs should start"; "That was way too many cores for a debug job! Write restarts".

**Speed test.**
- 7302962_2–10 (normal queue, 1 h runs) cancelled. 7302962_1 = `speed/T300_ref` finished: 35 SCF steps, 3322 s (≈ 95 s per step on 2 × 32), 0.69 GB/rank peak. It is the converged reference for the accuracy check.
- Debug attempt 1, 7314173 (5 variants × 64 = 320 tasks): never started, cancelled. The debug QOS caps a job at 10 nodes, and the free icelake cores were scattered.
- Debug attempt 2, **7315550** (128 tasks, `vfast` and `fastR`, 64 ranks each, stopped at 1500 s): running since 20:45, ends ≈ 21:12. Each step is spread over 10 nodes, so its s/SCF is not comparable with the 2-node reference; the step count to convergence and the accuracy (if converged) are. Analyse: `python ~/Claude/tools/fe_r1_speed.py speed --prefix dbg_ --cfgs T300 --ref T300_ref` (run in R1/).
- **RC: 128 cores was far too many for a debug job.** The next speed test must be small, e.g. a single variant on ≤ 32 ranks with NELM capped at a few steps (s/SCF only), or a smaller cell. Script: `R1/fe_r1_speed_dbg.sh` (VARIANTS env; `--nodes=1-10` because of the QOS cap). Change its size before reuse.

**srun + PMI2 works for VASP 6.6.1** (7315550: "running 64 mpi-ranks … on 10 nodes", SCF iterating). Recipe: oneAPI 2025.3 `setvars.sh`, explicit 2025.3 `LD_LIBRARY_PATH` + `~/lib`, `I_MPI_PMI_LIBRARY=/usr/lib64/libpmi2.so`, `I_MPI_FABRICS=shm:ofi`, `FI_PROVIDER=mlx`, `srun --mpi=pmi2 -K1`. RC: "I always use srun with PMI2". The Oct-14 failure recorded in memory `vasp-batch-launch` was the environment (2026.1 via `load_intel`, no FI_PROVIDER), not srun.

**Main finding: the R1 slowness was rank placement, not the INCAR.**
- 7286822 (`--ntasks=64`, Intel mpirun/hydra, grants scattered over 3–7 nodes): 12 COMPLETED, **26 TIMEOUT** at 4 h, 1 cancelled.
- Completed tasks: about 70 s per SCF step (e.g. task 1 on hpc-53-[10-16], 43 min).
- Timed-out tasks: **730–925 s per step** (old/T3000/recal/1, 16 steps in 4 h; task 20 on hpc-34-26, hpc-52-31, hpc-53-08) and **1290–1420 s per step** (old/T5000/recal/1, 10 steps). That is 10–20× slower. The NBANDS increase (1088 → 1232 → 1344) explains only 1.1–1.3×.
- Same pattern as the QE x73b case in `modelpimslurmjob.sh`: hydra places ranks without regard to the per-node grant and oversubscribes cores. srun + PMI2 places one rank per granted CPU.
- Timed-out dirs (27 not finished): old/T300/recal/{4,8}, T500/{1,2}, T1000/1, T1500/{1,2}, T2500/{1,2,3}, T3000/{1,2,3}, T3500/{1,2,3}, T4000/1, T4500/{1,2,3,4}, T5000/{1,2,3}, T5500/{2,3,5}. Their OUTCARs are partial; the job script reruns any dir without "General timing".

**Next steps (in order).**
1. When 7315550 ends: the table (above), then pick the INCAR (VeryFast + EDIFF 1e-5 unless its accuracy fails). Report to RC.
2. Switch `R1/fe_r1_job.sh` (and `A1/fe_a1_job.sh`) from `mpirun -np $SLURM_NTASKS` to `srun --mpi=pmi2 -K1` with the env above (drop `unset I_MPI_PMI_LIBRARY`). Held 7297693/7297695 have the old script baked in: cancel them and resubmit with the new script rather than releasing.
3. Resubmit the 26 timed-out + task-12 dirs of `tasks_old.txt` (the indices of 7286822 that are not COMPLETED) with the new script.
4. Check A1 7286841 (27 COMPLETED, 13 running at 21:00) for the same placement slowdown (LOOP times per task against its node list).
5. Then §9 items 3–5.

**Jobs at 21:00.**

| job | what | state |
|---|---|---|
| 7286822 | R1 old 1–11, 13–38 | finished: 12 completed, 26 timeout, 1 cancelled |
| 7297693, 7297695 | R1 old 12, 39–100; old_b 1–50 | HELD (resubmit with the srun script instead) |
| 7302962_1 | T300_ref, 2 × 32 | completed (3322 s) |
| 7315550 | debug speed test vfast + fastR | running, ends ≈ 21:12 |
| 7286841 | A1 sampling | 27 completed, 13 running |

