# Fei et al. 2023 (Nature 620, 794) in detail, and what it means for MgO against MgSiO₃

*2026-10-15. RC: "We should compare in detail with s41586-023-06215-0 … particularly to compare MgO and MgSiO3."
Tool: `tools/fei2023_model.py` (re-implements the paper's model and adds periclase). Output: `fei2023_model.txt` and figure `fei2023_mgo_bdg.pdf/png` (this directory).*

## 1. What Fei et al. did

**Experiments:**
- Bridgmanite + ferropericlase (Fp) grain growth at 27 GPa and 2200 K, for 1.5–1000 min.
- Fp fraction X from 0 to 60 vol%, with (Mg₀.₉Fe₀.₁) compositions.
- Grain sizes are 2-D (no stereological correction).

**Growth law** (their Eq. 1):

$$d^n=k\,t,\qquad n=A'e^{X/B'}+C',\qquad \log_{10}k=A''e^{X/B''}+C'' \tag{1}$$

- n = 2.9 without Fp (boundary-diffusion-controlled growth), and n = 5.2 at X ≈ 30 % (Zener-pinned Ostwald ripening).
- A′ = −2.43, B′ = −0.022, C′ = 5.17. **A″ = +2.91, C″ = −4.12**, with B″ = −0.114 and X as a fraction.
  - The text extraction gives the opposite signs for A″ and C″, which would mean log k(0) = +1.2.
  - ED Table 2 has k(0) = 2–14×10⁻² µmⁿ/s. Our signs reproduce both the table and Fig. 4a.
- **No activation energy or activation volume for growth was measured** (a single P and T). The temperature scaling behind Fig. 4d (the geotherm) is therefore not given in the paper.

**Grain size after 4.5 Gyr at 2200 K** (our re-implementation; matches Fig. 4a):

| X_Fp | 0 | 3 % | 5 % | 10 % | 20 % |
|---|---|---|---|---|---|
| n | 2.74 | 4.55 | 4.92 | 5.14 | 5.17 |
| d (4.5 Gyr) | 0.66 m | 2.3 mm | 1.07 mm | 0.59 mm | 0.42 mm |

Along their geotherm (Fig. 4d): about 0.3–0.8 mm in pyrolite and about 1.3–5 mm in bridgmanite-enriched rock.

**Creep:** diffusion creep (Nabarro–Herring + Coble) plus pure-climb creep. Si is the rate-limiting species. Parameters are from Yamazaki et al. 2000, measured at 25 GPa:

$$\dot\varepsilon_{diff}=\frac{A\sigma V_m}{RTd^2}\left(D_{lat}+\frac{\delta D_{gb}}{d}\right),\qquad \dot\varepsilon_{climb}=\frac{D_{lat}\,\sigma^3V_m}{\pi b^2RTG^2\ln(4G/\pi\sigma)} \tag{2}$$

- A = 16/3, V_m = 25.5 cm³/mol, G = 210 GPa, b = 0.5 nm.
- D_lat = 2.39×10⁻¹⁸ m²/s and δD_gb = 1.90×10⁻²⁴ m³/s at 27 GPa / 2200 K.
- **Both activation volumes (1.7 and 4.0 cm³/mol) are borrowed from olivine.** The slope of their viscosity–depth profile depends on the lattice one (ED Fig. 5).

## 2. Checks of the paper

1. **Their Eq. 3 (pure climb) is dimensionally wrong as printed:** b appears in the numerator, which gives m³/s.
   - The Nabarro / Boioli form (our Eq. 2) gives 9×10⁻¹⁶ s⁻¹ for bridgmanite at 0.5 MPa / 2200 K. Fig. 4b shows about 3×10⁻¹⁵.
   - A factor of 3.3 reproduces their Fig. 4c at every stress: 5×10²¹, 2×10²⁰ and 4×10¹⁹ Pa s at 0.1, 0.5 and 1 MPa for X = 0.
   - The constant they actually used is not stated (`--climb-factor 3.3` in our tool).
