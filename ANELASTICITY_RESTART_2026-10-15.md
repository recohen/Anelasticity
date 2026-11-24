# Anelasticity restart, 2026-10-15
Read first: `ANELASTICITY_RESTART_2026-10-13.md` (all decisions and paths up to 10-14), then `INPROGRESS.md`, `ANELASTICITY_TODO.md` (T20–T23) and `ANELASTICITY_DONE.md`.

## New since 10-13 restart
1. **DFT model comparison written up** (`results_dft/MGO_DFT_MODEL_COMPARISON.md`, summary §5l).
   - MgO-only model: +5 to +9 GPa relative to PBEsol at fixed V, and +7 to +13 GPa relative to the Tange EOS.
   - VIB: −1 / −10 GPa; its ΔG_f is 1–2.6 eV above DFT.
2. **PBE check of the MgO-only model** (RC: "Yes please compare mgo with pbe too"): VASP array 4520046 in `/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck/PBE` (README there). When it finishes:
   - `dft_compare.py --tag mgo --gf P20_T2000_perfect P20_T2000_bound --L 2 --temp 2000` and the P140 pair at 3000 K, run from `PBE/`;
   - also without `--tag` (Deng against PBE);
   - add a PBE column to the write-up and §5l, plus the PBE − PBEsol shift of ΔG_f;
   - if the MgO-only model matches PBE, relabel the MgO-only pressures.
3. **RC direction 10-15:** drive the system to find collective events; concentrate on dislocations and grain boundaries; boundary rheology → grain-size model.
   - Plan: `ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md` (Eqs. 1–4; steps D1–D7, G1–G6).
   - The 3×1 boundary NEB (4407041) showed a collective step, so G1 (an explicit disconnection dipole) is the way to transferable boundary kinetics.
4. **D1 running:** 4593708–4593711 (`LAMMPS/MgO/Dislocations/edge_P175_T3500_long`, README). Next: core-tracking tool for `disl.dump`, waiting times, v(τ).
5. **Still pending from before:** bridgmanite lowf sweeps 4446443/4 analysis; A0 follow-ups; summary §5i slope update.
6. **Literature (RC added papers 10-15):** `LITERATURE_NOTES_2026-10-15.md`. Key points:
   - van Driel's Σ5 structures C/D and barriers match our "slides at 20 GPa, locked at 140 GPa", but their coupling mode (1.0) differs from ours (0.6).
   - Cordier 2012's kink-pair width (150–200 Å) means the D1 lines are too short for kink pairs, hence D1b.
   - Clean-boundary sliding is far too fast for seismic loss; blocking and accommodation (triple junctions, boundary diffusion) matter, so G4 is central.
   - Fei 2023 grain sizes: 0.3–5 mm.
   - Plan §5 lists the revisions.
7. **RC 10-15:** "Yes" to bridgmanite boundaries from van Driel's [100] tilts ((021) first) and to the long runs (D1b submitted; G4 polycrystal to build).
   - Detailed comparisons written: `results_cordier2023/CORDIER2023_COMPARISON.md` (the paper RC meant) and `results_fei2023/FEI2023_COMPARISON.md`.
   - Top new item: G-diff (boundary O diffusion in MgO at 30–120 GPa). It could reverse Cordier's conclusion.
8. **Builders ready, not yet run:** `build_mgo_polycrystal.py` and `build_bdg_tilt_gb.py` (DONE 10-15). Next jobs, all with the Deng model:
   - (a) NPT lattice of Bdg and MgO at the Cordier states (30/2000, 60/2300, 90/2500, 120/2800);
   - (b) Bdg (021) shift scan + minimise at 30 GPa → lowest γ_gb, compared with van Driel 1.41 J/m² at 25 GPa;
   - (c) anneal MgO polycrystals and the Σ5 bicrystal;
   - (d) G-diff runs (boundary-resolved MSD; analysis tool still to write).
9. **Submitted 10-15 (RC: "go ahead with the Deng NPT lattices and GB jobs"):** 4612142 (lattices), 4612192 (Bdg GB scan, 30 GPa), 4612246 (G-diff Σ5, 5 states), 4612253 (polycrystal anneal 60/2300). Record: `/groups/carnegie_poc/rcohen/LAMMPS/DengStates/README.md`. Analysis tools ready: `bdg_gb_energy.py`, `gb_diff.py`.
   - r-RESPA: RC 10-15 "not worth it for a factor of 2-3"; time-step test 1–5 fs submitted (4620528) instead. Background: `pair deepmd` has respa_enable = 0, so inner/middle/outer is refused, but `run_style respa N n hybrid ...` with `pair_style hybrid/overlay` (or hybrid/scaled) assigns whole sub-styles to levels and does not check respa_enable (LAMMPS src/respa.cpp). Route without C++ changes: cheap short-range potential F_s on the inner level, DeePMD − F_s (hybrid/scaled with −1 × F_s) on the outer level. Expected gain only ≈ 2–3× (MgO optical modes limit the outer step). Not yet tested.
