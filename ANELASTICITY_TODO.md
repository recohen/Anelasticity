# Anelasticity TODO

- **T10: Green–Kubo at 8000 K and 7000 K** (4146463, 4146464; `4096atom/{8000K,7000K}/GK`, ~17 h each). Analyse with `gk_viscosity.py pres.dat`: $\eta_0$, $\zeta_0$, $G(t)$, $G^*(\omega)$, $M''(\omega)$. Compare with the sweep (shear: $\eta'$ at 10 GHz–5 THz; uniaxial: adiabatic GK vs thermostatted sweep). Check NVE drift and the 7000 K MSD (still liquid?).
- **T11: 7000 K sweeps running** (4147084 shear, 4147085 uniaxial with the new τ_T rule, restart 10-07 §5).
- **T12: 8000 K uniaxial rerun running** (4147331, `8000K/FreqSweep_x2`, same τ_T/ε₀ table as 7000 K; each task starts from its old `FreqSweep_x/P*/eq.data`).
- **T6: compare with RC's Green–Kubo $G(t)$.** Ask RC where the earlier GK runs live.
- **T7: cooling sequence** at constant volume (7000 K is the first step). Lower $\gamma_{max}$ in the supercooled liquid.
- **T8: fit relaxation spectrum $H(\tau)$** (plan Eq. 4) to $G^*(\omega)$, now also from GK.
- **T9: optional fix of the user's notebooks**, only if RC asks.
- Collect/plot: tools/anelastic_collect.py -> results/ (T13, RC request 10-07). Rerun when all jobs finish.
- **T14: cooling sequence**: 6000 K liquid (GK + sweeps running); 5000 K and 4000 K crystallized → GK + reduced solid sweeps + perfect-B1 GK reference running (restart 10-07 §7, §7a).
- **T15 (10-08): V = 9.6397 Å³/atom series** (restart 10-08 §3): GK 6000, 4000, 3000 (melt-grown), 3000 perfect/Schottky/bicrystal running; sweeps auto-launch. Manual: confirm 3000 K crystallized → launch `3000K/FreqSweep_solid` and `2000K/GK` (from `3000K/GK/eq.data`, NEQ 100 ps) → `2000K/FreqSweep_solid`. Then `anelastic_collect.py --cases tools/anelastic_cases_MgO_V9.6397.py`; compare with V6.6868 (fig vs p).
- **T16 (10-08): trajectories** `R6/Trajectories` (4233485) — check, tell RC how to view (methods doc §5).
- Final V6.6868 collect when 4163822, 4230008, 4233462 finish (default case file).
- **T17 (10-08, RC interest): defect relaxation from rates, not trajectories.** Goal: put the defect loss peak at any frequency, without assuming a single activation energy (the Karato form $Q^{-1}\propto(\omega\tau_0e^{E^*/RT})^{-\alpha}$). Steps:
  1. **Done 10-08:** hop statistics from MD (summary §5a). The rates curve: Mg $E_a$ 3.6 → 2.1 eV and O 4.6 → 2.1 eV from 3500 to 5000 K. ASE–DeePMD validated against LAMMPS (`ase_dp_check.py`).
     Original plan: **Hop statistics from MD.** Run short dumps of the Schottky cell at several T, at fixed V. Locate vacancies by Wigner–Seitz analysis and classify the events (single Mg or O hops, pair reorientation, cluster moves). Get rates $k_i(T)$ and test whether each is Arrhenius.
  2. **Done 10-08:** NEB (summary §5b). Pair rotation 2.57 eV (Mg) and 3.09 eV (O); isolated jumps 3.77 / 4.65 eV; pair binding 3.25 eV. TST pair rotation matches the MD Mg rates within 1.5×; O is 2–3× faster than predicted (another mechanism).
     Original plan: **NEB with DeePMD.** Use a small cell at the same V to get the elementary barriers and their distribution, plus harmonic-TST prefactors.
  3. **Done 10-08:** elastic dipoles (summary §5c). The bound pair is nearly isotropic, ΔG = −1.39 eV, so its Zener ΔC₁₁ is 0.12 GPa at 5000 K, about 100× below the measured Schottky THz loss; that loss is dynamic, not orientational. Selection rules confirmed. Bound-pair formation energy 2.44 eV at fixed V.
     Next: test the dynamic-loss mechanism (T dependence of the excess loss; strain-modulated saddle occupation). Then decide whether a kMC is still worth doing (Zener is negligible), and move to grain boundaries and dislocations.
     Original plan: **Elastic dipole tensors.** Get them from relaxed defect cells. They give the relaxation strengths $\Delta_i$ and the channel selection rules: a tetragonal ⟨100⟩ defect in a cubic crystal relaxes only $(C_{11}-C_{12})/2$, not $C_{44}$. The measured C₄₄ (xz) Schottky loss at 5000 K therefore points to another mechanism.
  4. **Assemble** $Q^{-1}(\omega,T)=\sum_i\Delta_i\,\omega\tau_i/(1+\omega^2\tau_i^2)$ with $\tau_i(T)$ from steps 1–2. Test time–temperature superposition against direct MD sweeps at 2–3 temperatures where they overlap, then extrapolate to seismic frequencies.
- **T18 (10-08, RC chose): grain-boundary sliding from rates** (Σ5 bicrystal at both volumes).
  1. **Done 10-08 (job 4264732; summary §5d).** At V6.6868 the boundaries are locked (β ≥ 3–20×10⁹ Pa s/m). At V9.6397 they slide perpendicular to the tilt axis (β ≈ 5×10⁶–5×10⁷ Pa s/m) and are locked along it. Still needed: longer runs or replicas for the T dependence, and a boundary-resolved MSD with grain motion removed.
     Original plan: **Equilibrium sliding friction.**
     - Runs: 20 ps NVT + 300 ps NVE; V6.6868 at 4000/4500/5000 K, V9.6397 at 2000/2500/3000 K.
     - Measure the relative displacement u of the two grain interiors. Then $D_u=k_BT/(2\beta A)$ gives the linear (small-amplitude) friction β(T) directly, and its Arrhenius behaviour tests the single-E question.
     - Analysis: `tools/gb_slide.py`.
     - Compare with the sweeps: at V9.6397 3000 K, γ₀ = 0.03 gives β ≈ 2.3×10⁶ Pa s/m, but that run was nonlinear; at V6.6868 the boundaries are locked at γ₀ = 0.01.
  2. **Done 10-09, partly (summary §5e).** γ-lines: easy along x, hard along y. At 140 GPa the boundary reconstructs in MD and its corrugation grows 3–4×, which explains the locking. At 18 GPa, MD sliding goes by shear-coupled migration. The cell β is area-dependent, so it is not transferable.
     Size test done 10-10 (summary §5f): β_x is area-independent at V9.6397; V6.6868 9× still locked. Next: a disconnection NEB with MD-derived end states. Fix the automatic NEB end-point choice in `gb_sliding_neb.py`.
     3×1 test done 10-11 (summary §5h): still a collective step, with no localized disconnection.
     3×1 NEB, first try 10-12 (job 4359736): stage 1 gives ≈ 29.5 eV = 0.175 J/m², 1.0–1.8× the 1× barrier rather than 3×, a hint of partial localization. The climbing stage diverged. Rerun with a guarded climbing stage and a saddle-localization check: job 4407041. Next: if the saddle is localized, build an explicit disconnection dipole.
     Original plan: **Static sliding landscape.** Compute the γ-line or γ-surface of the boundary (energy against rigid in-plane translation, with relaxation) using ASE and DeePMD. Then run NEB of the sliding (or shear-coupled migration) step at both volumes: barrier and strain coupling.
  3. **Done (first pass), summary §5d:** `gb_grain_model.py`. V9.6397: relaxed at seismic frequencies. V6.6868: only an upper bound on the peak frequency, so step 2 (NEB) is required.
     Original plan: **Grain-scale model.** Combine β(T, p) with grain size d using elastically accommodated sliding (Raj–Ashby / Zener): $\tau\sim\beta d/G$ with relaxation strength from the grain geometry. That gives $Q^{-1}(\omega,T,p,d)$ at seismic frequencies. Check against the direct sweeps where they overlap.
- **T19 (10-11, RC request): repeat the MgO program for MgSiO3** (Deng's finite-T DeePMD model, `LAMMPS/MgSiO3`).
  - Done: test sweep at 1 THz (restart 10-11 §3).
  - RC 10-11: start from the liquid and cool, and from the crystal and heat, at the same V. Ladders are done; GK and sweeps are submitted (restart 10-11 §4).
  - **Done 10-12:** all 16 GK runs and sweeps collected (`results_MgSiO3_V6.5669/`, summary §5i). Liquid η₀ is 7.5 / 12.8 / 23 / 220 mPa s at 7000–4000 K, with no crystallization. Bridgmanite stays crystalline to 5000 K and has a 5 THz internal-strain resonance.
  - Running: 4000 K shear linearity test (job 4406967, γ₀ = 0.05/0.1).
  - **RC 10-12:**
    - Stay at this volume and compare with MgO (no second volume for now).
    - First defect: the Mg–O vacancy pair (Schottky-type V_Mg + V_O) in bridgmanite, by analogy with MgO's Schottky cell.
    - RC will look into the grain-boundary literature (Pbnm as a distorted perovskite); wait for that before building boundaries.
  - **T dependence (RC 10-12: single E, or T-independent?).** First pass in summary §5j. Proposed to complete it:
    1. **In progress:** V_Mg + V_O bridgmanite at 3000 K (aging 4407370) as well as 4000 and 5000 K (sweeps, plus hop rates from the GK MSD), to give the T dependence of the defect relaxation.
    2. **Submitted 10-12 (RC approved):** perfect-B1 MgO sweeps at V6.6868 at 4000 and 3000 K (ladder 4407426, sweeps 4407427 and 4407428; `B1perfect_Ladder/README.md`), to separate phonon Q⁻¹ ∝ T from defect loss in MgO.
    3. Optional: more MgO liquid temperatures (7500 and 6500 K) to test the 2.3σ curvature. About 17 P100-h each.
  - V_Mg + V_O cells built (`tools/build_vacancy_pairs.py`) and aging (4407170, 4407171). Next: GK and solid sweeps at 4000 and 5000 K next to the perfect crystal, as in MgO §3.

- **T20 (10-13, RC request): vacancy formation and migration free energies, then D(P,T), for MgO and bridgmanite** (Ita & Cohen 1997/1998 method, with nonequilibrium `fix ti/spring` and PLUMED umbrella sampling). Test of Cordier et al. 2023 (periclase slower than bridgmanite). Plan: `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` §1–2, phases A0–A3. Decisions pending (plan §5).
- **T21 (10-13, RC request): dislocations in MgO** (½⟨110⟩{100}): drag B at 175 GPa / 3500 K and $\eta_{eff}=B/\rho b^2$ against Perez et al. 2025 (η ≤ 10² Pa s); Granato–Lücke string damping for anelasticity. Plan §3a, phase B1.
- **T22 (10-13, RC request): bridgmanite slip systems [100](010) and [010](100)**: CRSS against T at 25 GPa, testing the change at about 1800 K (Guan et al. 2026). Plan §3b, phase B2. Needs RC approval for 25 GPa (off V6.5669).

- **T23 (10-15, RC direction): dislocation and grain-boundary rheology by driving, down to seismic frequencies.** Plan: `ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md`.
  - RC: "driving the system with strains would help overcome the need to find the collective motions by random chance. I would concentrate on dislocations and grain boundaries. If we know the grain boundary rheology we can model effects of grain size."
  - Approach: driven MD finds the mechanisms, NEB/PLUMED anchors ΔG(τ) at low τ, and a Kocks–Argon–Ashby rate law gives the linear mobility. That feeds a Granato–Lücke line model and a grain-size model (Eq. 4 there).
  - D1 submitted (4593708–11). Next: the G1 disconnection-dipole builder for Σ5. Check with RC before the large items G4 and D7 (≈ 150 P100-h each).
- **T24 (10-15, RC: compare in detail with Cordier 2023, MgO vs MgSiO3).** Write-up: `results_cordier2023/CORDIER2023_COMPARISON.md` §4, in priority order:
  1. G-diff: boundary-resolved δD_b(Mg, O) in MgO Σ5 at Cordier's 4 geotherm states (Deng model), then Bdg (021)/(013).
  2. A1/A2 at the same states.
  3. A3 (Bdg intrinsic).
  4. D2 / D1b (drag B(T), T_a).
  5. Redo Cordier Fig. 2b with our numbers.
  - Also `results_fei2023/` for the grain-size side.

- **RC1 (RC 2026-11-15, written into the stale copy `Claude/Resnick/Anelasticity/ANELASTICITY_TODO.md`; copied here): trajectories for animations.** "We need animations for a talk so we need short trajectories that illustrate that process and what is happening--these can be suitable for reading using vmd, so lammps trajectory files. We do not need for every run--just a few representative samples."
  - **Done 11-15:** six movies in `/groups/carnegie_poc/rcohen/LAMMPS/TalkTrajectories` (README; `vmd -e movie.vmd` in each): edge-dislocation glide, Σ5 boundary migration/stick–slip, vacancy hops (2), liquid shear, liquid crystallizing under shear. Tools `traj_for_vmd.py`, `vmd_movie.tcl`. Tested in VMD 1.9.4 (text mode).
  - Optional: a bridgmanite vacancy-hop movie (needs a ≈ 1 P100-h run).
- **T25 (RC question 11-15): lower frequencies by kMC, or effective activation energies?** Answer and proposals: restart 11-15 §4. RC approved 11-15: Σ5 T series at 60 GPa (6929623_1–3, `DengStates/MgO_S5_P60_Tseries`) and MgO Schottky 20 GHz at 4000/4500 K (6929639, 6929640, `V6.6868/4096atom/<T>K/FreqSweep_Schottky_aged`) submitted. Schottky cell-size test submitted 11-15 (6929874, `5000K/FreqSweep_Schottky_L6`).
- **T23 update 11-15:** D1/D1b analysed (B = 1.76e-4 Pa s, no threshold; drive bug fixed). Next proposed: B(T) at 2000 and 5000 K.
- **T24 update 11-15:** G-diff MgO Σ5 done (frozen except 60/2300). Next: polycrystal G-diff; Bdg (021)/(013) G-diff after the γ issue.
- **T26 (RC 11-15): diffusivity for liquids and solids; RC hypothesis "η and D scale with O motion; D_O depends on O density".** First test from existing GK data: `results_Tdep/LIQUID_SE_ODENSITY.md` (tool `liquid_se.py`). SE holds (r_SE 0.86–1.0 Å) for all hot melts but O is not singled out (D_Mg ≈ D_O); breaks down in supercooled MgSiO₃ (4035 K). D_O is not a single function of n_O (MgSiO₃ denser in O but faster). Proposed: matched-n_O Deng runs (≈ 15–25 P100-h); solids via Ita & Cohen TI = plan A1–A3. Waiting for RC.
- **11-15 RC: "start A1/A2" and "Yes please do" (matched-pressure liquids).** Submitted: A1 6930969 + 6930970 (`FreeEnergy/A1_MgO_Deng`, new fixed-V formation route), A2 6931057 (`FreeEnergy/A2_MgO_Deng_mig`, new umbrella-integration tool), liquids 6931065 (`LiquidPT_Deng`). Next after them: DFT snapshot corrections per state; Deng MD hop rates for A2 validation; A3 bridgmanite.
- **11-16:** A1/A2, liquids, Schottky, Σ5 analysed (restart 11-16 §2). A3 running (RC 11-16: "Go ahead with A3 for bridgmanite too"; `FreeEnergy/A3_Bdg_Deng`). Then (RC "Yes do 1 2 3 4 5") submitted: DFT check of the separated MgO pair (decides D_O vs Cordier); Schottky 20 GHz reruns; Σ5 unlocking T at 90/120 GPa; MgO TST vs direct hops; Rosenfeld scaling (INPROGRESS §1b).
- **11-16:** A3 analysed: O vacancy fast (0.9–1.9 eV), V_Mg slow (4.7–6.0 eV); bridgmanite formation energies need a hop-proof method (proposal INPROGRESS §3, ≈ 60 P100-h). MgO TST confirmed (κ ≈ 1). Σ5 locked at 90/120 GPa up to 3400/3800 K.
- **11-17:** A3b done (bridgmanite Schottky energies, V_Mg migration, intrinsic D; summary §5p). Open: Si vacancy path, ladder-vs-direct closure, DFT corrections for bridgmanite (INPROGRESS §3).
- **11-17 (RC "Yes do a and b … put c as optional in the TODO list"):**
  - A3b follow-ups (a) Si path search (NEB + V_Si MD) and (b) TS 80 check: submitted.
  - Schottky reruns analysed: nanovoids.
  - **Optional (c):** DFT correction of the bridgmanite vacancy formation energies. Use DeePMD NVT snapshots of the single-vacancy cells (V_Mg, V_Si, V_O2) and the perfect cell at 1–2 states, VASP single points with the Deng training settings, and FEP as for MgO (`VASP/MgO_vacancy_DFTcheck`, `tools/dft_compare.py`). ≈ 4 cells × 8 frames × 2 states of 960 atoms; ≈ 10–20 min per frame on 64 cores, so ≈ 1000–2000 core-h. Also consider the bridgmanite separated-defect long-range question (as MgO item 1).

  - **hcp Fe (RC 11-17):** pick production route after CPU check 7058477 and H200 test 7058548; propose on-the-fly hcp training (VASP 6.6.1; hcp cells 300–350 GPa, 4000–7000 K, + liquid/bcc), refit, validate, then the anelastic protocol (restart 11-17 §7.3). Rebuild the GPU plugin from 6.6.1.
- **11-18 (RC: "plan a set of runs for solid Fe at core conditions … Q and the effective viscosity"):** plan in `ANELASTICITY_PLAN_FE.md`; waiting for RC on its §8 decisions; A0 first.
- **11-18:** Fe A0 running (A0b Γ-only 7190356, AIMD timing 7183764_31); next: settings + A1 cost to RC; OUTCAR→ML_AB converter; scans 7166452/7166454. Restart `ANELASTICITY_RESTART_2026-11-18.md`.
- **11-19 (RC "Continue training Fe vasp ML potential"):** scans analysed (CPU 64×1 = 9.13 steps/s; H200 ≤ 1.10 → CPU for production; `tools/vasp_lammps/README.md`). A1 smoke on-the-fly run 7273834 (`VASP/Fe/hcp_fcc/ML/A1`, README). New tools `fe_a1_setup.py` (smoke, ramps), `vasp_mlab.py` (ML_AB info/append/check; round trip tested on 913 + 2 A0 points). A0b 7190356 and k2 MD 7183764 still PENDING (est. start 11-19 05:00 and 09:00).
- **11-19 07:20:** A0b analysed (`results_Fe/A0b_summary.txt`): Γ-only not converged in 64-atom cells (k2 needed or a cheaper shifted mesh to test), ENCUT 700, SIGMA = k_BT (old 0.2588 off by 0.1–0.2 eV/Å and 3–9 GPa). ML_AB stores TOTEN. Smoke OOM at 3 GB/task → 8 GB. Waiting for RC: k-mesh, T bands vs DeePMD fparam, old ML_AB recompute/drop.
- 11-19 13:30, Fe R1 (RC "Go ahead and stage the first recalculation batch and submit"): 100 old ML_AB configs recomputing (7286822; ~55 s per SCF step on 64 ranks for 128 atoms at 300 K → ≈ 0.5–1 h each); 40 A1 constant-T sampling runs (7286841). Next: mldp post-processing per band, first DeePMD fit (fparam = k_BT) on R1 old + R1b hcp/fcc frames.
- 11-19 16:00: restart written (`ANELASTICITY_RESTART_2026-11-19.md`); R1 pending tasks held for speed test 7302962.
- 2026-11-19 21:00: restart §10. R1 7286822: 26 tasks TIMEOUT at 10–20× s/SCF (mpirun placement on scattered grants); switch R1/A1 scripts to srun --mpi=pmi2; resubmit timed-out + held tasks; speed test 7315550 (debug, too large per RC: keep debug jobs small).
- 2026-11-22 16:15: restart `ANELASTICITY_RESTART_2026-11-22.md`. Fe DP energy errors solved by se_e2_a + se_e3 (00h finishing). Quadrupolar edge dipoles stable; M1 GK, M1q and B1q sweeps finished, lock-in only (results_dislocations/M1_edge001_4000K.md §7); M1q 1 ps G″ < 0 open.
- 2026-11-23: Fe 00h finished and summarized (results_Fe/FE_DEEPMD_SUMMARY.md); iteration 01 MD 7906537 submitted; remap-x reruns lock-in in results_dislocations/M1_edge001_4000K.md §9.
