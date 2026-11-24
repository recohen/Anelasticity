# Plan: dislocation and grain-boundary rheology from driven MD and stress-dependent rates, down to seismic frequencies

*2026-10-15. RC: "I think that driving the system with strains would help overcome the need to find the collective motions by random chance. I would concentrate on dislocations and grain boundaries. If we know the grain boundary rheology we can model effects of grain size."*

## 0. Idea

NEMD and Green–Kubo stop near 1 GHz. Equilibrium kinetic Monte Carlo reaches lower frequencies, but only for events it can find. The events that matter here (kink pairs, unpinning, disconnection nucleation, coupled boundary migration) are collective and rare, so random search will not find them. Instead:

1. **Drive** (stress, strain rate, large-amplitude oscillation) so the collective events happen within MD time. MD then *finds* the mechanism and gives its rate at high stress.
2. **Anchor at low stress** with NEB/string calculations along the discovered path at τ = 0 and intermediate τ. Add biased sampling (PLUMED, with the driven coordinate as the collective variable) where entropy matters.
3. **Fit a transition-state rate law** for each mechanism. Kocks–Argon–Ashby form:

$$r(\tau,T)=\nu\exp\!\left[-\frac{\Delta G(\tau)}{k_BT}\right],\qquad \Delta G(\tau)=\Delta G_0\left[1-\left(\frac{\tau}{\tau_c}\right)^{p}\right]^{q},\qquad \Omega^\ast=-\frac{\partial\Delta G}{\partial\tau} \tag{1}$$

   With forward and backward events, the net velocity of a defect with step length λ is

$$v=\lambda\,\nu\,e^{-\Delta G_0/k_BT}\,2\sinh\!\left(\frac{\tau\,\Omega^\ast_0}{k_BT}\right)\quad(\tau\ll\tau_c) \tag{2}$$

   This gives the **linear-response** (seismic-amplitude, τ ≲ 1 MPa) mobility, which no driven run can measure directly:

$$M_0=\frac{v}{\tau}\Big|_{\tau\to0}=\frac{2\lambda\,\nu\,\Omega^\ast_0}{k_BT}\,e^{-\Delta G_0/k_BT}. \tag{3}$$

4. **Feed the rate laws into mesoscale models:**
   - a dislocation line (Granato–Lücke with thermally activated motion and pinning);
   - grain-boundary sliding and migration in a polycrystal (Raj–Ashby / Zener plus diffusional accommodation, §2.4).

   These give $Q^{-1}(\omega,T,P,d,\rho)$ at seismic frequencies, including grain-size effects.
5. **Validate** wherever MD and the rate law overlap: driven MD at high τ and T, and the GHz NEMD sweeps.

**Main risk: the mechanism can switch at low stress.** The path found at GPa stresses need not be the one that operates at MPa. Mitigations:
- step τ down until events stop on the MD time scale, and check that Ω* and the path stay the same;
- compute the zero-stress NEB for every distinct path found;
- for boundaries, prefer pre-existing defects (disconnections) to nucleation at low stress, because a nucleation barrier diverges as τ → 0 (§2.2).

## 1. Dislocations (phase D)

Conditions:
- **MgO:** 175 GPa / 3500 K (Perez; MgO-only model; note its +12 GPa pressure offset, `results_dft/`). Then mantle points: ≈ 25 GPa / 2000 K and ≈ 135 GPa / 2500–3500 K, with the Deng model ≤ 160 GPa.
- **Bridgmanite:** Guan's [100](010) and [010](100) at 25 GPa, RC-approved (plan FE_DISLOCATIONS §3b).

