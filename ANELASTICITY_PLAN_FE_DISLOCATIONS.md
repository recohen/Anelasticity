# Plan: vacancy free energies, diffusion and dislocations in MgO and MgSiO₃ (2026-10-13)

**RC request (10-13):**
1. Do the free-energy integrations of Ita & Cohen (1997, 1998) to get vacancy formation free energies and diffusion rates.
2. Put in dislocations: Guan et al. (2026) report a slip-system change in bridgmanite at about 1800 K.
3. Compare with Perez et al. (2025) for MgO at high strain rate.

Papers are in `Papers/`:
- Ita & Cohen, PRL 79, 3198 (1997): `PhysRevLett.79.3198.pdf`.
- Ita & Cohen, GRL 25, 1095 (1998): `Ita_et_al-1998-...pdf`.
- Cordier et al., Nature 613, 303 (2023): `s41586-022-05410-9.pdf`.
- Guan et al., Commun. Earth Environ. 7, 183 (2026): `s43247-026-03212-9.pdf` and its SI.
- Perez et al., PRB 111, 144108 (2025): `Perez.pdf`.

## 0. Why this matters, and what the papers set up

- **Cordier et al. 2023.**
  - Claim: periclase deforms 10³–10⁷× more slowly than bridgmanite at mantle strain rates, so the lower mantle's rheology is that of bridgmanite.
  - Basis: climb in MgO is limited by O self-diffusion, which they take from the **Ita & Cohen fit** (their Eq. 1, Table 1). D_O falls to 10⁻³¹ m²/s at 90–120 GPa.
  - Bridgmanite side: pure climb creep (Reali et al. 2019) with an assumed vacancy fraction $X_v=10^{-5}$.
  - The conclusion therefore rests on (i) D_O(P,T) in MgO and (ii) diffusion in bridgmanite. Both are what an Ita–Cohen-type calculation gives, and DeePMD can now do it for both minerals with the same model.
  - *Note:* Cordier Table 1 lists $E_0=0.4\times10^{-19}$ J. Their Table 2 enthalpies (9.15 eV at 30 GPa, 15.09 eV at 120 GPa) are reproduced only with Ita & Cohen's $E_0\approx9.4\times10^{-19}$ J (5.9 eV) for O. The 0.4 appears to be a typo; only Table 1 is affected.
- **Guan et al. 2026** (25 GPa, 1700–2100 K, strain rates 10⁻⁶–10⁻⁴ s⁻¹):
  - The dominant slip system changes at about 1800 K, from [010](100) below to [100](010) above.
  - The authors argue that dislocation creep, not diffusion or pure climb creep, may control the lower mantle.
  - The mechanism of the change is unknown. A temperature-dependent crossover of the lattice friction (Peierls stress) or mobility of the two systems is the obvious candidate, and MD can test it directly.
- **Perez et al. 2025** (laser-driven Richtmyer–Meshkov):
  - Solid single-crystal MgO has an effective viscosity of at most about $10^2$ Pa s at 175 ± 15 GPa, about 3500 K and $\dot\varepsilon=10^6$–$10^7$ s⁻¹. That implies a flow stress of about 1 GPa or less.
  - The conditions are close to our V6.6868 MgO crystal (140–190 GPa).
  - In the athermal glide regime, a drag-controlled dislocation population has the Newtonian effective viscosity of Eq. 12 below. MD can compute the drag coefficient $B$ at these conditions.
- **Correction to our own records (summary §5c, and the bridgmanite "≈ 1.9 eV per pair" note in `crystal_VMgO/README.md`).**
  - The fixed-V quantity $E(N-2)-\frac{N-2}{N}E_{perf}$ (2.44 eV in MgO) leaves out the $P\,v_f$ term of Eq. 3 below. At 140–190 GPa that term is of order $P\cdot2\Omega\approx$ 12–16 eV.
  - Ita & Cohen's bound-pair $\Delta G_f$ is 13–17 eV at 80–140 GPa.
  - Thermal Schottky pairs are therefore **not** expected near 5000 K. The extra vacancies seen above 4500 K in fixed-N MD (§5a, "atoms in flight") must be Frenkel pairs.
  - The free-energy work below gives the correct numbers.

## 1. Vacancy formation free energies (Ita & Cohen Eqs. 2–6, nonequilibrium version)

**Method.** Frenkel–Ladd switching to an Einstein crystal, as in Ita & Cohen (adiabatic switching, de Koning–Antonelli λ(t), their Eq. 6). In LAMMPS this is `fix ti/spring` (Freitas, Asta & de Koning, Comput. Mater. Sci. 112, 333 (2016)), which is present in our deepmd_py311 build.

