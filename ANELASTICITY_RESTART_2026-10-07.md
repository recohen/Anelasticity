# Anelasticity restart 2026-10-07

Read with `REQUIREMENTS.md`, `ANELASTICITY_TODO.md`, `ANELASTICITY_DONE.md`, `ANELASTICITY_PLAN.md`. `ANELASTICITY_RESTART_2026-10-06.md` still holds the GPU fix (§1), sweep design (§2), the full result tables (§3), and the tools (§5); this file adds what changed on 10-07. All LAMMPS paths below are under `/groups/carnegie_poc/rcohen/LAMMPS/MgO/4096atoms/V6.6868/4096atom` (`R`).

## 0. What to check FIRST

1. `squeue -u recohen`:
   - **4115169_5**: uniaxial P = 100 ps, `R/8000K/FreqSweep_x/P100ps_r0`; watcher `tools/sweep_watch.sh R/8000K/FreqSweep_x:4115169:uniaxial` appends to `lockin_results.txt`.
   - **4146463**: GK 8000 K, `R/8000K/GK`.
   - **4146464**: GK 7000 K, `R/7000K/GK`.
   - **4147084** shear sweep 7000 K, `R/7000K/FreqSweep`; **4147085** uniaxial sweep 7000 K, `R/7000K/FreqSweep_x` (§5). Watcher: `tools/sweep_watch.sh R/7000K/FreqSweep:4147084:shear R/7000K/FreqSweep_x:4147085:uniaxial`.
2. GK jobs stopped by the 24 h limit: `sbatch gk.sh` in the same dir (picks up `restart.gk`). Done when `slurm-*.out` shows `PRODUCTION_STEP 1500000 of 1500000`.
3. Analyse: `python tools/gk_viscosity.py <dir>/pres.dat --tmax 5 --nblock 8` (cohen_env). Writes `gk_G.dat`, `gk_spectrum.dat` next to `pres.dat`. Check the NVE drift line and that `msd.dat` grows linearly at 7000 K (liquid). The MSD reference resets at each restart.

## 1. Green–Kubo runs

`tools/gk_stress.lammps`: reads `DATA`, rescales velocities to TEMP, NVT (Nosé–Hoover, 0.1 ps) for NEQ steps, writes `eq.data`, then **NVE** production with the pressure tensor every 2 fs (`pres.dat`: step pxx pyy pzz pxy pxz pyz temp pe etotal, bar). NVE keeps the thermostat out of the stress correlations, which matters for the bulk channel (§3).

| T (K) | start | NEQ | production | job |
|---|---|---|---|---|
| 8000 | `8000K/FreqSweep/P1ps_r0/eq.data` | 5 ps | 1.5 ns NVE | 4146463 |
| 7000 | same 8000 K `eq.data` | 20 ps NVT at 7000 K | 1.5 ns NVE | 4146464 |

Speed 24.4 steps/s (P100, `graph_c.pb`): ≈ 17 h each, ≈ 1.4 P100-days total.

`tools/gk_viscosity.py` (equations in its docstring):
$$G(t)=\frac{V}{10k_BT}\sum_{\alpha\beta}\langle P^{os}_{\alpha\beta}(0)P^{os}_{\alpha\beta}(t)\rangle \tag{1}$$
$$\eta_0=\int_0^{t_c}G(t)\,dt \tag{2}$$
$$G'(\omega)=\omega\int_0^{t_c}G\sin\omega t\,dt,\qquad G''(\omega)=\omega\int_0^{t_c}G\cos\omega t\,dt \tag{3}$$
$$\zeta_0=\frac{V}{k_BT}\int_0^{t_c}\langle\delta p(0)\delta p(t)\rangle dt \tag{4}$$
$$M_r(t)=\frac{V}{k_BT}\langle\delta P_{\alpha\alpha}(0)\delta P_{\alpha\alpha}(t)\rangle=K_r(t)+\tfrac43G(t) \tag{5}$$
Block errors over NBLOCK blocks. A cosine taper over the last 20 % of $t_c$ is the default (`--nowin` turns it off). Validated on synthetic Maxwell data: $\eta=10$ exact, recovered $9.7\pm0.4$ mPa s; $G''(1\,\mathrm{THz})=48\pm2$ vs 45 GPa exact.