| step | what | output | cost (P100 h) |
|---|---|---|---|
| D1 | Edge ½[110](001), MgO 175 GPa / 3500 K: a long line (NZ = 24, about 33 k atoms) so kink pairs fit; constant τ = 0.15, 0.25, 0.35, 0.5 GPa for 150 ps each; track the core (disregistry / CNA) | v(τ) below the 0.25–0.5 GPa threshold seen in §5k: waiting times, whether glide is jerky (kink pairs) or smooth | 4 × 10 |
| D2 | Same at 2500 and 3000 K (and 2 replicas at the threshold τ) | T dependence → ΔG(τ), Ω* (Eq. 1) | 8 × 10 |
| D3 | Screw ½[110] (expected to control strength in rocksalt) and the {110} system, same driven protocol | which character controls; v(τ, T) | 10 × 10 |
| D4 | NEB (string) of the discovered kink-pair / Peierls step at τ = 0 and 2–3 intermediate τ; 0 K Peierls stress by quasi-static loading | ΔG₀, τ_c, p, q | CPU/GPU, ≈ 20 |
| D5 | Pinning: a bound vacancy pair (and a single vacancy) placed at the core; binding energy (static), then drive the line across it | unpinning ΔG(τ) and Ω* | 4 × 10 |
| D6 | Line model: Granato–Lücke string with drag B (§5k), kink-pair-limited mobility (Eq. 3) and thermal unpinning; a kink-level KMC only if the analytic model is not enough | $Q^{-1}(\omega; L, \rho, c_v, T)$; does a peak fall at 0.01–1 Hz? | CPU |
| D7 | Bridgmanite D1–D5 for Guan's systems at 25 GPa (Deng model) | CRSS(T), the 1800 K transition, and the same seismic $Q^{-1}$ | ≈ 150 |

## 2. Grain boundaries (phase G): rheology law → grain-size model

Status:
- **Σ5 MgO at 18–20 GPa** slides freely by shear-coupled migration (β ≈ 4×10⁶ Pa s/m, local, area-independent; GHz band).
- **At 140 GPa** it is locked. Driven migration starts at τ ≈ 2–3 GPa.
- **3×1 NEB, 4407041 (analysed 10-15):** forward barrier 28.3 eV (0.168 J/m² per boundary); not converged, the climbing stage was stopped. The saddle displacement is spread uniformly over the six x-slabs (0.14–0.22 each, against 0.167 for fully collective). **The step is collective, with no localized disconnection.** So the 140 GPa flat boundary moves only by collective steps, and low-stress kinetics must come from disconnections built in explicitly (G1).

| step | what | output | cost (P100 h) |
|---|---|---|---|
| G1 | **Explicit disconnection dipole** in Σ5 (long-x cell, 2 steps of opposite sign; Burgers vector b_d and step height h from the coupling factor 0.6–0.67): build tool, relax at 20 and 140 GPa | disconnection core structure, energy per length | build plus a few h |
| G2 | Drive G1 at constant τ (several τ, 2–3 T per pressure) | disconnection velocity v_d(τ,T), threshold, kink-pair-like glide along the disconnection line → Eq. 1 | ≈ 60 |
| G3 | NEB of disconnection glide (one period) at τ = 0 and intermediate τ; nucleation barrier of a disconnection loop vs τ (for the high-stress regime) | ΔG₀ and Ω* for glide; ΔG_nuc(τ) | ≈ 30 |
| G4 | **General boundaries:** 2–3 more misorientations (e.g. Σ13, Σ17, an asymmetric or high-Σ boundary) and one small polycrystal (6–8 grains, about 25–30 k atoms, with triple junctions) under oscillatory and constant-stress driving at 20 and 135 GPa; boundary-resolved diffusion δD_b from the same runs | spread of boundary viscosities; triple-junction constraint; whether Σ5 is typical | ≈ 150 |
| G5 | **Grain-size model:** compliance $J^*(\omega;d)$ from (i) elastically accommodated sliding with boundary viscosity from Eq. 3, $\tau_e\approx\kappa\,\beta d/G_U$, (ii) diffusional accommodation (Coble / Raj–Ashby), and (iii) a spread of boundary types (G4) → an absorption band rather than one Debye peak; fit to the extended-Burgers form used for olivine (Jackson & Faul 2010) | $Q^{-1}(\omega,T,P,d)$ and the grain-size exponent; modulus dispersion; predictions along a lower-mantle geotherm | CPU |
| G6 | Bridgmanite boundaries: after RC's literature review (RC 10-12: wait before building them) | | – |

For sliding with a distributed relaxation (a boundary-viscosity spectrum $P(\ln\beta)$), the compliance generalizes Eq. 13 of the summary:

$$J^*(\omega)=J_U\left[1+\Delta_J\int\frac{P(\ln\beta)\,d\ln\beta}{1+i\omega\tau_e(\beta,d)}\right]-\frac{i}{\omega\,\eta_{diff}(d)},\qquad \tau_e=\kappa\frac{\beta d}{G_U},\qquad \eta_{diff}\propto\frac{k_BT\,d^3}{\Omega\,\delta D_b} \tag{4}$$

