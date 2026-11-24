# MgO vacancy formation and migration free energies and diffusion, Deng model (A1 + A2, analysed 2026-11-16)

Runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A1_MgO_Deng` (jobs 6930969 perfect, 6930970 defects) and `.../A2_MgO_Deng_mig` (6931057); READMEs there. Plan: `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` §1–2. Raw outputs in this directory: `A1_analysis.txt`, `A2_analysis.txt`, `A1A2_MgO_D.txt`.
Tools: `tools/ti_einstein_analyze.py --gf` (Eq. 1), `tools/vac_mig_analyze.py` (Eqs. 2–3).

## 1. Methods in brief
Formation (Frenkel–Ladd switching, 6 forward/backward replicas of 40 ps; defect cell at the perfect crystal's mean NPT box):

$$\Delta G_f=F_D(V_I)-\tfrac{N-L}{N}F_I(V_I)+\tfrac{L}{N}PV_I-\frac{(P_D-P_I)^2V_I}{2K_T}\tag{1}$$

Migration (umbrella integration along the straight jump coordinate s, 21 sequential windows from the site to the midpoint, 15 ps each):

$$\Delta G_m=\max_s G(s)-\min_{s<s^*}G(s),\qquad G(s)=\int\kappa\,(s_k-\langle s\rangle_k)\,ds\tag{2}$$

$$\Gamma=\nu^*e^{-\Delta G_m/k_BT},\qquad \nu^*=\frac{\sqrt{k_BT/2\pi m}}{\int_{\rm well}e^{-(G-G_{min})/k_BT}ds}\tag{3}$$

Diffusion (Ita & Cohen Eq. 1; Schottky: W = 2, Z_f = 1, Z_m = 12, l = a/√2; no correlation factor):

$$D_i=\tfrac16 Z_m\,l^2\,\Gamma_i\,c_v,\qquad c_v=e^{-\Delta G_f^{sep}/2k_BT}\ \text{(intrinsic)},\quad c_v=X_v=10^{-5}\ \text{(extrinsic)}\tag{4}$$

No hops: max |dr| ≤ 0.88 Å in every TI replica except one replica of P120 n6 bound (2.84 Å; that cell agrees with n4 anyway); max other-atom displacement ≤ 0.80 Å in every migration window.

## 2. Formation and migration free energies (Deng model, raw)

| P (GPa) | T (K) | ΔG_f bound, 510 atoms (eV) | ΔG_f separated, 1726 atoms (eV) | ΔG_b (eV) | ΔG_m Mg (eV) | ΔG_m O (eV) | ν* Mg, O (THz) |
|---|---|---|---|---|---|---|---|
| 20 | 2000 | 5.27 ± 0.11 | 6.50 ± 0.18 | 1.23 | 2.19 | 2.39 | 7.3, 10.6 |
| 30 | 2000 | 6.04 ± 0.06 (1726: 6.10 ± 0.25) | 7.66 ± 0.28 | 1.62 | 2.42 | 2.66 | 8.0, 11.4 |
| 60 | 2300 | 8.43 ± 0.12 | 10.01 ± 0.27 | 1.58 | 2.95 | 3.31 | 9.2, 13.3 |
| 80 | 2000 | 9.31 ± 0.10 | 11.62 ± 0.22 | 2.30 | 3.32 | 3.69 | 10.1, 14.2 |
| 90 | 2500 | 10.13 ± 0.11 | 12.13 ± 0.25 | 2.00 | 3.37 | 3.83 | 10.2, 14.6 |
| 120 | 2800 | 11.28 ± 0.11 (1726: 11.07 ± 0.34) | 13.61 ± 0.26 | 2.32 | 3.66 | 4.29 | 10.7, 15.7 |
| 140 | 3000 | 12.45 ± 0.17 | 15.30 ± 0.23 | 2.84 | 3.85 | 4.54 | 11.3, 16.3 |

ΔG_m errors are ± 0.01 eV (statistical). Size check: the bound pair in 510 and 1726 atoms agrees within 0.06 and 0.21 eV (within error).

**Method check (fixed-volume formation, Eq. 1):** the A0 bound-pair values with separate NPT volumes were 5.15 ± 0.21 (20/2000) and 11.90 ± 0.24 / 12.68 ± 0.31 eV (140/3000, TS 40 / 20 ps). Eq. 1 gives 5.27 ± 0.11 and 12.45 ± 0.17 eV, with half the error and no PΔV noise. The second-order term is ≤ 0.02 eV.

## 3. Comparison with Ita & Cohen 1997 (VIB model; PRL Table I, converted from 10⁻¹⁹ J)

| P, T | ΔG_f bound: VIB / Deng | ΔG_b: VIB / Deng | ΔG_m Mg: VIB / Deng | ΔG_m O: VIB / Deng |
|---|---|---|---|---|
| 20 GPa, 2000 K | 7.51 / 5.27 | – / 1.23 | 2.34 / 2.19 | 2.55 / 2.39 |
| 80 GPa, 2000 K | 13.23 / 9.31 | – / 2.30 | 3.22 / 3.32 | 3.65 / 3.69 |
| 140 GPa, 3000 K | 15.79 / 12.45 | 4.37 / 2.84 | 3.74 / 3.85 | 3.88 / 4.54 |
| 0 GPa, 2000 K | – | 1.56 / – | – | – |

- **Migration agrees** with VIB within 0.15 eV at 20 and 80 GPa (both species) and for Mg at 140 GPa; O at 140 GPa / 3000 K is 0.66 eV higher in Deng. Ita & Cohen's ν = 5.2 THz (lowest projected-motion peak) against our TST ν* = 7–16 THz (Eq. 3; it rises with P as the well stiffens).
- **Formation is 2.2–3.9 eV lower in Deng** for the bound pair, and the binding energy is smaller (2.84 vs 4.37 eV at 140 GPa). The A0 DFT check (PBEsol snapshots, bound pair) puts +0.95 eV (20 GPa) and +1.27 eV (140 GPa) on the Deng values, so 1–2.6 eV of the gap remains between DFT and VIB for the bound pair (as found in A0).
- **The separated pair has not been checked against DFT.** That is the critical gap: (i) D (Eq. 4) depends on ΔG_f^{sep}; (ii) the DeePMD model is short-ranged (6 Å cutoff, no long-range electrostatics), while the separated V_Mg and V_O are oppositely charged defects with long-range Coulomb interaction and lattice polarization. VIB includes these via Ewald sums. The separated-pair ΔG_f is therefore the least trustworthy number here, in either direction.

## 4. Diffusion coefficients and Cordier et al. 2023

Eq. 4, Deng values as computed (no DFT correction):

| P, T | c_v intrinsic | D_Mg intr. | D_O intr. | D_Mg (X_v = 10⁻⁵) | D_O (X_v = 10⁻⁵) | Cordier Table 2 D_O (Ita–Cohen fit) |
|---|---|---|---|---|---|---|
| 30 GPa, 2000 K | 2.2×10⁻¹⁰ | 2.3×10⁻²² | 8.5×10⁻²³ | 1.0×10⁻¹⁷ | 3.8×10⁻¹⁸ | 6.5×10⁻²⁷ |
| 60 GPa, 2300 K | 1.1×10⁻¹¹ | 5.4×10⁻²⁴ | 1.3×10⁻²⁴ | 5.0×10⁻¹⁸ | 1.2×10⁻¹⁸ | 3.05×10⁻²⁹ |
| 90 GPa, 2500 K | 5.9×10⁻¹³ | 1.5×10⁻²⁵ | 2.4×10⁻²⁶ | 2.5×10⁻¹⁸ | 4.1×10⁻¹⁹ | 3.5×10⁻³¹ |
| 120 GPa, 2800 K | 5.7×10⁻¹³ | 2.2×10⁻²⁵ | 2.4×10⁻²⁶ | 4.0×10⁻¹⁸ | 4.2×10⁻¹⁹ | 5.4×10⁻³¹ |

(m²/s; 20, 80, 140 GPa rows in `A1A2_MgO_D.txt`.)

- Intrinsic D_O from the Deng model is **1.3×10⁴ to 7×10⁴ times** Cordier's values at their four states. If the bound-pair DFT correction (+1.0 to +1.2 eV) applied to the separated pair, the factor would be ≈ 7×10² to 5×10³.
- Almost all of this comes from ΔG_f^{sep}: Deng's 15.3 eV against VIB's ≈ 20.2 eV (bound + binding) at 140 GPa / 3000 K is worth exp(4.9 eV/2k_BT) ≈ 10⁴. Migration contributes less than 10× (O at 140 GPa).
- **Implication, if it holds:** Cordier's ε̇ in periclase scales with D_O, so their periclase/bridgmanite strength contrast (≈ 10³ at 800 km, ≈ 6×10⁵ at 2600 km) would drop by 10³–10⁴, to near parity or below at 800 km. This is the same direction as the DFT spot check (CORDIER2023_COMPARISON.md §2.1) but larger.
- **It does not yet hold**, because of the separated-pair caveat (§3). The decisive check is a DFT one: static relaxed and finite-T snapshot energies of the separated pair in the largest affordable cell (216 and 512 atoms), against the Deng model at the same geometries, with and without an explicit long-range electrostatic correction.
- Mg is extrinsic in real MgO (trivalent impurities set X_v); O is intrinsic (Ita & Cohen; Cordier). The extrinsic columns are for reference.

## 5. Next steps
1. DFT check of the separated pair: **submitted 11-16** (RC "Yes do 1 2 3 4 5"): static binding curve E_b(d) at d = 2–13 Å (DFT vs DeePMD, fixed-cell relaxations, 512-site cells) and finite-T FEP of the farthest pair at 20/2000 and 140/3000; `/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck/README.md` Part 3 (jobs 6963424, 6963519 → VASP arrays).
2. TST check in MgO: **done 11-16, §6 (TST confirmed, κ ≈ 1)**; submitted 11-16: direct-MD hops and independent-window umbrella at the same (V, T) in the A2 cell (20 GPa box at 3000, 3400 K; 60 GPa box at 3800, 4200 K); `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A2b_MgO_TSTcheck` (jobs 6963299, 6963300).
3. Correlation factor (f ≈ 0.78 for vacancy diffusion on an fcc sublattice) and bound-pair (Z_m = 8, W = 1) contribution for D; activation volumes from the P dependence (plan Eq. 10).
4. Ita's 80/4000 and 140/5000 K by T integration (plan Eq. 5).

## 6. TST check against direct MD hop counts (A2b, analysed 2026-11-16)
Runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A2b_MgO_TSTcheck` (jobs 6963299, 6963300; README there). Same A2 cell (separated V_Mg + V_O, 510 atoms) at the A1 boxes of 20/2000 (V20) and 60/2300 (V60), heated to 3000–4200 K. Direct MD runs 2 ns at each state. Umbrella windows are independent, 21 from 0 to l/2.

