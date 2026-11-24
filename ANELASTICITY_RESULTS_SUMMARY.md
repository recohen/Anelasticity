# MgO anelasticity and viscosity from DeePMD MD: results summary

Status as of 2026-10-08. Methods, tools and pitfalls are in `ANELASTICITY_METHODS.md` (equation numbers below refer to this document). Full tables are in `results/results_all.md` and every point is in `results/results_all.csv`. Rerun everything with `python tools/anelastic_collect.py [--cases tools/anelastic_cases_MgO_V9.6397.py]`.

Setup:
- **System:** 4096 atoms; DeePMD model `graph_c.pb`, the same model at both volumes; P100 GPUs.
- **Oscillatory NEMD sweeps:** shear (xz) and uniaxial (x), from fix deform wiggle with nvt/sllod and a lock-in analysis.
- **Green–Kubo (GK):** 1.5 ns NVE runs.

## 1. Quantities

For a sinusoidal strain $\gamma(t)=\gamma_0\sin\omega t$, the stress is

$$\sigma(t)=\gamma_0\left[G'(\omega)\sin\omega t+G''(\omega)\cos\omega t\right] \tag{1}$$

The quality factor and dynamic viscosity are

$$Q=\frac{G'}{G''},\qquad \eta'(\omega)=\frac{G''}{\omega},\qquad \eta_0=\lim_{\omega\to0}\frac{dG''}{d\omega} \tag{2}$$

Uniaxial runs measure the longitudinal modulus,

$$M^*=K^*+\tfrac43G^*,\qquad \frac{M''}{\omega}\xrightarrow{\omega\to0}\zeta_0+\tfrac43\eta_0 \tag{3}$$

The effective (complex) viscosity, which applies to both liquid and solid, is

$$|\eta^*(\omega)|=\frac{|G^*(\omega)|}{\omega}=\frac{\sqrt{G'^2+G''^2}}{\omega} \tag{4}$$

For a liquid, $|\eta^*|\to\eta_0$ as $\omega\to0$. For a crystal, $G'\to G_{eq}>0$, so $|\eta^*|\simeq G_{eq}/\omega$ diverges.

## 2. Liquid MgO, $V$ = 6.6868 Å³/atom (≈ 175–193 GPa)

| T (K) | ⟨p⟩ (GPa) | $\eta_0$ GK (mPa s) | $\eta_0$ sweep, Eq. 2 (mPa s) | $\zeta_0$ GK (mPa s) | $G_\infty$ (GPa) | $\tau_0=\eta_0/G_\infty$ (ps) |
|---|---|---|---|---|---|---|
| 8000 | 192.8 | 8.19 ± 0.20 | 7.93 ± 0.12 | 0.86 ± 0.04 | 285 | 0.029 |
| 7000 | 183.4 | 11.18 ± 0.29 | 11.16 ± 0.20 | 1.17 ± 0.06 | 284 | 0.039 |
| 6000 | 174.9 | 18.30 ± 0.48 | 17.14 ± 0.27 | 1.64 ± 0.13 | 287 | 0.064 |

- **GK and NEMD agree** within 1–2σ for $\eta_0$. Both rise on cooling, by a factor of 2.2 from 8000 to 6000 K. The full spectra $\eta'(\omega)$ also agree from 10 GHz to 5 THz (`results/fig_shear_viscosity.png`).
- **Viscoelastic crossover.** The liquid is Newtonian below about 0.2 THz. $G'$ appears near 1 THz, and above that the liquid becomes solid-like (shear $Q$ ≈ 1 at 5 THz).
- **Bulk viscosity is small,** $\zeta_0/\eta_0\approx0.1$. Uniaxial $M''/\omega$ from the sweeps (adiabatic thermostat) is consistent with $\zeta_0+\frac43\eta_0$ from GK at 6000 and 7000 K. At 8000 K the 50 GHz point is about 4σ high.
- **The pressure rises with T** at fixed V by about 9 GPa per 1000 K in the liquid ($(\partial p/\partial T)_V=\alpha K_T$). It drops about 14 GPa on freezing at fixed V.

Liquid shear $Q$:

| T (K) | 0.2 THz | 1 THz | 5 THz |
|---|---|---|---|
| 8000 | < 0.35 | 0.37 ± 0.06 | 0.83 ± 0.07 |
| 7000 | 0.086 ± 0.023 | 0.50 ± 0.02 | 1.1 ± 0.07 |
| 6000 | 0.27 ± 0.02 | 0.76 ± 0.05 | 1.1 ± 0.08 |

## 3. Crystalline MgO (B1), $V$ = 6.6868 Å³/atom

The liquid crystallized at constant V at 5000 K and below: PE fell 0.46 eV/atom and p fell 23 GPa. Solid runs use this melt-grown crystal, which is rotated and polycrystalline relative to the box, at 5000 and 4000 K. At 5000 K there are also three reference cells: a perfect box-aligned B1 cell, 20 bound Schottky pairs, and a Σ5 (310)/[001] tilt bicrystal.

### 3.1 Moduli and Q

| cell | T (K) | G′ at 0.2 THz (GPa) | shear Q, 0.2 / 1 / 5 THz | uniaxial Q, 0.2 / 1 / 5 THz |
|---|---|---|---|---|
| melt-grown | 4000 | 278 | 60 ± 12 / 26 ± 3 / 17 ± 1 | 127 ± 8 / 66 ± 6 / 23 ± 2 |
| melt-grown | 5000 | 258 | 31 ± 7 / 19 ± 0.5 / 13 ± 1 | 108 ± 36 / 49 ± 5 / 30 ± 5 |
| perfect B1 | 5000 | 171 | > 155 / > 120 / 173 ± 44 | 71 ± 12 / 27 ± 1 / 11 ± 0.1 |
| Schottky (20 pairs) | 5000 | 148 | 10 ± 2 / 12 ± 3 / > 6.5 | 42 ± 8 / 23 ± 1 / 16 ± 3 |
| bicrystal | 5000 | 138 | 21 ± 3 / resonance / resonance | 201 ± 44 / 58 ± 4 / 18 ± 0.4 |

- **Values of Q** of 10–200 are typical of a dissipating crystal. They fall with T and with frequency, and they fall with defects. In shear, the perfect crystal is nearly lossless; Schottky defects lower Q about 15-fold and the boundaries about 7-fold.
- **Orientation:** the box-aligned cells measure C₄₄ in xz shear (≈ 171 GPa). The melt-grown crystal mixes in the stiffer (C₁₁−C₁₂)/2, which is why its G′ is higher (258 GPa).
- **Low frequency (20–50 GHz),** γ₀ = 0.01: Schottky and bicrystal G′ is flat within error and Q stays above about 2–9. Only the bicrystal at 20 GHz hints at softening (108 ± 15 GPa).
- **Bicrystal at γ₀ = 0.03 (jobs 4230008, 1.0–1.25 M steps): the boundaries slide.** G′ falls to 32 GPa (50 GHz) and 35 GPa (20 GHz), against 129 and 108 GPa at γ₀ = 0.01. Q falls to 0.62 and 0.88, and $\eta'$ is 0.17 and 0.32 Pa s. The third harmonic is strong ($|\sigma_3/\sigma_1|$ = 0.21–0.25). The response is therefore strongly amplitude-dependent and nonlinear: stick–slip sliding of the boundaries above a threshold strain between 1 and 3 %. This is the hallmark of grain-boundary (and dislocation) friction, not of linear anelasticity.
- **Aged Schottky cell** (1.5 ns aged, γ₀ = 0.02; job 4233462; PE stationary within 2 eV): Q = 8.2 ± 1.4 at 200 GHz and 9.7 ± 3.0 at 50 GHz. At 20 GHz, Q = 3.7 ± 0.9 (G″ = 38 ± 9 GPa, PE stationary within 0.3 eV). G′ is 142, 131 and 141 GPa at 200, 50 and 20 GHz. The loss persists after ageing and **rises toward low frequency** ($G''\propto\omega^{-1.1}$ from 50 to 20 GHz, $\eta'$ = 0.014, 0.043, 0.30 Pa s), while G′ stays flat. That is the onset of a slow, viscous-like process below 20 GHz, plausibly vacancy-diffusion (Nabarro–Herring-type) relaxation on the cell scale. Zener reorientation is ruled out (§5c). **11-16: the cell-size test does not support the cell-scale reading (§5n item 3). 11-17: in both the 8×8×8 and 6×6×6 cells all vacancies have aggregated into one nanovoid; the sub-50 GHz loss belongs to the void, not to dispersed vacancies (§5p item 4).**
- **Bicrystal slab resonance** at $f_1\approx v_s/L_z\approx$ 1 THz. Near it the response is inertial, not anelastic (G′ = 27 GPa and Q ≈ 0.8 at 5 THz; large harmonics at 1 THz).

### 3.2 Crystal viscosity: what can and cannot be measured

- **Green–Kubo in a crystal is not a viscosity.** At fixed cell shape GK drops the static (Born) part of $G(t)$. What is left decays on the phonon relaxation time, so $\int G\,dt$ (3–6 mPa s) is internal friction from phonon damping. This is the low-frequency limit of $G''/\omega$, not flow.
- **Opposite T slopes resolved.** For a relaxation with time τ,

$$\frac{G''}{\omega}=\frac{\Delta G\,\tau}{1+\omega^2\tau^2} \tag{5}$$

GK gives the $\omega\tau\ll1$ limit, $\Delta G\,\tau$, which falls with T. The sweeps at 0.2–5 THz sit at $\omega\tau\gtrsim1$, where $G''/\omega\approx\Delta G/(\omega^2\tau)$ rises with T. At the same frequency and in the same (off-diagonal) shear channel, GK and NEMD agree:

| crystal | f | GK $\eta'$ (mPa s) | sweep $\eta'$ (mPa s) |
|---|---|---|---|
| 4000 K melt-grown | 0.2 THz | 4.26 | 3.71 ± 0.73 |
| 4000 K melt-grown | 1 THz | 1.73 | 1.76 ± 0.18 |
| 5000 K melt-grown | 0.2 THz | 4.87 | 6.67 ± 1.45 |
| 5000 K melt-grown | 1 THz | 2.34 | 2.29 ± 0.06 |
| 5000 K perfect B1 | 0.2 THz | 0.51 | 0.13 ± 0.37 |
| 5000 K perfect B1 | 1 THz | 0.22 | 0.08 ± 0.08 |

- **Effective viscosity and a bound on flow.** The crystal's $|\eta^*|$ (Eq. 4) at 0.2 THz is 110–220 mPa s, against 8–18 mPa s for the liquid, and it grows as $1/\omega$. Suppose the crystal relaxed at most like a Maxwell body ($G''/G'=1/\omega\tau$, $\eta=G\tau$). Using the 2σ upper error on $G''$,

$$\eta_0\ \ge\ \frac{G'\,Q}{\omega},\qquad Q=\frac{G'}{G''+2\sigma_{G''}} \tag{6}$$

| cell | T (K) | $|\eta^*|$ at 0.2 THz (mPa s) | flow $\eta_0$ bound, Eq. 6 (mPa s) |
|---|---|---|---|
| liquid | 8000 / 7000 / 6000 | 8.0 / 11.5 / 17.7 | (GK $\eta_0$ 8.2 / 11.2 / 18.3) |
| melt-grown | 5000 | 205 | ≥ 4,400 |
| melt-grown | 4000 | 221 | ≥ 9,400 |
| perfect B1 | 5000 | 136 | ≥ 21,000 |
| Schottky | 5000 | 118 | ≥ 850 |
| bicrystal | 5000 | 110 | ≥ 1,700 |

The crystal is therefore at least 300–1000× more viscous than the liquid next to it in T. The bound is set by the observation time, roughly $G\,t_{run}$, not by the material. Real creep viscosities of MgO, about 10¹⁸–10²² Pa s, would need about 10 years of simulated time.

- **Causality (Kramers–Kronig) check.** When the loss varies slowly in ln ω,

$$\frac{dG'}{d\ln\omega}\simeq\frac{2}{\pi}G''(\omega) \tag{7}$$

Results by cell (`results/fig_kk.png`, table §2a of `results/results_all.md`):
- **Melt-grown and perfect crystals:** agree within 1σ from 0.2 to 5 THz. For example, at 5000 K, 0.2–1 THz: 7.6 ± 1.0 against 7.3 ± 0.6 GPa. The measured loss is therefore a linear, causal material response.
- **Bicrystal near its resonance:** fails, as expected.
- **Heated 5 THz uniaxial points:** fail, as expected.
- **Unaged Schottky cell at 0.2–1 THz:** fails (−4.4σ). The cell was ageing during the sweep; the aged-cell runs test this.

## 4. Second volume, $V$ = 9.6397 Å³/atom (≈ 18–50 GPa), in progress

Plan: liquid at 6000 and 4000 K. At 3000 K, a melt-grown crystal plus perfect, Schottky and bicrystal cells. At 2000 K, a melt-grown crystal.
- **Melt-grown crystal:** the 3000 K cell crystallized in NVT (PE −0.55 eV/atom, 19.7 GPa, strong Bragg peaks). The 2000 K GK run starts from it.
- **Early sweep results:**
  - **Liquid 6000 K (≈ 50 GPa):** $\eta'\approx$ 3.3–3.7 mPa s from 0.05 to 1 THz, about 5× less viscous than the 6000 K liquid at V6.6868.
  - **Liquid 4000 K (≈ 38 GPa):** 4.5 (1 THz) and 7.2 mPa s (0.2 THz). The 50 GHz point (69 mPa s) is invalid: **the liquid crystallized under shear** (γ₀ = 0.32, P = 20 ps). PE fell by 0.38 eV/atom within the first 70 ps, while the P = 5 and 100 ps runs stayed liquid. The point is marked FAILED in `lockin_results.txt`. This task saved a trajectory for its first 60 ps, so the shear-induced crystallization can be animated (`4000K/FreqSweep/P20ps_r0/traj.lammpstrj`).
  - **Lag correction (Eq. 6 of the methods doc):** raw lock-in values must be corrected before computing Q. This adds $G'\omega\Delta t$ to $G''$: 0.76 GPa at 1 THz and 0.15 GPa at 0.2 THz for G′ ≈ 120 GPa. Earlier quotes of Q ≈ 300 were uncorrected. The corrected values are below.
  - **Perfect B1 at 3000 K:** G′ = 120 GPa; shear Q ≈ 100 at 1 THz and > 200 at 0.2 THz.
  - **Schottky at 3000 K:** G′ = 114–117 GPa; shear Q ≈ 80 (1 THz), ≈ 200 (0.2 THz), ≈ 700 (50 GHz), > 400 (20 GHz). It is nearly lossless at low frequency, unlike the 5000 K Schottky cell at V6.6868 (Q ≈ 10). This fits a dynamic defect loss that scales with the jump rate, which is much lower at 3000 K.
  - **Melt-grown crystal:**
    - At 3000 K: G′ = 88 (0.2 THz), 96 (1 THz), 105 GPa (5 THz), with shear Q ≈ 24, 12, 9.
    - At 2000 K: G′ = 95, 100, 115 GPa, with Q ≈ 30, 13, 16.
    - G′ falls toward low frequency, unlike the perfect crystal, and the GK MSD reaches 10.8 Å² in 1 ns against 0.24 Å² for the perfect crystal. Both point to partly relaxed, mobile grain boundaries.
  - **Bicrystal at 3000 K: the boundaries slide freely.** G′ ≈ 0 at 0.2 THz and below (2.3 ± 1.1, −0.05 ± 0.08 and −0.5 ± 0.1 GPa at 0.2 THz, 50 GHz and 20 GHz), with η′ = 7.8 mPa s at both 20 and 50 GHz.
    - **Not melted:** Bragg peaks remain (S/N = 0.70), the MSD is 8 Å² in 1.3 ns, and the excess PE (0.053 eV/atom) corresponds to a boundary energy of about 2.9 J/m².
    - **Interpretation:** the two boundaries carry all of the xz shear like viscous films.
    - **Sliding friction coefficient:** $\beta=\sigma/\Delta v=2\eta'/L_z\approx2.3\times10^{6}$ Pa s/m.
    - **Contrast with V6.6868:** there, at 5000 K and γ₀ = 0.01, the boundaries are locked (G′ = 108–129 GPa) and slide only at γ₀ = 0.03. Compression strongly suppresses grain-boundary sliding.
    - **Implication for real grains:** with this β, a grain of size $d$ relaxes in $\tau\sim\beta d/G$, about 20 ns for $d$ = 1 mm. Freely sliding boundaries of this kind would therefore be fully relaxed, not dissipating, at seismic frequencies.
- **Green–Kubo and sweep viscosities, liquid** (`results_V9.6397/results_all.md`):

| T (K) | ⟨p⟩ (GPa) | $\eta_0$ GK (mPa s) | $\eta_0$ sweep (mPa s) | $\zeta_0$ GK (mPa s) | $G_\infty$ (GPa) | $\tau_0$ (ps) |
|---|---|---|---|---|---|---|
| 6000 | 49.5 | 3.49 ± 0.08 | 3.46 ± 0.13 | 0.80 ± 0.05 | 124 | 0.028 |
| 4000 (supercooled) | 37.8 | 7.99 ± 0.15 | 7.17 ± 0.23 (2 points) | 1.51 ± 0.06 | 125 | 0.064 |

- **Pressure dependence of the liquid viscosity:**
  - At 6000 K, $\eta_0$ is 18.3 mPa s at 175 GPa (V6.6868) and 3.5 mPa s at 50 GPa (V9.6397), a factor of 5.2. $G_\infty$ falls from 287 to 124 GPa.
  - $\tau_0=\eta_0/G_\infty$ is 0.064 ps against 0.028 ps, so compression slows structural relaxation about 2.3×.
- **The supercooled 4000 K liquid crystallizes under strain.** Three of its ten sweep tasks crystallized during the run: shear at P = 20 ps, and uniaxial at P = 0.2 and 100 ps. PE fell by 0.38–0.46 eV/atom. They are marked FAILED. The 4000 K sweep $\eta_0$ therefore rests on two points and lies about 10 % below GK.
- **GK of the crystals:** $\int G\,dt$ at $t_c$ = 1 ps is 4.8 mPa s for the melt-grown crystal at 3000 and 2000 K, 1.2 for perfect B1 and 1.3 for Schottky. This is phonon damping (§3.2), not viscosity. For the bicrystal, $\eta(t_c)$ grows from 1.0 to 2.6 mPa s between 1 and 3 ps, a slow sliding tail that a 1 ps cutoff cannot capture. The equilibrium sliding runs (T18) measure it directly.
- **Cost:** ≈ 32 steps/s on a P100 (24 at V6.6868), ≈ 9 P100-days for the full series. GK runs end about 13 h after start.

## 5. Other work this session

- **Trajectories for animations:** 8 sample runs at V6.6868, 5000 K and 8000 K, in `R6/Trajectories` (`traj.lammpstrj`, `id type x y z ix iy iz`):
  - liquid shear at 1 and 20 ps periods;
  - liquid uniaxial;
  - perfect, aged-Schottky and bicrystal cells at 20 ps;
  - the bicrystal at γ₀ = 0.1 for viewing, and at its 1 ps resonance.

  At V9.6397, the 20 ps shear tasks of each sweep also dump trajectories. View them in OVITO with displacement or atomic-strain modifiers; solid strains are 0.01–0.03, so scale the displacements up.
- **OCTP** (Jamali et al., J. Chem. Inf. Model. 59, 1290, 2019):
  - **Install:** built with CMake as a LAMMPS runtime plugin (`build_octp_plugin/octpplugin.so`, loaded with `plugin load`). The production LAMMPS is untouched.
  - **Cost:** it runs at full speed, with negligible overhead.
  - **What it gives:** `fix ordern` is order-n sampling of the Einstein form of GK. It is not a multiple-time-step integrator, so the reachable time and frequency are unchanged.
  - **Test result** (8000 K liquid, 120 ps NVE, job 4236292; `results/fig_octp_vs_gk`):
    - **Agreement:** the OCTP Einstein slope $d\,\mathrm{MSD}/dt$ matches the GK running integral on the same trajectory from 2 fs to 2 ps. Its plateau, about 8.2 mPa s at 0.2–2 ps, matches $\eta_0$ = 8.19 from the 1.5 ns GK run.
    - **Speed:** 23.8 steps/s, the same as without OCTP.
    - **No gain at long lags:** beyond about 3 ps both estimates are noise-dominated in a 120 ps run. OCTP is not less noisy, as expected, because the two forms are mathematically equivalent.
    - **Bias in the running estimate:** MSD/t converges more slowly and lies low at short $t$.
    - **Use:** OCTP is correct and free to run alongside other measurements. It saves storing the stress series, but gives nothing our GK analysis lacks.
- **r-RESPA** is not supported by `pair deepmd` (`respa_enable = 0`). Routes to longer times:
  - a larger time step after a drift test (≤ 2×);
  - several GPUs per run;
  - a faster surrogate potential fitted to DeePMD, which could be 100–1000× faster;
  - for defect relaxations, rates from NEB/kMC barriers combined with relaxation strengths from MD.

## 5a. Vacancy jump rates from MD (T17 step 1)

Setup:
- **Cell:** 20-pair Schottky cell at $V$ = 6.6868 Å³/atom (138–148 GPa); NVT, 200 ps at each T, positions every 0.1 ps (`DefectHops/<T>K`, job 4238025).
- **Analysis:** `tools/vacancy_hops.py` assigns atoms to Wigner–Seitz sites on the ideal lattice.
- **Rate estimate:** the jump rate per vacancy comes from on-lattice tracer diffusion, which is free of recrossings,

$$\Gamma_v=\frac{6D^*}{f\,c_v\,\lambda^2},\qquad \lambda=\frac{a}{\sqrt2},\quad f=0.78 \tag{8}$$

  Here $c_v$ is the vacancy site fraction. Direct hop counts depend on the minimum residence time chosen, so they are printed only as a check.

| T (K) | p (GPa) | $D^*_{Mg}$ (Å²/ps) | $D^*_{O}$ (Å²/ps) | $\Gamma_{Mg}$ (ps⁻¹) | $\Gamma_{O}$ (ps⁻¹) | vacancies Mg/O (mean) |
|---|---|---|---|---|---|---|
| 3501 | 138.2 | 1.8×10⁻⁴ | 8.4×10⁻⁵ | 0.020 | 0.0093 | 20.1 / 20.1 |
| 4003 | 141.7 | 8.4×10⁻⁴ | 5.8×10⁻⁴ | 0.089 | 0.062 | 20.7 / 20.5 |
| 4505 | 144.9 | 2.0×10⁻³ | 1.6×10⁻³ | 0.195 | 0.156 | 23.0 / 22.5 |
| 5004 | 148.3 | 3.8×10⁻³ | 2.8×10⁻³ | 0.337 | 0.265 | 24.6 / 23.7 |

- **Mechanism:** more than 95 % of jumps go to the nearest same-sublattice site, along ⟨110⟩ at a distance $a/\sqrt2$. Second-neighbour ⟨100⟩ and longer jumps rise with T, to about 4 % at 5000 K.
- **Not a single activation energy.** The local apparent $E_a=-k_B\,d\ln\Gamma/d(1/T)$ falls steeply with T:

| interval (K) | $E_a$, Mg (eV) | $E_a$, O (eV) |
|---|---|---|
| 3500–4000 | 3.61 | 4.57 |
| 4000–4500 | 2.42 | 2.84 |
| 4500–5000 | 2.12 | 2.08 |

  A single Arrhenius fit (2.84 eV for Mg, 3.38 eV for O) misses the 3500 K points. Statistical error at 3500 K is about ±13 % (about 55 O hops, 136 Mg hops), so the curvature is well beyond noise (`results/fig_vacancy_arrhenius`).
- **Likely causes of the curvature:**
  - extra thermally generated defects above 4500 K (up to 36 vacancies and 5–8 atoms in flight per frame);
  - vacancy clustering and binding (PE drifts by 20–50 eV over the run);
  - anharmonic and entropic softening of the barrier near melting.

  Static (NEB) barriers at the same volume, the next step, will separate these effects.
- **Consequence for extrapolation:** an activation energy fitted at high T underestimates relaxation times at lower T. Here it would be off by a factor of about 3 already at 3500 K, for oxygen.

## 5b. Static barriers from NEB (T17 step 2)

Setup:
- **Method:** `tools/neb_vacancy.py` (ASE + DeePMD, climbing-image NEB, fixed cell at $V$ = 6.6868 Å³/atom, static $p$ = 115.8 GPa), job 4246743, results in `NEB/n5/neb_results.json`.
- **Prefactors:** harmonic TST with the Vineyard prefactor over a local Hessian (78–79 atoms within 5 Å),

$$k=\nu^*\exp\!\left(-\frac{E_b}{k_BT}\right),\qquad \nu^*=\frac{\prod_{i=1}^{3n}\nu_i^{\rm ini}}{\prod_{j=1}^{3n-1}\nu_j^{\rm sad}} \tag{9}$$

- **Size convergence:** the isolated Mg barrier is 3.773 eV in the 512-atom cell and 3.771 eV in the 1000-atom cell.

| event (1000 atoms) | $E_b$ (eV) | $\nu^*$ (THz) | $\Delta E$ final−initial (eV) | largest strain derivatives $dE_b/d\varepsilon$ (eV) |
|---|---|---|---|---|
| isolated Mg vacancy, ⟨110⟩ jump | 3.77 | 24.3 | 0 | xx, yy −15.3; zz +13.0; xy +15.3 |
| isolated O vacancy, ⟨110⟩ jump | 4.65 | 22.4 | 0 | xx, yy −16.6; zz +9.8; xy +14.2 |
| bound pair: Mg jump, pair rotates (Zener step) | **2.57** | 39.8 | 0 | xy −10.4 |
| bound pair: O jump, pair rotates | **3.09** | 46.2 | 0 | xy +9.6 |
| bound pair: Mg jump, pair dissociates (to 1.118 a) | 4.45 | 27.4 | +2.16 | xx −18.9; yy −17.4; xy +15.9 |
| bound pair: O jump, pair dissociates | 5.11 | 38.2 | +2.16 | xx −19.3; yy −16.8; xy −15.5 |

The pair binding energy, $E$(separated) − $E$(nearest-neighbour pair), is **3.25 eV**.

**Comparison with MD** (rates per vacancy, ps⁻¹; TST from Eq. 9; a pair-rotating vacancy has 4 target sites, an isolated one 12):

| T (K) | TST pair rotation, Mg | MD hop count, Mg | TST pair rotation, O | MD hop count, O | TST isolated, Mg |
|---|---|---|---|---|---|
| 3501 | 0.032 | 0.034 | 0.0066 | 0.014 | 0.0011 |
| 4003 | 0.092 | 0.141 | 0.024 | 0.079 | 0.0052 |
| 4505 | 0.21 | 0.28 | 0.065 | 0.23 | 0.018 |
| 5004 | 0.41 | 0.47 | 0.14 | 0.38 | 0.046 |

- **Mg:** in the MD the Mg vacancies move almost entirely by rotating around their bound O vacancy. Harmonic TST with the static 2.57 eV barrier reproduces the MD rate within 1.0–1.5× from 3500 to 5000 K, with no fitted parameters. Isolated-vacancy migration (3.77 eV) is 10–30× slower and plays little part.
- **O:** it moves 2–3× faster than O-mediated pair rotation predicts, so additional O mechanisms operate. These could be cluster moves or the extra defects that appear above 4500 K.
- **Answer to the single-activation-energy question:** the elementary barriers are well defined and independent of T. What changes with T is the mixture of mechanisms (pair rotation, dissociation, free migration, thermally created defects), and that makes any single fitted $E_a$ an average that depends on T. The tracer-diffusion estimate (§5a) also assumes uncorrelated free vacancies ($f$ = 0.78). Pair rotation is strongly correlated, so that estimate mixes mechanisms further.
- **Anelastic consequence (preliminary).** The bound pair is a tetragonal ⟨100⟩ defect. By symmetry, rotating it relaxes only $(C_{11}-C_{12})/2$, not $C_{44}$. Its Zener relaxation time is

$$\tau^{-1}=6\,(k^{\rm rot}_{Mg}+k^{\rm rot}_{O}) \tag{10}$$

  where $k^{\rm rot}$ is the rate to one target site.
  - **At 5000 K:** τ ≈ 1.2 ps, so the loss peak is near 0.13 THz. This fits the extra uniaxial loss of the Schottky cell at 0.2 THz (Q 42 against 71 for the perfect crystal).
  - **The large C₄₄ (xz) loss** of the Schottky cell must come from other defects, such as clusters, consistent with the cell ageing.
  - **At seismic frequency:** with these barriers, the Zener peak reaches 1 Hz only near 950 K at this density. At mantle temperatures it lies at MHz–GHz, so bound Schottky pairs alone would give negligible seismic attenuation. This needs step 3 (relaxation strength from the pair's elastic dipole) and step 4 (kMC) before it can be relied on.

## 5c. Elastic dipoles and Zener relaxation strengths (T17 step 3)

Setup:
- **Method:** `tools/defect_dipoles.py` (ASE + DeePMD, 1000-atom cell, fixed V; job 4250315; `NEB/dipoles/dipoles.json`).
- **Dipole tensor:** $G_{ij}=V\,[s_{ij}({\rm defect})-s_{ij}({\rm perfect})]$, so that $E(\varepsilon)=E(0)+G:\varepsilon$.
- **Relaxation strength:** the relaxed reduction of the modulus $M_E=E{:}C{:}E$ for a strain pattern $E$ is

$$\Delta M_E=\frac{n_d}{k_BT}\,{\rm Var}_\alpha\!\left(G^\alpha:E\right) \tag{11}$$

  over the cubic orientation variants α. The Debye peak height is $Q^{-1}_{max}=\Delta M_E/(2M_E)$.
- **Static elastic constants** at this V (116 GPa): C₁₁ = 1287, C₁₂ = 267, C₄₄ = 218, C′ = 510 GPa.

| configuration | $E-E$(1NN pair) (eV) | $G$ (eV) | relaxes | $\Delta M$ at 5000 K, 20 pairs per 4096-atom cell |
|---|---|---|---|---|
| bound pair, 1NN ⟨100⟩ | 0 | diag(19.88, 21.27, 21.27) | C′, C₁₁ only | ΔC₁₁ = 0.12 GPa (0.01 %), ΔC′ = 0.35 GPa |
| pair, 2NN ⟨111⟩ | +1.73 | 17.89 diagonal, 0.46 off-diagonal | C₄₄ only | ΔC₄₄ = 0.06 GPa (0.03 %) |
| pair, 3NN ⟨210⟩ | +2.16 | eigenvalues 12.5, 18.4, 18.5 | all | ΔC₁₁ = 1.65 GPa, ΔC₄₄ = 0.24 GPa (if all pairs were 3NN) |
| isolated V_Mg, V_O | — | isotropic (6.47, 8.59) | none (cubic) | 0 |

- **Selection rules confirmed numerically:** ⟨100⟩ pairs relax only C′ and C₁₁; ⟨111⟩ pairs relax only C₄₄.
- **The bound pair is almost isotropic** ($G_\parallel-G_\perp=-1.39$ eV), so its Zener relaxation is tiny: $Q^{-1}_{max}\approx5\times10^{-5}$ at this concentration (about 1 % of sites).
- **Zener relaxation does not explain the measured defect loss.** The measured excess uniaxial loss of the Schottky cell at 0.2 THz is $M''\approx$ 9.5 GPa. That implies $\Delta M\approx$ 20 GPa, about 100× more than any orientational (Zener) relaxation of these configurations. The THz defect loss must be dynamic instead: phonon scattering by vacancies, or the transient stress of jumps in progress. The barriers shift strongly with strain (|$dE_b/d\varepsilon$| ≈ 15 eV), and a rough estimate of the transient-stress mechanism gives a few GPa, the right order. Both mechanisms are fast and, beyond the jump rate itself, not thermally activated, so neither moves to seismic frequencies in the way a Zener peak would.
- **Thermal defects:** the bound-Schottky-pair formation energy at fixed V is $E(N-2)-\frac{N-2}{N}E_{perf}$ = 2.44 eV (separated pair: 5.69 eV). Thermal pairs are therefore expected near 5000 K, consistent with the vacancy count rising above 4500 K in §5a.
  - **Correction (2026-10-13):** this fixed-V energy leaves out the $P\,v_f$ term of the formation Gibbs energy (Ita & Cohen 1997, Eq. 3; plan `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` Eq. 3). At 140 GPa that term is of order $P\cdot2\Omega\approx$ 12 eV. Ita & Cohen's bound-pair $\Delta G_f$ is 13–17 eV at 80–140 GPa. Thermal Schottky pairs are therefore **not** expected at 5000 K, and the extra vacancies seen above 4500 K in fixed-N MD (§5a) must be Frenkel pairs. The proper free energies are planned (plan §1).
- **Implication for seismic attenuation:** in this model, isolated and bound Schottky vacancies give negligible Zener-type loss at any frequency. Seismic-band defect attenuation would have to come from other defects: dislocations, grain boundaries, or charged and aliovalent defects that DeePMD does not represent.

## 5d. Grain-boundary sliding from equilibrium MD, and a grain-scale model (T18 steps 1 and 3)

Setup:
- **Runs:** Σ5 bicrystal, 20 ps NVT + 300 ps NVE, no applied strain (job 4264732; `MgO/4096atoms/GBslide`; `tools/gb_slide.py`; `results/fig_gb_sliding`).
- **Friction from diffusion:** the relative displacement $u$ of the two grain interiors diffuses with

$$D_u=\frac{k_BT}{2\beta A},\qquad \eta_{cell}=\frac{\beta L_z}{2} \tag{12}$$

  for friction β per boundary (stress = β × sliding velocity) and boundary area $A=L_xL_y$.
- **Locked boundaries:** a direction counts as locked when its MSD saturates (log–log slope < 0.5). Then only a 2σ lower bound on β is given.

| volume | T (K) | x, perpendicular to tilt axis: β (Pa s/m) | y, along tilt axis: β (Pa s/m) | grain $u_{rms}$ (Å) |
|---|---|---|---|---|
| V6.6868 (140–150 GPa) | 4020 | locked, ≥ 6.5×10⁹ | locked, ≥ 1.1×10¹⁰ | 0.1–0.3 |
| | 4501 | locked, ≥ 2.2×10¹⁰ | locked, ≥ 3.7×10⁹ | 0.1 |
| | 5052 | locked, ≥ 6.4×10⁹ | locked, ≥ 2.9×10⁹ | 0.1–0.2 |
| V9.6397 (14–20 GPa) | 2011 | 5.2×10⁷ (±100 %) | locked, ≥ 3.2×10⁹ | 0.95 |
| | 2519 | 4.9×10⁶ (±50 %) | locked, ≥ 3.2×10⁹ | 3.0 |
| | 2998 | 8.0×10⁶ (±70 %) | locked, ≥ 2.3×10⁹ | 6.1 |

- **Compression locks the boundary.** At 140–150 GPa there is no sliding in 300 ps in either direction, up to 5000 K. At 14–20 GPa the boundary slides perpendicular to the tilt axis, which is the shear-coupled (Cahn–Taylor) direction of a ⟨001⟩ tilt boundary, at 2000–3000 K. Along the tilt axis it stays locked. The anisotropy in β is at least 300×.
- **Consistency with the sweeps (V9.6397, 3000 K).**
  - The linear (equilibrium) cell viscosity is $\eta_{cell}$ = 27 mPa s. The sweeps give 17 mPa s at 0.2 THz (γ₀ = 0.01) and 7.8 mPa s at 20–50 GHz (γ₀ = 0.03, nonlinear). Large amplitude gives a lower effective viscosity, consistent with stick–slip.
  - At V6.6868, $\tau_{cell}\ge$ 34–78 ps gives $\omega\tau\ge$ 4–24 at 20–50 GHz. That matches the locked, nearly elastic γ₀ = 0.01 sweeps.
- **Temperature dependence (V9.6397, x):** β falls about 10× from 2011 to 2519 K (apparent $E_a\approx$ 2 eV), then is flat to 3000 K within the large errors (one 300 ps run per T). This is too noisy to test a single activation energy. Longer runs or replicas would be needed.
- **Boundary diffusion:** δD_b taken from the whole-cell MSD (Mg ≈ O, 0.8–3×10⁻²⁰ m³/s at 2000–2500 K, 6.5×10⁻¹⁹ at 3000 K, V9.6397) still contains the grain translation from sliding. It is therefore an upper bound. A boundary-resolved MSD with grain motion removed is needed.

### Grain-scale model (`tools/gb_grain_model.py`; `results/fig_gb_Q_model`)

The compliance is

$$J^*(\omega)=J_U\left[1+\frac{\Delta_J}{1+i\omega\tau_e}\right]-\frac{i}{\omega\eta_C},\qquad \tau_e=\kappa\frac{\beta d}{G_U},\qquad \eta_C=\frac{k_BT\,d^3}{3A_C\,\Omega\,\delta D_{eff}} \tag{13}$$

- **Elastically accommodated sliding** (Zener; Raj–Ashby): $\kappa\approx1$. Zener's spherical-grain relaxation strength is $\Delta_J$ = 0.75 at V6.6868 (ν = 0.28) and 0.96 at V9.6397 (ν = 0.19).
- **Coble creep:** $A_C=148/\pi$, Ω is the MgO formula volume, and $\delta D_{eff}$ is the series combination of Mg and O.
- **Inputs:** $G_U$ = 250 GPa (V6.6868) and 105 GPa (V9.6397). These are static Hill averages, scaled by the measured thermal C₄₄ softening. Static constants: C₁₁/C₁₂/C₄₄ = 1287/267/218 GPa at V6.6868 and 286/92/147 GPa at V9.6397.

Results:
- **V9.6397, ≈ 15–20 GPa, 2000–3000 K:**
  - **Sliding peak frequency:** about 0.2–2 MHz for 1 mm grains.
  - **Loss at 1 Hz:**

    | grain size | Q⁻¹(1 Hz) |
    |---|---|
    | 1 mm | 10⁻⁷–10⁻⁶ |
    | 1 cm | 10⁻⁶–10⁻⁵ |

    Coble creep would take over only for d ≲ 0.1 mm (and its δD is an upper bound).
  - **Implication:** freely sliding boundaries like this Σ5 are fully relaxed at seismic frequencies. They lower the seismic shear modulus (by up to the Zener strength) rather than attenuate.
- **V6.6868, ≈ 140–150 GPa, 4000–5000 K (core–mantle-boundary-like):**
  - The boundaries are locked in MD, so β is only a lower bound. The sliding peak lies at or below about 0.5–10 kHz for 1 mm–1 cm grains.
  - It would enter the seismic band if the true β is about 10³–10⁵ times the bound, which MD cannot exclude.
  - The actual high-pressure β must come from static rates: NEB of the shear-coupled sliding step (T18 step 2).
- **Caveats:**
  - Σ5 is one special, low-energy boundary, and real polycrystals have a spectrum of boundaries and triple-junction constraints.
  - Geometric factors are O(1).
  - The relaxed-modulus estimate assumes free sliding on all boundaries.

## 5e. Static sliding landscape of the Σ5 boundary (T18 step 2)

Setup:
- **Method:** `tools/gb_sliding_neb.py` (ASE + DeePMD, 3920 atoms, fixed cell; `GBslide/neb/`).
- **Relaxed γ-lines:** grain A is translated rigidly by Δ, the sliding coordinate of the grain interiors (> 6 Å from the boundaries) is held fixed, and everything else relaxes. They were computed for the as-built boundary and for MD-equilibrated boundaries quenched to 0 K (V6.6868 after 1.5 ns at 5000 K and 300 ps at 4000 K; V9.6397 after 300 ps at 2000 K).

| boundary | x (⊥ tilt axis): corrugation | y (tilt axis): maximum |
|---|---|---|
| V6.6868 as-built | ≤ 0.018 J/m², minima every $a/\sqrt{10}$ = 1.19 Å; NEB barrier 0.36 eV per cell (0.006 J/m²) | 1.93 J/m² |
| V6.6868 MD-equilibrated (4000 K) | 0.03–0.07 J/m² (one trapped point excluded) | 1.20 J/m² |
| V9.6397 as-built | flat (\|γ\| ≤ 0.002 J/m²) for \|Δ\| ≤ 2.4 Å, then 1.1–1.5 J/m² | 0.99 J/m² |
| V9.6397 MD-equilibrated (2000 K) | flat for \|Δ\| ≤ 1.3 Å, then 0.6–1.35 J/m²; a lower state (−0.17 J/m²) at Δ = p/2 | 0.98 J/m² |

- **Anisotropy:** sliding perpendicular to the tilt axis is easy and along it is hard (1–2 J/m²) at both volumes and for both structures. This matches the MD at V9.6397, where x slides and y is locked.
- **Boundary reconstruction at high pressure.** At 140 GPa the MD-equilibrated boundary has 3–4× the x-corrugation of the as-built one. For rigid sliding of the whole periodic cell (two boundaries, $2A$ = 898 Å²), the barrier rises from 0.36 eV to about 3–4 eV. At 4000–5000 K that gives about $10^8$ jumps/s, so there is no sliding within 300 ps, consistent with the locked MD. The as-built barrier would predict free sliding (β ≈ 2.5×10⁵ Pa s/m), so the structure matters.
- **Large MD displacements at 18 GPa are coupled motion.** Rigid sliding at V9.6397 is free only within ±1.3–2.4 Å and then costs about 1 J/m² (about 70–95 eV per cell). Yet in MD the grains moved by $u_{rms}$ = 6 Å at 3000 K, while both boundaries migrated about 10 Å (z = 29.8/62.8 → 19.7/53.0 Å). Sliding beyond the flat region therefore goes by shear-coupled boundary migration (Cahn–Taylor), which rigid γ-lines and rigid-translation NEB cannot represent.
- **Consequence for the grain model (§5d).** In a periodic cell, rigid sliding is a collective event whose barrier scales with the boundary area. So the cell β (from MD or from TST) is not a transferable material constant. Real boundaries slide by localized disconnections (steps with dislocation content), whose barrier does not depend on the total area. The per-area quantity that does transfer is the ideal sliding stress, roughly $\tau_p\approx\pi\,\Delta\gamma/\lambda$. That is about 1–2 GPa at V6.6868 and several GPa beyond the flat region at V9.6397. The §5d grain-scale Q⁻¹ values are therefore provisional.
- **NEB caveat:** the automatic end-point choice picked a non-equivalent state for V9.6397 MD (+50 eV) and downhill relaxations elsewhere, so the NEB numbers in the job logs are not barriers. The γ-lines are the reliable result.

**What is needed for a transferable β:**
1. ~~A size test~~ done, §5f: β_x does not depend on area, so the mechanism is local.
2. A disconnection NEB, with end states taken from an MD migration step, for the coupled-migration mechanism at both volumes.

## 5f. Size test of boundary sliding (T18; job 4283403, 2026-10-09/10)

Setup:
- **Runs:** the same Σ5 bicrystal replicated in the boundary plane, 300 ps NVE (250 ps for 9×, 200 ps for V6.6868 9×). Directories `GBslide/V9.6397_3000K{,_2x1,_2x2,_3x3}`, `GBslide/V6.6868_5000K{,_3x3}`; analysis `GBslide/size_analysis/` (`tools/gb_slide.py`); figure `results/fig_gb_size`.
- **Test:** for a local mechanism β is a material constant, so by Eq. 12 $D_u\propto 1/A$. A collective (rigid) mechanism would make β grow with $A$, and the barrier would scale with $A$ as in §5e.
- **Robustness check:** β was also refitted over four lag windows (2–10, 5–20, 10–40 and 25–80 ps; `Downloads/gbsize_check.py`), because a single run per size gives large errors.

| cell | $A$ (Å²) | atoms | $u_{rms}$ (Å) | β_x, 0.1–0.33 $t_{run}$ (10⁶ Pa s/m) | β_x over lag windows 2–10 / 5–20 / 10–40 / 25–80 ps (10⁶ Pa s/m) | y |
|---|---|---|---|---|---|---|
| V9.6397 3000 K 1× | 573 | 3 920 | 6.1 | 8.0 (±130 %) | 2.9 / 3.6 / 6.0 / 7.7 | locked, ≥ 2.3×10⁹ |
| 2×1 | 1146 | 7 840 | 4.1 | 3.0 (±30 %) | 2.2 / 3.7 / 5.5 / 3.1 | locked, ≥ 2.4×10⁹ |
| 2×2 | 2292 | 15 680 | 1.2 | 4.7 (±40 %) | 2.0 / 2.1 / 2.2 / 4.1 | locked, ≥ 2.3×10⁹ |
| 3×3 | 5156 | 35 280 | 2.2 | 10 (±200 %), ≥ 1.9 | 1.5 / 2.4 / 5.1 / 7.1 | locked, ≥ 1.1×10¹⁰ |
| V6.6868 5000 K 1× | 449 | 3 920 | 0.1–0.2 | locked, ≥ 6.4×10⁹ Pa s/m | — | locked, ≥ 2.9×10⁹ |
| 3×3 | 4040 | 35 280 | < 0.1 | locked, ≥ 3.7×10⁹ Pa s/m | — | locked, ≥ 1.5×10⁹ |

Results:
- **β_x does not depend on area at V9.6397, 3000 K.** Over a 9× change in $A$, β_x stays at 2–10×10⁶ Pa s/m in every lag window, with no trend. $D_u$ falls roughly as $1/A$ (0.045 → 0.004 Å²/ps). Sliding perpendicular to the tilt axis is therefore local (disconnection- or migration-mediated), and β ≈ 4×10⁶ Pa s/m (geometric mean, factor ~2) is a transferable per-area friction at 18 GPa and 3000 K. This removes the main caveat of §5e for V9.6397.
- **The windowed β rises from short to long lags** (about 2 → 6×10⁶) in most cells. The motion is not simple Brownian sliding: it is fast over a few ps and slower over tens of ps. Shear-coupled migration with occasional pinning, as in §5e, would give this. For the grain model the long-lag value (5–8×10⁶) is the relevant one.
- **Frequency band.** These are equilibrium runs, so β is in principle the ω → 0 limit, but a lag window t only resolves frequencies above about 1/(2πt). The windows 2–10 / 5–20 / 10–40 / 25–80 ps correspond to about 16–80 / 8–30 / 4–16 / 2–6 GHz. β is therefore a **GHz-band friction**, the same band as the forced sweeps. It has not converged with lag, and it rises toward low frequency. If migration is pinned at long times, β(ω) keeps growing as ω → 0. Using it at seismic frequencies (mHz–Hz) needs either ns-length runs that show D_u(t) reaching a constant, or event rates from NEB and TST.
- **The 140 GPa boundary is still locked when the cell is 9× larger** (5000 K, 200 ps; MSD saturates at ~3×10⁻³ Å² in both directions). More room for local mechanisms does not unlock it on this time scale. Locking at high pressure is therefore not a small-cell artefact. β there needs a disconnection or coupled-migration NEB (rate) rather than MD.
- **Along the tilt axis (y)** every cell at both volumes is locked.

## 5g. Stress-driven coupled migration and zero-stress NEB at 140 GPa (T18, 2026-10-10)

Setup:
- **Driven MD** (`tools/gb_drive.lammps`; `GBslide/drive/`): V6.6868 Σ5 bicrystal (1×, A = 449 Å²) with opposite x-forces on the two grain interiors. The traction per boundary is τ = F/(2A). Runs are 100 ps at 4000 and 5000 K.
- **Quench and NEB** (`tools/gb_event_neb.py`): every snapshot is quenched at zero force to give the sequence of minima, then CI-NEB runs between neighbouring minima (9 images, all atoms free, fixed cell).

| T (K) | τ = 0.5 GPa | 1 GPa | 2 GPa | 3 GPa |
|---|---|---|---|---|
| 4000 | locked | locked | locked | coupled migration, u = 7.0 Å in about 5 ps |
| 5000 | locked | locked | coupled migration, u = 7.2 Å in about 10 ps | coupled migration, u = 7.5 Å (pause at 2.7 Å) |

Results:
- **Mechanism: shear-coupled migration.** Under load both boundaries move 11–13 Å in z while u_x grows by about 7 Å, a coupling of about 0.6 (the ⟨100⟩ Cahn–Taylor value for Σ5 is 2 tan(θ/2) = 0.67). Motion stops once the boundaries reach the forced interior groups, which is an artefact of the set-up.
- **The end state is equivalent to the start.** Quenched at zero force, ΔE = −0.4 / +0.3 eV over the cell (< 0.01 J/m²). Along the way the boundary passes near-degenerate minima about 1.3–1.9 Å apart in u, and quenched energies scatter by ±2 eV through local disorder.
- **NEB barriers between neighbouring minima** (4000 K / 3 GPa run, frames 0–5): 16.6, 18.0, 28.1 and 14.2 eV for Δu_x = 1.32, 1.92, 1.35 and 0.54 Å. That is 0.25–0.50 J/m² per boundary. One segment (2→3) did not converge.
- **These are collective barriers.** In the 1× cell (L_x = 30 Å) the whole boundary moves at once, so the barrier scales with area, and the TST rates (10⁻⁹–10⁻² s⁻¹) are not transferable.
- **Consistency check.** The athermal stress estimate τ_c ≈ γ_b/Δu ≈ 0.3 J/m² / 1.5 Å ≈ 2 GPa matches the MD onset of 2–3 GPa.
- **A transferable barrier needs a localized disconnection.** That needs room along x. The driven runs in a 3×1 cell (L_x = 89 Å, job 4336984) test this: a lower onset stress and a step that runs along the boundary would identify a disconnection mechanism.

## 5h. Driven boundary in a 3×1 cell at 140 GPa: is the step localized? (T18, job 4336984, 2026-10-11)

Setup: same as §5g, with the bicrystal replicated 3× along x (L_x = 89.4 Å, L_y = 15.1 Å, L_z = 59.6 Å, 11 760 atoms, A = 1347 Å² per boundary). 20 ps NVT + 100 ps driven, snapshot every 1 ps. Scan: `gb_event_neb.py scan` → `GBslide/drive/analysis_3x1/{gb_events.json,fig_gb_drive.*}`.

| T (K) | τ = 1 GPa | 1.5 GPa | 2 GPa | 2.5 GPa |
|---|---|---|---|---|
| 4000 | – | locked (u = 0.06 Å) | one step, u = 1.5 Å at 3–4 ps, then locked | locked (u = 0.4 Å) |
| 5000 | locked (0.2 Å) | locked (0.03 Å) | coupled migration, u = 5.0 Å over frames 8–14, then stops | – |

Results:
- **The onset stress barely moves.**
  - At 5000 K it is still between 1.5 and 2 GPa, as in the 1× cell.
  - At 4000 K a single step occurred at 2 GPa (the 1× cell needed 3 GPa), but nothing happened at 2.5 GPa. Motion at this stress is therefore stochastic within 100 ps.
  - There is no clear area effect of the kind a disconnection mechanism would produce.
- **Quenched states of the 5000 K / 2 GPa run, frames 9–17.**
  - Method: LAMMPS FIRE quench (`tools/gb_quench.lammps`, `drive/gb_quench_job.sh`, job 4346903), analysed with `tools/gb_quench_u.py`. Output in `V6.6868_3x1_5000K_tau2/quench/quench_u.txt`.
  - Frames 10 and 12–16 quench to minima with identical energy (to 10⁻⁶ eV). Frames 12–16 are the same structure. Frame 10 differs from them by Δu_x = 1.18 Å and Δz_b ≈ 2–3 Å, a coupling of about 0.5. It is one translation period of coupled migration: symmetry-equivalent states.
  - Frame 9 lies 14.2 eV lower (0.08 J/m² per boundary) and has a different boundary structure. The slab z_b finder fails on it.
  - Frames 11 and 17 have the same u as frame 12 but lie 27.7 and 12.9 eV above it. Each has one disordered x-slab on one boundary: a local defect, not a partly advanced step.
- **No localized disconnection is seen.** In every equivalent minimum, z_b is uniform in x to within about 3 Å (one atomic plane) across all six slabs, both in the quenched states and in the MD frames, where the 5000 K noise is larger. The step still advances the whole boundary at once, even with L_x = 89 Å.
- **Quench caveat:** the image flags in `quench_<k>.data` are stale (`read_dump … replace yes`). Positions must be rebuilt as MD frame + minimum-image displacement. The naive unwrap gives u drifting by 4.4 Å per frame. ASE quench of 11 760 atoms fails (“cannot allocate mem for nlist”, jobs 4346889 and 4346900), so use LAMMPS for these cells. Cause: GPU memory. With no external neighbour list, DeePMD's TF op builds a dense n_loc × n_all buffer on the GPU (n_all rounded up to a power of 2, here 65 536 for rc = 7 Å), about 9 GB, plus the previous 4.6 GB buffer held while it grows. The 4096-atom 1× cell needs only 0.8 GB. Host RSS was 2 GB of 18 GB, so the task memory limit is not the issue. Fix: pass `neighbor_list=NewPrimitiveNeighborList(...)` to `deepmd.calculator.DP` (memory ∝ n_loc × max_nbor), or use a larger-memory GPU.
- **NEB between quenched frames 10 and 12 (ASE + DeePMD with ASE neighbour lists, P100, job 4359736, 22 h; archived in `V6.6868_3x1_5000K_tau2/neb_try1/`).**
  - Quenched ends (ASE FIRE, fmax 0.03): ΔE = −0.99 eV, Δu = (0.94, −0.16, 0.0) Å.
  - Stage 1 (9 images, no climbing image) converged to fmax 0.1 eV/Å with the highest image **≈ 29.5 eV above the start, 0.175 J/m² per boundary**.
  - The climbing-image stage then diverged: fmax rose from 0.17 to 70 eV/Å with FIRE's default maxstep of 0.2 Å, and the final band (peak 1303 eV) is meaningless. The interpolation was not the cause: no atom crosses the box between the two ends (max |Δr| = 2.3 Å).
  - **Interim reading:** 29.5 eV is 1.0–1.8× the 1× cell's 16.6–28 eV (§5g), not the 3× expected if the whole boundary moved at once. In J/m² it is 0.175, against 0.25–0.50 in the 1× cell. The saddle in the wider cell is therefore cheaper per area, which hints at partial localization, although the end states look collective. The number is only an estimate until a climbing image converges.
  - **Rerun:** job 4407041, 24 h. `gb_event_neb.py` now:
    - saves the stage-1 band (`neb_10_12_stage1.traj`);
    - runs the climbing stage with maxstep 0.05 Å, keeps the lowest-fmax band, stops if fmax grows 5× and checkpoints every 50 steps (`neb_10_12_ci.traj`; restart with `--from-band`);
    - reports where the saddle displacement lies along x: the share of $\sum|\Delta r|^2$ in each of 6 x-slabs, where 1/6 each means collective.
- **Rerun 4407041 (analysed 2026-10-15).**
  - Stage 1: 28.6 eV (0.170 J/m²).
  - The guarded climbing stage was stopped as diverging, and the best band was kept (not converged). Forward barrier 28.3 eV (0.168 J/m² per boundary).
  - The band passes through an intermediate state 9.5 eV below the start.
  - **Saddle displacement per x-slab:** 0.155, 0.152, 0.219, 0.140, 0.160, 0.174 (fully collective = 0.167). **The step is collective; there is no localized disconnection**, even with L_x = 89 Å.
  - Conclusion: the low-stress kinetics of the 140 GPa boundary must come from explicit, pre-existing disconnections. This is G1–G3 of `ANELASTICITY_PLAN_DRIVEN_RHEOLOGY.md`.
- **Next (superseded by the driven-rheology plan):**
  1. Read the localization of the converged saddle.
  2. If the saddle is localized, build an explicit disconnection dipole in a long-x cell. Otherwise, drive at lower stress for longer times to look for nucleation.

## 5i. MgSiO₃ at $V$ = 6.5669 Å³/atom and comparison with MgO (T19, 2026-10-11/12)

**Setup.**
- 1280 atoms at fixed V (100–161 GPa), with X. Deng's finite-temperature DeePMD model (`graph_c.pb`, fparam = $k_BT$).
- Same protocol as MgO §2–3 (methods §2): Green–Kubo (1.5 ns NVE), liquid shear and uniaxial sweeps at 10 GHz–5 THz, and crystal sweeps at 0.2–5 THz.
- **Two branches at the same V:**
  - the liquid, cooled from 8000 K;
  - Pbnm bridgmanite, heated from 2000 K.
  - Start states come from T ladders (`tools/T_ladder.lammps`).
- **Tools:**
  - `tools/stage_T_series.py`;
  - `tools/anelastic_cases_MgSiO3_V6.5669.py`;
  - `anelastic_collect.py`, now with a per-case GK cutoff (`GKTC`) and a crystal branch (`XTAL`) in `fig_vs_T`.
- **Output:**
  - `results_MgSiO3_V6.5669/` (results_all.md/csv, fig_*);
  - run directories under `/groups/carnegie_poc/rcohen/LAMMPS/MgSiO3/1280atoms/V6.5669/{liquid,crystal}/<T>K/`.

**State checks.**
- **The liquid does not crystallize down to 4000 K.** PE is flat over each 1.5 ns run.
  - Diffusion coefficients in $10^{-9}$ m²/s (Mg, Si, O): 8.7, 9.7, 11.7 at 7000 K; 5.4, 4.1, 5.7 at 6000 K; 2.8, 2.3, 3.1 at 5000 K; 0.3, 0.3, 0.4 at 4000 K.
  - At 4000 K the MSD still reaches about 260 Å² in 1.5 ns, so it is a deeply supercooled liquid, not a glass.
  - MgO, by contrast, crystallized at 5000 K, and at 6000 K after 1 ns.
- **The crystal stays crystalline up to 5000 K** (123 GPa): MSD ≤ 0.3 Å², with no PE drift. This is near or above the experimental melting curve, so it is superheated over 1.5 ns.
- **At 4000 K the cooled liquid lies 0.45 eV/atom above the crystal.**
- **Uniaxial thermostat check (methods Eq. 11).**
  - $(\partial p/\partial T)_V$ = 10.3 MPa/K, from the GK pressures at 5875 and 7073 K.
  - With $C_V$ = 3–4.5 $k_B$/atom this gives $K_S-K_T=T(\partial p/\partial T)_V^2/C_V\approx$ 55–85 GPa.
  - Thermal relaxation then adds at most $(K_S-K_T)/(\omega\tau_T)$ = 1.4, 1.4, 0.3, 0.03 and 0.01 GPa to $M''$ at 5 THz–10 GHz, which is ≤ 3% of the measured $M''$. The τ_T ≫ P rule holds.

**Liquid viscosity** (GK cutoffs from the η(t) plateaus: 2, 2, 5 and 20 ps at 7000–4000 K):

| T (K) | ⟨p⟩ (GPa) | $\eta_0$ GK (mPa s) | $\eta_0$ sweep slope (mPa s) | $\zeta_0$ GK (mPa s) | $\zeta_0/\eta_0$ | $G_\infty$ (GPa) | MgO $\eta_0$ at same T (GPa) |
|---|---|---|---|---|---|---|---|
| 7000 | 161.1 | 7.49 ± 0.26 | 7.33 ± 0.49 | 1.77 ± 0.16 | 0.24 | 284 | 11.18 ± 0.29 (183) |
| 6000 | 148.7 | 12.80 ± 0.48 | 11.55 ± 0.41 | 3.23 ± 0.25 | 0.25 | 299 | 18.30 ± 0.48 (175) |
| 5000 | 141.2 | 23.2 ± 1.7 | 22.9 ± 1.8 | 5.27 ± 0.62 | 0.23 | 310 | crystallized |
| 4000 | 129.1 | 220 ± 19 | 49 ± 9 (nonlinear, see below) | 50 ± 11 | 0.23 | 319 | crystallized |

- **GK and the sweeps agree at 5000–7000 K** for $\eta_0$, as they did for MgO.
- **At 4000 K the low-frequency sweep points are nonlinear.** The amplitude rule $\gamma_0\omega=10^{11}$ s⁻¹ gives γ₀ = 0.32 and 0.5 at 50 and 10 GHz. There $|\sigma_3/\sigma_1|$ = 0.14 and 0.10, and $\eta'$ = 58 and 112 mPa s, against 110 and 219 from GK: shear thinning.
  - From 0.2 to 5 THz the sweeps agree with GK (35.8 against 34.7 mPa s at 0.2 THz).
  - A linearity test (γ₀ = 0.05 and 0.1, `liquid/4000K/FreqSweep_lin`, job 4406967) is running.
  - For supercooled liquids the amplitude rule needs $\gamma_0\omega\tau_\alpha\ll1$, with $\tau_\alpha$ the slow (α) relaxation time, about 10 ps at 4000 K. $\tau_0=\eta_0/G_\infty$ = 0.7 ps is not the right time scale here.
- **At the same T, liquid MgSiO₃ is about 1.4× less viscous than liquid MgO** (7.5 against 11.2 mPa s at 7000 K), but at 20–25 GPa lower pressure. It is also much more fragile: η rises 9.5× from 5000 to 4000 K, against 2.2× from 8000 to 6000 K for MgO.
- **Bulk viscosity is relatively 2.4× larger:** $\zeta_0/\eta_0\approx0.24$, against 0.1 for MgO. This is consistent with the Si–O coordination changes available to the silicate melt.

**Q comparison at 0.2 and 1 THz** (sweeps, lag-corrected; bounds are 2σ):

| material, cell | T (K) | p (GPa) | shear Q 0.2 / 1 THz | uniaxial Q 0.2 / 1 THz |
|---|---|---|---|---|
| MgSiO₃ liquid | 7000 | 161 | < 0.43 / 0.25 ± 0.11 | 46 ± 8 / 14 ± 3 |
| MgO liquid | 7000 | 183 | 0.086 ± 0.023 / 0.50 ± 0.02 | 37 ± 6 / 9.0 ± 0.3 |
| MgSiO₃ liquid | 6000 | 149 | 0.21 ± 0.06 / 0.46 ± 0.14 | 27 ± 4 / 8.6 ± 0.8 |
| MgO liquid | 6000 | 175 | 0.27 ± 0.02 / 0.76 ± 0.05 | 23 ± 2 / 8.0 ± 0.4 |
| MgSiO₃ liquid | 4000 | 129 | 1.0 ± 0.1 / 2.6 ± 0.2 | 11 ± 1 / 13 ± 2 |
| MgSiO₃ bridgmanite, perfect | 5000 | 123 | > 109 / 63 ± 15 | 154 ± 19 / 63 ± 10 |
| MgO B1, perfect (C₄₄) | 5000 | 152 | > 155 / > 120 | 71 ± 12 / 27 ± 1 |
| MgO melt-grown polycrystal | 5000 | 152 | 31 ± 7 / 19 ± 0.5 | 108 ± 36 / 49 ± 5 |
| MgSiO₃ bridgmanite, perfect | 4000 | 115 | > 69 / > 54 | > 182 / 98 ± 13 |
| MgO melt-grown polycrystal | 4000 | 145 | 60 ± 12 / 26 ± 3 | 127 ± 8 / 66 ± 6 |
| MgSiO₃ bridgmanite, perfect | 3000 | 108 | > 209 / 98 ± 34 | > 269 / 118 ± 17 |
| MgSiO₃ bridgmanite, perfect | 2000 | 100 | > 234 / 156 ± 36 | > 273 / 175 ± 10 |

- **Liquids:** the shear Q of the two liquids is similar at the same T. Uniaxial Q is slightly higher in MgSiO₃, despite its larger $\zeta_0/\eta_0$, because $M'$ is lower (≈ 610–660 against 640–690 GPa).
- **Perfect crystals at 5000 K:**
  - Shear loss is higher in bridgmanite (Q = 63 against > 120 for MgO's C₄₄ at 1 THz).
  - Uniaxial loss is lower in bridgmanite (Q = 63 against 27 at 1 THz, and 154 against 71 at 0.2 THz).
  - MgO's longitudinal loss is Akhiezer-like: M′ rises from 1191 to 1312 GPa between 0.2 and 5 THz.
- **Bridgmanite has a 5 THz resonance that rock-salt MgO cannot have.** Between 1 and 5 THz the uniaxial $M'$ of bridgmanite falls (806 → 763–767 GPa at every T), while $M''$ rises to 18–50 GPa. The 5 THz shear loss is largest at the lowest T ($G''$ = 48 GPa at 2000 K, 20 GPa at 5000 K). The local Kramers–Kronig test fails at 1–5 THz by 8–40σ, whereas it holds at 0.2–1 THz within about 3σ.
  - This is the signature of strain driving an internal coordinate below its resonance: a Raman-active (A_g) mode, such as an octahedral tilt in Pbnm, coupled to strain through the internal-strain tensor Λ.

$$M^*(\omega)=M_{\rm clamped}-\sum_k\frac{\Lambda_k^2/m_k}{\omega_k^2-\omega^2-i\omega\Gamma_k} \tag{14}$$

  - At ω → 0, Eq. 14 gives the relaxed modulus. As ω approaches $\omega_k$ from below, $M'$ falls and $M''$ peaks with width $\Gamma_k$.
  - In B1 MgO every atom sits at an inversion centre, so Λ = 0 and the term is absent.
  - The resonance is phonon physics, not anelasticity. Crystal Q for the comparison should use ≤ 1 THz.
  - It is consistent with pressure hardening of $\omega_k$: p rises from 100 to 123 GPa with T at fixed V, which moves the mode away from 5 THz and lowers the 5 THz loss.
- **Bottom line so far:**
  - At the same T and THz frequency, perfect bridgmanite has a shear Q at most about half that of perfect MgO (MgO's is only a lower bound), a uniaxial Q about 2× higher, and less loss than melt-grown (polycrystalline) MgO in both channels.
  - The melt-grown/defect contrast seen in MgO (Q 19 against > 120 at 5000 K, 1 THz) means defects and boundaries, not the perfect lattice, will set the comparison. The next step is the MgSiO₃ Schottky-type defect cell (V_Mg + V_O), followed by boundaries.

## 5j. Temperature dependence: one activation energy, curved, or T-independent? (2026-10-12)

**Method.** `tools/T_dependence.py` runs on `results_gk.csv` (new collector output) and `results_all.csv` for all three cases, giving `results_Tdep/{T_dependence.md,.csv}` and `fig_T_dependence`. For each quantity y(T) it computes:
- the local apparent energy between neighbouring temperatures, $E_{loc}=s\,k_B\,\Delta\ln y/\Delta(1/T)$, with s = +1 for η, ζ and s = −1 for D and $Q^{-1}$;
- a single-E Arrhenius fit;
- a power law $y\propto T^n$, where n = 0 means T-independent;
- for 4 or more points, VFT, $\ln y=a+sB/(T-T_0)$.

All series are at fixed V, so the energies are **isochoric**. The isobaric value is larger:

$$E_P=E_V+k_BT^2\left(\frac{\partial\ln\eta}{\partial p}\right)_T\left(\frac{\partial p}{\partial T}\right)_V \tag{15}$$

For liquid MgO at 6000 K the two volumes give $(\partial\ln\eta/\partial p)_T$ = 0.013 GPa⁻¹ (activation volume ≈ 1.1 Å³). With $(\partial p/\partial T)_V$ = 8.4 MPa/K, $E_P-E_V\approx$ 0.35 eV. The correction grows only as T², so it shifts the energies below by about 0.2–0.4 eV without changing their curvature.

**1. Liquids: no single activation energy. Both melts are super-Arrhenius, and MgSiO₃ strongly so.**

| liquid | quantity | $E_{loc}$ (eV), high T → low T | single Arrhenius χ²/ν | VFT |
|---|---|---|---|---|
| MgSiO₃ (129–161 GPa) | η₀ | 1.60 ± 0.15 (5875–7073 K), 2.20 ± 0.30 (5168–5875 K), 3.56 ± 0.18 (4035–5168 K) | 34.5 | $T_0$ = 2770 ± 160 K, χ²/ν = 0.1 |
| MgSiO₃ | D_O | 2.15 ± 0.16, 2.21 ± 0.26, 3.21 ± 0.14 | 13 | $T_0$ = 1940 ± 260 K, χ²/ν = 0.8 |
| MgSiO₃ | D_Si | 2.59 ± 0.45, 2.13 ± 0.29, 3.48 ± 0.11 | 7.6 | $T_0$ = 2230 ± 370 K |
| MgO, V6.6868 (175–193 GPa) | η₀ | 1.34 ± 0.15 (6977–8112 K), 1.79 ± 0.13 (5986–6977 K) | 3.3 | – (3 points) |
| MgO, V6.6868 | D_Mg, D_O | 1.88 ± 0.14 → 2.20 ± 0.10 (Mg); 1.87 ± 0.29 → 1.89 ± 0.30 (O) | 2.0, 0.0 | – |
| MgO, V9.6397 (38–50 GPa) | η₀ | 0.83 ± 0.03 (3968–6010 K, 2 points) | – | – |

- **MgSiO₃:** the apparent energy of viscosity more than doubles, from 1.6 to 3.6 eV, between 7000 and 4000 K. A single-E Arrhenius fit is rejected (χ²/ν = 34), and VFT fits within errors. The divergence temperature $T_0$ ≈ 2800 K lies about 1200 K below the lowest liquid run, so extrapolating from the melt to lower T with a single E would underestimate η badly. Diffusion shows the same curvature; Si and O jumps steepen most at 4000–5000 K.
- **MgO:** curvature is present but weaker. $E_{loc}$ for η₀ rises from 1.34 to 1.79 eV (2.3σ). O diffusion is Arrhenius at 1.9 eV within errors over 6000–8100 K. MgO crystallizes below about 5500 K, so its supercooled range cannot be explored. At 40–50 GPa (V9.6397) the energy is about half (0.8 eV), so the barrier grows with compression.
- **Decoupling.** In MgSiO₃, $D\eta/T$ (Stokes–Einstein) is not constant. η rises 29× from 7073 to 4035 K, while $T/D_O$ rises only 16×. This is the usual sign of a fragile liquid approaching a glass transition.

**2. Crystals at THz: not activated. The loss is close to linear in T, as expected for anharmonic phonon damping.**

| crystal | channel, f | $E_{loc}$ (eV) | single E (eV), χ²/ν | power n, χ²/ν |
|---|---|---|---|---|
| bridgmanite, perfect, 2000–5000 K | uniaxial 1 THz | 0.20 ± 0.08, 0.19 ± 0.20, 0.77 ± 0.36 | 0.24 ± 0.04, 1.2 | **0.98 ± 0.14**, 0.6 |
| bridgmanite, perfect, 2000–5000 K | shear 1 THz | 0.24 ± 0.21, −0.13 ± 0.66, 0.98 ± 1.02 | 0.25 ± 0.09, 0.3 | **0.95 ± 0.36**, 0.2 |
| MgO melt-grown, V6.6868, 4000–5000 K | shear / uniaxial 1 THz | 0.55 ± 0.18 / 0.52 ± 0.22 | – | 1.4 ± 0.5 / 1.4 ± 0.6 |
| MgO melt-grown, V9.6397, 2000–3000 K | shear / uniaxial 1 THz | 0.02 ± 0.03 / 0.11 ± 0.02 | – | **0.1 ± 0.1** / 0.5 ± 0.1 |

- **Perfect bridgmanite:** $Q^{-1}\propto T^{1.0}$, and a "fit" energy of 0.24 eV is an order of magnitude below any atomic barrier. Classical anharmonic phonon damping gives $Q^{-1}\propto T$, because phonon populations scale with T above the Debye temperature. This loss is not thermally activated in the Arrhenius sense. Classical MD has no quantum freeze-out, which is irrelevant at mantle temperatures.
- **MgO melt-grown at 18–20 GPa:** shear $Q^{-1}$ at 1 THz is **T-independent** within errors from 2000 to 3000 K. This crystal holds mobile, freely sliding boundaries (§4). Their loss at THz is set by boundary viscosity and geometry, not by a barrier. At 140 GPa the melt-grown MgO loss rises faster than T (n ≈ 1.4), the first sign of a thermally assisted component.
- **At 0.2 THz** the perfect-crystal loss is mostly unresolved (Q > 100–270). The fits are in the table but carry little weight.

**3. Where activation does enter: the elementary defect and boundary events,** and each is curved too.
- **MgO vacancy jumps (§5a):** $E_{loc}$ falls from 3.6 to 2.1 eV (Mg) and from 4.6 to 2.1 eV (O) between 3500 and 5000 K, against static NEB barriers of 2.6–3.8 eV (§5b). The curvature comes from a changing mix of mechanisms, not one barrier.
- **The 140 GPa Σ5 boundary:** it migrates only by collective steps with barriers of 14–30 eV per cell (§5g–h), which no single per-area energy describes.

**Answer so far.**
1. At the THz frequencies MD reaches directly, crystal loss is not activated: perfect crystals go as $Q^{-1}\propto T$, and boundary-rich MgO at low pressure is T-independent.
2. Liquid relaxation is activated but super-Arrhenius, strongly so in MgSiO₃ (VFT, $T_0$ ≈ 2800 K).
3. Seismic loss must come from the activated defect and boundary relaxations. Their rates are measured, but their apparent energies are T-dependent, so a single-E (Karato-type) extrapolation from high T is not supported for either material.
4. **Update 2026-10-13: both missing series are done** (full write-up: `results_Tdep/T_DEPENDENCE_RESULTS.md`).
   - **MgO perfect B1, 3000–5000 K:**
     - uniaxial 1 THz: $Q^{-1}$ = 0.020, 0.030, 0.037, so $Q^{-1}\propto T^{1.22\pm0.11}$. The formal E of 0.40 ± 0.03 eV is far below any barrier, so this is phonon damping.
     - uniaxial 0.2 THz: T-independent ($n$ = 0.2 ± 0.4, $Q^{-1}$ ≈ 0.014), plausibly Akhiezer damping with ωτ_ph ≪ 1.
     - C₄₄ shear: unresolved (Q > 300) at every T.
   - **Bridgmanite V_Mg + V_O (6 pairs), 3000/4000/5000 K:**
     - 1 THz $Q^{-1}$: no excess over the perfect crystal at 3000 K; +25–60 % at 4000–5000 K, but each difference is only about 1σ. The defect THz loss is unresolved.
     - O vacancies: $\Gamma_v$ ≈ 5×10⁹, 3×10¹⁰, 2×10¹¹ s⁻¹. One energy fits, E = 2.36 ± 0.12 eV (χ²/ν = 0.6; $E_{loc}$ 1.8 ± 0.8 then 3.3 ± 1.2 eV, a weak test).
     - Mg vacancies: frozen below 5000 K (≤ 0.3 jumps per vacancy in 1.5 ns); 1.4×10¹⁰ s⁻¹ at 5000 K. This is the opposite of MgO, where Mg and O vacancies move at similar rates.
     - Si moves at 5000 K without Si vacancies (antisites or Frenkel defects?), not yet analysed.
   - **Revised answer:**
     - THz crystal loss is phonon loss, T-linear or T-independent, in both minerals.
     - The activated processes are the vacancy jumps: single-E for O in bridgmanite, curved in MgO.
     - The bridgmanite defect relaxation still has to be measured below 50 GHz (the MgO Schottky analogue) before the seismic-band comparison can be made.

## 5k. Edge-dislocation drag in MgO at 175 GPa / 3500 K and the Perez et al. (2025) bound (2026-10-13)

Full write-up: `results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md`. Run: job 4452807.
- **Setup:** ½[110](001) edge dislocation, 8232 atoms, MgO-only DeePMD model; τ = 0.1–1 GPa applied through rigid blocks.
- **Superseded 2026-11-15 (§5m):** B = 1.76 × 10⁻⁴ Pa s with no threshold down to 0.15 GPa; the values below used a top block that was not rigid.
- **Drag:** viscous glide at τ ≥ 0.5 GPa with $v=b\tau/B$ and **B = 2.2 × 10⁻⁴ Pa s**. No steady glide at τ ≤ 0.25 GPa: either a threshold or too short a run (100 ps runs to follow).
- **Effective viscosity:** $\eta_{eff}=B/(\rho b^2)$ = 330, 33, 3.3 and 0.33 Pa s for ρ = 10¹³, 10¹⁴, 10¹⁵ and 10¹⁶ m⁻².
  - This meets Perez's η ≤ 10² Pa s for ρ ≳ 3 × 10¹³ m⁻², or about 10¹⁴ m⁻² with orientation factors.
  - Drag-limited flow stress at 10⁷ s⁻¹ is ≤ 0.33 GPa for ρ ≥ 10¹⁴ m⁻², so the ≲ 1 GPa strength is set by the threshold, not drag.
- **Granato–Lücke:** with this B, string damping (plan Eq. 13) peaks at 7 kHz for L = 100 µm and needs L ≈ 1 cm for 1 Hz. Drag-controlled dislocation loss is not a seismic-band mechanism; kink-pair or pinning processes would be needed.

## 5l. MgO models against DFT and experiment (2026-10-14)

Full write-up: `results_dft/MGO_DFT_MODEL_COMPARISON.md`; figure `results_dft/mgo_dft_model_comparison.pdf/png`.

VASP PBEsol single points (Deng training settings) were run on 8 MD frames each of perfect and bound-pair MgO (512/510 atoms) at 20 GPa / 2000 K and 140 GPa / 3000 K. Each frame was scored with both DeePMD models; the experimental EOS is Tange et al. 2009.

- **EOS:**
  - Deng ≈ PBEsol (ΔP ≤ 0.3 GPa at fixed V); within 2.3 GPa of experiment.
  - **MgO-only model: +5 to +9 GPa relative to PBEsol at fixed V, and +7 to +13 GPa relative to experiment (20–175 GPa).** It was trained with PBE: confirmed 2026-11-15 (§5m).
  - VIB (Ita & Cohen): −1 GPa at 20 GPa, −10 GPa at 140 GPa.
- **Forces:** RMSE against PBEsol is 0.054–0.074 eV/Å for the MgO-only model and 0.066–0.082 eV/Å for the Deng model (RMS force 1.6–3.0 eV/Å).
- **Bound-pair ΔG_f model error** (DFT − model, Eq. 2 there):
  - Deng: +0.95 and +1.27 eV;
  - MgO-only: +0.72 and +0.96 eV;

  so both underbind the pair by about 1 eV.
- **DFT-corrected ΔG_f** is 6.10 eV (20 GPa) and 13.2–14.8 eV (140 GPa), against VIB 7.51 and 15.79 eV. VIB is 1.0–2.6 eV too high, and this is not from its EOS.
- **Consequence for this summary:** pressures quoted for MgO-only runs are 7–13 GPa above the experimental scale. V6.6868 (175–193 GPa) is ≈ 162–180 GPa; the edge run labelled 175 GPa is at ≈ 162 GPa. Volume-based comparisons are unaffected.

## 5m. Results of 2026-11-15 (jobs finished 10-15 to 10-17)

1. **MgO edge dislocation, long lines (D1, D1b; `results_dislocations/MGO_EDGE_DISLOCATION_RESULTS.md` §8, figure `edge_vtau_core`).**
   - The drive's top block was not rigid (`fix aveforce` on unequal masses): its Mg and O sublattices slid apart, and the block-based velocities were 21 % low. Fixed in `disl_drive.lammps` (`fix rigid/nve single`). The stress reached the dislocation correctly.
   - From glide-plane core tracking: **v = bτ/B with B = (1.755 ± 0.027) × 10⁻⁴ Pa s** for τ = 0.15–0.5 GPa, no threshold (τ₀ = −0.006 ± 0.014 GPa), the same for 63 and 262 Å lines. The line stays straight to within one Peierls valley; no kink pairs. Phonon-drag glide at 3500 K / ≈ 162 GPa.
   - η_eff = 256 Pa s at ρ = 10¹³ m⁻² (Perez bound met above 2.6 × 10¹³ m⁻²). Granato–Lücke peak 1.25× higher than in §5k; still not seismic.
2. **The MgO-only model is PBE-trained** (`results_dft/MGO_DFT_MODEL_COMPARISON.md` §8): against PBE its pressure is within 0.3–1.0 GPa and its energy offset is constant. Its bound-pair ΔG_f is low by 0.5–0.9 eV against PBE (a model error); PBEsol − PBE is only 0.05–0.16 eV.
3. **G-diff, MgO Σ5 at the Cordier/Fei states (Deng model; `results_cordier2023/CORDIER2023_COMPARISON.md` §5).** Frozen in 1 ns at 27/2200, 30/2000, 90/2500, 120/2800 GPa/K: δD_b < 10⁻²³ m³/s, sliding locked. At 60/2300 the boundaries migrate with stick–slip sliding (14 jumps of 1–3.5 Å per ns), β_x = 7.4 × 10⁶ Pa s/m. For this boundary, grain-boundary diffusion does not overturn Cordier's conclusion (Coble η ≳ 10²¹ Pa s at 0.4 mm).
4. **Bridgmanite V_Mg + V_O at 50 and 20 GHz** (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.3): G″ unresolved (Q ≥ 65–280) at 4000 and 5000 K, against Q = 9.7 and 3.7 for MgO aged Schottky at a similar vacancy fraction. Bridgmanite vacancy loss is at least 20–35× smaller.
5. **Time step (Deng model):** 2 fs is safe for production (ΔP ≤ 0.3 GPa); 3 fs fails for Bdg (ΔP 0.75 GPa), 5 fs blows up. PE bias at 2 fs is 3–10 meV/atom, so keep 1 fs for activated rates (`DengStates/README.md`).
6. **MgO polycrystal** (26 k atoms, 60 GPa / 2300 K, 300 ps): runs on the P100; no grain growth in 300 ps.
7. **Bdg boundary energy:** energy-only γ_E (no PΔV) is 2.49 (021), 2.57 (013), 1.77 (011) J/m², still 1.8× van Driel for (021).
8. **Talk trajectories (RC1):** six VMD-ready movies in `/groups/carnegie_poc/rcohen/LAMMPS/TalkTrajectories` (README there).

## 5n. Results of 2026-11-16 (jobs of 11-15)

1. **MgO vacancy free energies, Deng model (A1/A2; `results_freeenergy/MGO_VACANCY_FREE_ENERGIES.md`).** Bound-pair ΔG_f 5.3–12.5 eV, separated 6.5–15.3 eV (20–140 GPa); ΔG_m(Mg) 2.2–3.9, ΔG_m(O) 2.4–4.5 eV. Migration matches Ita & Cohen (VIB) within 0.15 eV except O at 140 GPa; formation is 2–4 eV below VIB. Raw intrinsic D_O is 10⁴–10⁵ × Cordier's values, driven by the separated-pair ΔG_f, which still needs a DFT check (short-range model, no long-range electrostatics).
2. **Liquids at matched (P, T), one model (`results_Tdep/LIQUID_SE_ODENSITY.md` §6).** MgO and MgSiO₃ have η₀ within 5–13 % and D_O within 1.2–1.4× at 50–150 GPa, 6000–7000 K; Stokes–Einstein holds in each; D_O is not a function of the O number density alone.
3. **MgO Schottky 20 GHz loss (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.4).** G″ rises with T (E_app = 3.2 ± 0.6 eV, 4000–5000 K). The 6×6×6 cell shows almost no 20 GHz loss and a lower, flat G′, contradicting both τ ∝ L² and a local mechanism; the 8×8×8 20 GHz values (18 cycles) may include slow-event noise. The cell-scale-diffusion reading of §3.1 is withdrawn pending reruns.
4. **Σ5 at 60 GPa (`results_cordier2023/CORDIER2023_COMPARISON.md` §5.1):** locked at 2000 K, shear-coupled migration at 2300–2900 K (15–38 jumps/ns, β_x ≈ 10⁷ Pa s/m), no Arrhenius law.
5. **A3 bridgmanite** set up and running (restart 11-16 §3). Direct MD of an isolated O vacancy (V6.5669, separated V_Mg + V_O, `FreeEnergy/A3_Bdg_Deng/README.md`): Γ_v = 6.0×10¹⁰ s⁻¹ at 3021 K and 3.1×10¹¹ s⁻¹ at 4020 K (12 and 31 hops), E ≈ 1.7 ± 0.4 eV, 10–12× the per-vacancy rate in the V_Mg + V_O MD cell; mostly O1 ↔ O2 edge jumps.
6. **Submitted 11-16 (RC "Yes do 1 2 3 4 5"; INPROGRESS §1b):** DFT check of the separated MgO pair (binding curve and FEP), Schottky 20 GHz reruns (2 ns 8×8×8; 1.5 ns-aged 6×6×6), Σ5 unlocking T at 90/120 GPa, MgO TST against direct hops, Rosenfeld scaling of the liquids.

## 5o. Results of 2026-11-16, evening (A3; items 3–5 of the 11-16 proposals)

1. **Bridgmanite vacancies, A3 (`results_freeenergy/BDG_VACANCY_A3.md`).**
   - The O vacancy is very mobile: edge-jump barriers are 0.9 (30 GPa) to 1.9 eV (120 GPa), and the per-vacancy hop rate is 3×10¹⁰–5×10¹¹ s⁻¹ at the Cordier states, ≈ 10⁴ × periclase. TST is confirmed by direct MD (κ ≈ 0.6). O1 and O2 vacancy sites are within 0.07 eV.
   - V_Mg is slow: ΔG_m = 4.7–6.0 eV at 60–120 GPa.
   - The same mobility spoils the Frenkel–Ladd formation runs of every cell with V_O (hops at λ ≈ 0; hop-averaged tether sites; at 30 GPa the defects rearranged: V_O–V_Si clustering, pair dissociation). Provisional hop-free values: MgO partial (separated) 8.5–11.8 eV at 60–120 GPa, 1.5–1.8 eV below periclase's; the full Schottky closes Eq. 2 at 90 GPa (30.2 eV).
   - Si migration is unusable.
   - Fix proposed: single-vacancy cells, and low-T Frenkel–Ladd plus ⟨E⟩(T) integration (≈ 60 P100-h).
2. **MgO TST check (`MGO_VACANCY_FREE_ENERGIES.md` §6).** Direct MD hop counts at 3000–4200 K agree with the umbrella TST: κ = 0.5–1.6, mean 1.0. ΔG_m changes ≤ 0.17 eV with T at fixed V. The separated vacancies meet and bind within 0.5 ns; bound pairs hop at different rates (bound-pair channel).
3. **Σ5 at 90 / 120 GPa (`CORDIER2023_COMPARISON.md` §5.2).** Locked at every state up to 3400 / 3800 K; at 60 GPa it unlocks at ≈ 2000–2300 K. The unlocking temperature rises by > 1100 K from 60 to 90 GPa, so the boundary is mobile only near the top of the lower mantle.
4. **Rosenfeld scaling of the liquids (`results_Tdep/LIQUID_SE_ODENSITY.md` §7, `rosenfeld.{pdf,png}`).** Against the two-body excess entropy s₂, MgO and MgSiO₃ fall on one line: D*_O within 8 % rms, η* within 10 % (ln D*_O = −0.39 + 0.96 s₂/k_B; ln η* = −1.37 − 0.90 s₂/k_B; close to Rosenfeld's universal form). At equal O density they were 4× apart. The reduced Stokes–Einstein product η*D*_O = 0.13–0.16. (The first g(r) job, 6963196, wrote no data; fixed and rerun as 6999519.)
5. **A3 redo (A3b) submitted** (RC "Yes, run the A3 redo"): `FreeEnergy/A3b_Bdg_single`, jobs 7000466/7/8.

## 5p. Results of 2026-11-17: A3b, bridgmanite vacancies redone (`results_freeenergy/BDG_VACANCY_A3.md` §5–6)
1. **Hop-proof formation energies.** Single-vacancy cells; V_Mg and V_Si by Frenkel–Ladd at T; V_O by Frenkel–Ladd at low T₁ plus an ⟨E⟩(T) ladder. All 96 replicas are hop-free.
   - Formation energies, 30 → 120 GPa: MgO partial 6.2 → 12.2 eV, SiO₂ partial 12.3 → 22.6 eV, full Schottky 18.5 → 34.8 eV. These agree with the hop-free A3 subset within 0.4 eV.
   - The MgO partial Schottky is 1.4–1.9 eV cheaper in bridgmanite than in periclase.
   - The ladder F_I of the perfect crystal sits 0.4–0.8 eV (≤ 0.9 meV/atom) below the direct value, probably the switching bias of the direct runs. It does not enter the formation energies; the TS 80 ps test is running (7045833).
2. **V_Mg migration** (clean): 3.9 / 4.8 / 5.5 / 6.1 eV at 30 / 60 / 90 / 120 GPa.
   **V_Si migration is still unresolved:** the straight jump is cooperative (O neighbours move 2–3 Å), so a path search is needed.
3. **Intrinsic diffusion (Eq. 7–8 there):**
   - the defect population is MgO partial Schottky;
   - D_O in bridgmanite is 2×10⁻²¹–4×10⁻¹⁷ m²/s, ≈ 10⁵ × periclase at the same (P, T);
   - D_Mg is 10⁷–10⁹ × slower than D_O.
   - Raw Deng values; real bridgmanite is extrinsic (Fe³⁺, Al).
4. **MgO Schottky 20 GHz reruns (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.5).**
   - The 8×8×8 loss is reproducible: G″ = 27 ± 2 GPa (2 ns, new seed) against 38 ± 9 GPa.
   - The 6×6×6 cell stays nearly lossless after 1.5 ns ageing: G″ = 2.3 ± 0.5 GPa, G′ = 119 GPa.
   - Trajectories show that in both cells every vacancy sits in one nanovoid: 40 sites in the 8×8×8 cell, 16 in the 6×6×6 cell. That is the fate of a 10⁶-fold vacancy supersaturation.
   - A Debye fit with G_R ≈ 119 and G_U ≈ 171 GPa gives τ ≈ 7.6 ps (40-site void) and ≈ 0.5 ps (16-site void).
   - So the "Schottky" low-frequency loss (and its E_app = 3.2 eV) is void anelasticity and cannot be carried to the mantle.

## 6. Figures (`results/`, PDF and PNG)

| figure | content |
|---|---|
| `fig_vs_T` | Viscosities (liquid $\eta_0$, $\zeta_0$; crystal Eq. 6 bounds), moduli, shear and uniaxial Q versus T, with pressure on the right axis |
| `fig_effective_viscosity` | $|\eta^*|$ versus f for liquids and crystals; log viscosity versus T at 0.2 THz with the flow bounds |
| `fig_kk` | Crystal G′ and M′ versus f, with the curve predicted from the loss by Eq. 7 |
| `fig_shear_viscosity` | Liquid $\eta'(\omega)$ from sweeps and GK |
| `fig_shear_moduli`, `fig_uniaxial_loss`, `fig_uniaxial_storage` | Liquid moduli spectra |
| `fig_Q` | Shear and uniaxial $Q^{-1}$ versus f, all valid sweeps |
| `fig_solid` | Crystal loss moduli and $Q^{-1}$ versus f, all cells |
| `fig_gk_time` | GK running integrals versus cutoff |
| `fig_octp_vs_gk` | OCTP Einstein vs GK running integral, same trajectory |
| `fig_vacancy_arrhenius` | Vacancy jump rates versus 1/T with single-$E_a$ fits |
| `fig_gb_sliding` | Grain relative-displacement MSD and boundary friction β versus 1/T, both volumes |
| `fig_gb_size` | Grain-displacement MSD and β for 1×–9× boundary area (§5f) |
| `GBslide/drive/analysis/fig_gb_drive` | Driven coupled migration at 140 GPa: u_x(t) and boundary z(t) (§5g) |
| `GBslide/drive/analysis_3x1/fig_gb_drive` | Same for the 3×1 cell (§5h) |
| `results_MgSiO3_V6.5669/fig_vs_T` (and the same fig_* set) | MgSiO₃: liquid (cooled) and bridgmanite (heated) branches versus T (§5i) |
| `results_Tdep/fig_T_dependence` | Arrhenius plots of liquid η₀ and D (and bridgmanite V_Mg + V_O D), crystal Q⁻¹ at 1 THz (perfect B1 MgO, perfect and vacancy bridgmanite), and local apparent energies (Eq. 1 of `T_dependence.md`) for MgSiO₃ and MgO at both volumes (§5j) |
| `fig_gb_Q_model` | Grain-scale $Q^{-1}(f)$ from MD β and δD_b (Eq. 13) for d = 1 µm–1 cm |

## 7. Open items

1. Aged-Schottky low-frequency sweeps (job 4233462) and bicrystal γ₀ = 0.03 sweeps (job 4230008). These decide whether a defect relaxation peak is visible at 20–50 GHz.
2. Finish the V9.6397 series and collect it. Check the 4000 K liquid at 50 GHz and the 3000 K bicrystal at 0.2 THz.
3. ~~OCTP versus GK comparison~~ done 2026-10-09 (§5, `fig_octp_vs_gk`): equivalent to GK, no gain at long lags.
4. Possible next steps: a relaxation-spectrum fit (TODO T8), a comparison with RC's earlier GK runs (T6), and a time-step (2 fs) drift test.