Comparisons to make: GK $\eta'(\omega)$ vs the sweep's shear values (3.1, 7.1, 7.9, 8.1, 8.0 mPa s at 5 THz–10 GHz); GK $\zeta$ vs the uniaxial estimate $\zeta\approx1.8\pm3$ mPa s.

## 2. T2 done: compressed model

`tools/compare_dp_models.py MODEL_A MODEL_B data...` (job 4146365, dir `rcohen/Downloads/T2_compress`). Over four 8000 K configurations: $\Delta F$ = 1 µeV/Å rms, 12 µeV/Å max (forces 5.0 eV/Å rms); $\Delta E$ < 10⁻⁷ eV/atom; $\Delta W/V$ < 10⁻⁴ GPa.

## 3. Thermostat test (uniaxial, 1 THz, ε₀ = 0.03), `R/8000K/FreqSweep_x_tauT`, job 4145234

| $\tau_T$ (ps) | $\omega\tau_T$ | $M'$ (GPa) | $M''$ (GPa) |
|---|---|---|---|
| 1.0 | 6.3 | 684.2 ± 2.0 | 61.3 ± 2.2 |
| 0.1 (sweep) | 0.63 | 540.5 ± 3.8 | 92.7 ± 3.9 |
| 0.02 | 0.13 | 609.2 ± 2.7 | 73.1 ± 2.4 |

Reading:
- The thermostat adds a Debye-type thermal relaxation between the adiabatic and isothermal moduli, as proposed in §7 of the 10-06 restart.
- **Near-isothermal** ($\tau_T$ = 0.02 ps): $M'=609$ GPa. This agrees with $K_T+\frac43G'(1\,\mathrm{THz})=581+22=603$ GPa, where $K_T=581$ GPa is the low-frequency (50–200 GHz, $\omega\tau_T\ll1$) value.
- **Excess loss:** $M''-\frac43G''=73-60=13$ GPa, i.e. $\zeta'(1\,\mathrm{THz})\approx2$ mPa s, consistent with $\zeta\approx1.8\pm3$ mPa s from P20.
- **Nearly adiabatic** ($\tau_T$ = 1 ps): $M'=684$ GPa gives $K_S\gtrsim662$ GPa, so $K_S-K_T\gtrsim80$ GPa.
- **Sweep point** ($\tau_T$ = 0.1 ps): $\omega\tau_T\approx0.6$ sits on the thermal loss peak, so $M''=93$ GPa is inflated. This explains the "non-monotonic" $M'$.
- **Consequence:** the sweep's low-frequency uniaxial points (50, 10 GHz) are isothermal, i.e. $K_T$. GK in NVE gives the adiabatic response.

`anelastic_sweep.lammps` takes an optional `-var TDAMP` (default 0.1 ps; backup in `rcohen/Downloads/anelastic_sweep.lammps.bak_2026-10-07`).

## 4. Pitfalls found today

- LAMMPS equal-style formulas have no two-argument `min()`; use `ternary(a<b,a,b)`.
- `srun` from this Claude session runs inside RC's 4-CPU `sys/dash` job 4055787 and hangs ("step creation still disabled"). Use `sbatch` for CPU work.
- In batch scripts, `conda activate` needs `shopt -s expand_aliases` after sourcing `.bashrc`.

## 5. 7000 K sweeps (submitted 04:3x, 10-07)

Start: every task copies `R/7000K/GK/eq.data` (end of the 20 ps NVT at 7000 K from the 8000 K state; P = 183 GPa; PE flat at −14050 ± 50 eV over 2–20 ps; MSD 5 Å² at 1 ps, so liquid). No re-equilibration (NEQ = 0). The 8000 K `sweep.sh` was extended with a `TDAMP` column in `tasks.txt`.

**Shear** (4147084, τ_T = 0.1 ps as at 8000 K; no first-order T coupling): same γ̇₀ = 10¹¹ s⁻¹ amplitudes as 8000 K; runs 20, 60, 60, **200** (10 cycles), 300 ps.

