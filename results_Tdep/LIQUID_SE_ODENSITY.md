# Do viscosity and diffusion scale with O motion, and does D_O depend on the O density? (RC hypothesis, 2026-11-15)

RC: "for liquids viscosity and diffusivity scale with the motion of O, and the diffusivity of O depends on the density of O/volume." For solids, diffusivities need the Ita & Cohen free-energy route (PRL 79, 3198, 1997; GRL 1998).

Data: the existing 1.5 ns GK runs (η₀ from GK, D from the same runs' MSD, second half). Tool: `tools/liquid_se.py` → `liquid_se.txt` (this directory). No new runs.

The slip Stokes–Einstein (SE) radius is

$$r_{SE}=\frac{k_BT}{4\pi\,\eta_0\,D_O}. \tag{1}$$

If η and D_O scale together, $r_{SE}$ is constant. The O number density is $n_O=x_O/V$ (x_O = 1/2 for MgO and 3/5 for MgSiO₃, V per atom).

| liquid | V (Å³/atom) | n_O (Å⁻³) | T (K) | p (GPa) | η₀ (mPa s) | D_Mg | D_Si | D_O (Å²/ps) | r_SE (Å), D_O | r_SE (Å), D_Si |
|---|---|---|---|---|---|---|---|---|---|---|
| MgO | 6.6868 | 0.0748 | 8112 | 192.8 | 8.19 | 1.255 | – | 1.086 | 1.00 | – |
| MgO | 6.6868 | 0.0748 | 6977 | 183.4 | 11.18 | 0.810 | – | 0.703 | 0.98 | – |
| MgO | 6.6868 | 0.0748 | 5986 | 174.9 | 18.30 | 0.442 | – | 0.417 | 0.86 | – |
| MgO | 9.6397 | 0.0519 | 6010 | 49.5 | 3.49 | 1.909 | – | 1.958 | 0.97 | – |
| MgO | 9.6397 | 0.0519 | 3968 | 37.8 | 7.99 | 0.665 | – | 0.604 | 0.90 | – |
| MgSiO₃ | 6.5669 | 0.0914 | 7073 | 161.1 | 7.49 | 0.865 | 0.975 | 1.167 | 0.89 | 1.06 |
| MgSiO₃ | 6.5669 | 0.0914 | 5875 | 148.7 | 12.80 | 0.541 | 0.410 | 0.569 | 0.89 | 1.23 |
| MgSiO₃ | 6.5669 | 0.0914 | 5168 | 141.2 | 23.17 | 0.276 | 0.231 | 0.313 | 0.78 | 1.06 |
| MgSiO₃ | 6.5669 | 0.0914 | 4035 | 129.1 | 219.6 | 0.031 | 0.026 | 0.041 | 0.49 | 0.79 |

Models: MgO uses the MgO-only (PBE) model, so its pressures are on the PBE scale; MgSiO₃ uses Deng (PBEsol).

## 1. "Viscosity and diffusivity scale with O motion": supported for hot melts, but O is not singled out

- $r_{SE}$ = 0.86–1.00 Å for every hot liquid: both MgO volumes (40–190 GPa, 4000–8100 K) and MgSiO₃ from 5200 to 7100 K. η₀ varies by 6× and D_O by 5× across these, while $r_{SE}$ varies by ±8 %. So η₀ ≈ k_BT/(4π · 0.9 Å · D_O) predicts the viscosity from O diffusion to about 10 %.
- It **breaks down in deeply supercooled MgSiO₃**: $r_{SE}$ = 0.49 Å at 4035 K. From 7073 to 4035 K η rises 29×, but T/D_O rises only 16×, so ηD_O/T grows by 1.8× (as in summary §5j). With D_Si the drop is smaller (1.06 → 0.79 Å), so in the supercooled melt η follows the slowest species (Si) better than O. (Not a tetrahedral network at these pressures: see §5.)
- **O is not distinguishable from the cations at high T:** D_Mg/D_O = 0.97–1.16 in MgO, and D_Mg, D_Si and D_O agree within 30 % in hot MgSiO₃. The melts move collectively, so any species would give a near-constant $r_{SE}$. The data support "η and D scale together", not specifically "O controls".
- $r_{SE}$ ≈ 0.9 Å is well below the O²⁻ radius (≈ 1.3–1.4 Å). SE is used here as a scaling law, not as a hydrodynamic model.

## 2. "D_O depends on the O density": not as a single function of n_O

At about 6000 K:

| liquid | n_O (Å⁻³) | T (K) | D_O (Å²/ps) |
|---|---|---|---|
| MgO, V9.6397 | 0.0519 | 6010 | 1.96 |
| MgO, V6.6868 | 0.0748 | 5986 | 0.42 |
| MgSiO₃, V6.5669 | **0.0914** | **5875** (colder) | **0.57** |

- Within MgO, D_O falls 4.7× as n_O rises 44 %, consistent with the hypothesis.
- But MgSiO₃ has the **highest** O density (22 % above compressed MgO) and is 110 K colder, yet its O diffuses **36 % faster**. A single D_O(n_O, T) would make it the slowest. Per O, MgSiO₃ also has less volume (10.9 against 13.4 Å³), so "free volume per O" does not rescue it either.
- **Caveat:** the two minerals use different models (PBE vs PBEsol), and the MgO-only pressure is about 5–9 GPa higher than PBEsol at the same V. At fixed n_O this cannot reverse a 36 % difference in the wrong direction, but it should be removed in a clean test.
- Other candidate scaling variables: pressure (MgSiO₃ is at 149 GPa vs 175 GPa for MgO), or excess entropy (Rosenfeld scaling).

## 3. Clean test proposed (same model, same T, matched n_O)
Deng model for both, 6000 K (and 5000 K), 1.5 ns GK each:
1. MgSiO₃ liquid at V = 0.6/0.0748 = 8.02 Å³/atom (n_O equal to MgO V6.6868) and at 11.56 Å³/atom (n_O equal to MgO V9.6397);
2. MgO liquid with the Deng model at V6.6868 and V9.6397.
That separates n_O from pressure and from the model. About 2–4 P100-h per run (1280 / 4096 atoms), ≈ 15–25 P100-h in all.

Range caveat: the Deng model is trained to about 160 GPa. MgO at V6.6868 / 6000 K is ≈ 170 GPa on its scale (slightly outside), and MgSiO₃ at 11.56 Å³/atom is a low-pressure melt (probably < 10 GPa) that may be outside its training set. A safer variant matches n_O in the middle of the range (e.g. both at n_O ≈ 0.065–0.075 Å⁻³) and adds one more volume per mineral.

## 4. Solids
- Here D = c_v · D_v, with c_v from the formation free energy and D_v from the migration free energy, so MD MSD is useless without vacancies. The Ita & Cohen route (thermodynamic integration for ΔG_f, plus migration) is plan phases A1–A3 (`ANELASTICITY_PLAN_FE_DISLOCATIONS.md`). A0 (Frenkel–Ladd test of the bound pair) is done, and the DFT check puts a ≈ 1 eV correction on the Deng ΔG_f.
- **In solids O is not generally the controlling species:** in bridgmanite our MD already shows O vacancies fast and Mg vacancies frozen below 5000 K, and the literature (e.g. Ammann et al. 2010, Nature 465, 462) has Si as the slowest species, which controls diffusion creep. In periclase, O is the slower species (Cordier et al. 2023 use D_O). So the solid analogue of the hypothesis would be "rheology follows the slowest species", which differs between the two minerals.

## 5. Follow-up (RC 11-15: "no Si network at high pressure"; "surprised MgSiO₃ has a much higher O density than MgO")

**Si–O structure of the MgSiO₃ melt** (snapshots `liquid/{4000,7000}K/GK/eq.data`; cutoffs Si–O 2.3 Å, Mg–O 2.6 Å):

| T (K) | p (GPa) | ⟨CN Si–O⟩ | CN 5 / 6 / 7 (fraction of Si) | ⟨CN Mg–O⟩ | O bonded to 0 / 1 / 2 / ≥3 Si |
|---|---|---|---|---|---|
| 4035 | 129 | 5.95 | 0.15 / 0.75 / 0.09 | 7.7 | 0.00 / 0.23 / 0.57 / 0.20 |
| 7073 | 161 | 5.91 | 0.25 / 0.48 / 0.19 | 7.4 | 0.02 / 0.26 / 0.46 / 0.25 |

- RC is right that there is no tetrahedral (glass-forming) network: Si is octahedral. But with Si/O = 1/3 and CN ≈ 6, each O is shared by 2 Si on average, and 77 % of O bridge two or more SiO₆ units at 4000 K. The melt is a fully connected framework of edge/corner-sharing SiO₆, not a depolymerized melt. "Network former" in §1 meant this; the wording is corrected there.
- Whether it is a good glass former: in MD the MgSiO₃ melt stayed liquid for 1.5 ns at 4035 K (VFT T₀ ≈ 2800 K, summary §5j), while MgO crystallized readily below ≈ 5500 K. That is MD-time-scale evidence only.

**O density at equal P and T:** MgSiO₃ really is denser in O than MgO, in crystals as well as in melts.

| | MgO | MgSiO₃ (bridgmanite) | MgSiO₃ / MgO |
|---|---|---|---|
| ambient, volume per O (cm³/mol O) | 11.25 | 24.45 / 3 = 8.15 | n_O 1.38× |
| Deng NPT, 30 GPa / 2000 K, n_O (Å⁻³) | 0.5/8.548 = 0.0585 | 0.6/7.764 = 0.0773 | 1.32× |
| Deng NPT, 120 GPa / 2800 K, n_O (Å⁻³) | 0.5/6.781 = 0.0737 | 0.6/6.403 = 0.0937 | 1.27× |

The reason is that Si does not take space in the O framework; it sits inside the O octahedra. Si⁴⁺ is small (r ≈ 0.40 Å) and pulls its O in to 1.8 Å (Mg–O ≈ 2.1 Å in MgO), so the SiO₆ edges are short (O–O ≈ 2.5 Å, against 3.0 Å in MgO at ambient). In MgO, by contrast, every O carries one large Mg. With 3 O per formula unit and only one large cation, MgSiO₃ packs O more densely.

**At equal P and T, the two melts have the same transport.** MgO at about 149 GPa and 6000 K, interpolated between its two volumes (ln η and ln D_O linear in p at 6000 K), against MgSiO₃ at 148.7 GPa and 5875 K:

$$\ln y(p)=\ln y_1+\frac{p-p_1}{p_2-p_1}\ln\frac{y_2}{y_1} \tag{2}$$

| | η₀ (mPa s) | D_O (Å²/ps) | n_O (Å⁻³) |
|---|---|---|---|
| MgO, Eq. 2 at 148.7 GPa (model scale) | 12.9 | 0.58 | ≈ 0.07 |
| MgO, Eq. 2 at 156 GPa (≈ 148.7 GPa on the PBEsol scale, +7 GPa PBE offset) | 14.3 | 0.53 | ≈ 0.072 |
| MgSiO₃, 148.7 GPa, 5875 K | 12.8 | 0.57 | 0.0914 |

- So η₀ and D_O agree within about 10 % at equal p and T, although MgSiO₃ has ≈ 27 % more O per volume. The two-point interpolation and the 110 K offset (≈ 7 % in D) set the uncertainty.
- **Revised reading of RC's hypothesis:** transport in these high-pressure melts is governed by O mobility as a function of p and T, nearly independent of composition; it is not set by the O number density. The matched-density test of §3 would turn into a matched-*pressure* test: Deng-model MgO and MgSiO₃ at the same (p, T) over 50–150 GPa and 4000–7000 K would test this directly and remove the model difference.

## 6. Matched-(P, T) test, Deng model for both liquids (job 6931065, analysed 2026-11-16)

Runs: `/groups/carnegie_poc/rcohen/LAMMPS/LiquidPT_Deng` (README there). MgO 1000 atoms (melted at 10000 K), MgSiO₃ 1280 atoms; NPT 60 ps → mean box → 1.5 ns NVE GK. Tool `tools/liquid_pt.py` (η₀ at $t_c$ = 1 ps with 8-block errors, Eq. 1; D from the second half of the MSD, Eq. 2; $r_{SE}$ by Eq. 1 at the top). Table `liquid_pt.txt`, figure `liquid_pt.{pdf,png}` (this directory). Every state stayed liquid (O MSD 4000–21000 Å² at 1.5 ns), including MgO at 150 GPa / 6000 K.

| liquid | target (GPa, K) | T_NVE (K) | p (GPa) | V (Å³/atom) | n_O (Å⁻³) | η₀ (mPa s) | D_Mg | D_Si | D_O (Å²/ps) | r_SE (Å) |
|---|---|---|---|---|---|---|---|---|---|---|
| MgO | 50, 6000 | 6046 | 50.2 | 9.507 | 0.0526 | 3.25 ± 0.04 | 1.93 | – | 1.92 | 1.06 |
| MgSiO₃ | 50, 6000 | 6092 | 50.6 | 8.810 | 0.0681 | 3.03 ± 0.07 | 1.81 | 1.66 | 2.37 | 0.93 |
| MgO | 100, 6000 | 5997 | 100.1 | 7.819 | 0.0639 | 7.35 ± 0.19 | 0.92 | – | 0.95 | 0.94 |
| MgSiO₃ | 100, 6000 | 6159 | 101.2 | 7.349 | 0.0816 | 6.38 ± 0.12 | 1.34 | 0.79 | 1.21 | 0.87 |
| MgO | 150, 6000 | 5937 | 149.5 | 6.933 | 0.0721 | 13.49 ± 0.21 | 0.54 | – | 0.46 | 1.05 |
| MgSiO₃ | 150, 6000 | 6007 | 150.1 | 6.565 | 0.0914 | 11.72 ± 0.30 | 0.55 | 0.55 | 0.65 | 0.87 |
| MgO | 100, 7000 | 7092 | 100.7 | 8.006 | 0.0625 | 4.52 ± 0.14 | 1.68 | – | 1.56 | 1.11 |
| MgSiO₃ | 100, 7000 | 6809 | 98.4 | 7.531 | 0.0797 | 4.29 ± 0.08 | 1.69 | 1.77 | 1.91 | 0.91 |

(T_NVE is the mean of the NVE run; it differs from the target by up to 3 %, worth up to ≈ 10 % in D.)

**Results**
- **At equal p and T the two melts have nearly the same viscosity:** η₀(MgSiO₃)/η₀(MgO) = 0.93, 0.87, 0.87 at 50, 100, 150 GPa (6000 K) and 0.95 at 100 GPa / 7000 K. Both rise 4× from 50 to 150 GPa.
- **O diffuses 25–40 % faster in MgSiO₃ than in MgO at the same (p, T)** (D_O ratio 1.23, 1.28, 1.40 at 6000 K; 1.22 at 7000 K, where MgSiO₃ is 280 K colder), although MgSiO₃ has 23–30 % more O per volume.
- **D_O is not a single function of n_O** (panel c): the two minerals lie on separate curves 0.015–0.02 Å⁻³ apart; at equal n_O ≈ 0.07 Å⁻³, D_O(MgSiO₃) ≈ 2.4 Å²/ps against ≈ 0.6 Å²/ps for MgO, a factor ≈ 4. Against p (panel b) the two curves are parallel and close (ln D_O falls by 1.3–1.4 per 100 GPa in both).
- **Stokes–Einstein holds in both** with nearly constant radii: r_SE = 0.94–1.11 Å (MgO) and 0.87–0.93 Å (MgSiO₃). With one model the 10 % offset is real: for a given η₀, O moves ≈ 15 % faster in MgSiO₃.
- The model artefact of §2 is gone: the earlier MgO-only (PBE) comparison gave η₀ 12.9 vs 12.8 mPa s and D_O 0.58 vs 0.57 at ≈ 149 GPa; with the Deng model for both, η₀ 13.5 vs 11.7 and D_O 0.46 vs 0.65 at 150 GPa. The conclusion is unchanged in sign, sharper in size.

**Answer to RC's hypothesis (revised again):**
1. "Viscosity and diffusivity scale with O motion": yes, within each liquid, η₀ ∝ T/D_O to ±10 % over 50–150 GPa and 6000–7000 K (constant r_SE); the constant differs by ≈ 15 % between the two compositions.
2. "D_O depends on the O number density": not as a universal variable. At fixed n_O the two minerals differ by ≈ 4× in D_O; at fixed p and T they differ by only 1.2–1.4×. Pressure (with T) is the better scaling variable for these high-pressure melts; n_O carries a composition-specific offset (Si sits inside the O framework, §5, so a denser O packing in MgSiO₃ does not mean less free volume for O motion).
3. Next test: excess-entropy (Rosenfeld) scaling, s₂ from g(r) of the same states, would tell whether a single structural variable collapses both minerals. **Submitted 11-16** (job 6963196, 50 ps g(r) reruns, `tools/liquid_rdf.lammps`; analysis `tools/rosenfeld.py`; `LiquidPT_Deng/README.md`).

## 7. Excess-entropy (Rosenfeld) scaling (jobs 6963196 → 6999519, analysed 2026-11-16)
Partial g_ab(r) of the 8 matched-(P, T) liquids of §6: 50 ps NVT at the same box (`tools/liquid_rdf.lammps`; 360 bins to 9 Å; mean |g − 1| beyond 8 Å ≤ 0.03, which contributes ≤ 0.01 k_B to s₂). Analysis `tools/rosenfeld.py`; output `rosenfeld.txt`, figure `rosenfeld.{pdf,png}` (here and in `LAMMPS/LiquidPT_Deng`). η₀ and D are from §6.

$$\frac{s_2}{k_B}=-2\pi\rho\sum_{ab}x_ax_b\int_0^{r_c}\left[g_{ab}\ln g_{ab}-(g_{ab}-1)\right]r^2dr \tag{3}$$

$$D_O^*=D_O\,\rho^{1/3}\sqrt{m_O/k_BT},\qquad \eta^*=\eta_0\,\rho^{-2/3}\,(\bar m\,k_BT)^{-1/2} \tag{4}$$

| liquid | p (GPa) | T (K) | −s₂/k_B | D*_O | η* | η*·D*_O |
|---|---|---|---|---|---|---|
| MgO | 50 | 6046 | 2.74 | 0.051 | 2.76 | 0.141 |
| MgO | 100 | 5997 | 3.49 | 0.027 | 5.50 | 0.149 |
| MgO | 150 | 5937 | 4.06 | 0.014 | 9.37 | 0.129 |
| MgO | 101 | 7092 | 2.89 | 0.041 | 3.16 | 0.128 |
| MgSiO₃ | 51 | 6092 | 2.52 | 0.065 | 2.44 | 0.158 |
| MgSiO₃ | 101 | 6159 | 3.12 | 0.035 | 4.53 | 0.158 |
| MgSiO₃ | 150 | 6007 | 3.57 | 0.020 | 7.81 | 0.153 |
| MgSiO₃ | 98 | 6809 | 2.58 | 0.052 | 2.94 | 0.153 |

Fits (ln y = A + B s₂/k_B):

| | MgO | MgSiO₃ | both |
|---|---|---|---|
| D*_O | −0.41 + 0.94 s₂ (rms 0.06) | −0.18 + 1.04 s₂ (rms 0.07) | −0.39 + 0.96 s₂ (rms 0.08) |
| η* | −1.53 − 0.93 s₂ (rms 0.003) | −1.66 − 1.03 s₂ (rms 0.06) | −1.37 − 0.90 s₂ (rms 0.10) |

- **One structural variable collapses both melts.** Against s₂, D*_O of MgO and MgSiO₃ falls on one line within 8 % rms. Against the O number density (§6) the same points were ≈ 4× apart. η* collapses within 10 % rms, with MgSiO₃ ≈ 15–20 % above MgO at equal s₂.
- **The exponents (0.9–1.0) and prefactor (D* ≈ 0.68 e^{0.96 s₂}) are close to Rosenfeld's universal liquid relations** (D* ≈ 0.6 e^{0.8 s_ex}, η* ≈ 0.2 e^{−0.8 s_ex}; Rosenfeld 1977, Phys. Rev. A 15, 2545; 1999, J. Phys.: Condens. Matter 11, 5415). Our exponents are a little larger because s₂ is only the two-body part of s_ex.
- **Reduced Stokes–Einstein:** η*·D*_O = 0.13–0.16, constant to ±10 % across both liquids. That is the reduced-unit form of §6's constant r_SE.
- **Answer to RC's hypothesis (final):** O motion controls viscosity in both melts. The variable that sets D_O is not the O number density but the structural (pair) excess entropy, which combines density, temperature and composition. Pressure works almost as well (§6) because s₂ is close to a single function of p at fixed T for these two melts. This is a liquid result only; in the solids the rate is set by vacancy concentration and barriers (§4; `results_freeenergy/`).
