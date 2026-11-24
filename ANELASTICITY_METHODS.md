# Anelasticity and viscosity from MD: methods, tools and lessons (MgO, 2026-10-05 to 10-08)

This is the self-contained guide for repeating the MgO work at another volume or for another material. It covers the physics, the protocol that worked, every tool, the cost and the pitfalls. Dated restart docs (`ANELASTICITY_RESTART_<date>.md`) hold the run-by-run history and job IDs. `REQUIREMENTS.md` holds the user's standing rules. The current MgO results are in `results/results_all.md` (V = 6.6868 Å³/atom) and `results_V9.6397/` (second volume, running).

## 1. What is measured

The goal is a deformation's complex modulus over 3–5 decades of frequency, plus the zero-frequency viscosities. Two independent routes are used:

1. **Oscillatory NEMD.** `fix deform wiggle` imposes the strain, and a lock-in fit is made at the known drive frequency.
2. **Green–Kubo (GK).** Equilibrium NVE stress autocorrelations.

For the liquid they must agree at overlapping frequencies (they do for MgO). For the crystal, only the sweep gives the elastic storage modulus.

### 1.1 Definitions

Shear (xz tilt; strain = tilt/$L_z$; stress $\sigma_{xz}=-P_{xz}$):

$$\gamma(t)=\gamma_0\sin\omega t,\qquad \sigma(t)=\gamma_0\left[G'(\omega)\sin\omega t+G''(\omega)\cos\omega t\right] \tag{1}$$

$$G^*=G'+iG'',\qquad Q^{-1}=\tan\delta=\frac{G''}{G'},\qquad \eta'(\omega)=\frac{G''}{\omega} \tag{2}$$

Uniaxial (x length; strain $\delta L_x/L_x$) measures the longitudinal modulus:

$$M^*=K^*+\tfrac43G^*,\qquad \frac{M''}{\omega}\xrightarrow{\omega\to0}\zeta_0+\tfrac43\eta_0 \tag{3}$$

Viscosity is the low-frequency slope of the loss modulus:

$$\eta_0=\lim_{\omega\to0}\frac{dG''}{d\omega} \tag{4}$$

It is estimated three ways:
- secants between sweep points;
- a weighted fit through the origin for $f\le200$ GHz;
- the analytic GK derivative $\int G(t)[\cos\omega t-\omega t\sin\omega t]\,dt$.

$Q$ has special cases:
- **Liquid-like points:** if $|G''|>|G'|$, $Q=G'/G''$ is computed directly.
- **Unresolved points:** reported as 2σ bounds ("$Q>$" or "$Q<$").
- **GK $Q$:** given only for liquid shear. The GK storage modulus lacks $K_0$ (longitudinal) and the Born term (crystal).

### 1.2 Lock-in analysis (`tools/anelastic_lockin.py`)

Stress and strain are fitted to $a+bt+\sum_{k=1}^{3}[s_k\sin k\omega t+c_k\cos k\omega t]$, and the modulus is the ratio of the complex first harmonics. Points to know:
- **Error bars** come from blocks of whole cycles.
- **Nonlinearity:** the harmonic ratios $|\sigma_2/\sigma_1|$ and $|\sigma_3/\sigma_1|$ flag it. Above 0.1 the point is nonlinear or resonant.
- **Bin averaging:** stresses written as $N_{av}$-step averages are corrected exactly:

$$H(\omega)=\frac{\sin(N_{av}\omega\Delta t/2)}{N_{av}\sin(\omega\Delta t/2)}\,e^{-i\omega(N_{av}-1)\Delta t/2} \tag{5}$$

- **Flips:** box flips at $|xz|>L_x/2$ are unwrapped, so γ₀ > 0.5 is allowed.
- **Never use FFT peak picking.**

**One-step lag.** `fix deform` updates the box at end_of_step, so the virial at step $n$ belongs to the box of step $n-1$. Every lock-in phase is therefore low by $\omega\Delta t$. This was proven by halving Δt on a perfect crystal: δ = −1.47° at 1 fs and −0.48° at 0.5 fs, both +0.33° to +0.42° after correction. `anelastic_collect.py` applies

