# Literature notes, 2026-10-15: grain boundaries, dislocations and grain size (papers RC added to `Papers/`)

Digests were made by reading the full texts; numbers read from figures are marked (fig.). Inferences of ours are marked [ours]. Items marked † still need checking against the PDF before they are cited in a paper.

## 1. van Driel thesis (UCL 2021) and van Driel et al. 2020 (PCM 47:11): Σ5 (310)/[001] in MgO, bridgmanite boundaries

### MgO Σ5 (310)/[001] (thesis Ch. 4; the paper)

- **Method:**
  - DFT (PBE, plus an LDA check) at 0 K;
  - AIRSS search for boundary structures;
  - one CSL period by one tilt-axis period (about 260 atoms; two boundaries);
  - CI-NEB at constant V with 20 atoms fixed at the grain centres;
  - the coupled translation is **prescribed** as a₀/10[310].
  - No MD, no temperature, no disconnections.
- **Structure sequence (PBE, Table 4.1):**

| P (GPa) | structure | γ_gb (J/m²) | V_gb (Å³/Å²) |
|---|---|---|---|
| 1.2 | A (open, voided) | 1.47 | 1.201 |
| 21.4 | C (compact, asymmetric, rigidly shifted) | 2.72 | 0.335 |
| 61.5 | C | 4.15 | 0.230 |
| 91.5 | C | 5.06 | 0.203 |
| 101.6 | D (half-plane offset along [001], "dislocation pipes") | 5.18 | 0.093 |
| 121.6 | D | 5.48 | 0.083 |

  - A → C happens at about 5–6 GPa and C → D at about 90–100 GPa.
  - The symmetric kite structure (B) of earlier work is never the ground state; it is the saddle of C's migration.
  - LDA gives the same sequence, with γ about 0.3 J/m² higher.
- **Barrier and 0 K critical stress of shear-coupled migration:**

| structure | migration barrier | critical stress, σ_c = max dγ/du |
|---|---|---|
| A | 0.49–0.52 J/m² | – |
| C | 32 mJ/m² (11 GPa), peak 64 mJ/m² (41 GPa), 26 mJ/m² (91.5 GPa) | 0.8–2 GPa |
| D | 199 mJ/m² (101.6 GPa), ≈ 257 mJ/m² (121.6 GPa) (fig.) | ≈ 8–12 GPa (fig.) |

  - Coupling factor: β = 1.00 (C) and 0.97 (D), the ⟨110⟩ mode.
- **Rate law:** v = ν u exp[−γ(σ) d²/k_BT], where d is the *grain size*, i.e. a whole boundary face moves coherently. On that basis, shear-coupled migration is negligible for d > 0.05 µm.

**Against ours:**
1. **Pressure trend agrees.** Our boundary slides at about 20 GPa and is locked at 140 GPa, which matches regime C (barrier ≈ 50 mJ/m², σ_c ≈ 1.5 GPa) followed by D. Their D barrier extrapolated to 140 GPa [ours] is about 0.30 J/m², inside our collective NEB range of 0.17–0.5 J/m².
2. **Coupling mode differs.** Our MD coupling factor of 0.6 is the ⟨100⟩ mode (2 tan(θ/2) = 0.667); their prescribed path is the ⟨110⟩ mode (1.0). Their barriers may therefore belong to a different mechanism from the one our MD selects.
3. **Onset stress.** Our driven onset at 140 GPa (1.5–3 GPa at 4000–5000 K) is 4–8× below their 0 K σ_c for D. That is the expected direction (thermal activation; larger cells).
4. **The extensive-barrier rate law is their key pitfall.** Our step to explicit disconnections (plan G1–G3) supplies what is missing.

### Bridgmanite boundaries (thesis Ch. 5–6)

- **GAP potential:** PBE, 1000 eV, about 30 000 structures; no boundaries or defects in training, but checked against DFT for boundaries to 1.7 % in γ.
- **Boundaries:** six [100] tilt boundaries, (011), (012), (013), (014), (021) and (023), at 25–125 GPa. AIRSS + GAP structure search; MD at 1800–4900 K on 8–13.5 k atoms.
- **Energies:** γ_gb is 1.4–3.2 J/m² at 25 GPa and 2.9–6.9 J/m² at 125 GPa; (021) is lowest, 1.41 J/m² at 25 GPa. Transitions: (013) near 75 GPa and (021) near 80 GPa.
- **Boundary diffusion** (D₀ fixed across P):

| species | log₁₀ D₀ (m²/s) | ΔH (eV) | ΔV (cm³/mol) |
|---|---|---|---|
| Mg | −6.69 | 1.61 | 1.45 |
| Si | −6.0 | 2.12 | 1.54 |
| O | −6.2 | 1.44 | 2.00 |

  - Diffusive width 0.6–1.1 nm.
  - D_gb(Si) = 2.0×10⁻¹³ m²/s at 23 GPa / 1866 K. That is about 10³ above Yamazaki et al. 2000, which they attribute to D₀.