Hamiltonian along the path:

$$H(\lambda)=(1-\lambda)\,U_{DP}+\lambda\sum_i\tfrac12k_{s(i)}\,|\mathbf r_i-\mathbf r_{i0}|^2+K \tag{1}$$

Free energy of the solid, with forward (f) and backward (b) switching to cancel dissipation:

$$F=F_E-\tfrac12\left(W_f-W_b\right),\qquad W_{f,b}=\int\Big\langle \sum_i\tfrac12k\,\Delta r_i^2-U_{DP}\Big\rangle\,d\lambda \tag{2}$$

The Einstein reference (classical) includes the fixed-centre-of-mass correction $\Delta F_{CM}$:

$$F_E=3k_BT\sum_i\ln\frac{\hbar\omega_i}{k_BT}+\Delta F_{CM},\qquad \omega_i=\sqrt{k_{s(i)}/m_i} \tag{2a}$$

The spring constant comes from the equilibrium MSD:

$$k_s=\frac{3k_BT}{\langle\Delta r^2\rangle_s} \tag{2b}$$

Formation Gibbs energy of a defect with L vacant sites in an N-site cell (Ita & Cohen PRL Eq. 3):

$$\Delta G_f=F_D^{N-L}(V_D)-\frac{N-L}{N}F_I^N(V_I)+P\left[V_D-\frac{N-L}{N}V_I\right] \tag{3}$$

$V_I$ and $V_D$ come from NPT runs at (P, T). The deepmd_py311 build has `fix npt` for MgO and an orthorhombic `aniso` barostat for Pbnm.

**Defects:**
- **MgO** (Ita & Cohen):
  - bound Schottky pair (V_Mg + V_O nearest neighbours);
  - separated pair (maximum separation in a 1000-atom cell, with image correction);
  - binding $\Delta G_b$ from the difference.
- **Bridgmanite:**
  - MgO partial Schottky (V_Mg + V_O, bound and separated). This is the cell type already in MD, `crystal_VMgO`.
  - SiO₂ partial Schottky (V_Si + 2V_O).
  - Full Schottky (V_Mg + V_Si + 3V_O).
- **Chemical reference for partial Schottky defects.** The removed MgO (or SiO₂) unit goes to coexisting periclase (or the SiO₂ phase), so the formation energy needs the corresponding chemical potential:

$$\Delta G_f^{MgO\text{-}PS}=G_D-G_I+g_{MgO}^{per}(P,T) \tag{4}$$

  So **MgO must be computed with the same model as bridgmanite**. X. Deng's MgSiO₃ model was trained on MgO crystal and melt at 20–160 GPa (`input_v2_compat.json`: `64mg64o.NPT_20-160GPa`), so it can serve as the reference. Cross-check: the bound-pair ΔG_f in MgO from the MgO-only model (`graph_c.pb`, md5 6357206b) against the Deng model (`graph_c.pb`, md5 0e06a7e2).

**Practical points:**
- **Mobile vacancies at high T.** A vacancy that hops during the switch breaks the tether (the hopping atom pays $\tfrac12k\ell^2$ of several eV). Check every switching run for displacements greater than half a jump length and discard or shorten as needed. Ita & Cohen used 10–15 ps switches up to 5000 K.
- **Independent check where hops are frequent:** integrate the enthalpy difference from a lower temperature $T_0$, where the vacancies stay put:

$$\frac{\Delta G_f(T)}{T}=\frac{\Delta G_f(T_0)}{T_0}-\int_{T_0}^{T}\frac{\Delta H_f(T')}{T'^2}\,dT' \tag{5}$$

  For the Deng model (fparam = $k_BT$), add $\langle\partial U/\partial T\rangle$ by rerunning the frames with fparam shifted.
- **Precision target:** σ(ΔG_f) ≤ 0.1 eV. This needs about 0.1 meV/atom on F for 500–1300-atom cells: 5–10 independent forward/backward pairs per state.
- **Cell sizes:** MgO 512 (4×4×4, as Ita's 216–1000 range) with a 1000-atom size check; bridgmanite 1280 (the existing box) with a 640-atom check.

## 2. Migration free energies and diffusion

**Migration free energy:** a free-energy profile along the jump coordinate $\xi=(\mathbf r_j-\mathbf r_{ref})\cdot\hat e$, with transverse relaxation free (as Ita & Cohen):

$$\Delta G_m=-k_BT\ln\frac{P(\xi^\ddagger)}{\int_{\rm well}P(\xi)\,d\xi}\;\;\text{or}\;\;\Delta G_m=-\int_{\xi_0}^{\xi^\ddagger}\langle F_\xi\rangle_\xi\,d\xi \tag{6}$$

- **Implementation:** PLUMED (`fix plumed` is linked into our build), umbrella windows plus WHAM. Use the jump symmetry: run half the path.
- **Rate (transition-state theory):**

$$\Gamma=\nu^*\,e^{-\Delta G_m/k_BT} \tag{7}$$

  $\nu^*$ is measured as Ita & Cohen did (Fourier transform of the migrating ion's motion projected on the path; they found 5.2 THz).
- **Validation:** compare Eq. 7 with the **direct MD hop rates we already have**: MgO §5a at 3500–5000 K, and bridgmanite V_O and V_Mg from 10-13 at 3000–5000 K. Then use Eq. 7 down to mantle temperatures (2000–2800 K), where MD cannot see hops.

**Self-diffusion coefficient** (Ita & Cohen Eq. 1, intrinsic):

$$D_i=\frac{Z_f}{6}Z_m\,\ell^2\,\nu\,\exp\!\left(-\frac{\Delta G_f}{W k_BT}-\frac{\Delta G_m}{k_BT}\right) \tag{8}$$

For MgO, W = 2, $Z_f$ = 1, $Z_m$ = 12 (Schottky); W = 1, $Z_f$ = 6, $Z_m$ = 8 (bound). For bridgmanite the analogous factors come from the site multiplicities of Pbnm.

The extrinsic case (GRL 1998) replaces $e^{-\Delta G_f/Wk_BT}$ with the impurity-fixed vacancy fraction $X_v$:

$$D_i=\tfrac16 Z_m\ell^2\nu\,X_v\,e^{-\Delta G_m/k_BT} \tag{9}$$

**Fit of D(P,T)**, for direct comparison with Cordier's use of Ita & Cohen (their Eq. 1):

$$\ln D=\ln(a^2\nu)+\frac{S_0+PS_0'}{k_B}-\frac{E_0+PV_0+P^2V_0'}{k_BT} \tag{10}$$

**Deliverables:**
1. Validation against Ita & Cohen (VIB model) at their grid: 20 GPa / 2000 K, 80 GPa / 2000 and 4000 K, 140 GPa / 3000 and 5000 K.
2. D_O, D_Mg in MgO and D_O, D_Mg, D_Si in bridgmanite along Cordier's geotherm points: 30 GPa / 2000 K, 60 / 2300, 90 / 2500, 120 / 2800. Both intrinsic and extrinsic (Eq. 9 with $X_v=10^{-5}$, Cordier's value).
3. The climb-limiting ratio: D_O(periclase) against D_Si (or the slowest species) in bridgmanite. **This directly tests Cordier's conclusion.**
4. Feed into anelasticity: the vacancy-mediated relaxation times (Nabarro–Herring / grain-scale, summary §5d model) at seismic frequencies.

## 3. Dislocations

### 3a. MgO at high pressure and strain rate (Perez)

**Started 10-13 (RC: "we should also pursue the comparison with Perez").**
- **Model: the MgO-only model** (`graph_c.pb`, md5 6357206b, the one used for the V6.6868 anelasticity runs at 140–193 GPa). Perez's 175 GPa lies above the Deng model's 160 GPa training limit.
- **Tools:**
  - `tools/build_mgo_edge_slab.py`: x = [110], y = [001], z = [1-10]; two-block edge construction.
  - `tools/npt_lattice.lammps`: a(P, T).
  - `tools/disl_drive.lammps`: rigid blocks; piston normal force −P·A on the top block; resolved shear τ as a force on the top block; output `drive.dat`.
  - `tools/disl_job.sh`: chains NPT → build → drive.
  - `tools/disl_velocity.py`: v from the plastic slip of the top block (Δx_top = b per sweep of Lx), then B = bτ/v and η_eff = B/(ρb²) for ρ = 10¹³–10¹⁶ m⁻².
- **First production:** edge, 175 GPa, 3500 K, τ = 0.1, 0.25, 0.5, 1.0 GPa, 8232 atoms (24 × 14 × 6). The lowest τ that moves the dislocation bounds the Peierls stress at 3500 K; compare with Perez's yield strength (≲ 1 GPa).
- **Next:** screw character; T = 2000 and 5000 K; {110} slip for comparison; size check (NX = 48).

- **Slip system above 50 GPa:** ½⟨110⟩{100} (Amodeo et al. 2012; Cordier 2012). Build edge and screw dislocation dipoles (quadrupolar periodic arrangement) at V6.6868 with Volterra displacements, then relax.
  - New tool: `tools/build_dislocation.py` (Volterra fields plus image sum).
  - atomsk and ovito are not installed. Core tracking uses LAMMPS centro-symmetry / CNA (both in the build) and the disregistry.
- **0 K Peierls stress** under an incremental shear, at 0, 50, 140 GPa. Check against Amodeo et al. 2012 (pressure-induced {110} → {100} change).
- **Drag coefficient** at 3500 K, 175 GPa: steady velocity under a constant applied resolved shear stress τ = 0.1–2 GPa, for edge and screw:

$$v=\frac{b\,\tau}{B} \tag{11}$$

- **Effective viscosity of a glide-controlled crystal** (Orowan, $\dot\varepsilon=\rho b v$):

$$\eta_{eff}=\frac{\tau}{\dot\varepsilon}=\frac{B}{\rho\,b^2} \tag{12}$$

  Compare with Perez's bound $\eta\le10^2$ Pa s and yield strength ≲ 1 GPa. Example: $B\approx10^{-4}$ Pa s, b = 2.6 Å and ρ = 10¹⁴ m⁻² give η ≈ 15 Pa s, the right order. Direct check: shear a dislocation-bearing cell at $\dot\varepsilon$ = 10⁸–10⁹ s⁻¹ and measure the flow stress.
- **Anelasticity link:** Granato–Lücke string damping. With line tension $C\approx\mu b^2/2$ and segment length L, the overdamped string has

$$\tau_d=\frac{B L^2}{\pi^2 C} \tag{13}$$

  This places a dislocation loss peak at a frequency fixed by B (from MD) and L. It is a candidate for the seismic-band loss that point defects do not give (summary §5c).

### 3b. Bridgmanite slip systems (Guan)

- **Systems:** [100](010) and [010](100), edge and screw, in Pbnm; b ≈ 4.7–4.9 Å at 25 GPa.
- **Conditions:** 25 GPa (Guan's pressure, inside the Deng training range) at T = 1400, 1700, 1900, 2200, 2500 K. Also V6.5669 (about 110 GPa, our MgO–MgSiO₃ comparison volume) at 2500 and 3500 K. *This leaves V6.5669, so it needs RC's approval (see §5).*
- **Measured:** critical resolved shear stress (CRSS) under a slow stress ramp, and the velocity–stress relation, for each system against T. Guan's change at about 1800 K predicts that the CRSS of [100](010) falls below that of [010](100) above about 1800 K at 25 GPa.
- **Static check first:** 0 K γ-surfaces and Peierls stresses (cheap, minimizations), against Kraych/Carrez (Lille).
- **Cost driver:** large cells (b ≈ 4.8 Å needs 30–60 k atoms for a dipole). 1268 atoms run at 85 steps/s on a P100, so 40 k atoms run at about 2.5 steps/s, about 11 h per 100 ps.

## 4. Cost estimate (P100-hours) and order

| phase | content | P100-h |
|---|---|---|
| A0 | TI machinery test: perfect and bound-pair MgO (512 / 510 atoms) at 80 GPa / 2000 K and 140 GPa / 3000 K against Ita & Cohen (13.2 and 15.8 eV); spring constants, switching-time convergence | ≈ 8 |
| A1 | MgO formation (bound and separated) at the Ita grid (5 states) and the Cordier geotherm (4 states), MgO-only model plus Deng model at 2 states | ≈ 60 |
| A2 | MgO migration (Mg, O) by umbrella sampling at the same states; validation against §5a rates | ≈ 50 |
| A3 | Bridgmanite formation (3 defect types) and migration (Mg, Si, O) at the geotherm states and V6.5669 | ≈ 140 |
| B1 | MgO dislocations: builder, 0 K Peierls, drag at 3500 K / 175 GPa (edge, screw; 4 stresses), $\dot\varepsilon$-controlled check | ≈ 100 |
| B2 | Bridgmanite: γ-surfaces and 0 K Peierls (CPU or GPU, cheap), then finite-T CRSS for 2 systems × 2 characters × 5 T at 25 GPa | ≈ 300–400 |

**Proposed order:**
1. A0 now (test scale).
2. A1 and A2.
3. A3, in parallel with B1.
4. B2 last; it is the most expensive.

## 5. Decisions (RC, 2026-10-13)

1. **P–T grid:** Ita & Cohen validation points plus the four Cordier geotherm points. ✔
2. **Bridgmanite defects:** all three Schottky types (MgO partial, SiO₂ partial, full). ✔
3. **Model:** X. Deng's model for both minerals ("if it is trained on MgO"). Checked, from the files listed in `input_v2_compat.json`:

   | composition | phase | frames (128–160-atom cells, 20–160 GPa) |
   |---|---|---|
   | MgO | B1 crystal, 300 K–9000 K | 1600 |
   | MgO | melt | 1000 |
   | MgSiO₃ | bridgmanite / post-perovskite | 1600 / 1200 |
   | Mg–Si–O | melts, various x | 12258 |
   | SiO₂ | stishovite, CaCl₂, pyrite, melt | 7300 |

   One system (`MgSiO.09.64mg64o.melt.lambda_6k`) has no data files. **Caveat:** there are no defect, surface or dislocation configurations, so defect energetics are extrapolated from crystals and melts. Phase A0 therefore adds a DFT spot check: relaxed bound-pair and separated-pair energies in 128- and 250-atom MgO and a 160-atom bridgmanite V_Mg + V_O cell, VASP at 0 K, against DeePMD at the same geometry.
4. **Chemical potentials** in a periclase-saturated assemblage: $\mu_{MgO}=g_{per}$ and $\mu_{SiO_2}=g_{Bdm}-g_{per}$, both from the same model. This replaces the $g^{per}_{MgO}$ of Eq. 4 for the SiO₂-type defects.
5. **Dislocations:** bridgmanite at 25 GPa (Guan) and at V6.5669. ✔ ovito was not asked about; core positions come from LAMMPS CNA / centro-symmetry and the disregistry unless RC wants ovito installed.

## 6. Comparison with previous work (RC 10-13: "we should compare with previous work")

Every result gets a comparison table against earlier calculations and experiments at matching (P, T). References still to collect into `Papers/` are marked (†). Citations from memory are to be checked against the PDFs before they appear in a summary.

| quantity | previous work to compare with |
|---|---|
| MgO bound and separated pair $\Delta G_f$, $\Delta G_m$ (Mg, O), 0–140 GPa | Ita & Cohen 1997 (PRL, Table I) and 1998 (GRL, Table 1), VIB model, MD free-energy integration; Karki & Khanduja 2006, Am. Mineral. 91, 511 (DFT, static) (†); Runevall & Sandberg 2011, JPCM 23, 345402 (DFT) (†); Ammann, Brodholt & Dobson 2010, RiMG 71, 201 (†) |
| MgO $D_O$, $D_{Mg}$ (P, T); fit Eq. 10 | Yang & Flynn 1994 PRL (intrinsic O, experiment); Van Orman et al. 2003 GRL (high-P experiment); Ita & Cohen fit as used by Cordier et al. 2023 (Table 1, with $E_0$ corrected to 9.4×10⁻¹⁹ J) |
| bridgmanite vacancy formation and migration, D_Si, D_O, D_Mg | Wright & Price 1993 JGR (static, empirical potentials; cited by Ita & Cohen 1998); Ammann et al. 2010 Nature 465, 462 (DFT, diffusion in lower-mantle minerals) (†); Reali et al. 2019 Sci. Rep. 9, 2053 (the D used in pure climb creep; Cordier's bridgmanite side); Xu et al. 2011 EPSL (Si and O self-diffusion in bridgmanite, experiment) (†); Holzapfel et al. 2005 Science (Si diffusion in bridgmanite, experiment) (†) |
| our own MD rates | MgO §5a (MD hop rates 3500–5000 K) and §5b (static NEB); bridgmanite V_O / V_Mg rates (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.3) |
| MgO dislocation Peierls stress, slip change {110} → {100} with P | Amodeo, Carrez & Cordier 2012 Phil. Mag. 92, 1523 (cited in Cordier 2023); Cordier et al. 2012 Nature 481, 177 |
| MgO drag and high-rate viscosity | Perez et al. 2025 PRB (η ≤ 10² Pa s, 175 GPa, about 3500 K); drag-scaling assumption $B\propto T$ in Cordier 2023 Methods (B from 300 K experiment) |
| bridgmanite slip systems against T | Guan et al. 2026 (change at about 1800 K, 25 GPa); Kraych, Carrez & Cordier 2016 EPSL 452, 60 (glide model); Peierls–Nabarro studies cited by Guan (refs 33–35) (†); Hirel et al. 2020 Acta Mater. (twin walls, in `Papers/`) |
| MgO–MgSiO₃ creep contrast | Cordier et al. 2023 Fig. 2b ($\eta_{Per}/\eta_{Bdm}$ = 10³–10⁷ along the geotherm) |