$$\kappa=\frac{\Gamma_v^{MD}}{Z\,\nu^*e^{-\Delta G_m/k_BT}},\qquad Z=12 \tag{5}$$

| (V, T) | ΔG_m Mg / O (eV) | κ Mg / O (free vacancies) | hops (free) Mg / O |
|---|---|---|---|
| V20, 3000 K | 2.15 / 2.41 | 1.6 ± 0.3 / 1.3 ± 0.4 | 28 / 11 |
| V20, 3400 K | 2.06 / 2.34 | 0.64 ± 0.08 / 0.93 ± 0.15 | 67 / 38 |
| V60, 3800 K | 2.87 / 3.30 | 0.97 ± 0.17 / 0.49 ± 0.22 | 33 / 5 |
| V60, 4200 K | 2.78 / 3.35 | 0.87 ± 0.12 / 1.31 ± 0.34 | 56 / 15 |

- **The A2 transition-state rates are confirmed:** κ = 0.5–1.6, mean 1.0, which bounds the barrier error at ≈ 0.1–0.15 eV.
- **The barriers depend little on T at fixed volume:** relative to A2 at 2000 / 2300 K, Mg is lower by 0.04–0.17 eV and O changes by ±0.05 eV. So the D values of §4 are not limited by the migration part.
- **In the MD the separated vacancies meet and bind** after 0.3–0.5 ns, and then spend half the time as a nearest-neighbour pair. The rates above use only the free time (new `site_hops.py` pair tracking).
  - The bound pair hops faster at V60 / 4200 K (Mg 2×, O 4×) and slower at V20 (0.3–0.5×). That is the bound-pair channel of Ita & Cohen (Z_m = 8, W = 1), which §4 still omits.
- **What is left in the D_O comparison with Cordier** is the separated-pair formation energy, which the DFT check (§5 item 1, running) addresses.