The grain size enters through $\tau_e\propto d$ (sliding) and $\eta_{diff}\propto d^3$ (diffusion), so the peak frequency and the low-frequency loss scale as $d^{-1}$ and $d^{-3}$. Checking these exponents against experiment (olivine, MgO) is a direct test.

## 3. Driving protocols (common tools)

| protocol | use | existing tool |
|---|---|---|
| constant shear stress on rigid blocks, piston normal load | waiting times and velocity v(τ) | `disl_drive.lammps`, `gb_drive.lammps` |
| constant strain rate (to 10⁶ s⁻¹ at about 10 k atoms in 1 ns) | flow stress vs rate → Ω* from the slope ∂τ/∂ln γ̇ | new: `fix deform` variant |
| large-amplitude oscillatory strain at 0.1–1 GHz | nonlinear loss, hysteresis, the onset amplitude | `anelastic_sweep.lammps` |
| biased sampling along the driven coordinate (PLUMED; CV = block displacement or core position) | free-energy profile at τ = 0 including entropy | PLUMED linked (plan FE_DISLOCATIONS §2) |
| NEB under stress (strained cell or applied traction) | ΔG(τ) on the discovered path | `gb_event_neb.py`, `neb_vacancy.py` |

Throughput: the 8232-atom edge slab runs at about 19 steps/s on one P100 (1.6 ns/day). 33 k atoms runs at about 0.4 ns/day.

## 4. Order and first jobs

1. **D1 now** (continues the §5k next steps): 4 jobs, about 40 P100-h.
2. Build the G1 disconnection dipole while D1 runs.
3. D2/D4 and G2/G3 follow from what D1 and G1 show.
4. G4 and D7 are the big items (≈ 150 P100-h each); check with RC before submitting.

## 5. Revisions after the literature RC added (2026-10-15; `LITERATURE_NOTES_2026-10-15.md` §5)

1. **D0 (new, static, cheap):**
   - DeePMD γ-lines {110}⟨110⟩ and {100}⟨110⟩ and C_ij at 0, 60 and 100 GPa against Carrez 2009 Tables 1–2;
   - 0 K τ_p of the {100} edge at 100 GPa (Peierls–Nabarro–Galerkin 0.92 GPa vs 1D-PN 11 GPa; Cordier 2012).
2. **D1 caveat and D1b (new):**
   - The critical kink-pair width is 60–80 b ≈ 150–200 Å, so the 64 Å lines of D1 give drag and onset, not kink pairs.
   - D1b: a line ≥ 300 Å (thin slab, about 60 k atoms) near threshold, then screws on {100} and {110}.
   - Fit ΔG(τ) ourselves; Cordier 2012 gives τ_p, ΔH₀ and w_c, not (p, q).
3. **G0 (new, static, cheap):** Σ5 against van Driel (thesis Table 4.1):
   - γ_gb and V_gb at 1.2–121.6 GPa;
   - structures C (5–90 GPa) and D (≥ 90–100 GPa), including whether our 140 GPa reconstruction is D;
   - one-period NEB in both coupling modes (⟨100⟩, 0.667, which our MD shows, and ⟨110⟩, 1.0, theirs).
4. **G emphasis shifts.**
   - Clean-boundary sliding (ζ_GB ≈ 4×10⁶ Pa s/m, renamed from β) relaxes in 10⁻⁸–10⁻⁷ s for d = 0.3–5 mm, while diffusion-limited relaxation takes ~10¹² s. Seismic-band loss therefore depends on how sliding is *blocked* (triple junctions, disconnections) and *accommodated* (boundary diffusion).
   - G4 (polycrystal with triple junctions) and the boundary-resolved δD_gb (Mg, O; Si in bridgmanite) become core outputs, not extras.
   - G5 grain sizes: 0.1 mm–1 cm, centred on 0.3–1 mm (pyrolite) and 1–5 mm (bridgmanite-rich, Fei 2023).
5. **Link to T20:** Fei 2023's viscosity profile rests on Si lattice diffusion in bridgmanite, with an activation volume borrowed from olivine. Computing ΔG_f + ΔG_m for Si in bridgmanite (plan FE_DISLOCATIONS A2/A3) tests it directly.
6. **Bridgmanite boundaries (G6):** van Driel's [100] tilt boundaries ((021) lowest, then (013) and (011)) give starting points and benchmarks. Still waiting for RC's go-ahead.
