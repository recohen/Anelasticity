# Anelasticity restart, 2026-11-22 (16:15 PST): Fe DeePMD energy errors solved (00h retrain finishing), quadrupolar dislocation dipoles stable, both sweeps finished but only lock-in done

**Read first:**
1. This file.
2. `INPROGRESS.md` (jobs).
3. `QUESTIONS.md` (open decisions for RC).
4. `results_Fe/DP_energy_errors.md` (Fe DeePMD).
5. `results_dislocations/M1_edge001_4000K.md` (dislocations, §§5–7).
6. `ANELASTICITY_PLAN_DISLOCATION_Q.md` (plan; Eq. 3 = the Debye form, $\tau = B/(k+\rho b^2G_U)$).

The previous restart is `ANELASTICITY_RESTART_2026-11-19.md`. No restart was written on 11-20 or 11-21: their work is in INPROGRESS rows and in §1 below. Session log: `sessions/2026-11-20_0324_b662d795.md` (one session, 11-20 to 11-22).

**Coordination:** another Claude session (WSDA) owns `~/Claude/WSDA` and `~/Claude/Resnick`, and the many `rn406`-type jobs in squeue are its jobs. This session owns `~/Claude/Anelasticity` and its tools.

**Standing rules:**
- **Paths:**
  - Docs and tables go in `~/Claude/Anelasticity` (`results_<topic>/`), tools in `~/Claude/tools`.
  - Run dirs hold only job I/O plus a README.
  - Use `/resnick/groups/carnegie_poc/rcohen/tmp` as the tmp dir, never `/tmp`.
- **Jobs:**
  - Jobs of 30 min or less go in `-q debug`, one running at a time.
  - Use srun with PMI2.
  - Never use X. Deng's Fe model, even for tests. Her MgSiO₃ model and her dpdata tools are fine.
- **Docs:** after every doc edit, run `~/Claude/tools/obsidian_poke.sh`.
- **Terminology (RC 11-22):** "A constant shift in the energy for a potential doesnt matter unless it shows a problem"; "A shift that depends on volume and structure is not an offset". Call these energy errors, not offsets.

## 1. Since the 11-19 restart (11-20, 11-21, in brief)
- **11-20 decision.** RC: "We dont have time to rerun. We need to train the deepmd potential as discussed. Do run vasp for configs but no vasp ml runs". So there are no more VASP-MLFF runs.
- **11-20 recalculations.** R1 (139 old configs) and R1b (328 FPS frames from the 8 finished A1 trajectories plus rattled frames) were recalculated with srun/PMI2 and are finished.
- **11-20 defects.** R1d added defect cells, all hcp, 0–350 GPa (RC: "Up to 350 GPa, not only 350 GPa"): vacancy, vacancy jumps, the Σ7 tilt boundary and the {10−12} twin (tw13). They are finished.
- **11-21 tw13 frames.** All 50 tw13 frames had diverged. The fix was LREAL Auto, AMIN 0.01, a larger FFT grid (`fe_r1d_regrid.py`) and even k-meshes (RC: "I don't like odd meshes"). The single test ran first (RC: "test a single failed run first"). After that, all 50 reruns converged (7591334); 47 frames were kept.
- **11-21 model 00 (7588075).** Forces were fine, but there were per-state energy errors of 30–87 meV/atom at low SIGMA: + for hcp, − for fcc. The retrains 00e/00f with energy weight ×10/×50 did not remove them.
- **11-21 dislocations.** RC: "add [dislocations] to our MgO and MgSiO3 production runs". The plan is `ANELASTICITY_PLAN_DISLOCATION_Q.md`. The MgO and B1 bridgmanite edge-dipole pilots both finished with their cores intact. RC: "Submit the M1 sweep while we wait".

## 2. Fe DeePMD: energy errors solved (RC 11-21 "Please sort it out")
The full write-up is `results_Fe/DP_energy_errors.md`.

**The DFT labels are consistent:**

| check | result |
|---|---|
| E–P | 1.1 GPa, uniform |
| E–F | 0.3 meV/Å |
| k-mesh | 3–6 meV/atom |
| every label | TOTEN, not enthalpy |
| perfect fcc−hcp | 122.6 meV/atom at V 7.25 |

**Cause: the descriptor.** `se_e2_a` carries angles only to ℓ = 1. The fcc and hcp descriptors differ by 0.4 %, against a 3–5 % thermal spread, so every se_e2_a variant fits fcc−hcp at about 54 meV/atom.

**Fix.** The hybrid `se_e2_a + se_e3` (se_e3: rcut 4.5, rcut_smth 2.0, sel 80, neuron [16,32,64]) gives 124.4 meV/atom (test model 00t3b). The small se_e3 [2,4,8] and DPA-1 did not help. se_e3 costs about 9× in training (0.075 against 0.0085 s/batch on a P100).

