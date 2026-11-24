# Fe DeePMD potential: results to date (2026-11-23)

Current model: **00h**, at `/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/DP/00h/graph_c.pb` (compressed) and `graph.pb`.
The energy-error diagnosis is in `DP_energy_errors.md`. The DFT settings tests are in `A0b_summary.txt` and `A0c_summary.txt`. The plan is
`../ANELASTICITY_PLAN_FE.md` §3.

## 1. Short answer

00h fixes the one serious defect of model 00:
- **Phase energy.** It gets the hcp–fcc energy difference right: $E_{fcc}-E_{hcp}$ = 124.5 meV/atom on perfect cells at $V$ = 7.25 Å³/atom, against DFT 122.6. Model 00 gave 53.8.
- **State-mean errors.** Every state of the training set has a mean error of ≤ 18 meV/atom. The rms by group is 2–7 meV/atom. Model 00 had 30–87 meV/atom at low SIGMA.
- **Forces and stress.** Forces are better than model 00: rmse 0.198 eV/Å, which is 4.9 % of the rms DFT force component (4.08 eV/Å). Model 00 was at 0.22–0.34. Stress rmse is 0.67 GPa.
- **MD.** It runs stable 3-ps NPT at 300 GPa and 2400 K for the hcp (64 atoms), twin (100 atoms) and basal edge dipole (176 atoms) cells.

There are three limits:
1. **Training-set errors only.** Every error quoted here is measured on the training set; nothing was held out. The first real test is iteration 01, which is now running (§6). It runs MD with 00h on structures the model has not seen, then DFT-checks frames picked by SOAP-FPS.
2. **No physical properties yet.** Beyond fcc−hcp, I have not computed any physical property with 00h: no EOS against DFT, no $c_{ij}$, phonons, melting or defect energies. These are the next checks.
3. **Speed.** The hybrid descriptor is about 5× slower than model 00 in LAMMPS: 79–103 steps/s for 64–176 atoms on a P100, against about 500 for model 00. This matters for the large anelastic cells; see §5.

## 2. DFT reference settings

PBE, Fe_sv PAW, non-magnetic (ISPIN 1), ENCUT 700 eV, PREC Accurate, LREAL .FALSE., ISMEAR −1 with SIGMA = $k_BT$, and a true shifted 2×2×2 mesh (4 k-points, KBLOWUP .FALSE.). The 100-atom twin cells instead use LREAL Auto, AMIN 0.01 and an FFT grid ≥ 9.6/Å. VASP 6.6.1.

| test | result |
|---|---|
| A0b: Γ-only in 64-atom cells | not converged: 30–106 meV/atom, 1–4 GPa against 2×2×2 |
| A0b: ENCUT 700 → 900 | 0.6 meV/atom, ≤ 0.8 GPa |
| A0b: SIGMA | must be $k_BT$ of the state: a fixed 0.026 eV at high T changes $F$ by 106–270 meV/atom (P0–P330) |
| A0c2: shifted 2×2×2 against 3³ / 4³ | 0.008–0.015 eV/Å and ≤ 0.1 GPa at $k_BT$; 0.03–0.09 eV/Å at 300 K |
| eostest: $-\mathrm{d}E/\mathrm{d}V$ against $P$ | 1.10–1.23 GPa, uniform over hcp/fcc at P100/P200 |
| eostest: $-\mathrm{d}E/\mathrm{d}s$ against $F$ | agree to 0.3 meV/Å |
| phasetest: perfect fcc−hcp at $V$ = 7.25, $c/a$ 1.60 | 122.8 (primitive), 122.6 (64-atom MP 4³) meV/atom |

Every label is TOTEN, so the training set does not mix energy and enthalpy.

## 3. Training data (670 frames, 151 systems)

