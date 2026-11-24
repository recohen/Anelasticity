# Edge-dislocation drag in MgO at 175 GPa and 3500 K, and the Perez et al. (2025) viscosity bound

*2026-10-13. Run: `/groups/carnegie_poc/rcohen/LAMMPS/MgO/Dislocations/edge_P175_T3500` (job 4452807; README there).
Plan: `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` §3a. Figure: `edge_velocity.pdf/png` (this directory).*

**Update 2026-11-15 (§8):** the velocities in §3 are about 21 % low (the top block was not rigid), and the long-line runs D1/D1b show linear viscous glide down to 0.15 GPa with no threshold. Corrected **B = 1.76 × 10⁻⁴ Pa s**. Read §8 before using §3–5.

## 1. Question

Perez et al. (PRB 111, 144108, 2025) used the laser-driven Richtmyer–Meshkov instability in single-crystal MgO. They found an effective viscosity of at most about $10^2$ Pa s at 175 ± 15 GPa, about 3500 K and $\dot\varepsilon = 10^6$–$10^7$ s⁻¹.
- Their hydrocode fits are best for 0–100 Pa s. 1000 Pa s fits only the ripple growth, and higher values fail.
- The implied flow stress, $\eta\dot\varepsilon$, is at most about 1 GPa. Extrapolated static yield strengths at 175 GPa are 7.5–15 GPa (Meade & Jeanloz, as quoted by Perez).

**Can glide of ½⟨110⟩{001} dislocations, limited only by drag, give a viscosity this low?** We computed the drag coefficient $B$ directly with DeePMD MD at Perez's conditions.

## 2. Method

**Model:** the MgO-only DeePMD model (`graph_c.pb`, md5 6357206b). It was used for all our V6.6868 MgO anelasticity runs at 140–193 GPa. The Deng MgSiO₃ model is trained only to 160 GPa.

**Lattice:** NPT on a 4×4×4 B1 cell (`tools/npt_lattice.lammps`) gives a = 3.7044 Å at 175.0 GPa and 3500 K, so $b = a/\sqrt2$ = 2.6194 Å.

**Geometry** (`tools/build_mgo_edge_slab.py`; Osetsky & Bacon two-block method):
- One ½[110](001) edge dislocation, the high-pressure slip system above about 50 GPa (Amodeo et al. 2012).
- Axes: x = [110] (b, glide direction), y = [001] (glide-plane normal), z = [1-10] (line).
- The lower half has 25 repeats along x and the upper half 24, both strained to $L_x = 24.5\,b$ = 64.18 Å.
- Cell: 24 × 14 × 6, 8232 atoms. Periodic in x and z, free in y. One-repeat rigid blocks at top and bottom.

**Loading** (`tools/disl_drive.lammps`):
- Minimize, then 10 ps at 3500 K (Nosé–Hoover on the mobile region).
- The top block carries a piston force $-P\,A$ along y, with $A = L_xL_z$.
- At each step τ = 0.1, 0.25, 0.5 and 1.0 GPa, a force $\tau A$ along x is applied for 30 ps.

**Velocity:** each time the dislocation sweeps $L_x$, the top block advances by $b$. So the dislocation velocity follows from the slope of the top-block displacement $\Delta x_{top}(t)$:

$$v=\frac{L_x}{b}\,\frac{d\,\Delta x_{top}}{dt} \tag{1}$$

The slope is fitted after discarding the first third of each stress segment. Its error is the larger of the fit error and the scatter over three sub-blocks.

**Drag:** in the viscous (phonon-drag) regime,

$$v=\frac{b\,\tau}{B}. \tag{2}$$

**Effective viscosity:** with Orowan's relation $\dot\gamma=\rho b v$ for mobile dislocation density $\rho$, a drag-controlled crystal is Newtonian with

$$\eta_{eff}=\frac{\tau}{\dot\gamma}=\frac{B}{\rho\,b^2}, \tag{3}$$

and the flow stress at strain rate $\dot\gamma$ is

$$\tau_f=\eta_{eff}\,\dot\gamma=\frac{B\,\dot\gamma}{\rho\,b^2}. \tag{4}$$

Analysis: `tools/disl_velocity.py <dir> --plot`.

## 3. Results

![edge velocity](edge_velocity.png)

*Left: top-block displacement through the stress steps. Right: dislocation velocity against applied shear stress. The dashed line is Eq. 2 with B fitted to τ = 0.5 and 1 GPa.*

| τ (GPa) | v (m/s) | B (Pa s) | ⟨T_mobile⟩ (K) | ⟨σ_xy⟩ in the mobile region (GPa) |
|---|---|---|---|---|
| 0.10 | 316 ± 78 | not steady glide | 3501 | −0.14 |
| 0.25 | 50 ± 108 | stalled | 3500 | −0.35 |
| 0.50 | 585 ± 97 | (2.24 ± 0.37)×10⁻⁴ | 3498 | −0.44 |
| 1.00 | 1170 ± 135 | (2.24 ± 0.26)×10⁻⁴ | 3502 | −0.96 |