**Uniaxial** (4147085), new thermostat rule. A Nosé–Hoover thermostat on a uniaxially strained cell adds a Debye loss
$$M''_{th}(\omega)=\Delta M_{th}\frac{\omega\tau_T}{1+\omega^2\tau_T^2},\qquad \Delta M_{th}=K_S-K_T\approx80\ \mathrm{GPa} \tag{6}$$
which is removed by choosing $\omega\tau_T$ large enough that $\Delta M_{th}/(\omega\tau_T)\lesssim0.02\,M''$. The viscous heating rate
$$\dot T=\frac{\omega M''\varepsilon_0^2}{2\rho c_v},\qquad \rho c_v\approx3nk_B=6.2\ \mathrm{MJ\,m^{-3}K^{-1}} \tag{7}$$
then limits $\varepsilon_0$ (steady offset $\dot T\tau_T$, or rise $\dot T\,t_{run}$ when $\tau_T>t_{run}$, kept ≲ 100 K). The thermostat mass is the knob ($Q\propto\tau_T^2$); the chain length does not change the coupling time.

| P (ps) | ε₀ | τ_T (ps) | run (ps) |
|---|---|---|---|
| 0.2 | 0.010 | 2 | 40 |
| 1 | 0.015 | 10 | 40 |
| 5 | 0.020 | 250 | 100 |
| 20 | 0.03 | 10⁴ | 300 |
| 100 | 0.03 | 10⁵ | 1100 |

The uniaxial values then are adiabatic ($K_S$-based), comparable to NVE GK. Check the mean T of each run (`v_tt` in `stress.dat`).
Cost: shear 0.64 M + uniaxial 1.58 M steps ≈ 26 P100-h; longest task (uniaxial P100) ≈ 13 h.

**The 8000 K uniaxial sweep (τ_T = 0.1 ps) is contaminated by Eq. 6 at all frequencies**: $\Delta M_{th}\,\omega\tau_T$ = 2.5 GPa at 50 GHz (measured $M''$ = 3.9) and 0.5 GPa at 10 GHz. Its $M''$ and the $\zeta\approx1.8$ mPa s estimate are not usable; its $M'$ at ≤ 200 GHz is $K_T$. Rerun with the table above approved by RC: job 4147331 in `R/8000K/FreqSweep_x2` (each task from its old `FreqSweep_x/P*/eq.data`); watcher `tools/sweep_watch.sh R/8000K/FreqSweep_x2:4147331:uniaxial`.

## 6. Results collection and plots (RC request 10-07)

`tools/anelastic_collect.py [--gk-tc 1.0] [--fmax-fit 0.2]` reads every `lockin_results.txt` and both GK `pres.dat` and writes `Anelasticity/results/`:
- `results_all.md`: tables, with equations numbered in the file;
- `results_all.csv`: every sweep point plus the GK spectra;
- figures as PDF and PNG: `fig_shear_moduli`, `fig_shear_viscosity`, `fig_uniaxial_loss`, `fig_uniaxial_storage`, `fig_gk_time`. They use Liberation Sans, which has Arial's metrics; Arial itself is not installed on the cluster.

Viscosity from the slope of the loss modulus, $\eta_0=\lim_{\omega\to0}dG''/d\omega$, is computed three ways:
- secants between sweep frequencies;
- a weighted fit through the origin for f ≤ 200 GHz;
- the analytic GK derivative $\int G(t)[\cos\omega t-\omega t\sin\omega t]\,dt$. It is noise-dominated above about 3 THz, so the plots stop there.

The GK cutoff $t_c$ is 1 ps: G(t) has decayed by 0.5 ps, and a longer $t_c$ adds tail noise that grows with ω.

Partial GK results (~130 ps, 10-07 05:xx):
- 8000 K: $\eta_0=8.1\pm0.8$, $\zeta_0=0.9\pm0.2$ mPa s.
- 7000 K: $\eta_0=10.6\pm0.8$, $\zeta_0=1.1\pm0.1$ mPa s.
- The GK $G'$ and $G''$ agree with the sweep at 1 and 5 THz within errors.
- The NVE 8000 K run sits at ⟨T⟩ = 8112 K, because the energy was set by the end of the NVT stage.

A background wait in this session runs the final collect when all of 4146463/4, 4147084/5, 4147331 and 4115169 have finished. If the session is gone, run `anelastic_collect.py` by hand.

## 7. Cooling sequence: 6000 K and 5000 K (RC request 10-07)