| group | source | atoms | systems | frames |
|---|---|---|---|---|
| a1_hcp, a1_fcc | R1b: SOAP-FPS frames from VASP on-the-fly MD (A1; VASP-MLFF used only as a sampler), plus rattled cells at the 32 states without a trajectory. P = 0–360 GPa, T = 300 K to about 1.05 T_m | 64 | 20 + 20 | 138 + 183 |
| def_vac, def_vacmig | R1d: hcp with a vacancy, and basal/non-basal jumps at f = 0.25/0.5/0.75. P = 0–350 GPa | 63 | 20 + 10 | 58 + 40 |
| def_s7, def_s7slide | R1d: Σ7 [0001] tilt boundary, plus rigid shifts | 52 | 19 + 5 | 37 + 20 |
| def_tw13, def_tw13slide | R1d: {10−12} twin (Σ13), plus shifts (SCF fixed 11-21) | 100 | 20 + 5 | 32 + 15 |
| old, old_b | R1: 150 SOAP-FPS frames of the old bcc and liquid ML_AB set at 266–300 GPa, 300–10 000 K | 128 | 18 + 14 | 98 + 49 |

VASP ML_AB files (checked 11-23): only `Fe/bcc/ML/Orthogonal/P300GPa/ML_AB` (913 configs) is used, as 150 SOAP-FPS frames recomputed at R1 settings; its own labels are not used (ENCUT 900, PREC Normal, LREAL Auto, EDIFF 1e-4, fixed SIGMA 0.2588). The A1 on-the-fly ML_ABN (687 configs in 14 of 40 states) are not used as labels (Γ only, ENCUT 500, EDIFF 1e-4); A1 frames come from the XDATCAR trajectories, recomputed. Not used at all: `bcc/ML/Orthogonal/P100GPa` (185 configs, 128 atoms, Fe_sv, 655–7535 K, P 77–277 GPa; 40 SOAP-FPS frames submitted at R1 settings 11-23, R1/p100, job 7959061, for the next split) and the low-pressure bcc sets (`bcc/ML`, `P10GPa`, `P20GPa`, `bcc/2500K`; 866–2242 configs, Fe (not Fe_sv) PAW, ENCUT 400–500, mostly ISPIN 2).

Frames were dropped if SCF hit NELM, if the top band was occupied above 1e-2, or if |F| > 30 eV/Å. fparam = SIGMA = $k_BT$.

## 4. Model history

| model | change | $E_{fcc}-E_{hcp}$ (meV/atom; DFT 122.6) | rms state-mean error at σ < 0.07 eV (meV/atom) | F rmse (eV/Å) |
|---|---|---|---|---|
| 00 | se_e2_a rcut 6, sel 200, fit [240,240,240], 600k steps, energy weight 0.04 → 2 | 53.8 | 27.6 | 0.22–0.34 |
| 00e / 00f | energy weight ×10 / ×50 | 59.6 / 13.4 | 21.9 / 35.2 | worse |
| 00t … 00ta | se_e2_a variants, small se_e3, DPA-1 (300 K data only) | −5 to +1 | 47–71 | — |
| 00t3b | **+ se_e3** rcut 4.5, rcut_smth 2.0, sel 80, [16,32,64] (300 K data only) | 124.4 | 5.5 | 0.15–0.18 |
| **00h** | 00 input + 00t3b descriptor, energy weight 0.2 → 20, all data + tw13, 600k steps (15.8 h on a P100) | **124.5** | **4.5** | **0.14–0.24** |
| 00t4c | **DPA4C** (pt-expt; channels 32, lmax 2, rcut 6; 300 K data only, 100k steps, 72 min on a V100) | 127.0 | 0.5 | 0.05–0.06 |
| **00d** | **DPA4C**, all 00h data, 1M steps (10.5 h on a V100) | **126.3** | **3.1** | **0.04–0.12** (dp test 0.093) |

The cause (`DP_energy_errors.md` §3): se_e2_a carries angular information only up to ℓ = 1, which vanishes by symmetry at
both the fcc and hcp sites. Its fcc and hcp descriptors therefore differ by only 0.4 %, against a 3–5 % thermal spread.
The three-body se_e3 embedding sees $\cos\theta_{jik}$ directly.

## 5. Model 00h: final errors on the training data

The mean energy error of state $s$ is