- **Coble viscosity** matches lower-mantle profiles for d = 5 mm–4 cm (Ch. 6; Ch. 7 says 6 mm–3 cm).
- **No driven MD, no sliding friction, no Q⁻¹.**

## 2. Dislocations in MgO: Cordier, Amodeo & Carrez 2012 (Nature 481, 177, plus SI); Carrez et al. 2009 (MSMSE 17, 035010)

**Carrez 2009 (1D Peierls–Nabarro from GGA γ-lines):**

| P | {110}: γ_max | {110}: ideal shear stress | {100}: γ_max | {100}: ideal shear stress |
|---|---|---|---|---|
| 0 GPa | 1.05 J/m² | 13.1 GPa | 2.18 J/m² | 25.3 GPa |
| 60 GPa | 3.72 J/m² | 45.3 GPa | 3.67 J/m² | 42.7 GPa |
| 100 GPa | 5.28 J/m² | 65.8 GPa | 4.11 J/m² | 48.3 GPa |

- Elastic constants:

| P | C₁₁ (GPa) | C₁₂ (GPa) | C₄₄ (GPa) |
|---|---|---|---|
| 0 GPa | 279 | 93 | 146 |
| 60 GPa | 778 | 179 | 187 |
| 100 GPa | 1088 | 230 | 202 |

- 1D-PN gives τ_p({100} edge) = 9.5–11 GPa at 60–100 GPa. The narrow-core 1D model fails here (see below).

**Cordier 2012 (Peierls–Nabarro–Galerkin cores, elastic-interaction kink-pair model, Orowan / dislocation dynamics):** Peierls stress τ_p (MPa) / ΔH₀ (eV):

| P (GPa) | screw {110} | screw {100} | edge {110} | edge {100} |
|---|---|---|---|---|
| 0 | 150 / 1.18 | 1600 / 2.57 | 80 / 0.68 | 300 / 2.92 |
| 30 | 600 / 3.89 | 750 / 3.40 | 310 / 2.38 | 570 / 5.55 |
| 60 | 1300 / 6.04 | 750 / 3.95 | 760 / 3.65 | 640 / 6.98 |
| 100 | 1950 / 7.95 | 850 / 4.29 | 620 / 4.70 | **920 / 8.12** |

- **Critical kink-pair width:** w_c(τ_p/2) = 40–110 b, with w ∝ 1/√τ at low τ.
- **Velocity law:**

