# Anelasticity restart 2026-10-09

Read first:
- `ANELASTICITY_RESULTS_SUMMARY.md` — all results so far, Eqs. 1–13.
- `ANELASTICITY_METHODS.md` — methods, tools, pitfalls and porting.
- `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md`, `REQUIREMENTS.md`.

`ANELASTICITY_RESTART_2026-10-08.md` covers the V9.6397 set-up and the trajectories.

Paths:
- `M` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms`
- `R6` = `M/V6.6868/4096atom`
- `R9` = `M/V9.6397/4096atom`
- `G` = `M/GBslide`

Tools are in `/resnick/home/recohen/Claude/tools`. Python analysis uses `cohen_env`. Batch jobs that use ASE/DeePMD must call `$CONDA_PREFIX/bin/python` after `conda activate .../deepmd_py311`, because plain `python` resolves to an interpreter without deepmd.

## 0. What to check FIRST

| job | what | dir | action when done |
|---|---|---|---|
| 4283403_2 | GB sliding size test, V9.6397 3000 K, 4× area (15 680 atoms, 300 ps NVE) | `G/V9.6397_3000K_2x2` | analysis runs automatically (see below) |
| 4283403_3 | same, 9× area (35 280 atoms, 250 ps) | `G/V9.6397_3000K_3x3` | " |
| 4283403_4 | V6.6868 5000 K, 9× area (35 280 atoms, 200 ps): does the locked boundary slide when local mechanisms have room? | `G/V6.6868_5000K_3x3` | " |

Notes on the size test:
- All three tasks started 2026-10-09 at about 05:40, with a 24 h limit (TIMEOUT 86100).
- If a run times out, LAMMPS stops gracefully and still writes `end.data`. `slide.dat` keeps everything up to that point, so the analysis works on a partial run.
- **Analysis** (if the background waiter b1j51ayd1 is gone, run it by hand):

```
source /resnick/home/recohen/cohen_env/bin/activate
python tools/gb_slide.py $G/V9.6397_3000K $G/V9.6397_3000K_2x1 $G/V9.6397_3000K_2x2 $G/V9.6397_3000K_3x3 \
       $G/V6.6868_5000K $G/V6.6868_5000K_3x3 --out $G/size_analysis
