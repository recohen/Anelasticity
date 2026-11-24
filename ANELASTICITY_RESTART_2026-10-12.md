# Anelasticity restart 2026-10-12

Read first: `INPROGRESS.md` (running jobs and what to do when each finishes), `ANELASTICITY_RESULTS_SUMMARY.md` (§5h for the MgO 3×1 NEB, §5i for MgSiO₃ against MgO), `ANELASTICITY_METHODS.md`, `ANELASTICITY_TODO.md` (T18, T19), `ANELASTICITY_DONE.md`, `REQUIREMENTS.md`. Earlier detail is in the 10-11 restart.

Paths:
- `DR` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/GBslide/drive`
- `V` = `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3/1280atoms/V6.5669`
- Tools: `/resnick/home/recohen/Claude/tools`

## 0. RC decisions (10-12)

1. Rerun the MgO 3×1 NEB with the fixes (one more P100-day): yes.
2. MgSiO₃ defects: start with the Mg–O vacancy pair (V_Mg + V_O). RC will look into the grain-boundary literature (Pbnm as a distorted perovskite) before boundaries are built.
3. Stay at V = 6.5669 Å³/atom. The goal is to compare MgSiO₃ with MgO.

## 1. Done 10-12

1. **MgSiO₃ program complete at V6.5669** (summary §5i, `results_MgSiO3_V6.5669/`).
   - Liquid (cooled), 7000–4000 K:
     - no crystallization;
     - η₀ (GK) = 7.5, 12.8, 23.2, 220 mPa s;
     - ζ₀/η₀ ≈ 0.24;
     - sweeps agree with GK at ≥ 5000 K.
   - Bridgmanite (heated), 2000–5000 K: stays crystalline.
   - Q against MgO:
     - perfect-crystal Q at 1 THz, 5000 K: shear 63 (MgO C₄₄ > 120), uniaxial 63 (MgO 27);
     - both exceed melt-grown MgO (shear 19, uniaxial 49).
   - Bridgmanite shows a 5 THz internal-strain resonance (summary Eq. 14), so crystal Q comparisons use ≤ 1 THz.
2. **4000 K liquid shear at 10 and 50 GHz is nonlinear** (γ₀ = 0.5 and 0.32 from the Eq. 10 rule; |σ₃/σ₁| ≈ 0.1; η′ is half the GK value). Linearity test 4406967 is running. Methods §1.4 now states the supercooled-liquid rule $\dot\gamma_0\tau_\alpha\ll1$.
3. **Collector extensions:** `GKTC`, `XTAL`, `SOLID_SPAN`/`SOLID_LABEL` (methods tool table), plus a table bug fix.
4. **MgO 3×1 NEB, first try (4359736).**
   - Stage 1 gives ≈ 29.5 eV (0.175 J/m²), 1.0–1.8× the 1× barrier rather than 3×.
   - The climbing stage diverged (maxstep 0.2 Å). The files are archived in `DR/V6.6868_3x1_5000K_tau2/neb_try1/`.
   - The tool is hardened; the rerun is 4407041.

## 2. Next steps

1. **MgO 3×1 NEB rerun (4407041).**
   - Read the stage-1 line and the climbing-stage result in `DR/slurm-4407041.out`, plus the `saddle image … share of |dr|^2 per x-slab` line.
   - If it times out, restart from `neb_10_12_ci.traj` with `EXTRA="--from-band V6.6868_3x1_5000K_tau2/neb_10_12_ci.traj"`.
   - The climbing stage needs the stage-1 band as its start. `--from-band` skips stage 1 and goes straight to the climbing stage.
2. **MgSiO₃ 4000 K linearity test (4406967).**
   - Run `sweep_watch.sh V/liquid/4000K/FreqSweep_lin:4406967:shear`, then re-run `anelastic_collect.py --cases tools/anelastic_cases_MgSiO3_V6.5669.py`.
   - Expect η′(50 GHz) ≈ 110 and η′(10 GHz) ≈ 220 mPa s if the cause is nonlinearity.
   - If confirmed, replace the 4000 K sweep slope in summary §5i.
3. **MgSiO₃ V_Mg + V_O cell: built 10-12** with the new `tools/build_vacancy_pairs.py`: 6 pairs, 1268 atoms in `V/crystal_VMgO/build/`, with the same sites at 4000 and 5000 K. Aging is done at 4000 and 5000 K (stable; vacancies hop), and production is submitted (GK 4407925/4407927, sweeps 4407926/4407928). 3000 K aging is done too; production GK 4408168 and sweep 4408169. Full record: `V/crystal_VMgO/README.md`.
   - Pairs: Mg plus its nearest O (1.69–1.92 Å), chosen in the 2000 K state; charge-neutral (Mg²⁺ + O²⁻); pair centres ≥ 6 Å apart. Density matches the MgO Schottky cell (20 pairs per 4096 atoms).
   - After aging: GK and solid sweeps at 4000 and 5000 K, compared with the perfect crystal (MgO §3, `FreqSweep_Schottky`).
   - Also consider static vacancy barriers (NEB, as §5b) for Mg and O in bridgmanite.
4. **Grain boundaries in bridgmanite:** wait for RC's literature check.
5. **T dependence (RC question 10-12: single activation energy, or T-independent?).** First answer in summary §5j (`tools/T_dependence.py`, `results_Tdep/`). The liquids are super-Arrhenius; crystal THz loss is not activated (Q⁻¹ ∝ T). Runs to finish it:
   - MgSiO₃ V_Mg + V_O at 3000 K was added (aging job 4407370; same sites), so the vacancy series covers 3000–5000 K.
   - RC approved **MgO perfect-B1 sweeps at 4000 and 3000 K** (V6.6868): ladder 4407426, then sweeps 4407427 and 4407428. Record in `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom/B1perfect_Ladder/README.md`.