$$M^*_{\rm corr}=M^*_{\rm lock\text{-}in}\,e^{i\omega\Delta t} \tag{6}$$

The correction matters for solids at THz frequencies. At 5 THz it adds ≈ 5 GPa to $G''$, which is the size of the whole loss.

### 1.3 Green–Kubo (`tools/gk_viscosity.py`, called by `anelastic_collect.py`)

NVE run, stress tensor every 2 fs, mean stress removed per component (a crystal carries a static stress):

$$G(t)=\frac{V}{10k_BT}\sum_{\alpha\beta}\langle P^{os}_{\alpha\beta}(0)P^{os}_{\alpha\beta}(t)\rangle,\qquad \eta_0=\int_0^{t_c}G\,dt \tag{7}$$

$$\zeta_0=\frac{V}{k_BT}\int_0^{t_c}\langle\delta p(0)\delta p(t)\rangle dt,\qquad G^*(\omega)=i\omega\int_0^{t_c}G(t)e^{-i\omega t}dt \tag{8}$$

Settings and caveats:
- **Cutoff:** $t_c=1$ ps for MgO, where G(t) has decayed by 0.5 ps. A longer cutoff only adds noise.
- **Errors:** 8 blocks.
- **Ensemble:** NVE is essential. A thermostat adds its own relaxation to the bulk channel.
- **In a crystal:** $G(0)$ lacks the Born term and $\int G\,dt$ is a low-frequency loss, not a viscosity.

### 1.4 Noise, amplitude and run length (`tools/anelastic_sweep_setup.py`)

Fluctuation–dissipation sets the lock-in error:

$$\delta\sigma^2\simeq C\,\frac{k_BT\,G''}{\omega VT_{run}},\qquad C\approx8 \tag{9}$$

In the viscous regime the relative error depends only on the strain-rate amplitude $\dot\gamma_0=\omega\gamma_0$. Liquid amplitudes therefore follow

$$\gamma_0=\mathrm{clip}(\dot\gamma_0/\omega,\,0.01,\,\gamma_{max}),\qquad \dot\gamma_0=10^{11}\ \mathrm{s^{-1}} \tag{10}$$

- $\gamma_{max}$ = 0.5 in the supercooled liquid (shear can nucleate the crystal).
- Linearity must be checked by repeating one frequency at a second amplitude. At 8000 K, γ₀ = 0.095 and 0.32 agree at 50 GHz.
- **Supercooled (slow) liquids break Eq. 10.** Linear response needs $\dot\gamma_0\tau_\alpha\ll1$, where $\tau_\alpha$ is the slow (α) relaxation time, read off where G(t) has decayed. $\tau_0=\eta_0/G_\infty$ is too short to use here. In MgSiO₃ at 4000 K ($\tau_\alpha\approx$ 10 ps), Eq. 10 gives γ₀ = 0.32 and 0.5 at 50 and 10 GHz. Those points are shear-thinned: $|\sigma_3/\sigma_1|$ = 0.10–0.14 and $\eta'$ is half the GK value. When G(t) lasts beyond a few ps, lower $\dot\gamma_0$ to about $0.1/\tau_\alpha$ and run longer: the error grows as $1/\gamma_0$ at fixed run length (Eq. 9).
- The GK cutoff must follow the same slow decay: $t_c$ = 20 ps at 4000 K against 1–2 ps for hot liquids. Set it per case with `GKTC` in the case file.
- Solids use γ₀ = ε₀ = 0.01. Low-frequency defect runs use 0.02–0.03 with harmonics checked.

The cost floor is cycles, not noise: one period at frequency $f$ costs $1/(f\Delta t)$ steps, which is $10^6$ steps at 1 GHz.

### 1.5 Thermostat artefacts (uniaxial)

A Nosé–Hoover thermostat on a volume-changing cell adds a Debye relaxation between the adiabatic and isothermal moduli:

$$M''_{th}(\omega)=\Delta M_{th}\frac{\omega\tau_T}{1+\omega^2\tau_T^2},\qquad \Delta M_{th}=K_S-K_T \tag{11}$$

For MgO at 8000 K, $\Delta M_{th}\approx80$ GPa. The rule is to choose $\omega\tau_T\gg1$, i.e. a nearly adiabatic run, with $\Delta M_{th}/(\omega\tau_T)\lesssim0.02\,M''$. The amplitude is then limited by viscous heating:

$$\dot T=\frac{\omega M''\varepsilon_0^2}{2\rho c_v},\qquad \rho c_v\approx3nk_B \tag{12}$$

Keep the steady offset $\dot T\tau_T$, or the total rise $\dot T t_{run}$, below about 100 K. The τ_T table that worked:

| P (ps) | ε₀ | τ_T (ps) | run (ps) |
|---|---|---|---|
| 0.2 | 0.010 | 2 | 40 |
| 1 | 0.015 | 10 | 40 |
| 5 | 0.020 | 250 | 100 |
| 20 | 0.03 | 10⁴ | 300 |
| 100 | 0.03 | 10⁵ | 1100 |

Shear has no first-order heating coupling, so τ_T = 0.1 ps is fine there (with `nvt/sllod` and `temp/deform`).

### 1.6 Finite-size resonance (bicrystal, any slab)

When the drive approaches the lowest transverse standing wave across the cell,

$$f_1\approx\frac{v_s}{L_z} \tag{13}$$

the response becomes inertial rather than anelastic. Signs are large harmonics, non-monotonic $G'$ and $M'$, and huge error bars. For MgO at 59.6 Å, $f_1$ ≈ 1 THz. Only $f\ll f_1$ is quasi-static. Compliant interfaces lower $f_1$ further.

### 1.7 Crystal: what Green–Kubo measures, effective viscosity, and a causality check

A crystal does not flow on MD time scales. Its full stress relaxation function levels off at the static modulus, $G(t\to\infty)=G_{eq}>0$, so $\int G\,dt$ diverges. Green–Kubo at fixed cell shape sees only the stress fluctuations: it drops the Born (static) term. The fluctuation $G(t)$ then decays on the phonon relaxation time τ (Akhiezer-type damping). Its integral is **internal friction, not a viscosity**. Two consequences:

- **Opposite T slopes.** For a single relaxation, $G''/\omega=\Delta G\,\tau/(1+\omega^2\tau^2)$. GK gives the $\omega\tau\ll1$ side, $\Delta G\,\tau$, which falls with T. The sweeps at 0.2–5 THz have $\omega\tau\gtrsim1$, giving $\Delta G/(\omega^2\tau)$, which rises with T. At the same frequency the two agree: MgO 4000 K at 1 THz gives GK 1.73 mPa s against the sweep's 1.76 ± 0.18.
- **Shear channels in an aligned crystal.** The GK average over five components mixes C₄₄-type (off-diagonal) and (C₁₁−C₁₂)/2-type (normal-difference) shear. An xz sweep on a cube-aligned cell sees only C₄₄. In perfect B1 at 5000 K the zero-frequency loss is 0.74 mPa s (off-diagonal) against 7.8 mPa s (normal difference). Compare a sweep with the matching GK components.

The **effective (complex) viscosity** is $|\eta^*|=|G^*|/\omega$. For a liquid it tends to $\eta_0$ as ω → 0. For a crystal it follows $G'/\omega$ and diverges. A **lower bound on a flow viscosity** follows from one sweep point. If the crystal relaxed at most like a Maxwell body ($G''/G'=1/\omega\tau$, $\eta=G\tau$), then, using the 2σ upper error on $G''$,

$$\eta_0\ \ge\ \frac{G'\,Q}{\omega},\qquad Q=\frac{G'}{G''+2\sigma_{G''}} \tag{14}$$

The bound grows only with the lowest frequency reached, roughly as $G\,t_{run}$. MgO at 0.2 THz gives η₀ ≥ 1–20 Pa s, against creep viscosities of 10¹⁸–10²² Pa s.