$$\Delta_s=\big\langle (E_{DP}-E_{DFT})/N\big\rangle_{s} \tag{1}$$

The table below gives, by group: the rms of $\Delta_s$ over states, and the mean scatter within a state, both in meV/atom (from `00h/offsets.txt`, `tools/dp_state_errors.py`). It also gives the force rmse in eV/Å.

| group | frames | rms $\Delta_s$ 00h | rms $\Delta_s$ 00 | within-state sd | F rmse 00h | F rmse 00 |
|---|---|---|---|---|---|---|
| a1_fcc | 183 | 5.8 | 21.9 | 1.8 | 0.150 | 0.267 |
| a1_hcp | 138 | 4.2 | 23.4 | 1.8 | 0.162 | 0.263 |
| def_vac | 58 | 6.1 | 10.8 | 1.9 | 0.194 | 0.301 |
| def_vacmig | 40 | 7.1 | 12.4 | 3.5 | 0.184 | 0.275 |
| def_s7 | 37 | 4.5 | 6.9 | 1.9 | 0.231 | 0.340 |
| def_s7slide | 20 | 4.6 | 10.6 | 2.2 | 0.237 | 0.323 |
| def_tw13 | 32 | 5.0 | — | 1.7 | 0.206 | — |
| def_tw13slide | 15 | 5.8 | — | 2.9 | 0.166 | — |
| old | 98 | 2.1 | 4.6 | 2.7 | 0.233 | 0.322 |
| old_b | 49 | 1.7 | 2.9 | 2.3 | 0.238 | 0.323 |

The same by SIGMA band:

| SIGMA band (eV) | frames | rms $\Delta_s$ 00h | rms $\Delta_s$ 00 | F rmse 00h |
|---|---|---|---|---|
| 0–0.07 | 223 | 4.5 | 27.6 | 0.144 |
| 0.07–0.20 | 110 | 4.7 | 12.5 | 0.162 |
| 0.20–0.40 | 193 | 6.2 | 8.1 | 0.215 |
| 0.40–1.00 | 144 | 3.3 | 3.7 | 0.232 |

At 300 K the hcp and fcc state errors no longer split by sign:
- hcp: +2.2, +9.8, +6.1, +2.4, +0.9 meV/atom at P0, P100, P200, P300, P360;
- fcc: +3.7, +4.5, +0.5, −1.2, −3.5 meV/atom.

Model 00 gave +35 to +87 for hcp and −30 to −55 for fcc.

The largest state errors are:

| state | error (meV/atom) |
|---|---|
| fcc P100 T2800 | +17.7 |
| fcc P100 T3800 | +17.0 |
| vacmig P350 T4500 | −15.9 |
| tw13 P100 T300 | +15.2 |
| vac P350 T2600 | −14.5 |

So the hot vacancy states at the highest pressures are biased about −14 meV/atom. These states should be watched in iteration 01.

The whole-set `dp test` (all 151 systems) gives energy rmse 5.5 meV/atom, force rmse 0.198 eV/Å and stress rmse 4.2e-3 eV/Å³ (0.67 GPa).

**MD speed** (`DP/01/speedtest`, P100, compressed model, 3000 NPT steps at 300 GPa, 2400 K, all stable):

| cell | atoms | steps/s |
|---|---|---|
| hcp | 64 | 103 |
| tw13 | 100 | 97 |
| dbe | 176 | 79 |

Model 00 ran at about 500 steps/s on cells of this size. The slowdown is the se_e3 term (sel 80 three-body pairs within 4.5 Å). **MPI** (`DP/01/speedtest/mpi`, job 7908389), in steps/s:

| cell | 1 rank, 1 GPU | 2 ranks, 1 GPU | 4 ranks, 1 GPU | 2 ranks, 2 GPUs | 4 ranks, 2 GPUs |
|---|---|---|---|---|---|
| dbe, 176 atoms | 78 | 44 | 25 | 96 | — |
| hcp, 4096 atoms | 6.4 | 5.6 | 5.1 | 11.8 | 9.9 |

Four independent 64-atom runs sharing one GPU give 95 steps/s in total, against 103 for a single run.