Each temperature starts from the end of the previous temperature's GK equilibration: `R/<T+1000>K/GK/eq.data`, then 20 ps NVT at T in the GK job. Both sweeps copy `R/<T>K/GK/eq.data`, with the same task tables as 7000 K except that the shear P100 point is capped at γ₀ = 0.5 (AMP = 15.0717 Å) in the supercooled liquid.

| T (K) | GK job | shear sweep | uniaxial sweep | state after 20 ps NVT |
|---|---|---|---|---|
| 6000 | 4151022 | 4151695 | 4151696 | liquid: P = 175 GPa, PE flat −14830 ± 50 eV, MSD 2.9 Å²/ps |
| 5000 | ~~4151697~~ → **4152373** | solid: 4163773 | (in solid sweep) | **crystallized** at 8–20 ps of NVT: PE −15700 → −17588 eV (−0.46 eV/atom), P 166 → 158 GPa, MSD 0.3 Å² plateau |
| 4000 | 4154636 (from the 5000 K crystal after 100 ps NVT) | solid: 4163775 | (in solid sweep) | crystal; PE flat −19000 ± 40 eV, P = 145 GPa |

If a temperature crystallizes (PE drop, MSD plateau), the solid protocol applies:
- strains γ₀ ≲ 0.01, longer runs;
- $Q^{-1}=G''/G'$;
- GK $G(t)$ then has a plateau and the viscosity is undefined.

The 4096-atom cube fits an 8×8×8 B1 crystal exactly. RC wants solid results too.

5000 K structure (`tools/xtal_check.py`, S(k) over box wavevectors): B1 Bragg peaks in the (200) shell (|n| ≈ 16, d = 1.88 Å) and the (220) shell (|n| ≈ 22). The intensity is spread over several unrelated directions with S/N ≈ 0.1, so the crystal is misoriented to the box, polycrystalline, or still growing. Job 4151697 was cancelled 2 ps into NVE; its files are in `5000K/GK/aborted_4151697_crystallizing/`. 4152373 continues from `eq_nvt20ps.data` with 80 ps more NVT, then 1.5 ns NVE.

Solid sweeps need a decision from RC.
- Use γ₀, ε₀ ≈ 0.005–0.01 to stay elastic.
- The loss $G''$ is small (Q⁻¹ ~ 0.01–0.1). At 4096 atoms the lock-in error on $G''$ is ≈ 3 GPa per 60 ps at γ₀ = 0.005, so about 600 ps per frequency is needed: ~3 P100-days per T for 5 frequencies × 2 modes.
- GK gives $G''(\omega)$ at all frequencies from one 1.5 ns run (0.7 P100-day). It is the cheaper route to the solid loss spectrum; the sweep then mainly fixes $G'$.

## 8. Update 08:40, 10-07
4115169_5 (8000 K uniaxial P100, τ_T = 0.1 ps) finished: $M'=581.9\pm1.0$, $M''=1.16\pm0.64$ GPa, 9 cycles. $K_T$ from 200/50/10 GHz: 579.6, 582.0, 581.9 GPa. $M''$ not used (§5).

### 7a. Solid (RC choices 10-07: reduced sweep, plus a perfect-crystal GK reference)