```

- **Interpretation:** take β(x) against boundary area. If β is roughly constant, sliding is local and the friction transfers to grains, so the §5d grain model can be redone with confidence. If β grows strongly with area, sliding is collective and a disconnection NEB is needed (TODO T18).
- **Interim result, 2× area (task 1, done):** D_u = 0.059 ± 0.016 Å²/ps and β_x = 3.0×10⁶ Pa s/m, against 0.045 ± 0.057 and 8.0×10⁶ for 1×. β does **not** grow with area, which points to a local mechanism. Along y the boundary is still locked (β ≥ 10⁹–10¹⁰).

All other GPU jobs from the 10-07 and 10-08 restarts are finished and collected.

## 1. Done 10-08 / 10-09 (details in the results summary)

1. **Docs.**
   - `ANELASTICITY_RESULTS_SUMMARY.md` (new): §§1–7, figure index and open items.
   - Methods doc §1.7: crystal GK is not a viscosity; effective viscosity; Maxwell flow bound (Eq. 14); causality check (Eq. 15). OCTP and r-RESPA notes are in §4.
2. **Collect script changes** (`anelastic_collect.py`):
   - `fig_vs_T` panel (a) shows crystal flow-η₀ lower bounds instead of GK ∫G dt, and the pressure line is dashed.
   - New `fig_kk` and table §2a (causality check, crystals only).
   - Calls `plot_effective_viscosity.make()`, which writes `fig_effective_viscosity`.
   - The case-file key for the γ₀ = 0.03 bicrystal is `5000 bicrystal g3`.
   - Final V6.6868 and V9.6397 collects are in `results/` and `results_V9.6397/`.
3. **Fixes.**
   - `sweep_watch.sh`: a task counts as complete when its last `PRODUCTION_STEP N of M` has N ≥ M. Backup: `Downloads/sweep_watch.sh.bak_2026-10-08`.
   - V9.6397 4000 K liquid tasks that crystallized are marked `FAILED(...)` in `lockin_results.txt`: shear P20; uniaxial P0.2 and P100. Originals are in `lockin_results.txt.orig`.
   - Bicrystal P50 at both volumes: lock-in rerun by hand.
4. **OCTP.**
   - Built with CMake as a runtime plugin: `lammps-stable_22Jul2025_update2/build_octp_plugin/octpplugin.so`, wrapper in `tools/octp_plugin/`. Production LAMMPS is untouched.
   - Test against GK: identical results, zero overhead, no gain at long lags (`results/fig_octp_vs_gk`).
5. **T17, vacancies (summary §5a–c).**
   - **ASE–DeePMD** matches LAMMPS exactly (`ase_dp_check.py`).
   - **Hop statistics** (`defect_hops.lammps`, `vacancy_hops.py`, `DefectHops/`): the apparent activation energy is curved, falling from 3.6 to 2.1 eV for Mg.
   - **NEB** (`neb_vacancy.py`, `NEB/`): pair rotation 2.57 eV (Mg) and 3.09 eV (O); isolated jumps 3.77 / 4.65 eV; binding 3.25 eV. Harmonic TST reproduces the MD Mg rates within 1.5×.
   - **Elastic dipoles** (`defect_dipoles.py`): the bound pair is nearly isotropic, so its Zener loss is negligible (ΔC₁₁ = 0.12 GPa). The measured THz Schottky loss is dynamic, not orientational.
   - **Aged Schottky (5000 K):** the loss rises toward 20 GHz (Q = 3.7).
6. **T18, grain boundaries (summary §5d–e).**
   - **Equilibrium sliding** (`gb_slide.lammps`, `gb_slide_array.sh`, `gb_grains.py`, `gb_slide.py`):
     - At 140 GPa the boundary is locked.
     - At 18 GPa it slides perpendicular to the tilt axis (β ≈ 5×10⁶–5×10⁷ Pa s/m) and is locked along it.
   - **Grain model** (`gb_grain_model.py`, `fig_gb_Q_model`): provisional.
   - **Static γ-lines** (`gb_sliding_neb.py`, `GBslide/neb/`; `elastic_static.py` for C_ij):
     - Sliding is easy along x and hard along y.
     - At 140 GPa the boundary reconstructs in MD, with 3–4× the corrugation, which explains the locking.
     - At 18 GPa, MD sliding comes with shear-coupled migration.
   - **Bug, not yet fixed:** the automatic NEB end-point choice in `gb_sliding_neb.py` picks non-equivalent or downhill states. Use the γ-lines, not the NEB barriers.

## 2. Next steps

1. **Finish the size test (§0).**
   - **If β_x is independent of area:** redo the grain-scale model (`gb_grain_model.py`) with the β from the largest cell, and lengthen the runs or add replicas for the T dependence at V9.6397 (2000–3000 K).
   - **If the 140 GPa 9× cell slides:** high-pressure boundaries slide locally after all, so measure β there. Otherwise the locking stands, and the high-pressure β needs disconnection NEB.
2. **Disconnection or coupled-migration NEB.** Take the end states from an MD migration step (for example the V9.6397 3000 K run, where the boundaries moved about 10 Å), and fix the end-point selection in `gb_sliding_neb.py`.
3. **Boundary-resolved diffusion.** Compute the MSD of boundary atoms with the grain translation removed, to get δD_b for the Coble term. The present values are upper bounds.
4. **Dynamic vacancy loss** (option 1 from 10-08): T dependence of the excess Schottky loss. Arrhenius behaviour would point to jump transients; near-linear T dependence to phonon scattering.
5. **Open from before:** T6 (comparison with RC's earlier GK), T8 (relaxation spectrum fit).