1. **Viscous glide at τ ≥ 0.5 GPa.** v doubles from 0.5 to 1 GPa, so Eq. 2 holds with **B = 2.2 × 10⁻⁴ Pa s**.
   - At 1 GPa the dislocation crosses the cell about 5 times in 30 ps.
   - v = 1170 m/s is about 15 % of the shear-wave speed, so this is still the linear, subsonic regime.
2. **τ ≤ 0.25 GPa: no steady glide.**
   - At 0.1 GPa the top block wanders by about 3 Å, which is consistent with thermal motion; the fitted 316 m/s is not a drag velocity.
   - At 0.25 GPa the dislocation stalls for most of the 30 ps.
   - So either there is a friction or pinning threshold between 0.25 and 0.5 GPa (a Peierls-type barrier at 3500 K), or 30 ps is too short to resolve slow motion. Longer runs will decide (§5).
3. **Checks:**
   - The thermostatted region holds 3500 K.
   - The mobile-region σ_xy tracks the applied τ (minus sign: compressive-positive convention).
   - The normal stresses average σ_yy ≈ 167.4 GPa, σ_xx ≈ 168.6 GPa and σ_zz ≈ 170.0 GPa, against the 175 GPa piston and the NPT lattice. These per-atom-stress pressures use an approximate mobile volume, $A(\Delta y-2\,\text{Å})$; a 3–4 % error in that volume would account for the difference. A perfect slab under the same piston will check this (§5).

## 4. Comparison with Perez et al. 2025

**Effective viscosity** (Eq. 3; b = 2.62 Å, B = 2.2 × 10⁻⁴ Pa s) and drag-limited flow stress (Eq. 4):

| ρ (m⁻²) | η_eff (Pa s) | τ_f at 10⁶ s⁻¹ | τ_f at 10⁷ s⁻¹ |
|---|---|---|---|
| 10¹³ | 330 | 0.33 GPa | 3.3 GPa |
| 10¹⁴ | 33 | 33 MPa | 0.33 GPa |
| 10¹⁵ | 3.3 | 3.3 MPa | 33 MPa |
| 10¹⁶ | 0.33 | 0.33 MPa | 3.3 MPa |

- **Drag-limited glide meets the Perez bound** (η ≤ 10² Pa s) for any mobile density above

$$\rho^\ast=\frac{B}{\eta_{max}\,b^2}\approx3\times10^{13}\ \text{m}^{-2}. \tag{5}$$

  Shock-loaded crystals typically hold $10^{14}$–$10^{16}$ m⁻². So phonon drag on ½⟨110⟩{001} dislocations easily explains a viscosity as low as Perez measured. It even allows values well below their 10² Pa s bound, consistent with their "0 Pa s and 100 Pa s fit best."
- **Strength is then set by something other than drag.** At ρ ≥ 10¹⁴ m⁻², drag alone gives a flow stress ≤ 0.33 GPa at 10⁷ s⁻¹. The non-glide threshold we see at τ ≈ 0.25–0.5 GPa (§3, item 2) is of the same order as Perez's implied ≲ 1 GPa. Both are far below the 7.5–15 GPa extrapolated static strengths. If the threshold is real, it, not drag, sets the high-rate strength.
- **Caveats on the comparison:**
  1. Eq. 3 is for resolved shear on one slip system. A macroscopic viscosity carries an orientation (Schmid/Taylor) factor $M$: $\eta_{macro}\approx M^2\eta_{eff}$, with $M\approx2$–3, so a factor of 4–9. Perez also define η through their hydrocode's deviatoric stress. These factors raise ρ* to about 10¹⁴ m⁻², which is still a modest density for shocked material.
  2. Only the edge character is computed. Screw dislocations in rocksalt are usually slower (higher lattice friction), and the strength is set by the slower species.
  3. Perez note that on 10⁻⁷–10⁻⁶ m scales viscosity is controlled by dislocation dynamics, while their 330 µm ripple wavelength samples larger scales, where micro-flows and grain rotation may contribute. Our B constrains the dislocation contribution only.
- **Literature B values** for MgO (300 K experiment, and MD at lower P) still need collecting (plan §6, †). Cordier et al. 2023 scale B ∝ T from a 300 K value; our 3500 K, 175 GPa value tests that assumption.

## 5. Anelastic implication (Granato–Lücke string damping)

With line tension $C\approx\mu b^2/2$, an overdamped pinned segment of length $L$ relaxes with

$$\tau_d=\frac{B\,L^2}{\pi^2 C},\qquad f_{peak}=\frac{1}{2\pi\tau_d}. \tag{6}$$