- **5000 K state after 100 ps of NVT:** PE dropped again at 70–80 ps (−17996 → −18470 eV), then is flat in NVE (−18470 ± 15 eV, ⟨T⟩ = 4979 K, P = 151.8 GPa, $E_{tot}$ conserved to 0.1 eV). S(k) shows **one B1 grain rotated to the box**: three mutually orthogonal (200) peaks, (8,−7,−12), (14,6,5), (2,−13,9), each with S/N = 0.74. MSD creeps from 0.8 to 1.05 Å² per 100 ps, so there is slow defect motion. A rotated crystal is incommensurate with the periodic box, so it must contain defects or strain.
- **Solid sweeps** `R/{5000,4000}K/FreqSweep_solid` (arrays 4163773 and 4163775, 6 tasks each): shear xz and uniaxial x at P = 0.2, 1 and 5 ps; γ₀ = ε₀ = 0.01; 200 ps each; uniaxial τ_T = 2, 10, 250 ps. Cost 1.2 M steps per T, ≈ 0.6 P100-day per T. My earlier estimate of 0.4 per T was low. `sweep_watch.sh` now reads MODE from tasks.txt column 11, so one root can mix modes.
- **Perfect-B1 reference** `R/5000K/GK_B1perfect` (4163822): `B1_8x8x8.data`, a = L/8 = 3.767929 Å, Maxwell velocities at 5000 K; 20 ps NVT, then 1.5 ns NVE.
- **GK in the solid:** `gk_viscosity.analyse` now subtracts the mean stress of every component, since a crystal can carry a residual static stress. This does not change the liquid results. In a crystal, $G(0)$ is only the fluctuation part of the modulus (no Born term), and $\int G\,dt$ is the low-frequency loss ($G''\approx\omega\int G\,dt$), not a viscosity.
- **Background waits in this session:** the watcher on the solid sweeps, and a final `anelastic_collect.py` run once no GK* or MgO* GPU job is left.
- **Perfect-B1 sweep** (RC request 10-07): `R/5000K/FreqSweep_B1perfect`, array 4168355. Same 6-task table as `FreqSweep_solid`, starting from `GK_B1perfect/eq.data` (after 20 ps NVT: PE −18550 ± 40 eV, P = 151.5 GPa; the crystal grown from the liquid sits ≈ 80 eV higher, from its defects). ≈ 0.6 P100-day. Watched by `sweep_watch.sh`; included in `anelastic_collect.py`.

### 7b. Controlled-defect crystals at 5000 K (RC choice 10-07: Schottky pairs + bicrystal; RC: "may need some defects in the solid to see anything")

Built with `tools/build_defect_crystals.py`. Each gets 50 ps NVT, then 1.5 ns NVE GK, plus the reduced 6-task solid sweep (γ₀ = ε₀ = 0.01, 200 ps each). Each sweep is submitted automatically when its GK `eq.data` appears (background wait in session).

| case | file | N | box (Å) | V/atom (Å³) | GK job | sweep dir |
|---|---|---|---|---|---|---|
| Schottky | `GK_Schottky/B1_schottky20.data` | 4056 | 30.1434³ | 6.753 | 4169847 | `FreqSweep_Schottky` |
| bicrystal | `GK_bicrystal/B1_S5_310.data` | 3920 | 29.788 × 15.072 × 59.576 | 6.823 | 4169848 | `FreqSweep_bicrystal` |