2. **Diffusion creep and grain sizes are reproduced:** at X = 20 % and d = 0.42 mm, η ≈ 9.5×10¹⁸ Pa s (Fig. 4c: about 10¹⁹).
3. **The Coble term is irrelevant in their model:** the crossover d* = δD_gb/D_lat = 0.8 µm. Their Methods text says both "D_lat ≫ δD_gb/d" and "D_lat ≪ δD_gb/d"; the first is correct.
4. **The contrast between 5 % and 20 % Fp is only about 5×** (5.8×10¹⁹ vs 9.5×10¹⁸ Pa s at 0.5 MPa). The "more than one order" requires X ≲ 3 %, where n changes sharply (Fig. 3d). The viscosity jump therefore rests on bridgmanite-enriched rock having very little Fp.
5. **Fp is not given a rheology.** It enters only as a pinning phase. This is where MgO against MgSiO₃ comes in.

## 3. MgO against MgSiO₃ in the same framework (27 GPa, 2200 K, σ = 0.5 MPa)

The same Eq. 2 was applied to periclase, with O as the rate-limiting species (V_m = 10.2 cm³/mol, b = 2.86 Å, G ≈ 170 GPa). The results show how much the comparison depends on defect chemistry and on boundary transport:

| phase, rate-limiting transport | D_lat (m²/s) | δD_gb (m³/s) | η at d = 0.4 mm (Pa s) | η at d = 3 mm (Pa s) |
|---|---|---|---|---|
| Bdg, Si (Fei / Yamazaki 2000; experimental, defect chemistry unknown) | 2.4×10⁻¹⁸ | 1.9×10⁻²⁴ | 8.5×10¹⁸ | 2.6×10²⁰ |
| Bdg, Si boundary from van Driel GAP MD (δ = 0.8 nm × D_gb = 4.5×10⁻¹³) | 2.4×10⁻¹⁸ | 3.6×10⁻²² | 6.2×10¹⁸ | 2.6×10²⁰ |
| MgO, O, **intrinsic** (Ita & Cohen fit as used by Cordier 2023) | 2.8×10⁻²⁴ | – | **1.7×10²⁵** | 2×10²⁶ |
| MgO, O, **extrinsic** (X_v = 10⁻⁵, the value Cordier assumes for Bdg; ΔG_m = 2.68 eV, Ita & Cohen) | 6.2×10⁻¹⁸ | – | **7.8×10¹⁸** | 9×10¹⁹ |
| MgO, O, intrinsic lattice + boundary (our DeePMD Σ5 δD_b upper bound, 10⁻²⁰) | 2.8×10⁻²⁴ | 1×10⁻²⁰ | **2.0×10¹⁸** | 9×10²⁰ |

