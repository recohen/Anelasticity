# Cordier et al. 2023 (Nature 613, 303), "Periclase deforms more slowly than bridgmanite under mantle conditions": detailed comparison with our MgO and MgSiO₃ results

*2026-10-15. RC: "For 3 I meant Cordier et al! https://doi.org/10.1038/s41586-022-05410-9 … particularly to compare MgO and MgSiO3."
Paper: `Papers/s41586-022-05410-9.pdf`. Related: `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` §0 and §2 (T20), `results_dft/MGO_DFT_MODEL_COMPARISON.md`, `results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md`, `results_fei2023/FEI2023_COMPARISON.md`.*

## 1. The paper's chain of argument

1. **O diffusion in periclase is intrinsic and slow.** O moves by thermally produced neutral Schottky pairs. Trivalent impurities make *Mg* vacancies, which do not help O. The D_O(P,T) used is Ita & Cohen's fit to their VIB free-energy integrations (our group's 1997 PRL):

$$\ln D^{O}_{sd}=\ln(a^2\nu_a)+\frac{S_0+PS_0'}{k_B}-\frac{E_0+PV_0+P^2V_0'}{k_BT} \tag{1}$$

   with ν_a = 5.4 THz, S₀ = 4 k_B, S₀′ = 0.02 k_B/GPa, V₀ = 16.7 Å³ and V₀′ = −0.038 Å³/GPa.
   - **E₀ = 9.4×10⁻¹⁹ J.** Their Table 1 prints 0.4×10⁻¹⁹ J, which is a typo. With 9.4×10⁻¹⁹ J, Eq. 1 reproduces their Table 2 to 2 %: 6.5×10⁻²⁷, 3.05×10⁻²⁹, 3.5×10⁻³¹ and 5.4×10⁻³¹ m²/s at 30/2000, 60/2300, 90/2500 and 120 GPa/2800 K (our check, 10-15).
   - Effective enthalpies from D = D₀e^{−ΔH/k_BT}, with D₀ = 7.2×10⁻⁴ m²/s: 9.15, 11.59, 13.56 and 15.09 eV.
2. **Periclase creep:** 2.5D dislocation dynamics, glide plus climb, 10–150 MPa.
   - Glide is *athermal*: "the lattice friction of MgO vanishes" in this P–T range. It is viscous drag, v = bτ/B, with B scaled linearly with T from a 300 K experiment (Singh & Coble 1974).
   - Climb is limited by D_O.
   - Result: n = 3.1. Strain rates are about 10⁻¹⁶ (30 GPa) to 10⁻²¹ s⁻¹ (90–120 GPa) at 10 MPa (Fig. 2a).
3. **Bridgmanite:** pure climb creep from Reali et al. 2019, with an *assumed* vacancy fraction X_v = 10⁻⁵ (range 10⁻³–10⁻⁶ in ED Figs 3–7) and Si/Mg diffusion from experiments.
4. **Contrast** η_Per/η_Bdm at 10 MPa (Fig. 2b): about 10³ at 800 km, 3×10⁵ at 1400 km, 1.5×10⁷ at 2000 km and 6×10⁵ at 2600 km (fig.).
   - In a 25 % periclase aggregate (POSO self-consistent homogenization), periclase barely deforms, and the aggregate is within a factor 1.65 of pure bridgmanite in flow stress.
5. **Robustness checks in the paper:**
   - Yoo et al.'s faster D_O (E₀ = 7.2×10⁻¹⁹ J, S₀ = 2 k_B);
   - X_v(Bdm) from 10⁻³ to 10⁻⁶;
   - 20 mol% FeO raising D_O by about 2000× through homologous-temperature scaling.
   - None of these overturns the conclusion.
6. **Not included:** grain and phase boundaries ("the role of grain or phase boundaries is not explicitly taken into account"), pipe diffusion, and any thermally activated glide in MgO.

## 2. Ingredient-by-ingredient comparison with our results

### 2.1 D_O in periclase: the VIB inputs (our DFT spot check, `results_dft/`)

**Formation free energy.** We compared the bound Schottky pair against PBEsol DFT: our DeePMD free energies, corrected to DFT by perturbation from snapshots.

| state | ΔG_f bound pair (eV) | VIB − DFT (eV) |
|---|---|---|
| 20 GPa / 2000 K | DFT 6.10–6.29; VIB 7.51 | +1.2 to +1.4 |
| 140 GPa / 3000 K | DFT 13.2–14.8; VIB 15.79 | +1.0 to +2.6 |

