# Anelasticity restart 2026-10-10

Read first: `ANELASTICITY_RESULTS_SUMMARY.md` (§5f is new), `ANELASTICITY_METHODS.md`, `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md`, `REQUIREMENTS.md`. The 10-09 restart covers the size-test set-up.

Paths: `M` = `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms`, `G` = `M/GBslide`, `DR` = `G/drive`. Tools are in `/resnick/home/recohen/Claude/tools`.

## 0. What to check FIRST

| job | what | dir | action when done |
|---|---|---|---|
| 4336984_1–6 | driven MD in a 3×1 cell (L_x = 89 Å, 11 760 atoms): 5000 K at τ = 1, 1.5, 2 GPa; 4000 K at 1.5, 2, 2.5 GPa; 20 ps NVT + 100 ps | `DR/V6.6868_3x1_*` (task file `drivetasks_3x1.txt`) | `gb_event_neb.py scan DR/V6.6868_3x1_* --out DR/analysis_3x1` |

What to look for:
- **Is the step localized?** Is the onset traction below the 1× cell's (2 GPa at 5000 K, 3 GPa at 4000 K)? Is the boundary step localized in x (z_b(x) in the snapshots)?
- **If yes:** quench the frames (`MODE=quenchall`), then NEB one disconnection step (`neb`, end states a few ps apart). The barrier should not depend on area. Then TST β(T) at zero stress.
- **If no** (still a collective step): go to a longer L_x, or build a disconnection dipole explicitly.

**Result of the 1× NEB (summary §5g):** the barriers are 14–28 eV per collective step of the whole boundary (0.25–0.5 J/m²). That is consistent with the 2–3 GPa MD onset but cannot be transferred.

## 1. Done 10-10

1. **Size test (4283403) analysed** — summary §5f, `results/fig_gb_size`.
   - At V9.6397 3000 K, β_x = 2–10×10⁶ Pa s/m for 1×–9× area with no trend, so the mechanism is local.
   - At V6.6868 5000 K the 9× cell is locked.
   - Frequency caveat added: equilibrium β is a GHz-band (2–80 GHz) friction and is not converged in lag, so it is not the seismic β.
2. **Stress-driven GB motion at 140 GPa** (`tools/gb_drive.lammps`, `DR/gb_drive_array.sh`, `DR/drivetasks.txt`, job 4330883).
   - Setup: V6.6868 bicrystal from `G/V6.6868_5000K/end.data`, opposite x-forces on the grain interiors (traction τ per boundary, F = 2τA), 5 ps NVT + 100 ps driven, snapshot every 1 ps.
   - **No motion at τ ≤ 1 GPa** (4000 and 5000 K), nor at 2 GPa and 4000 K.
   - **At τ = 2 GPa (5000 K) and 3 GPa (4000, 5000 K): shear-coupled migration.** The grains translate u ≈ 7 Å while both boundaries move about 11–13 Å in the same direction. The coupling is about 0.6, close to the ⟨100⟩ Cahn–Taylor value 0.67.
   - The motion then stops, because the boundaries enter the forced interior groups (14 Å thick) and the force partly cancels. This is an artefact of the set-up.
   - Scan: `tools/gb_event_neb.py scan` → `DR/analysis/{gb_events.json,fig_gb_drive.*}`.
3. **Zero-stress quenches** (`gb_event_neb.py neb --quench-only`, `quenchall`).
   - The state after migration is equivalent to the start (ΔE = −0.4 / +0.3 eV over 449 Å² × 2).
   - The path goes through near-degenerate minima about 1.3–1.9 Å apart in u. At 4000 K, 3 GPa, frames 0–5 give u = 0.18, 1.51, 3.42, 5.10, 6.43, 6.96 Å.
   - Quenched energies scatter by ±2 eV through local disorder.
   - The u ≈ 2.7 Å plateau of the 5000 K / 3 GPa run is a side state at +10–14 eV, held by the traction.
   - Files: `DR/<run>/quench_I_J.{json,traj,log}`.
4. **Tools.**
   - New: `gb_drive.lammps` and `gb_event_neb.py` (modes scan, quenchall, neb), with `DR/gb_event_neb_job.sh` (`MODE`, `RUN`, `I`, `J`, `EXTRA`).
   - Known limitation: `nmov` in quenchall counts the rigid grain translation, so it is about N whenever u changes. Use the u column instead.

## 2. Next steps

1. Collect the NEB chain (§0), then decide on the x-elongated cell test.
2. Stress dependence of the MD rate: the onset is between 1 and 2 GPa at 5000 K and between 2 and 3 GPa at 4000 K. Combined with the NEB barrier, this gives an activation volume. To keep the force on the grains, use thicker forced groups or forces applied only far from both boundaries, with the groups updated as the boundaries move.
3. Longer equilibrium runs (ns) at V9.6397 to see whether D_u(t) converges (the low-frequency β).
4. Still open from 10-09: grain model with the transferable β, boundary-resolved δD_b, dynamic vacancy loss, T6, T8.
