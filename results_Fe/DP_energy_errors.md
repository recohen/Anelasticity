# Fe DeePMD model 00: the structure- and volume-dependent energy errors and their fix (2026-11-21/22)

Run dirs: `/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/DP/{00,00e,00f,00t,00tnv,00tE,00tEF,00t3,00ta,00t3b,00h}`,
DFT checks in `.../ML/R1/{eostest,phasetest}`. Tool: `tools/dp_state_errors.py`.

## 1. Symptom

Not an offset: a constant shift would be harmless, but these change sign between hcp and fcc and grow with compression
(RC 11-22: "A shift that depends on volume and structure is not an offset"); they are energy errors in $E(V,\text{structure},T)$.

Model 00 (se_e2_a, rcut 6, 600k steps, 623 frames) fits forces to 0.15–0.34 eV/Å, but each thermodynamic state has its
own mean energy error

$$\Delta_s=\big\langle (E_{DP}-E_{DFT})/N\big\rangle_{s} \tag{1}$$

of +35 to +87 meV/atom for hcp and −30 to −55 meV/atom for fcc at 300 K, with a within-state scatter of only 1–4 meV/atom.
The errors depend on structure (sign), volume and SIGMA: they shrink with SIGMA and are ~0 at SIGMA ≥ 0.3 eV. On perfect cells at $V = 7.25$ Å³/atom, model 00 gives
$E_{fcc}-E_{hcp} = 54$ meV/atom.

## 2. The DFT labels are consistent

RC asked whether two kinds of energy were mixed (enthalpy against energy). They were not: every label is TOTEN, read by
dpdata vasp/outcar. PV would be about 5 eV/atom with the same sign for both phases, and $E_{TOTEN}-E(\sigma\to0)$ is −1
meV/atom at 300 K. Direct checks:

| check | result |
|---|---|
| energy vs stress: $-\mathrm{d}E/\mathrm{d}V$ from $V\times0.99, 1.01$ against the Simpson mean of $P$ (eostest, hcp/fcc P100/P200) | difference 1.10–1.23 GPa, the same for all four states (Pulay-like, uniform) |
| energy vs force: the largest-force atom displaced ±0.01 Å along $F$ (eostest `_fm`, `_fp`) | $-\mathrm{d}E/\mathrm{d}s$ = 3.7593 against $F\cdot\hat u$ = 3.7590 eV/Å (hcp), 3.5020 against 3.5010 (fcc) |
| k-mesh: 64-atom cell, 4-point shifted mesh, against primitive cells at 24³ (phasetest) | 3–6 meV/atom |
| perfect-crystal phase difference at $V=7.25$, $c/a=1.60$ | $E_{fcc}-E_{hcp}$ = 122.8 (primitive), 122.6 (64-atom MP 4³), 128.4 meV/atom (64-atom shifted 4-point) |

## 3. Cause: the descriptor cannot tell fcc from hcp

The se_e2_a descriptor is built from the generalized coordinates $s(r)\,(1,\hat{\mathbf r})$:

$$\mathcal D_{mn}=\sum_{j,k} g_m(r_{ij})\,g_n(r_{ik})\,s(r_{ij})\,s(r_{ik})\,\big(1+\hat{\mathbf r}_{ij}\cdot\hat{\mathbf r}_{ik}\big) \tag{2}$$

So it carries angular information only up to $\ell = 1$. At the centrosymmetric fcc site and the D$_{3h}$ hcp site,
$\sum_j g(r_{ij})\hat{\mathbf r}_{ij}=0$ for every radial channel. Equation 2 then reduces to products of radial sums,
and fcc and hcp differ only through their slightly different radial shells. Measured on the 300 K frames, the mean fcc
and hcp descriptors differ by $|\mathcal D_{fcc}-\mathcal D_{hcp}|/|\mathcal D| = 0.4\,\%$, while the thermal spread
within a state is 3–5 %. The fitting net cannot place a 123 meV/atom step on a 0.4 % signal buried under 3–5 % noise.

Tests, all trained on the ten a1 300 K states only (hcp and fcc, P = 0–360 GPa), 100k steps:

| model | change | $E_{fcc}-E_{hcp}$ (meV/atom; DFT 122.6) | rms state-mean error (meV/atom) |
|---|---|---|---|
| 00 (all data) | — | 53.8 | 27.6 (σ < 0.07 eV) |
| 00e / 00f (all data) | energy weight ×10 / ×50 | 59.6 / 13.4 | 21.9 / 35.2 |
| 00t | se_e2_a | 0.2 | fcc 47, hcp 71 |
| 00tnv | no virial | −3.4 | — |
| 00tE / 00tEF | energy only / energy ×500 | 0.8 / −4.9 | — |
| 00t3 | + se_e3, rcut 4, neuron [2,4,8] | −0.6 | — |
| 00ta | se_atten_v2 (DPA-1), 43k steps | −1.1 | — |
| **00t3b** | **+ se_e3, rcut 4.5, rcut_smth 2.0, sel 80, neuron [16,32,64]** (93k steps, timed out) | **124.4** | **fcc 5.3, hcp 5.8** |

The three-body embedding of se_e3 depends on $\cos\theta_{jik}$ itself, not only on $\ell\le1$ moments. It sees the
ABC/ABAB stacking directly. The small [2,4,8] version was too narrow to use it. With 00t3b the remaining state-mean errors are
±2–7 meV/atom at P ≥ 100 GPa and −18/+16 at P = 0 (undertrained at 93k steps). Forces improve too: 0.15/0.18 eV/Å against
0.17/0.29 for 00t.

## 4. Fix

Model **00h** (job 7715007, P100, up to 36 h, restartable):
- the model 00 input with the 00t3b hybrid descriptor;
- energy weight 0.2 → 20;
- 600k steps;
- training data: all of model 00's data (126 systems), plus the 25 tw13/tw13slide systems (47 frames) that failed SCF before and have now converged.

At the end, `job.sh` runs dp test and `dp_state_errors.py`. Iteration 01 (`fe_dp_explore.py`) will use 00h.

Cost: se_e3 training runs at 0.075 s/batch against 0.0085 for se_e2_a (P100), 9× slower. MD speed with the compressed
model still has to be measured.

## 5. 00h interim check (250k of 600k steps, 2026-11-22 10:10)

The 250k checkpoint gives $E_{fcc}-E_{hcp}$ = 123.9 meV/atom (DFT 122.6). Errors on all of its training data
(`DP/00h/errors_250k_interim.txt`), rms of the state-mean errors in meV/atom, against model 00:

| group | 00h at 250k | 00 |
|---|---|---|
| a1_fcc | 6.6 | 21.9 |
| a1_hcp | 5.2 | 23.4 |
| def_vac / def_vacmig | 6.7 / 7.8 | 10.8 / 12.4 |
| def_s7 / def_s7slide | 4.2 / 4.4 | 6.9 / 10.6 |
| def_tw13 / def_tw13slide | 4.6 / 4.9 | (not in 00) |
| old / old_b | 3.0 / 2.2 | 4.6 / 2.9 |
| SIGMA < 0.07 eV | 4.7 | 27.6 |

Force rmse is 0.14–0.23 eV/Å, against 0.22–0.34 for model 00. At 300 K the hcp and fcc state-mean errors are −2 to
+9 meV/atom with no systematic sign split.

## 6. 00h final (600k steps, finished 2026-11-22 19:19)

Perfect cells at $V$ = 7.25 Å³/atom: $E_{fcc}-E_{hcp}$ = **124.5 meV/atom** (graph.pb and graph_c.pb; DFT 122.6; model 00 53.8).
On the training data (`DP/00h/offsets.txt`):
- rms state-mean error is 4.5 meV/atom at σ < 0.07 eV (00: 27.6);
- by group it is 1.7–7.1 meV/atom;
- the largest single state is +17.7 (fcc P100 T2800);
- force rmse is 0.198 eV/Å, which is 4.9 % of the rms force component.

The full tables are in `FE_DEEPMD_SUMMARY.md` §5.

MD speed on a P100 (compressed model) is 79–103 steps/s for 64–176 atoms, about 5× slower than model 00. Iteration 01 MD with 00h is job 7906537.