If the free Schottky pair (W = 2 in Ita & Cohen's D) carries a similar error, then

$$\frac{D_O^{DFT}}{D_O^{VIB}}\approx\exp\!\left(\frac{\delta\Delta G_f}{2k_BT}\right) \tag{2}$$

is:

| state | δ = 1.0 eV | δ = 1.4 eV | δ = 2.6 eV |
|---|---|---|---|
| 30 GPa / 2000 K | 18 | 58 | 1900 |
| 60 GPa / 2300 K | 12 | 34 | 700 |
| 90 GPa / 2500 K | 10 | 26 | 420 |
| 120 GPa / 2800 K | 8 | 18 | 220 |

With W = 1 (bound-pair-mediated O transport) the factors would be squared.
- **Effect on the contrast:** since ε̇_Per ∝ D_O at fixed stress, Cordier's contrast drops from about 10³ to about 0.5–60 at 800 km, and from about 6×10⁵ to about 3×10³–8×10⁴ at 2600 km.
- **At the top of the lower mantle the conclusion "periclase slower" is no longer secure.** Deeper it survives, but by 2–4 orders less.
- Not yet checked:
  - the migration free energy ΔG_m (O), which enters as exp(−ΔG_m/k_BT) at full weight;
  - the free (separated) pair, which is what W = 2 refers to;
  - the size of the PΔV term (ΔG_f at 140 GPa still has a 0.8 eV switching-time spread).

**Equation of state.** VIB is 0.55 % too dense in a at 140 GPa / 3000 K, i.e. a pressure about 10 GPa too low against Tange 2009; at 20 GPa it is accurate. Cordier's "120 GPa" therefore sits at about 130 GPa on the experimental scale for Ita & Cohen's volumes. The effect on D through P V₀ is about 0.1 eV, which is small.

### 2.2 Glide in periclase: athermal and drag-limited? (our edge dislocation, `results_dislocations/`, plan D1/D1b)

- **Drag.** Our ½[110](001) edge at 175 GPa / 3500 K (MgO-only model; ≈ 162 GPa experimental scale) gives **B = 1.76×10⁻⁴ Pa s** (corrected 2026-11-15; `results_dislocations/` §8), from v ∝ τ at 0.15–0.5 GPa with no threshold, independent of line length (63 and 262 Å). Cordier scales B ∝ T from a 300 K value. Our number tests that scaling at one (P, T); B at 30–120 GPa and 2000–2800 K is plan D2. The 300 K value needs checking: Singh & Coble 1974 †.
- **Lattice friction.** Cordier assume none in 2000–2800 K. Our short line (16 Å) did not glide steadily at τ ≤ 0.25 GPa in 30 ps. Cordier 2012 extrapolates τ_p ≈ 1.2–1.5 GPa and ΔH₀ ≈ 10 eV at 175 GPa for the {100} edge.
  - At 10⁻¹⁶ s⁻¹ the athermal temperature T_a is about 2400–2900 K at 100–130 GPa (Cordier 2012), *close to* the geotherm. Thermally activated glide (not included in the 2023 DD) could therefore matter deep in the lower mantle.
  - **D1b result (2026-11-15):** a 262 Å line glides viscously down to 0.15 GPa at 3500 K with no kink-pair signature, so at 162 GPa T_a < 3500 K for this system with our model. Placing T_a needs runs at 2000–2800 K (proposed).
- **Consequence.** If glide is not athermal at depth, periclase is *slower* still (Cordier's conclusion is strengthened there). Near 800 km it is athermal in every estimate.

### 2.3 What Cordier leaves out: boundaries (our Σ5 MgO results; plan G)

- Our Σ5 (310)/[001] MgO boundary at about 14–20 GPa and 2000–3000 K gives δD_b ≈ 0.8–3×10⁻²⁰ m³/s for Mg and O alike (whole-cell MSD, an upper bound; summary §5d).
- **With that δD_b, Coble creep of periclase** at d = 0.4 mm and 0.5 MPa gives η ≈ 2×10¹⁸ Pa s. That is faster than climb-controlled bridgmanite at the same conditions (about 10¹⁹ Pa s at 27 GPa / 2200 K) and about 10⁷ times faster than Cordier's lattice-diffusion periclase (`results_fei2023/`, Table §3).
- **A grain-boundary path in periclase can overturn the conclusion,** if boundary O transport in MgO at 30–120 GPa is anywhere near this fast. The leverage is about 10⁷, compared with 10¹–10³ for the formation-energy correction.
- Our 140 GPa Σ5 boundary is structurally locked (sliding), and the boundary-diffusion rate there is unknown. So the pressure dependence of δD_b(O) in MgO is the decisive unknown.
- **Update 2026-11-15 (G-diff, §5):** with the Deng model and the boundary-resolved MSD, the Σ5 boundary at 27/2200, 30/2000, 90/2500 and 120/2800 shows **no boundary diffusion in 1 ns: δD_b < 1×10⁻²³ m³/s**, 3 orders below the whole-cell upper bound above. Scaling the Coble estimate (η ∝ 1/δD_b) gives η ≳ 10²¹ Pa s at d = 0.4 mm, slower than climb-controlled bridgmanite. For this special boundary the grain-boundary path does **not** overturn Cordier's conclusion. General boundaries (the polycrystal) are still to be tested.
- Pipe diffusion (Landeiro Dos Reis 2022, cited by Cordier) is a similar fast path. They used it only to dismiss Van Orman's higher D_O as extrinsic.

### 2.4 The bridgmanite side

- X_v = 10⁻⁵ is *assumed* (extrinsic: Al/Fe³⁺ charge balance), while periclase is treated as intrinsic. The asymmetry is defensible for O in MgO (trivalent cations make cation vacancies), but **no intrinsic bridgmanite calculation is used**.
- Plan A3 (approved 10-13) computes, with the same Deng model as MgO:
  - the formation free energies of the three bridgmanite Schottky types (V_Mg + V_O, V_Si + 2V_O, and the full MgSiO₃ Schottky);
  - Si, Mg and O migration.

  This gives the intrinsic X_v(P,T) and D, to set against both X_v = 10⁻⁵ and intrinsic MgO.
- Our bridgmanite V_Mg + V_O work so far (anelastic sweeps; summary §5i, §5j) is about loss, not diffusion. The direct MD hop rates at 3000–5000 K are a validation set for A3.
- Bridgmanite boundary diffusion: van Driel's GAP MD gives D_gb(Si) about 10³ above Yamazaki's experiments (Fei comparison §3). It matters only for d ≲ 0.15 mm.

### 2.5 Iron

Our models are Fe-free, as are Cordier's (end-members). Their homologous-temperature argument gives ×2000 for 20 % FeO, which is comparable to or larger than the DFT correction in §2.1. Together these two factors could take the 800 km contrast below 1.

## 3. Summary: is periclase slower than bridgmanite?

| factor | direction | size (orders of magnitude in the contrast) | status |
|---|---|---|---|
| VIB → DFT formation free energy (ours) | periclase faster | −1 to −3 | bound pair done; free pair and ΔG_m to do (A1, A2) |
| FeO in Fp (Cordier's own estimate) | periclase faster | −3.3 | literature |
| grain-boundary O diffusion in MgO (ours, upper bound, low P) | periclase faster | up to −7 | needs δD_b(O) at 30–120 GPa (new item G-diff) |
| thermally activated glide in MgO at depth (Cordier 2012; our D1b) | periclase slower | + | D1b running |
| intrinsic X_v in bridgmanite (A3) | either | ± several | to compute |
| Cordier baseline | periclase slower | +3 (800 km) to +7 (2000 km) | |

On present evidence, **"periclase deforms more slowly" holds in the mid and deep lower mantle if lattice diffusion controls periclase.** It is marginal near 800 km once the DFT and FeO corrections are applied. It could be reversed everywhere by a fast grain-boundary path in fine-grained Fp, which Cordier does not consider. The decisive calculations are all within our plan, using the same model for both minerals.

## 4. Calculations in priority order (Cordier's four geotherm states: 30/2000, 60/2300, 90/2500, 120/2800 GPa/K)

1. **G-diff (MgO Σ5 done 2026-11-15, §5; bridgmanite to do):** boundary-resolved δD_b for Mg and O in the MgO Σ5 bicrystal at the four states, Deng model, 4000-atom cells, 200–500 ps NVT, MSD with grain translation removed. Then the same for bridgmanite (021) and (013) (Si, Mg, O).
2. **A1/A2:** MgO free and bound pair ΔG_f, plus ΔG_m(O, Mg) at the four states. Gives D_O against Cordier Table 2 directly, plus the activation volume.
3. **A3:** bridgmanite intrinsic X_v and D_Si, D_Mg, D_O at the same states.
4. **D2:** drag B(T) at 30 and 90 GPa (against B ∝ T), and D1b kink-pair kinetics → T_a(P) along the geotherm.
5. **Synthesis:** redo Cordier's Fig. 2b (contrast against depth) with our D's and δD_b, including the Coble path for d = 0.1–1 mm. Feed into the Fei-type grain-size model.

## 5. G-diff results: MgO Σ5(310)[001] boundary at the Cordier/Fei states (2026-11-15)

*Runs: `/groups/carnegie_poc/rcohen/LAMMPS/DengStates/MgO_S5_diff/P<P>_T<T>` (job 4612246_1–5; Deng model; 3920 atoms; 50 ps NPT, then 1 ns NVT at the mean box; dumps every 1 ps). Analysis: `tools/gb_diff.py` (Eqs. 1–3 there: boundary-resolved in-plane MSD with grain motion removed; δD_b = 2 Σ_s [D(s) − D_bulk] Δs), plus the sliding friction from the grains' relative Brownian motion,*

$$\beta=\frac{k_BT}{2AD_u},\qquad \langle\Delta u^2\rangle=2D_ut \tag{3}$$

*(Eq. 4 of `gb_diff.py`, as summary Eq. 12). Output per state: `gb_diff.txt`, `gb_diff.{pdf,png}`, `gb_u.dat`.*

| P (GPa) / T (K) | boundaries | δD_b Mg (m³/s) | δD_b O (m³/s) | β_x (Pa s/m) | β_y (Pa s/m) |
|---|---|---|---|---|---|
| 27 / 2200 (Fei) | static | 1.6×10⁻²⁴ (noise) | 4.8×10⁻²⁵ (noise) | locked (MSD_u 0.04 Å² in 250 ps) | ≥ 5×10¹¹ |
| 30 / 2000 | static | −4.0×10⁻²⁴ (noise) | −4.0×10⁻²⁴ (noise) | locked | ≥ 1.5×10¹¹ |
| **60 / 2300** | **migrate by up to 15 Å and back** | 1.3×10⁻¹⁹ * | 1.3×10⁻¹⁹ * | **7.4×10⁶** | locked |
| 90 / 2500 | static | 6.5×10⁻²⁴ (noise) | 6.7×10⁻²⁴ (noise) | locked | ≥ 1.4×10¹² |
| 120 / 2800 | static | 1.0×10⁻²⁴ (noise) | 2.6×10⁻²⁴ (noise) | ≥ 2×10¹² | ≥ 3×10¹² |

\* Not diffusion: Mg and O give identical values, and the excess comes from atoms swept by the migrating boundary (collective, shear-coupled migration).

- **Four of five states: the boundary is frozen on 1 ns.** No boundary diffusion is resolved: |δD_b| ≤ 7×10⁻²⁴ m³/s, so δD_b < 1×10⁻²³ m³/s (about 2σ). Bulk D is also at the noise floor (≤ 6×10⁻¹⁵ m²/s). This is 3 orders below the earlier whole-cell upper bound (0.8–3×10⁻²⁰ m³/s, MgO-only model, ≈ 10–13 GPa true pressure, which included grain translation).
- **60 GPa / 2300 K is different:** the grains slide along x (perpendicular to the tilt axis, the Cahn–Taylor coupling direction) in discrete jumps. 14 jumps of 1.1–3.5 Å in 1 ns (mean waiting time ≈ 70 ps), and the boundaries migrate together by up to 15 Å and back. The coupling ratio (≈ 12 Å of sliding per 15 Å of migration, ≈ 0.8) is close to the geometric value 2 tan(θ/2) = 0.67 for Σ5 (θ = 36.9°). β_x = 7.4×10⁶ Pa s/m is close to the MgO-only V9.6397 values (5×10⁶–5×10⁷, summary §5d).
- Why 60 GPa slides while 27/2200 and 90/2500 do not is not clear from one run per state: a thermally activated event with a waiting time near 1 ns would be seen in some runs and not others. Replicas or longer runs are needed before reading this as a pressure effect.
- **Consequence for Cordier:** for this boundary, grain-boundary diffusion in periclase at 27–120 GPa is too slow to matter (Coble η ≳ 10²¹ Pa s at 0.4 mm, from η ∝ 1/δD_b and the §2.3 estimate). Sliding (anelasticity) is a separate question: it is active at 60/2300.
- **Caveats:** (i) Σ5 is a special, low-energy boundary; general high-angle boundaries are more open. The 8-grain polycrystal (60 GPa / 2300 K, 300 ps anneal, job 4612253) is the next test: its boundary-atom fraction stayed constant (0.28 by CN ≠ 6 at 2300 K) over the anneal (no grain growth), PE still drifting down by ≈ 0.15 meV/atom/ps at the end. (ii) 1 ns: rates below ≈ 10⁹ s⁻¹ per boundary site are invisible. (iii) Bridgmanite boundaries not yet done.

### 5.1 Σ5 at 60 GPa, temperature series (job 6929623_1–3; 2000, 2600, 2900 K; analysed 2026-11-16)
Runs: `/groups/carnegie_poc/rcohen/LAMMPS/DengStates/MgO_S5_P60_Tseries/P60_T<T>` (README there). Same cell and protocol as §5; `gb_diff.py` per state. Jumps: u_x smoothed with a 21-frame running median, sampled every 10 ps, steps > 1 Å counted.

| T (K) | boundaries | u_x jumps per ns (mean size, Å) | corr(u_x, boundary height) | β_x (Pa s/m, Eq. 3) |
|---|---|---|---|---|
| 2000 | static (b1 29.0–30.6 Å) | 0 | – | 2.8×10⁸ (MSD_u 0.48 Å² in 250 ps; near-locked) |
| 2300 (§5) | migrate by up to 15 Å | 15 (1.4) | −0.99 | 7.4×10⁶ |
| 2600 | sweep the whole grain (31 Å) | 38 (1.6) | −0.64 | 2.4×10⁷ |
| 2900 | sweep the whole grain (31 Å) | 23 (1.5) | −0.18 | 1.0×10⁷ |

- **Onset between 2000 and 2300 K at 60 GPa;** above it the boundaries move by shear-coupled migration (grain sliding u_x tied to boundary motion, |corr| up to 0.99) at 15–40 jumps/ns. At 2600 and 2900 K the boundaries sweep through the whole grain, so the bulk-vs-boundary diffusion split of `gb_diff.py` is meaningless there (δD_b comes out negative; not tabulated).
- **No Arrhenius law:** the jump rate and β_x are not monotonic above 2300 K (one 1 ns run per T, 15–40 events each). Between 2000 K (locked) and 2300 K the change in β is > 30×; the apparent energy of that step is > 5 eV but rests on one locked run. Once the boundaries can migrate, β ≈ 10⁷ Pa s/m independent of T within a factor of 3.
- So the 60/2300 sliding of §5 is not a single-run fluke: the boundary unlocks above ≈ 2300 K at 60 GPa. The open question of §5 (why 27/2200, 90/2500 and 120/2800 stay locked) remains; it points to a pressure-dependent unlocking temperature (≈ 2100–2300 K at 60 GPa, above 2500 K at 90 GPa and 2800 K at 120 GPa), which replicas at 90 and 120 GPa and higher T would test. **Done 11-16 (§5.2): still locked at 90 GPa up to 3400 K and at 120 GPa up to 3800 K.**
- For anelasticity: shear-coupled migration with β ≈ 10⁷ Pa s/m gives the MHz relaxation of the restart 11-15 §4 estimate (τ ≈ βd/G at d = 1 mm), now at mantle-relevant conditions for Σ5 at 60 GPa above ≈ 2300 K.

### 5.2 Σ5 at 90 and 120 GPa, temperature series (job 6963084_1–6; analysed 2026-11-16)
Runs: `/groups/carnegie_poc/rcohen/LAMMPS/DengStates/MgO_S5_P90P120_Tseries` (README there). The protocol is that of §5.1: 1 ns NVT at the 50 ps NPT mean box, and the same jump count.

| P (GPa) | T (K) | sliding jumps > 1 Å per ns | boundary migration | β (Pa s/m) |
|---|---|---|---|---|
| 90 | 2800 | 0 | none | 7.7×10⁸ (y), locked in x |
| 90 | 3100 | 0 | none | 2.5×10⁸ (y), locked in x |
| 90 | 3400 | 0 | none | locked |
| 120 | 3100 | 0 | none | locked |
| 120 | 3400 | 0 | none | locked (≥ 3×10¹¹) |
| 120 | 3800 | 0 | none | locked (≥ 3×10¹¹) |

- **The boundary stays locked up to 3400 K at 90 GPa and 3800 K at 120 GPa**, 900–1000 K above the Cordier geotherm. At 60 GPa it unlocks between 2000 and 2300 K (§5.1).
- **The unlocking temperature therefore rises by > 1100 K between 60 and 90 GPa (> 40 K/GPa).** That is steeper than typical MgO melting slopes at these pressures, so homologous temperature alone does not explain it. Possible causes, not tested: a pressure-induced change of the Σ5 boundary structure between 60 and 90 GPa, or a sliding barrier that rises steeply with P. A static γ(u) scan, or an NEB of one sliding/migration event at 60 and 90 GPa, would separate the two.
- **For Cordier's argument:** in the Deng model the MgO Σ5 boundary is mobile at mantle temperatures only at the top of the lower mantle (≈ 60 GPa). At 90–120 GPa it gives no grain-boundary sliding or migration on ns time scales, even 1000 K above the geotherm. A boundary-assisted (Coble-type or sliding) softening of periclase at depth is therefore not supported for this boundary.