**Full retrain `DP/00h` (job 7715007, P100, 36 h limit):**
- input is the 00 input plus the 00t3b descriptor;
- energy prefactor 0.2 → 20, 600k steps;
- data is `00/data` plus the 25 tw13 systems (151 systems).

At 16:10 it was at step 479k of 600k, so it ends about 19:30. Then `job.sh` freezes, compresses, runs `dp test` and runs `dp_state_errors.py graph.pb data` → `offsets.txt` (the name is kept for the running job.sh).

The interim at 250k (`00h/errors_250k_interim.txt`) gives perfect fcc−hcp 123.9 meV/atom. State-mean errors by group:

| group | rms state-mean error (meV/atom) |
|---|---|
| a1_fcc | 6.6 |
| a1_hcp | 5.2 |
| vac | 6.7 |
| vacmig | 7.8 |
| s7 | 4.2 |
| s7slide | 4.4 |
| tw13 | 4.6 |
| tw13slide | 4.9 |
| old | 3.0 |
| old_b | 2.2 |
| all states at SIGMA < 0.07 | 4.7 (model 00: 27.6) |

Forces are 0.14–0.23 eV/Å.

**Tools:**
- `tools/dp_state_errors.py`: the old name `dp_state_offsets.py` is a symlink. It evaluates 2 frames at a time, because se_e3 exhausted login-node memory.
- Scratch `pe.py` evaluates perfect fcc/hcp.

**Next for Fe:**
1. Check `00h/offsets.txt`, `dptest.log`, and the perfect fcc−hcp with the final graph.
2. Measure the LAMMPS MD speed with the compressed hybrid model, since se_e3 is slower.
3. Start iteration 01 (`fe_dp_explore`) with 00h. RC's loop is: our model → MD on hcp/fcc plus vacancies, twins, GBs and dislocations → SOAP+FPS → DFT test → add the worst 10–20 % → iterate.

## 3. Dislocations: the vertical-dipole cells were unstable; the quadrupolar rebuild is stable
**M1 (vertical cell, γ₀ 0.01) was nonlinear** (§§1–2 of the results doc). G″ < 0 at 1 ps and G′ < 0 at 5/20 ps, and the dipole flipped by Δs ≈ 14 Å every half cycle.

**RC "Submit option 1" → Green–Kubo run 7718928, now finished** (1 ns NVE, `Dislocations/M1_edge001_4000K_GK`). Final σ_xz (computed 16:10):

| quantity | value (GPa) |
|---|---|
| rms | 1.56 |
| full $V\langle\delta\sigma^2\rangle/k_BT$ | 1162 |
| the same from 1-ps averages | **1011** (quarters 912–1058) |
| control xy / yz | 11 / 1 |

By results Eq. 5 this gives κ_d/κ_im ≈ 0.82. **Cause: the edge dipole was built vertically** (both cores at the same x, no tilt). That is the unstable configuration of an edge dipole.

**RC "Yes change the builder and re-run the M1 and B1 pilots ... and then the sweeps".** `build_dislocation_dipole.py` now defaults to `--edge-geom quad`:
- the upper core is glided by Lx/2 and the tilt is xz = b/2 (Bulatov & Cai §5.5);
- `--quad-dx` gives an extra shift in units of b;
- `--edge-geom vertical` reproduces the old cell byte for byte.

**Pilot results:**

| pilot | job | separation (Å) | ⟨σ_xz⟩ (GPa) | energy |
|---|---|---|---|---|
| MgO `edge001q_4000K` | 7813930 | 18.5–20.6 (Lx/2 = 20.65) | 0.01 | 4.4 eV below the vertical cell |
| B1q `B1q_edge100_010_3000K` | 7813931 | 15.3–16.1 | +0.34 | 20.2 eV below |

The B1q pilot used `--quad-dx 0.5`: at 0 a Si–O pair at the glided core started 0.78 Å apart.

**Sweeps, all finished 14:00–14:52, lock-in only so far (16:10).** G′/G″ in GPa (`anelastic_lockin.py DIR --period P --mode shear`):

| period (ps) | M1q dipole | MgO perfect (c44) | M1q \|σ₃/σ₁\| | B1q dipole | bdg perfect, same orientation (c66) | B1q \|σ₃/σ₁\| |
|---|---|---|---|---|---|---|
| 0.2 | 165.5 / 19.0 | 180.6 / −5.0 | 0.008 | 308.4 / −2.2 ± 4.6 | not run | 0.008 |
| 1 | **312.7 / −97.2** | 179.8 / −0.7 | 0.081 | 200.8 / 12.3 | 259.4 / 4.4 | 0.012 |
| 5 | 88.9 / 12.6 | 179.0 / 0.2 | **0.15** | 220.7 / −0.5 | — | 0.014 |
| 20 | 82.5 / 8.1 ± 3.4 | 179.4 / −0.9 | 0.037 | 221.7 / 4.7 ± 15 | 256.4 / 0.5 | 0.011 |

