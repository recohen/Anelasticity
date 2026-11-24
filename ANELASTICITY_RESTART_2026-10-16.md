# Anelasticity restart, 2026-10-16

Read first: `ANELASTICITY_RESTART_2026-10-15.md` (items 1–9: DFT comparisons, driven-rheology plan, literature, Fei/Cordier comparisons, builders, DengStates submission, r-RESPA). Then `INPROGRESS.md`, `ANELASTICITY_TODO.md` (T20–T24) and `ANELASTICITY_DONE.md`.

Main run root for the new work: `/groups/carnegie_poc/rcohen/LAMMPS/DengStates` (README there). Deng model `graph_c.pb` (md5 0e06a7e2), fparam = k_B T, types 1 Mg 2 Si 3 O.

## 1. RC decisions 10-15
- "go ahead with the Deng NPT lattices and GB jobs": done (item 2).
- OCTP: was already done on 10-09 (equivalent to GK, no gain); summary §7 open item now marked done.
- r-RESPA: "It doesn't sound worth it to me for a factor of 2-3. Possibly we could even run at a 5 fs time step as is!" Not pursued. A 1–5 fs time-step test was submitted instead (4620528). Background on the r-RESPA route is in the 10-15 restart, item 9.

## 2. Job status (checked 10-16)

| job | state | what | next |
|---|---|---|---|
| 4612142_1–10 | **COMPLETED** | NPT lattices, MgO and Bdg, 5 states (`lattice/*/lattice.txt`, `npt_end.data`) | table below; add to a results doc |
| 4612192_1–3 | **COMPLETED**, γ computed (preliminary) | Bdg [100] tilt boundaries at 30 GPa, static, 32 rigid shifts per plane (`BdgGB_P30/gb0kl/gamma.txt`) | γ is 2× van Driel's value (item 4) |
| 4612246_1–5 | PENDING (its dependency is now satisfied) | G-diff: MgO Σ5, 1 ns NVT per state | `tools/gb_diff.py MgO_S5_diff/P<P>_T<T>` |
| 4612253 | PENDING | MgO polycrystal, 26 k atoms, 8 grains, anneal 300 ps at 60/2300 | check P100 memory at start |
| 4620528_1–3 | PENDING | time-step test, 1–5 fs (MgO 30/2000, MgO 120/2800, Bdg 120/2800) | `tools/dt_test.py DengStates/dt_test/*`; choose the production dt |
| 4593708–11 | **COMPLETED** 10-15 (9.6 h each), **not analysed** | D1: MgO edge, 175 GPa / 3500 K, τ = 0.15–0.5 GPa, 150 ps (`LAMMPS/MgO/Dislocations/edge_P175_T3500_long/tau*`) | `disl_core_track.py tau<τ>`, `disl_velocity.py tau<τ> --plot`; v(τ), waiting times; summary + plan D1 |
| 4602367/8 | **COMPLETED** (14 h), **not analysed** | D1b: 262 Å line, τ = 0.25/0.35 GPa (`…/edge_P175_T3500_L262/tau*`) | `disl_core_track.py` → kink pairs in x_c(z,t); compare with D1 |
| 4520046 | still PENDING | PBE single points (is the MgO-only model PBE-trained?) | 10-15 restart, item 2 |

## 3. Deng-model lattices (NPT, 30 ps eq + 50 ps average)

| state (GPa/K) | MgO a (Å) | MgO V (Å³/atom) | Bdg a, b, c (Å) | Bdg V (Å³/atom) |
|---|---|---|---|---|
| 27 / 2200 | 4.1153 | 8.712 | 4.7415, 4.8781, 6.8208 | 7.888 |
| 30 / 2000 | 4.0893 | 8.548 | 4.7116, 4.8577, 6.7845 | 7.764 |
| 60 / 2300 | 3.9561 | 7.739 | 4.5697, 4.7497, 6.6053 | 7.168 |
| 90 / 2500 | 3.8594 | 7.186 | 4.4560, 4.6722, 6.4686 | 6.733 |
| 120 / 2800 | 3.7855 | 6.781 | 4.3634, 4.6129, 6.3620 | 6.403 |

- Static (0 K) Bdg at 30 GPa (3×3×2 box/relax, fparam 2000 K): a, b, c = 4.6095, 4.8048, 6.6716 Å; h = −5.911511 eV/atom.
- Not yet compared with Tange (MgO) or with a Bdg EOS.

## 4. Bdg boundary energies at 30 GPa (preliminary)
γ is the boundary enthalpy, Eq. 1 of `bdg_gb_energy.py`; the PΔV part is about 0.6 J/m².

| plane | min γ (J/m²) | best shift | dV/A (Å) | van Driel (25 GPa) |
|---|---|---|---|---|
| (021) | 3.40 | dx = a/2, dy = 6/8 P_y, dz = 0 | 0.196 | 1.41 |
| (013) | 3.36 | dx = a/2, dy = 0, dz = 0 | 0.263 | – |
| (011) | 2.36 | dx = a/2, dy = 3/8 or 5/8 P_y, dz = 0.5 | 0.198 | – |

- Our γ is about 2.4× van Driel's for (021). Even the energy alone, γ − PΔV/A ≈ 2.8 J/m², is 2×.
- Suspects, in order:
  1. Only one termination was scanned (zoff = 0); van Driel scanned terminations and stoichiometry-preserving removals.
  2. Static CG from rigid shifts traps high-energy structures. A short MD anneal plus quench (e.g. 1500 K, 20 ps) should be tried on the best 3–5 shifts per plane.
  3. The rcut = 1.4 Å deletion plus the stoichiometry fix may leave unfavourable boundary chemistry.
  4. The definition: enthalpy vs energy, and the pressure (25 vs 30 GPa).
- The γ spread across shifts is large (2.4–4.5 J/m²), consistent with item 2.
- Next: anneal+quench job, a zoff scan, and recompute γ with energy only for a like-for-like comparison.

## 5. New tools 10-15 (all in `/resnick/home/recohen/Claude/tools`)
- `build_bdg_bulk.py`: perfect Pbnm supercell.
- `npt_lattice.lammps`: extended with NA NB NC, BARO, FPARAM; backward compatible.
- `state_lattice_array.sh`: lattice array job.
- `gb_min.lammps`: two-pass box/relax CG.
- `bdg_gb_scan_job.sh`: resumable; skips finished tags.
- `bdg_gb_energy.py`: γ and dV/A.
- `gb_diff.lammps` and `gb_diff_job.sh`: retype + scale Σ5 → NPT → mean box → NVT with dumps.
- `gb_diff.py`: boundary-resolved D(s) and δD_b with grain sliding removed (step correction). Synthetic test: 2 % error; `--ramp` overestimates by 60 %.
- `poly_anneal.lammps` and `poly_anneal_job.sh`: polycrystal anneal.
- `dt_test.lammps`, `dt_test_job.sh` and `dt_test.py`: time-step test.

## 6. Priorities for the next session
1. Analyse D1 and D1b (finished, waiting).
2. Check the first outputs of G-diff, the polycrystal (memory) and the dt test when they start. Then analyse G-diff → δD_b(P,T) into the Cordier doc §4 and the Fei doc §3.
3. Bdg γ discrepancy (item 4): anneal/quench + zoff scan.
4. The PBE comparison when 4520046 runs.
5. Older: bridgmanite lowf sweeps 4446443/4 analysis; A0 follow-ups; summary §5i slope.