With μ ≈ 300 GPa (rough value for MgO at 175 GPa; τ_d ∝ 1/μ) and B = 2.2 × 10⁻⁴ Pa s:

| L | 1 µm | 10 µm | 100 µm | 1 mm | 8.5 mm |
|---|---|---|---|---|---|
| f_peak | 72 MHz | 0.72 MHz | 7.2 kHz | 72 Hz | 1 Hz |

So drag-controlled string relaxation peaks in the seismic band only for unrealistically long free segments (about 1 cm). Seismic-band dislocation loss in MgO would need a slower process, for example kink-pair formation (the threshold behaviour of §3) or pinning and unpinning at point defects. Drag sets the high-frequency end of the spectrum, not the seismic one.

## 6. Next steps

1. 100 ps runs at τ = 0.25, 0.35 and 0.5 GPa to settle whether the threshold is real. Track the core position directly (centro-symmetry / disregistry) instead of inferring it from the top block.
2. Perfect-slab reference under the same piston, to check the 167 vs 175 GPa normal stress.
3. Screw character, and the {110} system for comparison.
4. T = 2000 and 5000 K (B against T; tests Cordier's B ∝ T).
5. Size check NX = 48, and NZ larger for line flexibility.
6. Collect literature values of B and Peierls stress for MgO (Amodeo et al. 2011/2012; Carrez/Cordier).

## 7. Reproduce

```
cd /groups/carnegie_poc/rcohen/LAMMPS/MgO/Dislocations/edge_P175_T3500
sbatch --export=ALL,TEMP=3500,PRESS=175,TAUS="0.1 0.25 0.5 1.0",TEQ=10000,TRUN=30000,NX=24,NY=14,NZ=6 disl_job.sh
source ~/cohen_env/bin/activate
python /resnick/home/recohen/Claude/tools/disl_velocity.py . --plot
```

## 8. Long-line runs D1 and D1b, and a correction to the velocities (2026-11-15)

*Runs: `/groups/carnegie_poc/rcohen/LAMMPS/MgO/Dislocations/edge_P175_T3500_long/tau{0.15,0.25,0.35,0.5}` (D1, jobs 4593708–11; line 63 Å, 32 928 atoms, 150 ps per τ) and `.../edge_P175_T3500_L262/tau{0.25,0.35}` (D1b, jobs 4602367/8; line 262 Å, NX 14, NZ 100, about 68 k atoms, 100 ps). Same model, lattice and loading as §2; dumps of the mobile atoms every 1 ps. Figure: `edge_vtau_core.{pdf,png}`, table `edge_vtau_core.txt` (this directory).*

### 8.1 The top block was not rigid: §3 velocities are about 21 % low

In `disl_drive.lammps` the top block was integrated with `fix nve` plus `fix aveforce`. `aveforce` gives every atom the same force, so the Mg and O sublattices of the block (masses 24.3 and 16.0) accelerated differently and slid through each other. In D1 at τ = 0.5 GPa, over 150 ps, the block's Mg moved 30.3 Å and its O 46.0 Å; every mobile plane above the glide plane moved 46.0 Å. The logged $\Delta x_{top}$ is the mass-weighted mean, 36.5 Å, so Eq. 1 underestimated v by a factor 46.0/36.5 = 1.26.

- The mismatch builds up in discrete slips of one Burgers vector (the block's Mg sublattice re-registers), at random times: 1.2–3.6 b per run.
- **The applied stress is still transmitted correctly.** The virial shear stress of the mobile region equals τ within error in every run (e.g. 0.495 ± 0.022 GPa at τ = 0.5), because each sublattice of the block moves at a steady mean speed and carries its share of the force.
- So the dislocation feels τ, and only the velocity read from the block is wrong. Glide-plane core tracking (§8.2) is unaffected.
- **Fixed for future runs:** the top block is now one rigid body (`fix rigid/nve single`, translation in x and y only; note in `tools/disl_drive.lammps`).
- §3 (job 4452807, 30 ps segments, no dumps) used the same block, so its B = 2.2 × 10⁻⁴ Pa s is high by about the same factor. Its "no steady glide at τ ≤ 0.25 GPa" was probably the block's stick–slip plus the short segments, not a threshold (see §8.3).

### 8.2 Glide-plane core tracking

`tools/disl_core_track.py` follows the slip across the glide plane, which lies between the atomic planes at $y_g-a/2$ and $y_g$ (the first plane of the upper block). In each slice along the line,

$$x_c(z,t)-x_c(z,0)=\frac{L_x}{b}\Big[\langle u_x\rangle_{y_g}(z,t)-\langle u_x\rangle_{y_g-a/2}(z,t)\Big]. \tag{7}$$

(The first version of the tool averaged the two thermal halves of the single plane at $y_g$; that is fixed.) The velocity is the slope of the line-mean $x_c$ over the last 2/3 of the run, with a 3-block error, and $B=b\tau/v$ (Eq. 2).

### 8.3 Results: linear viscous glide down to 0.15 GPa, no threshold, no length dependence

| run | line (Å) | τ (GPa) | v, core (m/s) | v, top block (biased) | B (10⁻⁴ Pa s) |
|---|---|---|---|---|---|
| D1 | 63 | 0.15 | 219 ± 16 | 174 | 1.80 ± 0.13 |
| D1 | 63 | 0.25 | 404 ± 20 | 316 | 1.62 ± 0.08 |
| D1 | 63 | 0.35 | 533 ± 28 | 425 | 1.72 ± 0.09 |
| D1 | 63 | 0.50 | 737 ± 19 | 583 | 1.78 ± 0.05 |
| D1b | 262 | 0.25 | 371 ± 15 | 291 | 1.77 ± 0.07 |
| D1b | 262 | 0.35 | 518 ± 16 | 414 | 1.77 ± 0.05 |

A weighted fit of all six points through the origin,

$$v=\frac{b}{B}\,\tau,\qquad B=(1.755\pm0.027)\times10^{-4}\ \text{Pa s},\quad \chi^2/\nu=0.59, \tag{8}$$

and a free intercept gives $v = (1467 \pm 66)\,\tau + (8 \pm 21)$ m/s, i.e. a threshold $\tau_0 = -0.006 \pm 0.014$ GPa: **none**.

- **No threshold** between 0.15 and 0.5 GPa. The 0.25–0.5 GPa "threshold" of §3 is not real.
- **No line-length dependence:** 63 and 262 Å give the same B within 1σ. The 262 Å line is longer than the critical kink-pair width estimated in plan §5 (150–200 Å), so kink-pair-limited glide would have shown up as a slower, length-dependent v.
- **Line shape.** The line stays straight to within about one Peierls valley ($a/2$ = 1.85 Å):
  - the fluctuation of $x_c(z)$ about its mean is 1.3–1.4 Å rms, uncorrelated between 1 ps frames (the 20 ps increments have exactly √2 × that rms), so these are fast thermal fluctuations, not long-lived kinks;
  - a static pattern of 1.1–2.0 Å rms (correlation 0.97–0.99 between the two halves of each run) is the imprint of the line shape in the reference frame (Eq. 7 measures $x_c - x_c(0)$), not a property of the moving line;
  - the estimated measurement noise from thermal vibration is about 0.5 Å.
- **Interpretation:** at 3500 K and ≈ 162 GPa (true scale), ½⟨110⟩{001} edge glide in MgO is in the phonon-drag regime (above the athermal temperature) down to at least 0.15 GPa, with no kink-pair or Peierls control resolved.

### 8.4 Consequences for §4 and §5

With B = 1.76 × 10⁻⁴ Pa s (0.80 × the §3 value):
- **Effective viscosity** (Eq. 3): η_eff = 256, 26, 2.6 and 0.26 Pa s for ρ = 10¹³, 10¹⁴, 10¹⁵ and 10¹⁶ m⁻². Perez et al.'s bound η ≤ 10² Pa s is met for ρ ≳ 2.6 × 10¹³ m⁻² (Eq. 5), or about 10¹⁴ m⁻² with orientation factors.
- **Granato–Lücke peak** (Eq. 6): all frequencies 1.25× higher than in the §5 table (9 kHz at L = 100 µm; 1 Hz needs L ≈ 9.5 mm). The conclusion is unchanged: drag-controlled string damping is not a seismic-band mechanism.
- Because no threshold appears down to 0.15 GPa at 3500 K, a seismic-band dislocation loss in MgO at these conditions cannot come from a kink-pair process on this system. Pinning/unpinning by point defects, or lower temperatures (below the athermal temperature), are the remaining candidates.

### 8.5 Next steps (proposed; not yet approved)
1. B(T): the same D1 cell at 2000 and 5000 K, τ = 0.25 and 0.5 GPa (tests Cordier's B ∝ T, and whether a threshold appears at 2000 K). With the rigid-block fix. 4 runs × ≈ 10 P100-h.
2. Screw ½[110] and the {110} system (plan D2/D4).
3. Perfect-slab reference for the 167 vs 175 GPa normal stress (§3).

Reproduce §8:
```
D=/groups/carnegie_poc/rcohen/LAMMPS/MgO/Dislocations; source ~/cohen_env/bin/activate
for r in $D/edge_P175_T3500_long/tau* $D/edge_P175_T3500_L262/tau*; do python ~/Claude/tools/disl_core_track.py $r; done
python ~/Claude/tools/disl_vtau_plot.py --out edge_vtau_core $D/edge_P175_T3500_long/tau* $D/edge_P175_T3500_L262/tau*
```