The MgO perfect values come from `4000K/FreqSweep_B1perfect` and `M1_edge001_4000K/ref_P20ps_xz`. Both sweeps used γ₀ = 0.005.

**First reading (not yet checked):**
- **B1q looks linear** (|σ₃/σ₁| ≤ 0.014).
  - It is relaxed by ΔG′ ≈ −35 GPa at 5–20 ps with ΔG″ ≈ 0, so the relaxation time is ≲ 1 ps.
  - At 1 ps, ΔG′ = −59 and ΔG″ = +8. That is more softening than at 5–20 ps; it is not monotonic, so check it.
  - 0.2 ps needs a perfect reference at 0.2 ps (none exists; the 0.2 ps perfect G′ is not 259).
- **M1q at 1 ps is still unphysical** (G″ < 0, as in the vertical M1 at 1 ps: 238/−195), and 5 ps is nonlinear (0.15).
  - The 0.2 ps and 20 ps points look physical: ΔG′ −15 / −97 and ΔG″ +24 / +9.
  - **Look at the 1 ps run first:**
    - the strain and stress time series;
    - the cores against the drive phase (does the glide lock to 1 THz?);
    - the energy balance with the thermostat (TDAMP 0.1 ps).
  - The perfect cell at 1 ps is normal (−0.7 ± 0.3), so the lock-in phase convention is fine.

**Next:**
1. Track the cores against the drive phase:
   - MgO: `disl_dipole_cores.py traj.lammpstrj --rc 2.4 --win 4–10` in each `M1q_edge001_4000K/P*`;
   - B1q: `--sub 2 --rc 3.6`.
2. Run the 1-ps diagnosis above.
3. Fit plan Eq. 3 (ΔJ, τ → B, k) to the physical points, and compare B with the driven-glide value 1.76 × 10⁻⁴ Pa s.
4. Write `M1q_edge001_4000K/README.md` (none yet) and results doc §7.
5. Possibly run a B1q perfect reference at 0.2 and 5 ps.

The Earth scaling argument is unchanged: with B ~ 10⁻⁴ Pa s the drag (Granato–Lücke) peak is at MHz–GHz, so the seismic band needs thermally activated terms.

## 4. Jobs at 16:10
| job | what | state |
|---|---|---|
| 7715007 | Fe DeePMD 00h, full retrain with the hybrid descriptor | RUNNING, step 479k/600k, ends ≈ 19:30 |
| 7718928 | M1 Green–Kubo (vertical cell) | COMPLETED (1 ns) |
| 7813930, 7813931 | MgO and B1q quad pilots | COMPLETED |
| 7817611_1–4 | M1q sweep | COMPLETED, lock-in done |
| 7820552_1–6 | B1q sweep plus the c66 references | COMPLETED, lock-in done |

## 5. Run directories
- **Fe:** `/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/`
  - `R1/` (old, old_b, def, scftest; README Parts 1–4)
  - `A1/bands`
  - `DP/00` (model 00), `DP/00t*` (descriptor tests; `00t3b` = the winner), `DP/00h` (the full retrain)
- **MgO:** `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/Dislocations/`
  - `edge001_4000K` (vertical pilot), `M1_edge001_4000K`, `M1_edge001_4000K_GK`
  - `edge001q_4000K`, `M1q_edge001_4000K`
- **Bridgmanite:** `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3/1280atoms/V6.5669/crystal/Dislocations/`
  - `B1_edge100_010_3000K` (vertical), `B1q_edge100_010_3000K`, `B1q_sweep_3000K` (README; `perfect.data` is 2560 atoms)
  - `sweep.env` is at `V6.5669/sweep.env`.

## 6. Tools changed (`~/Claude/tools`)
| tool | change |
|---|---|
| `build_dislocation_dipole.py` | `--edge-geom quad` (default) / `vertical`, `--quad-dx` |
| `gk_stress.lammps` | optional `DUMPN` (trajectory every N production steps, appended across restarts) |
| `dp_state_errors.py` | renamed from dp_state_offsets.py (symlink kept); evaluates in 2-frame chunks; "energy error" wording |
| `disl_dipole_cores.py` | unchanged; core tracking per window |

## 7. Priorities for the next session
1. **00h (after ≈ 19:30):**
   - check the final errors and fcc−hcp;
   - measure the MD speed;
   - update `DP_energy_errors.md` §5;
   - start iteration 01.
2. **Dislocation sweeps:** cores, the 1-ps anomaly, then the Eq. 3 fits (§3); write up as results doc §7 and report to RC.
3. **Open decisions for RC:**
   - slip systems;
   - the dislocation scope (≈ 300 against ≈ 60 P100-h);
   - `QUESTIONS.md` items 4–13.
4. **Older open items:**
   - the separated MgO pair DFT check (INPROGRESS §1 row 1);
   - the A3b follow-ups (finished, not analysed);
   - INPROGRESS §2.