- **Schottky:** 20 bound pairs (Mg vacancy plus its nearest O vacancy along ±x, ±y or ±z; tetragonal). Pair centres ≥ 6 Å apart. Removed from the perfect a = L/8 crystal in the same box. Expected signature: a Zener-type Debye peak at $\omega\tau_{reorient}\approx1$.
- **Bicrystal:** Σ5 (310)/[001] symmetric tilt. The grains are rotated ±18.43° about the tilt axis; periods are a√10/2 in-plane and a along the tilt axis. After the y↔z swap, the boundary normal is z and the tilt axis is y, so the xz shear drives boundary sliding. There are two boundaries, 29.8 Å apart. Coincident atoms (< 1.2 Å) were removed and stoichiometry restored: 80 atoms fewer than the perfect 4000, so the boundaries carry excess volume and P will be lower than in bulk. Shear amplitude = 0.01·Lz = 0.5958 Å; uniaxial amplitude = 0.01·Lx = 0.2979 Å.
- **`anelastic_collect.py`:** now takes a per-run box volume (`VBOX`) for the GK prefactor, since the bicrystal box differs.
- 50 ps NVT done for both cases, stable with no further transformation:
  - Schottky: PE −18300 ± 25 eV, P = 148.7 GPa.
  - Bicrystal: PE −17750 ± 25 eV, P = 141.7 GPa (lower than bulk because of the boundaries' excess volume).
  - Sweeps: Schottky 4172060, bicrystal 4172066 (6 tasks each), watched by `sweep_watch.sh`.

## 7c. Lock-in phase lag: test with half the timestep (2026-10-07)
The perfect B1 crystal (aligned with the box, $G' = C_{44} \approx 171$ GPa) gives these shear phase angles:
- 0.2 THz: $\delta = -0.02°$
- 1 THz: $\delta = -0.20 \pm 0.16°$
- 5 THz: $\delta = -1.47 \pm 0.08°$

The harmonics are small ($|\sigma_2/\sigma_1| < 0.004$), so this is not a nonlinear effect. A negative loss is unphysical.

The phase scales with $\omega$, which points to a constant lag between the stress and the box strain:

$$\delta_{\rm meas} = \delta_{\rm true} - \omega \tau_{\rm lag}, \qquad \tau_{\rm lag} \approx 0.8\ {\rm fs} \approx \Delta t \tag{9}$$

The likely source is the update order. `fix deform` sets the box at `end_of_step`, so the virial at step $n$ is computed in the box of step $n-1$. Meanwhile strain.dat records the box of step $n$.

Size of the correction, $\Delta G'' \approx G' \omega \tau_{\rm lag}$:
- Liquids: under 1 % at $f \le 1$ THz and about 5 % at 5 THz.
- Solids at 5 THz: $\Delta G'' \approx 4$–$7$ GPa, which is the same order as the loss itself.

Test:
- Directory: 5000K/FreqSweep_B1perfect_dt05, job 4188049.
- Shear at 5 THz with $\Delta t = 0.5$ fs.
- A new `DT` variable was added to anelastic_sweep.lammps; the backup is Downloads/anelastic_sweep.lammps.bak_2026-10-07b.
- Expected result: $\delta \approx -0.73°$ if Eq. (9) holds.
- Run the lock-in with `--dt 0.0005`.

## 7d. Defect sweeps at 5000 K: results (2026-10-07)
Shear lock-in values, before the lag correction of Eq. (9) ($+0.06°$, $+0.29°$, $+1.47°$ at 0.2, 1 and 5 THz):

| system | f (THz) | $G'$ (GPa) | $G''$ (GPa) | $\delta$ | $\lvert\sigma_2/\sigma_1\rvert$ |
|---|---|---|---|---|---|
| perfect B1 | 0.2 | 170.5 ± 0.4 | −0.06 ± 0.47 | −0.02° | 0.004 |
| perfect B1 | 1 | 171.3 ± 0.2 | −0.59 ± 0.48 | −0.20° | 0.002 |
| perfect B1 | 5 | 171.8 ± 0.2 | −4.4 ± 0.3 | −1.47° | 0.002 |
| Schottky (20 pairs) | 0.2 | 148.2 ± 1.6 | 14.1 ± 3.1 | 5.45° | 0.008 |
| Schottky | 1 | 150.0 ± 0.8 | 11.4 ± 2.6 | 4.33° | 0.001 |
| Schottky | 5 | 163.0 ± 4.0 | 6.5 ± 6.7 | 2.29° | 0.004 |
| bicrystal Σ5 | 0.2 | 137.6 ± 1.6 | 6.5 ± 1.1 | 2.71° | 0.008 |
| bicrystal | 1 | 216 ± 27 | 99 ± 58 | 24.5° | 0.125 |
| bicrystal | 5 | 28.2 ± 0.4 | 33.2 ± 2.3 | 49.7° | 0.023 |

**Schottky pairs.** The loss is clear and grows toward low frequency. $G'$ falls from 163 to 148 GPa between 5 and 0.2 THz, against $C_{44} = 171$ GPa for the perfect crystal. This is a Zener-type relaxation whose loss peak lies at or below 0.2 THz, so the relaxation time is of order 1 ps or longer.

**Bicrystal.** Only the 0.2 THz point is quasi-static. At 1 and 5 THz the driving is close to, or above, the lowest transverse standing wave across the slab:

$$f_1 \approx \frac{v_s}{L_z} \approx \frac{5.9\ {\rm km/s}}{59.6\ {\rm \AA}} \approx 1\ {\rm THz} \tag{10}$$

The compliant boundaries lower this frequency further. Sliding at the boundaries makes the motion non-affine, so inertia enters the response. The results are a finite-size resonance (large errors and harmonics at 1 THz, inertia-dominated $G'$ at 5 THz), not anelasticity.

The uniaxial bicrystal values are non-monotonic: $M' = 977$, 889 and 1174 GPa. The cause is the same.

**Next step (proposed, not submitted):** shear at $P = 20$ and 50 ps for the Schottky and bicrystal cells, to find the loss peak and grain-boundary sliding.

**Submitted (RC approved, 2026-10-07):** tasks 7–8 (P20ps_xz, P50ps_xz) were appended to tasks.txt in FreqSweep_Schottky (job 4195534) and FreqSweep_bicrystal (job 4195535).

| period | steps | cycles | NAV | NCHUNK |
|---|---|---|---|---|
| 20 ps | 400k | 20 | 100 | 5 |
| 50 ps | 500k | 10 | 250 | 2 |

- Shear strain amplitude: $\gamma_0 = 0.01$.
- Watched by sweep_watch.sh.
- Expected run time: about 5–6.5 h each.

## 7e. Quality factor Q in the collection (2026-10-07)
anelastic_collect.py now reports $Q$ (Eqs. 8–9 in its docstring and in results_all.md):
- **Formula:** $Q^{-1} = \tan\delta = G''/G'$ (or $M''/M'$), and $Q = 1/\tan\delta$.
- **Liquid-like points:** where $|G''| > |G'|$, $Q = G'/G''$ is computed directly, because $G' \to 0$ in a liquid.
- **Unresolved points:** reported as 2σ bounds.
- **CSV:** new columns Qinv, dQinv, Q, dQ, Q_text.
- **Tables:** the sweep table has a $Q$ column, and the new §1a gives $Q$ at every frequency (marked † when $|\sigma_2/\sigma_1| > 0.1$). The GK table has $Q = G'/G''$ for the liquids only.
- **Figures:**
  - New fig_Q has $Q^{-1}$ on the left axis and $Q$ on the right axis, for shear and uniaxial, with liquid GK curves. Bounds are drawn as arrows and nonlinear points get a black ×.
  - In fig_solid, the right panel was updated in the same way.
- Backup of the previous script: Downloads/anelastic_collect.py.bak_2026-10-07Q.

## 7f. Lag test result: the lag is exactly one MD step (2026-10-07)
The half-timestep run (job 4188049, perfect B1, shear, 5 THz, $\Delta t = 0.5$ fs) gives:

| quantity | value |
|---|---|
| $G'$ | 172.05 ± 0.35 GPa |
| $G''$ | −1.43 ± 0.21 GPa |
| $\delta$ | −0.48 ± 0.07° |
| $\lvert\sigma_2/\sigma_1\rvert$ | 0.002 |

This value comes from `anelastic_lockin.py --dt 0.0005`. The line that sweep_watch wrote to lockin_results.txt assumed 1 fs and is wrong; ignore it.

Correct each phase by one step, $\omega\Delta t$ = 1.80° (1 fs) and 0.90° (0.5 fs):

$$\delta_{\rm true} = \delta_{\rm meas} + \omega\,\Delta t \tag{11}$$

This gives $+0.33 \pm 0.08°$ and $+0.42 \pm 0.07°$, which agree. The lag is therefore one MD step, and the perfect crystal has a small real phonon loss at 5 THz: $Q \approx 170 \pm 40$.

anelastic_collect.py applies Eq. (10) of its docstring to every sweep point:

$$M^*_{\rm corr} = M^*_{\rm lock\text{-}in}\, e^{i\omega\Delta t} \tag{10}$$

The `--no-lag` option turns the correction off. The lockin_results.txt files themselves remain uncorrected.

## 7g. Low-frequency defect shear, P = 20 and 50 ps (jobs 4195534, 4195535)

| cell | f | $G'$ (GPa) | $G''$ (GPa) | $\delta$ | $\lvert\sigma_2/\sigma_1\rvert$ |
|---|---|---|---|---|---|
| Schottky | 50 GHz | 129.2 ± 4.9 | 4.8 ± 4.5 | 2.1° | 0.006 |
| Schottky | 20 GHz | 140 ± 9 | 37 ± 19 | 14.8° | 0.076 |
| bicrystal | 50 GHz | 128.9 ± 8.2 | 5.8 ± 7.7 | 2.6° | 0.035 |
| bicrystal | 20 GHz | 108 ± 15 | 15 ± 12 | 8.0° | 0.106 |

The lag correction at these frequencies is $\le 0.02°$.

**The Schottky cell is not stationary.** Its PE falls steadily in every run:
- $\approx 60$ eV over the 200 ps runs.
- $\approx 66$ eV over the 500 ps run at P = 50 ps, from −18318 to −18384 eV.
- $p$ falls from 148.5 to 147.2 GPa.
- $\langle p_{xz}\rangle$ jumps by about 1 GPa in one quarter of the 50 ps run.

The vacancies are annealing or clustering on the run time scale. The low-frequency Schottky loss therefore mixes reversible relaxation with irreversible ageing. The 20 GHz point in particular (37 ± 19 GPa) is not a linear anelastic modulus.

**The bicrystal is stationary** (PE constant to 0.5 eV, $p$ to 0.01 GPa). $G'$ softens monotonically toward low frequency, consistent with the onset of boundary sliding: 138 GPa (0.2 THz), 129 GPa (50 GHz), 108 GPa (20 GHz). $G''$ is not resolved below 0.2 THz.

The low-frequency errors are large: 4–19 GPa against 1–3 GPa at 0.2–1 THz. Stress noise in the solid rises at low frequency, and these runs have few cycles (20 and 10).

Options (not submitted):
1. Bicrystal at P = 20 and 50 ps with $\gamma_0 = 0.03$ and 2–3× longer runs, which would cut the errors by about 5×. Check linearity through the harmonics.
2. Schottky: anneal at 5000 K until PE reaches a plateau (watch PE), then repeat P = 5, 20 and 50 ps on the aged cell.

## 7h. Follow-ups submitted, and GK corrections (2026-10-08)
**1. Bicrystal, $\gamma_0 = 0.03$** (5000K/FreqSweep_bicrystal_g3, job 4230008):
- P20ps_xz: 1.0 M steps (50 cycles).
- P50ps_xz: 1.25 M steps (25 cycles).
- About 27 steps/s, so at most about 13 h per task.

**2. Aged Schottky cell** (5000K/FreqSweep_Schottky_aged, job 4230009):
- The 1.5 ns NVE GK run had already aged the cell. PE fell by 28 eV within 150 ps and then stayed flat for 1.35 ns, at $T = 5077$ K.
- Its final restart.gk is copied to restart_aged.gk. Each task converts it to aged.data on the GPU node (restart2data.lammps), then runs 100 ps NVT at 5000 K.
- Shear with $\gamma_0 = 0.02$:
  - P5ps_xz: 200k steps.
  - P20ps_xz: 800k steps.
  - P50ps_xz: 1 M steps.
- Watched by sweep_watch.sh.

**The 6000 K GK run crystallized at about 1050 ps** (NVE). PE fell by 1330 eV and the latent heat raised $T$ to 8490 K. anelastic_collect.py uses only the first 1040 ps (GKCUT). Result: $\eta_0 = 18.3 \pm 0.5$, $\zeta_0 = 1.64 \pm 0.13$ mPa s. All 6000 K sweeps stayed liquid (PE $\approx -14840$ eV; the crystal is $\approx -16100$ eV).

**Schottky GK.** The first 300 ps are skipped (GKSKIP). Even so, $G(0) = 376$ GPa and $\int_0^{1\,\rm ps} G\,dt = 289$ mPa s. The stress of the 20-pair cell wanders slowly, as vacancy jumps produce stress steps. This is a finite-size, rare-event signal and not a usable modulus. Treat the Schottky GK row as unreliable.

**New figure fig_vs_T (PDF and PNG):** results against $T$, each panel with the GK $\langle p\rangle(T)$ on a right-hand axis. The shaded band marks the melt-grown B1 crystal; defect cells are drawn as open markers at 5000 K.
- (a) Viscosities: GK $\eta_0$ and $\zeta_0$, and the sweep slope fits (Eq. 4). For the solid, $\int G\,dt$ is shown as open markers.
- (b) Moduli: $G_\infty$, $G'$ at 1 THz, and $M'$ at 10 GHz and 0.2 THz.
- (c) Shear $Q$ at 0.2 and 1 THz.
- (d) Uniaxial $Q$ at 0.2 and 1 THz.

$\langle p\rangle$ at fixed $V$:

| $T$ (K) | 8000 | 7000 | 6000 | 5000 (B1) | 4000 (B1) |
|---|---|---|---|---|---|
| $\langle p\rangle$ (GPa) | 192.8 | 183.4 | 174.9 | 151.8 | 144.9 |

Freezing lowers $p$ by about 23 GPa at constant volume.