$$v=\frac{\nu_D\,a'\,b\,L}{w^2}\,e^{-\Delta H_0/k_BT}\sinh\!\left[\frac{\Delta H_0-\Delta H^\ast(\tau)}{k_BT}\right] \tag{1}$$

  ΔH*(τ) comes from elastic-interaction theory, not from a Kocks (p, q) fit.
- **Slip systems:** {100} becomes the easier system above about 36 GPa (screw) and about 50 GPa (edge) [ours, from the tables]. Both systems are active in the lower mantle.
- **Mantle prediction** at 10⁻¹⁶ s⁻¹:
  - shallower than about 2000 km, MgO is athermal (CRSS < 1 MPa at ρ = 10⁸ m⁻²);
  - from 2200 to 2800 km it is thermally activated, with η ≈ 10²¹–10²² Pa s.

**Against our edge run (½[110](001), 175 GPa / 3500 K):**
- Extrapolating the {100}-edge column [ours] gives τ_p ≈ 1.2–1.5 GPa and ΔH₀ ≈ 10 eV, so an MD-window onset of about 0.6–1.1 GPa. We see 0.25–0.5 GPa, which is the same order.
- **But our line is too short to test kink pairs.** w_c ≈ 60–80 b ≈ 150–200 Å, while our lines are 16 Å (§5k) and 64 Å (D1, now running). Low-stress results from these lines depend on line length.
- Kink-pair work needs lines of at least 300–400 Å, plus the screw character, which has the lower ΔH₀ on {100}.

## 3. Bridgmanite dislocations: Ferré, Carrez & Cordier 2007 (PEPI 163, 283)

- **Method:** GGA (PW91) γ-lines + 1D PN at 30 GPa.
- **Peierls stresses:**
  - easiest: [100](010) and [010](100), τ_p = 7–15.5 GPa;
  - hardest: [001] systems, up to 67 GPa.
- **C_ij at 30 GPa** (GPa): C₁₁ 592, C₂₂ 672, C₃₃ 617, C₄₄ 235, C₅₅ 203, C₆₆ 192, C₁₂ 214, C₁₃ 197, C₂₃ 216.
- As with MgO, 1D-PN on narrow cores probably overestimates, so treat these as upper bounds. Bridgmanite lattice friction is still roughly 10× MgO's.

## 4. Grain size: Fei et al. 2023 (Nature 620, 794); Ritterbex et al. 2020 (EPSL 547, 116438)

**Fei et al. 2023:**
- **Grain growth** (27 GPa, 2200 K, 1.5–1000 min) follows dⁿ = kt:
  - n = 2.9 with no ferropericlase (boundary-diffusion control);
  - n = 5.2 at 30 % ferropericlase (Zener-pinned two-phase growth).
  - Most of the effect of ferropericlase occurs between 0 and 10 vol%.
- **Lower-mantle grain size** (extrapolated to 4.5 Gyr):
  - pyrolite: d ≈ 0.3–0.8 mm;
  - bridgmanite-enriched rock (5 % ferropericlase): d ≈ 1.3–5 mm.
- **Flow law:** diffusion creep (Nabarro–Herring, which dominates, plus Coble) plus pure climb (Boioli/Reali), with Si diffusion from Yamazaki et al. 2000:
  - D_lat = 2.4×10⁻¹⁸ m²/s and δD_gb = 1.9×10⁻²⁴ m³/s at 27 GPa / 2200 K;
  - **both activation volumes (1.7 and 4.0 cm³/mol) are borrowed from olivine.**
- **Result:** a 1–1.3 order viscosity step at 800–1200 km at 0.5–1 MPa, from the grain-size contrast alone.
- **Caveats:** the printed pure-climb Eq. 3 is dimensionally inconsistent; the k-fit signs look wrong; the 5 % vs 20 % ferropericlase contrast in Fig. 4c looks like only a factor of 3–5 (fig.).

**Ritterbex 2020:**
- Transition-zone minerals only. Pure climb creep dominates for d ≳ 0.2–4 mm and gives η ≈ 10²¹±¹ Pa s.
- Glide is slower than climb below about 0.5–1.2 GPa.
- Dislocation density ρ = (σ/μb)² gives about 10⁸ m⁻² at 1 MPa [ours: a useful input for dislocation anelasticity].

## 5. What this changes in our plan (`ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md`)

1. **Clean-boundary sliding is far too fast to attenuate seismically.**
   - Our Σ5 friction at 20 GPa, ζ_GB ≈ 4×10⁶ Pa s/m, gives τ_e = ζ_GB d/G ≈ 10⁻⁸–10⁻⁷ s for d = 0.3–5 mm. That is fully relaxed; it lowers the modulus but gives no seismic-band Q⁻¹.
   - A Zener peak at 1–1000 s with d = 1 mm needs an effective ζ of about 10¹⁴–10¹⁷ Pa s/m, 8–11 orders more.
   - Diffusional accommodation is the other bound: kT d³/(Ω G δD_gb) ≈ 10¹² s (Si, Fei's δD_gb, d = 1 mm).
   - **Seismic-band boundary loss lies between these limits:** boundary sliding blocked at triple junctions, steps and disconnections, relaxed by diffusion (Raj–Ashby; the Morris & Jackson 2009 spectrum †; the Jackson & Faul 2010 band †).
   - **Consequences for the G steps:**
     - G4 (polycrystal with triple junctions) becomes central;
     - boundary diffusion δD_gb (Mg, O; Si in bridgmanite) is an essential output, measured boundary-resolved with grain motion removed;
     - the stress dependence of disconnection motion (G1–G3) sets how quickly sliding is blocked.
   - **Naming:** we rename our boundary friction from β to ζ_GB, to avoid a clash with the coupling factor β.
2. **Σ5 benchmarks, cheap and static** (new step G0):
   - DeePMD γ_gb and V_gb against van Driel Table 4.1 at 1.2, 21.4, 61.5, 101.6 and 121.6 GPa;
   - a search for structures C and D, i.e. whether our 140 GPa reconstruction is D (planes offset along [001]);
   - the C → D transition pressure;
   - NEB in both coupling modes (⟨100⟩, 0.667, and ⟨110⟩, 1.0) in the one-period cell.
3. **Dislocation benchmarks (new D0):**
   - DeePMD γ-lines {110}⟨110⟩ and {100}⟨110⟩ at 0, 60 and 100 GPa against Carrez 2009 Table 2, and C_ij against Table 1;
   - the 0 K τ_p of the {100} edge at 100 GPa (PNG 0.92 GPa vs 1D-PN 11 GPa).
4. **D1 line length:** the running 64 Å lines show drag and onset, not kink pairs. Add D1b: a line ≥ 300 Å (thin slab, about 60 k atoms) near threshold, plus screws on {100} and {110}.
5. **Grain sizes for the grain-size model:** 0.1 mm–1 cm, centred on 0.3–1 mm (pyrolite) and 1–5 mm (bridgmanite-rich).
6. **The vacancy free energies (T20) feed directly into Fei's model.** Fei's viscosity profile depends on the Si lattice diffusivity and its activation volume, which is borrowed from olivine (1.7 cm³/mol). An Ita & Cohen-type ΔG_f + ΔG_m for Si in bridgmanite gives both the activation energy and volume. This is a high-value target.
7. **Bridgmanite boundaries:** van Driel's [100] tilt set gives starting structures and benchmarks: (021) lowest, then (013) and (011); diffusion parameters as listed above. Waiting for RC's go-ahead (RC 10-12).