So MPI helps only with one rank per GPU: 1.84× on 2 GPUs at 4096 atoms, and 1.23× at 176 atoms. Extra ranks on the same GPU slow it down. The 4096-atom Fe speed is 6.4 steps/s, against 22.8 for MgO with se_e2_a (P100), so 1 ns takes 43 h on one P100 and 24 h on two.

## 6. Iteration 01 (submitted 2026-11-23)

`fe_dp_explore.py DP 01 --model DP/00h/graph_c.pb --prev DP/00h` stages 425 MD runs. Each runs 20 ps with a dump every 20 fs.

**Systems:**
- hcp, fcc, vac1, vac2;
- the basal I2 stacking fault (sf);
- s7 and tw13;
- four ⟨a⟩ dislocation dipoles (basal and prismatic edge, screw on basal and prism);
- oscillating-shear versions of hcp, vac1, s7, tw13, dbe and dbs (γ 0.02, period 2 ps).

**States:** P = 0, 100, 200, 300, 350 GPa × T = 300 K and 0.4, 0.7, 0.95, 1.05 T_m.

Job **7906537_1–17** (P100, 3 h per system, about 1.8 h needed for the 176-atom cells). The edge dipoles use the
quadrupolar arrangement. I fixed `fe_dp_explore.py` to pass `edge_geom='quad'` after the 11-22 builder change broke the call.

**The loop (RC 11-23).** The bad structures, found by comparing with DFT, go into training. The rest go into a test pool, and a selection from the pool becomes the test structures. Iterate until the total accuracy no longer changes. The steps are:
- `fe_dp_sample.py` picks frames from the MD by SOAP-FPS, 3 per run. DFT is run on them (`fe_r1d_job.sh`).
- `fe_dp_split.py` computes the DFT error of the previous model on each frame. The worst 15 % per T band go to training, and the rest go to the pool `DP/NN/test_new`.
- `fe_dp_testset.py` (new, 11-23) selects 30 % per system type from the pool by SOAP-FPS. These go to `DP/test/itNN`. The test structures accumulate over iterations and are never trained on.
- The model is retrained from the previous one for 200k steps (`--init-frz-model`).
- `fe_dp_accuracy.py` (new, 11-23) scores the previous and the new model on all test structures (RMSE of E, F and stress) and appends the result to `DP/accuracy.txt`.

The convergence test is

$$|\Delta\mathrm{RMSE}_E| < 0.5\ \text{meV/atom},\quad |\Delta\mathrm{RMSE}_F| < 5\,\%,\quad |\Delta\mathrm{RMSE}_S| < 0.1\ \text{GPa} \tag{2}$$

between successive models, on the same test structures.

**Selection bias.** The newest test set is what remains after the previous model's worst frames were removed. It therefore flatters the previous model. From iteration 02 on, Eq. 2 uses only the earlier test sets. In iteration 01 the 00h → 01 comparison on it01 is biased towards 00h.

## 7. Open items

1. Held-out errors from iteration 01 (§6). They decide whether 00h is converged for the defect and dislocation structures.
2. Physical checks with 00h against DFT and experiment:
   - hcp and fcc EOS, and c/a(P);
   - $c_{ij}$ at 300 GPa;
   - vacancy formation energy;
   - Σ7 and twin energies;
   - the melting line (two-phase), against our VASP and against the literature.
3. 4096-atom MD speed. If it is too slow for the anelastic sweeps, test smaller se_e3 settings: sel 40, or rcut 4.0 with [8,16,32]. The fcc−hcp test is the criterion (00t3 [2,4,8] at rcut 4 failed).
4. bcc and liquid are present only near 300 GPa (old, old_b). Whether that is enough for the hcp anelasticity work depends on iteration 01.
5. Housekeeping: `00h/job.sh` called plain `python` for `dp_state_errors.py`, which is not the deepmd env, so `offsets.txt` was rerun by hand on 11-23. `fe_dp_train.sh` (iteration 01) already uses `$CONDA_PREFIX/bin/python`.