**Causality check.** $G'$ and $G''$ are related by Kramers–Kronig. When the loss varies slowly in ln ω, the local form is

$$\frac{dG'}{d\ln\omega}\simeq\frac{2}{\pi}\,G''(\omega) \tag{15}$$

`anelastic_collect.py` tests Eq. 15 between adjacent frequencies for every crystal sweep (table §2a, `fig_kk`). The melt-grown and perfect MgO crystals agree within 1σ from 0.2 to 5 THz, which confirms that the measured loss is a linear, causal response. Expected failures:
- the bicrystal slab resonance (Eq. 13);
- heated 5 THz points (†);
- cells that drift during the sweep (unaged Schottky);
- Maxwell liquids at ωτ ≪ 1, where $G''\propto\omega$ varies quickly in ln ω and the local form does not apply, so liquids are excluded from the check;
- **internal-strain resonances in non-centrosymmetric-site crystals** (bridgmanite, summary §5i Eq. 14): strain drives Raman-active optic modes, M′ falls and M″ rises toward 5 THz, and the local form fails by 8–40σ at 1–5 THz. Use ≤ 1 THz for crystal Q there. B1 MgO has no such term.

## 2. Protocol that worked

1. **Model.** Compress the DeePMD model with `dp --tf compress -i graph.pb -o graph_c.pb` (deepmd_py311 env), which runs 2.8× faster on a P100. Verify with `tools/compare_dp_models.py A B data...`: forces, energy and virial on several configurations. MgO gave ΔF = 1 µeV/Å rms.
2. **Cell.** Use 4096 atoms, a cube at fixed V. This fits an 8×8×8 rock-salt crystal exactly, with $a=L/8$.
3. **Liquid temperatures.** For each liquid T:
   - Start GK from the previous T's equilibrated state (`GK/eq.data`) or a known liquid, with 20 ps NVT at T then 1.5 ns NVE.
   - Run the shear sweep (P = 0.2, 1, 5, 20, 100 ps) and the uniaxial sweep (Table §1.5).
   - Both sweeps copy `GK/eq.data` into each task directory, so there is no re-equilibration.
4. **Cooling.** Step down at constant V until the liquid crystallizes. The signs are a sudden PE drop (MgO: −0.46 eV/atom), a pressure drop (−23 GPa at V6.6868) and an MSD plateau.
   - In NVE the latent heat raises T by thousands of K: 6000 K → 8490 K at 1.05 ns. Cut the analysis before the event (`GKCUT`).
   - The supercooled liquid can survive for > 1 ns and then crystallize, so always check PE across the whole NVE run.
5. **Solid at two temperatures.**
   - **Melt-grown crystal:** GK plus the reduced 6-task sweep (shear and uniaxial at 0.2, 1 and 5 THz; γ₀ = ε₀ = 0.01; 200 ps each). It comes out rotated or polycrystalline relative to the box, so check it with `tools/xtal_check.py`.
   - **Controlled-defect references at the same T** (`tools/build_defect_crystals.py`):
     - Perfect, box-aligned B1 (`schottky --npair 0`).
     - 20 bound Schottky pairs (Zener-type relaxation).
     - Σ5 (310)/[001] symmetric tilt bicrystal, boundary normal z (`--normal-z`), so the xz shear slides the boundaries.
   - Each defect cell gets 50 ps NVT, 1.5 ns NVE GK, the 6-task sweep, and low-frequency shear at P = 20 and 50 ps:
     - Schottky: γ₀ = 0.02, 0.8–1 M steps.
     - Bicrystal: γ₀ = 0.03, 1–1.25 M steps.
   - Schottky cells age: vacancies cluster and anneal, at 5000 K PE drops 28 eV within 150 ps. Run the low-frequency sweeps from the aged GK end state, check that PE is stationary in each run (`stress.dat` column 8), and skip the ageing part of the GK run (`GKSKIP`).
6. **Collect.** Run `tools/anelastic_collect.py --cases tools/anelastic_cases_<material>_<V>.py`. It writes `results_all.md`, `results_all.csv` and the figures listed in §3.

## 3. Tools (all in `/resnick/home/recohen/Claude/tools`; Python from `cohen_env`)

| tool | purpose |
|---|---|
| `anelastic_sweep.lammps` | Oscillatory NEMD.<br>• Modes: `MODE shear` (xz wiggle) and `MODE uniaxial` (x wiggle); fix nvt/sllod.<br>• Restartable in chunks of whole periods; picks up `restart.mgo` or `eq.data` automatically.<br>• Optional variables: `TDAMP`, `DT`, and `DUMPN`/`DUMPSTEPS` (trajectory, §5).<br>• Outputs: `stress.dat` (pxz pxy pyz pxx pyy pzz T PE), `strain.dat` |
| `sweep_array.sh` | Generic P100 array job for the above.<br>• `tasks.txt` columns: `dir TEMP PERIOD AMP NTOT NCHUNK NAV SEED NEQ MAXCHUNKS MODE TDAMP [DT DUMPN DUMPSTEPS DATA]`.<br>• Converts a restart file given as DATA. Submit with `sbatch -J NAME --array=1-N sweep_array.sh` |
| `launch_after_eq.sh ROOT NAME` | Waits for each task's DATA (a GK `eq.data`), copies it into the task directories, submits the array and runs the watcher |
| `sweep_watch.sh ROOT:JOB:MODE ...` | Runs the lock-in on each finished task and appends to `ROOT/lockin_results.txt`. Flags failed or incomplete tasks; resubmit those with `sbatch --array=i` |
| `anelastic_lockin.py DIR --period P --mode M [--dt]` | Lock-in (§1.2). Pass `--dt` when DT ≠ 1 fs |
| `anelastic_sweep_setup.py` | Amplitude and run-length design (Eqs. 9–10), cost table. Used for the 8000 K design; later tables were written directly |
| `gk_stress.lammps`, `gk_job.sh` | GK run: NVT for NEQ steps, then NVE. Outputs `pres.dat` every 2 fs, `msd.dat`, `eq.data`, `restart.gk`. Submit with `sbatch -J NAME --export=ALL,TEMP=..,DATA=..,NEQ=.. gk_job.sh`; resubmit the same way after the 24 h limit |
| `gk_viscosity.py pres.dat` | Standalone GK analysis (Eqs. 7–8) |
| `anelastic_collect.py --cases FILE` | All tables and figures.<br>• Case files: `anelastic_cases_MgO_V6.6868.py`, `anelastic_cases_MgO_V9.6397.py` and `anelastic_cases_MgSiO3_V6.5669.py`, which hold paths, labels, colours, per-run box volume, GK cut and skip, liquid set, defect T and plot ranges. Optional keys: `GKTC` (per-case GK cutoff), `XTAL` (crystal branch at the same T as the liquid, drawn as separate dashed lines in `fig_vs_T`) and `SOLID_SPAN`/`SOLID_LABEL` (shaded crystal range, may be None).<br>• Copy one for a new material or volume.<br>• Figures: `fig_shear_moduli`, `fig_shear_viscosity`, `fig_uniaxial_*`, `fig_gk_time`, `fig_solid`, `fig_Q`, `fig_vs_T` (dashed ⟨p⟩ on a right-hand axis; crystal panel (a) shows the Eq. 14 bound), `fig_kk` (Eq. 15), `fig_effective_viscosity` (via `plot_effective_viscosity.py`) |
| `build_defect_crystals.py` | Rock-salt Schottky, perfect and Σ5 bicrystal cells with Maxwell velocities. **Hard-wired to B1 and to the Mg/O masses.** The overlap cutoff `rcut` defaults to 0.3185 a, so it scales with the lattice |
| `plot_effective_viscosity.py` | $|\eta^*|$ vs f and vs T, with the Eq. 14 bound; called by the collect script, or standalone on a `results_all.csv` |
| `octp_plugin/` | OCTP (Jamali et al. 2019) as a LAMMPS runtime plugin, built with CMake into `lammps-stable_22Jul2025_update2/build_octp_plugin/octpplugin.so`; load with `plugin load`. Test input `octp_viscosity.lammps`, analysis `octp_compare.py` (§4) |
| `xtal_check.py` | S(k) on box wavevectors: Bragg peaks show crystallization and orientation |
| `compare_dp_models.py` | Compressed vs uncompressed model check (`--fparam` for finite-T models) |
| `T_dependence.py --case LABEL RESULTS_DIR ... --out DIR` | Single-E test: local apparent energy between neighbouring T, Arrhenius, power-law (T-independent if n = 0) and VFT fits for liquid η₀, ζ₀, D_i (from msd.dat) and crystal $Q^{-1}$ at 0.2 and 1 THz. Reads `results_gk.csv` (written by `anelastic_collect.py`) and `results_all.csv`. `--series LABEL SUBSTR NAME` picks the crystal sweep series of one case by a path substring (needed when two series share a directory name, e.g. `/crystal/` and `/crystal_VMgO/`). `--defect-gk LABEL SUBSTR NAME` adds crystal D_i from the GK msd.dat of non-liquid GK keys containing SUBSTR (vacancy hop rates, results Eq. 6) |
| `build_vacancy_pairs.py DATA... --ref REF --out-suffix S` | Removes bound cation–anion vacancy pairs (e.g. bridgmanite V_Mg + V_O) from any orthogonal LAMMPS data file at fixed box. Sites are chosen once in REF, a cold state of the same T ladder with the same atom ids, so the cells at every T carry identical defects. Options: `--npair`, `--shell` (random among the k nearest anions), `--dmin`. MgO-equivalent density: 6 pairs per 1280 atoms |
| `T_ladder.lammps`, `T_ladder_job.sh` | NVT temperature ladder (cooling or heating path) at a fixed cell. Writes `eq_<T>.data` per step and resets `fparam` at each T |
| `stage_T_series.py` | Stages and submits GK, liquid sweeps (shear and uniaxial) or the solid 6-task sweep for a list of T from ladder states. Amplitudes are scaled to L_x and L_z; it prints the cost |

## 4. Jobs and environment

- **Hardware and job header.** P100 only. The header is in `sweep_array.sh` and `gk_job.sh` (copied from RC's working script). Further rules:
  - No `cd` to the submit directory, no directory in the slurm output name, no `%` array limits.
  - TIMEOUT = time limit − 300 s (`timer timeout`).
  - Present the cost before large submissions.
- **Environment.** In batch scripts:
  - `source ~/.bashrc; shopt -s expand_aliases; module load cuda; conda activate /central/groups/carnegie_poc/rcohen/anaconda2/deepmd_py311`.
  - Set `LAMMPS_PLUGIN_PATH=$CONDA_PREFIX/lib`.
  - Thread counts: `OMP_NUM_THREADS=9`, `DP_INTER/INTRA = 3`.
  - The GPU build fix for deepmd-kit 3.2 is described in the 10-06 restart, §1.
- **No login-node or `srun` runs.** `lmp` needs libcuda, so it fails on the login node; even file conversions run inside GPU jobs. `srun` from the Claude session lands in RC's dashboard job and hangs; use `sbatch`.
- **Speed and cost.** 4096 atoms with `graph_c.pb` on a P100 run at 22–27 steps/s at V6.6868 (≈ 190 GPa) and ≈ 32 steps/s at V9.6397 (≈ 40 GPa). Costs are below; 1.5 ns GK ≈ 17 h.

| item | steps | P100-h |
|---|---|---|
| liquid T (GK + shear + uniaxial) | 3.7 M | ≈ 43 |
| solid cell (GK + 6-task sweep) | 2.7 M | ≈ 31 |
| defect low-frequency pair (P = 20 and 50 ps) | 1.8–2.25 M | ≈ 21–26 |

**OCTP and longer times.**
- **What OCTP is.** OCTP's `fix ordern` is order-n (multiple-window) *sampling* of the Einstein form, $\eta=\lim_t \frac{d}{dt}\frac{V}{2k_BT}\langle(\int_0^tP_{\alpha\beta}dt')^2\rangle$. It is not a multiple-time-step integrator, so MD cost and the lowest reachable frequency are unchanged. The Einstein slope equals the GK running integral. `pres.dat` already holds the stress every 2 fs, so any lag can be computed offline.
- **r-RESPA is not available.** `pair deepmd` sets `respa_enable = 0`: the network is one non-separable force with no inner/outer split.
- **Paths to longer times:**
  - a larger time step after an energy-drift test (≤ 2×);
  - several GPUs per run;
  - independent replicas for noise;
  - a cheaper surrogate potential, fitted to the DeePMD model, for long runs;
  - for defect relaxations, rates from barriers (NEB/kMC) with relaxation strengths from MD.

## 5. Trajectories for animations

`anelastic_sweep.lammps` writes `traj.lammpstrj` when `DUMPN > 0`:
- **Content:** `id type x y z ix iy iz` every DUMPN steps, with the tilted box of that step, while the production step < DUMPSTEPS.
- **Window:** rounded up to whole chunks.
- **Size:** ~250 kB per frame for 4096 atoms, so 300 frames ≈ 75 MB.
- **Restarts:** after a restart the file is appended and frames may repeat at chunk boundaries; drop duplicate timesteps.

Viewing in OVITO:
- Small solid strains (γ₀ = 0.01–0.03) are invisible directly. Use OVITO's Displacement vectors modifier with a scaling factor, or Atomic strain.
- For Schottky cells, Wigner–Seitz analysis against the start frame shows vacancy hops.
- The liquid at γ₀ = 0.32 and the bicrystal at γ₀ = 0.1 are visible as is.

Sample trajectory runs:
- **V6.6868** (`R/Trajectories`, job 4233485), 3–5 cycles each:
  - liquid 8000 K shear at P = 20 ps (γ₀ = 0.32) and P = 1 ps;
  - liquid 8000 K uniaxial at P = 5 ps;
  - perfect B1, aged Schottky and bicrystal at 5000 K, shear P = 20 ps;
  - bicrystal at γ₀ = 0.10 ("visual", nonlinear);
  - bicrystal at P = 1 ps (resonance).
- **V9.6397:** the P = 20 ps shear tasks (first 60 ps), and the solid 5 ps shear tasks (first 15 ps) carry dumps.

## 6. Pitfalls found (and fixed)

- **Units in fix deform.** It defaults to lattice units, so always give `units box`.
- **Strain definition.** Strain is tilt/$L_z$, not the raw tilt. The user's notebooks assumed 10 fs sampling and omitted the 2π.
- **Thermostat in uniaxial runs** (Eq. 11). τ_T = 0.1 ps contaminated every uniaxial $M''$ at 8000 K. Low-frequency uniaxial $M'$ from a strong thermostat is $K_T$; the adiabatic setting gives $K_S$-based values.
- **One-step lag in the stress phase** (Eq. 6). It made a perfect crystal look like it had negative loss.
- **Crystallization during NVE GK** (§2, step 4). Always check PE over the whole run.
- **Rare-event stress steps in small defect cells.** Vacancy hops in the 20-pair Schottky cell give an apparent $G(0)$ = 376 GPa and a meaningless $\int G\,dt$. Trust the sweeps there.
- **Bicrystal finite-size resonance** (Eq. 13).
- **Overlap cutoff in `build_defect_crystals.py`** must scale with $a$. A fixed 1.2 Å at a = 4.26 Å left atoms 1.35 Å apart; now 0.3185 a.
- **`write_data` needs a pair style.** Converting a restart to a data file therefore uses `pair_style zero 6.0` (`sweep_array.sh` does this). Without it the job died in 13 s (4230009).
- **LAMMPS syntax gotchas.** There is no two-argument `min()` in formulas; use `ternary()`. Index variables cannot be redefined; use `string` variables as flags.
- **Fonts.** Liberation Sans (Arial metrics) lacks ⁻ ₀ ₁ ⟨⟩, so plot labels use mathtext with `mathtext.default: regular`.
- **Green–Kubo in a crystal is not a viscosity** (§1.7). Do not plot $\int G\,dt$ of a crystal next to a liquid $\eta_0$. Use $|\eta^*|$ and the Eq. 14 bound, and compare the loss with a sweep at the same frequency and in the same shear channel.
- **Shear channel in aligned cells** (§1.7). A box-aligned crystal's xz sweep measures C₄₄; the melt-grown crystal mixes in (C₁₁−C₁₂)/2, so its G′ is higher (MgO 5000 K: 258 vs 171 GPa). Similar |η*| for defect cells is a stiffness effect; the dissipation differences are in Q.
- **Sweep timestep.** A sweep run with DT ≠ 1 fs needs `--dt` in the lock-in. The watcher assumes 1 fs.

## 7. Porting to another material: checklist

1. **LAMMPS inputs.** Since 10-11 the sweep, GK and ladder inputs take `MASSES data` (masses from the data file), `FPARAM kT` (finite-T models) and `NTYPES 3` (GK MSD). Set them once as `LMPEXTRA` in a `sweep.env` at the volume level; the job scripts search up to 3 directory levels. The LAMMPS types must follow the model's type map order.
2. **Model.** Compress it and check with `compare_dp_models.py`. Measure the speed with a short test before quoting a cost.
3. **Cell.** Choose N and V so that the expected crystal fits the cube, or accept a melt-grown polycrystal. Get pressures from a short NVT.
4. **Defect cells.** `build_defect_crystals.py` is rock-salt only. For other structures write the analogue: a perfect cell, a point-defect cell and a grain boundary with the normal along z. Point defects in any structure: `build_vacancy_pairs.py` on the equilibrated perfect crystal, then age it with `T_ladder_job.sh` (single T, about 200 ps) and stage it with `stage_T_series.py --kind solid`.
5. **Thermostat rule.** Re-derive τ_T for uniaxial runs from $K_S-K_T$ (Eq. 11). Measure it with a τ_T test at one frequency, as in 10-07 §3.
6. **GK cutoff.** Re-check $t_c$ from the decay of $G(t)$.
7. **Case file.** Make a new `anelastic_cases_*.py` (copy the V9.6397 one) and set OUT to a new results directory.
8. **Docs.** Equation numbers, LaTeX in docs, unicode in the terminal. Plots as PDF and PNG with a box, in Arial/Liberation at publication size.

## 8. MgO results so far (V = 6.6868 Å³/atom; details in `results/results_all.md`)

| T (K) | state | ⟨p⟩ GPa | η₀ (mPa s) | ζ₀ (mPa s) | notes |
|---|---|---|---|---|---|
| 8000 | liquid | 192.8 | 8.19 ± 0.20 | 0.86 ± 0.04 | $G_\infty$ ≈ 285 GPa; sweep and GK agree |
| 7000 | liquid | 183.4 | 11.18 ± 0.29 | 1.17 ± 0.06 | |
| 6000 | supercooled | 174.9 | 18.30 ± 0.48 | 1.64 ± 0.13 | GK crystallized at 1.05 ns, analysis cut at 1040 ps |
| 5000 | B1 (melt-grown) | 151.8 | – | – | shear Q ≈ 20–60; perfect B1 Q ≈ 170 at 5 THz |
| 4000 | B1 | 144.9 | – | – | |

Defect cells at 5000 K:
- **Schottky:** a clear Zener-type loss. $G'$ falls from 163 to 148 GPa between 5 and 0.2 THz, against $C_{44}$ = 171 GPa for the perfect crystal.
- **Bicrystal:** quasi-static only at ≤ 0.2 THz. $G'$ softens toward low frequency (138 → 108 GPa from 0.2 THz to 20 GHz), which is the onset of boundary sliding.