**Readings:**
- **The MgO/MgSiO₃ viscosity ratio spans 10⁷** (from about 0.25 to 2×10⁶) depending only on which transport is assumed for periclase.
- **Intrinsic lattice diffusion** (Cordier 2023's choice) makes periclase about 10⁶ times stronger than bridgmanite. But Cordier set the bridgmanite vacancy fraction to 10⁻⁵ (an extrinsic assumption) while treating MgO as intrinsic.
- **With the same extrinsic X_v in both minerals,** they are equally strong to within 10 %.
  - *Caveat (Cordier 2023, Methods):* trivalent cations in periclase create **Mg** vacancies, which do not raise the concentration of the neutral pairs that carry O. Through the Schottky equilibrium they may even suppress V_O.
  - So an extrinsic O row is physically doubtful for Fe³⁺/Al³⁺-bearing Fp. Treat it as a bound, not a scenario.
  - The comparison we can do cleanly is **intrinsic against intrinsic** (Schottky formation in both minerals, C1). See `results_cordier2023/CORDIER2023_COMPARISON.md`.
- **If the fast boundary diffusion in our MgO Σ5 runs holds at 27 GPa / 2200 K,** Coble creep makes periclase the *weaker* phase at pyrolite grain sizes. The crossover d* = δD_gb/D_lat is then of order metres, so Coble creep dominates at every grain size.
  - Our δD_b (0.8–3×10⁻²⁰ m³/s at 2000–2500 K, 14–20 GPa, MgO-only model) is an upper bound, because it still contains sliding.
  - Bridgmanite boundary transport, by contrast, is 4–5 orders slower (Fei / Yamazaki; van Driel).
- **This bears directly on Fei's argument.** In pyrolite, Fp forms an interconnected fine-grained network (Chandler 2021). If Fp is the weak phase by Coble creep, the pyrolite viscosity is set by Fp, not by bridgmanite grain size. The viscosity jump would then come from the loss of an interconnected weak Fp network when X_Fp drops below about 5–10 %. That is the same compositional trigger, but a different mechanism.

## 4. Grain-boundary sliding at Fei's grain sizes (anelasticity)

Our Σ5 MgO friction ζ_GB ≈ 4×10⁶ Pa s/m (20 GPa, 3000 K) gives τ_e = ζ_GB d/G ≈ 10⁻⁸–10⁻⁷ s at d = 0.3–5 mm. Clean-boundary sliding is fully relaxed at seismic periods. Seismic-band loss needs blocked sliding relaxed by diffusion (plan §5, item 4).
- **Diffusional relaxation time** kT d³/(Ω G δD_gb), with no O(1) geometric factors, at d = 0.4 mm:
  - periclase, with boundary diffusion as fast as in §3: about 7×10⁷ s (years);
  - bridgmanite (δD_gb = 2×10⁻²⁴): about 10¹¹ s.
- Both are far longer than seismic periods. Seismic Q⁻¹ then lies on the high-frequency tail of these relaxations (the Jackson–Faul-type ω^−α band, about 0.2–0.4 for olivine †), whose amplitude at 1–1000 s depends on how far away the relaxation time is.
- **Periclase boundaries, being 3 orders closer to the seismic band than bridgmanite's, would dominate the grain-boundary contribution to attenuation in pyrolite.** This needs the real δD_gb (C2 below) and the tail model (plan G5).

## 5. What we will compute (same Deng model for both minerals, RC 10-13)

All at Fei's 27 GPa / 2200 K plus two more pressures (for activation volumes) along the Cordier geotherm:

| | quantity | MgO | MgSiO₃ | tests in Fei |
|---|---|---|---|---|
| C1 | lattice diffusion: ΔG_f (Schottky) and ΔG_m by thermodynamic integration and umbrella sampling; intrinsic and extrinsic D; **activation volume** | O, Mg (A1/A2) | Si, Mg, O (A3) | D_lat and the olivine-borrowed 1.7 cm³/mol; the extrinsic-vs-intrinsic choice in Cordier 2023 |
| C2 | boundary diffusion δD_gb, boundary-resolved with grain motion removed | Σ5 (existing cells, Deng model at 27 GPa) | van Driel (021), (013) | Coble crossover; the Fp-weak-network scenario (§3) |
| C3 | boundary energy γ_gb and mobility M_gb (driven migration, plan G2) | Σ5 | (021), (013) | growth constant k(X = 0): parabolic estimate k ≈ M_gb γ_gb vs measured 2–14×10⁻² µm^2.9/s |
| C4 | **Bdg / MgO interphase boundary**: energy, diffusion, sliding (no published atomistic study) | – | interface | the n = 5 Ostwald/Zener regime; Fp coarsening |
| C5 | anelastic relaxation spectrum at Fei's grain sizes (plan G5) | | | seismic visibility of the jump at ~1000 km |

C1 is plan A1–A3 (approved 10-13) with the Fei state added. C2 and C3 extend plan G. C4 is new (needs the bridgmanite boundary builder plus an interface builder).

## 6. Caveats

- All MgO entries in §3 use literature or upper-bound parameters until C1 and C2 are done.
- The extrinsic MgO estimate uses Ita & Cohen's VIB ΔG_m (2.68 eV interpolated to 27 GPa). Our DFT spot check found VIB ΔG_f about 1–2.6 eV too high; ΔG_m has not yet been checked.
- Fei's D_lat(Si) is experimental, and its defect chemistry (intrinsic or extrinsic, Fe³⁺/Al) is not established.
- Fe in Fp (Mg₀.₈Fe₀.₂)O is not in our models.
