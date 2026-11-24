# Plan: Q and effective viscosity of solid Fe at inner-core conditions (2026-11-18)

**RC request (11-18):** "Plan a set of runs for solid Fe at core conditions like you did for MgO and MgSiO₃. We want Q and the effective viscosity for solid Fe." Earlier (11-17): hcp iron, 300–350 GPa, 5000–7000 K, VASP MLFF (`pair_style vasp`).

Status: **proposal only; nothing in this plan has been submitted.** Builds and speed tests: `tools/vasp_lammps/README.md` and restart 11-17 §7. Methods carried over from MgO/MgSiO₃: `ANELASTICITY_METHODS.md` (cited below as M-Eq. n), and summary §3, §5d, §5k.

## 0. What carries over, and what is different for Fe

The MgO/MgSiO₃ program had three parts, and all three carry over:
1. **Q from oscillatory NEMD** (lock-in, 20 GHz–5 THz) on perfect, point-defect, grain-boundary and melt-grown cells, with Green–Kubo cross-checks.
2. **Effective viscosity**, from $|\eta^*|$ and the flow bound (M-Eq. 14) directly from MD, and from mechanism rates extrapolated to seismic and creep time scales: vacancy diffusion (Ita–Cohen free energies), dislocation drag (Orowan) and boundary sliding (grain-scale model, summary Eq. 13).
3. **Validation** of the potential against DFT and experiment before production.

Six things are new for Fe:

1. **The current force field cannot be used for hcp.**
   - Its 913 training configurations are bcc and liquid only (restart 11-17 §7.3).
   - 350 GPa is at or beyond the edge of the training set.
   - **No fcc either (checked 11-18, RC's question).** I ran adaptive CNA (`tools/mlab_structure.py`; Stukowski 2012) on all 913 ML_AB configurations. The results are in Table 0 below.
   - Training on hcp **and fcc** (Phase A) has to come first. It is the largest new cost.

**Table 0.** Local structure of the 913 ML_AB configurations (atom fractions by adaptive CNA).

| configurations | V/atom (Å³) | fcc | hcp | bcc | other (liquid or too hot to classify) |
|---|---|---|---|---|---|
| 1–200 | 6.81–6.88 | 0 | 0 | 0.98–1.00 | ≤ 0.02 |
| 201–400 | 6.86–6.92 | ≤ 0.001 | ≤ 0.03 | 0.39–0.91 | 0.09–0.58 |
| 401–500 | 6.92–6.95 | 0.01–0.02 | 0.12–0.17 | 0.07–0.11 | 0.70–0.80 |
| 501–913 | 7.03–7.35 | ≤ 0.008 | ≤ 0.07 | ≤ 0.07 | 0.86–1.00 |

- **No configuration is mainly fcc or hcp.** The maximum fcc fraction is 0.12 and the maximum hcp fraction 0.29 (both configuration 426). Only 10 configurations have more than 25 % close-packed atoms.
- The close-packed atoms in configurations 401–500 are local fragments in hot bcc that is disordering or transforming, not crystals.
- **The 2025 crystallized start cell (`plugin_test/start8192.data`) has 16 % fcc, 23 % hcp, 2 % bcc and 60 % other.** So the current FF crystallizes the melt into stacking-disordered close-packed Fe, a structure it was never trained on.
- **Why fcc matters even if hcp is the stable phase.** A basal stacking fault in hcp is locally fcc. The same holds for the ribbons between basal partial dislocations, for twin and tilt boundary cores, and for a melt-grown polycrystal. The fcc–hcp energy difference at these pressures is small (tens of meV/atom or less (†)). It sets the stacking-fault energy, which controls partial splitting and the dislocation and boundary mechanisms of §5.
- **Validation tool.** The classifier was checked on ideal and noisy fcc, hcp and bcc lattices. All are 100 % correct at 0.08 Å random displacements. At 0.15 Å, 40–80 % of atoms are still classified and the rest fall to "other"; none are misassigned.
2. **Electronic temperature.** At 5000–7000 K the electronic entropy of Fe is not small, and forces and stresses are derivatives of the Mermin free energy at $T_{el}$.
   - The INCARs in the refit directory show SIGMA = 0.26 eV (3000 K) and 0.13 eV (1500 K). These are not $k_BT$ at 5000–7000 K. Which SIGMA each ML_AB configuration was computed with is still to be checked.
   - A VASP MLFF has no temperature input; Deng's DeePMD model has fparam $=k_BT$. So either one force field is fitted per temperature band, or the error of a single $T_{el}$ is shown to be small. The cheap test is A0(c).
3. **Anisotropy.** hcp is hexagonal and has five independent elastic constants. A single xz sweep is not enough (§2.2).
4. **c/a depends on T.** Cells must be NPT-relaxed with the c/a ratio free at every (P, T) before the fixed-cell sweeps (Steinle-Neumann et al. 2001 (†)). The MgO practice of a T series at one fixed cubic V does not carry over.
5. **The hcp site has no inversion centre** (site symmetry $\bar6m2$, $D_{3h}$). Like bridgmanite (summary §5i Eq. 14), strain couples to an optic mode, here the Raman-active $E_{2g}$ mode. It enters the basal channels ($C_{66}$, $C_{11}$) but not $C_{44}$ or $C_{33}$. Crystal Q should therefore be taken at ≤ 1 THz in the basal channels, and the Kramers–Kronig check (M-Eq. 15) will flag it. The $E_{2g}$ frequency at 330 GPa comes from the MLFF itself (A3).
6. **Cost.** On CPUs the VASP MLFF runs at 6.5 steps/s for 8192 atoms on one 64-core icelake node. That is about 4× more node time per atom-step than DeePMD MgO on one P100 (22–27 steps/s at 4096 atoms). The H200 is slower still (0.79 steps/s). MPI × OpenMP scans 7166452 (CPU) and 7166454 (H200) are queued, and all costs below will be rescaled to their result. §6 discusses a cheaper route.

A further caveat applies to all classical MD of a metal. The MD runs on the Born–Oppenheimer (Mermin) surface with no electron–phonon friction. The electronic contribution to phonon damping is therefore missing from the THz Q. It is irrelevant at seismic frequencies but should be stated with the THz numbers.

## 1. Quantities

The definitions are those of MgO (M-Eqs. 1–4).

$$G^*(\omega)=G'+iG'',\qquad Q^{-1}=\frac{G''}{G'},\qquad \eta'(\omega)=\frac{G''}{\omega},\qquad |\eta^*|=\frac{|G^*|}{\omega} \tag{1}$$

**Channels in a hexagonal crystal.** The orthohexagonal cell has x = [2$\bar1\bar1$0] (a), y = [01$\bar1$0] (√3 a) and z = [0001] (c).

| drive | modulus measured | internal-strain term? |
|---|---|---|
| xz (or yz) shear | $C_{44}^*$ | no |
| xy shear | $C_{66}^*=(C_{11}^*-C_{12}^*)/2$ | yes ($E_{2g}$) |
| uniaxial x | $C_{11}^*$ | yes |
| uniaxial z | $C_{33}^*$ | no |

**Isotropic aggregate.** For comparison with seismology, the aggregate shear modulus is formed from the complex constants as a Voigt average:

$$G_V^*=\frac{1}{15}\left[2C_{11}^*+C_{33}^*-C_{12}^*-2C_{13}^*+3\left(2C_{44}^*+C_{66}^*\right)\right] \tag{2}$$

$$Q_{agg}^{-1}=\frac{\mathrm{Im}\,G_V^*}{\mathrm{Re}\,G_V^*} \tag{3}$$

$C_{12}^*$ and $C_{13}^*$ are not driven directly:
- $C_{12}^*$ follows from $C_{11}^*-2C_{66}^*$.
- $C_{13}^*$ comes from the transverse stresses ($\sigma_{zz}$ under the x drive). The lock-in already fits all six stress components.
- A Reuss bound comes from the inverted compliance. Voigt and Reuss bracket the polycrystal. The melt-grown cell (B2) is the direct measurement.

**Effective viscosity.** There are three levels, as for MgO:
- (i) $|\eta^*|$ and the flow bound (M-Eq. 14) from the sweeps.
- (ii) Mechanism viscosities. Diffusion creep (Eq. 4), dislocation glide (Eq. 5), and boundary sliding with diffusional accommodation (Eq. 6).
- (iii) $Q^{-1}(\omega)$ at 0.01–1 Hz from the grain-scale model.

$$\eta_{NH}=\frac{k_BT\,d^2}{A_{NH}\,\Omega\,D_{Fe}},\qquad \eta_{C}=\frac{k_BT\,d^3}{A_C\,\Omega\,\delta D_{gb}} \tag{4}$$

$$\eta_{disl}=\frac{\tau}{\dot\varepsilon}=\frac{B}{\rho\,b^2}\quad(\text{drag-limited glide; Orowan } \dot\varepsilon=\rho b v,\ v=b\tau/B) \tag{5}$$

$$J^*(\omega)=J_U\left[1+\frac{\Delta_J}{1+i\omega\tau_e}\right]-\frac{i}{\omega\,\eta_{diff}(d)},\qquad \tau_e=\kappa\frac{\beta d}{G_U} \tag{6}$$

Here Ω is the atomic volume, d the grain size, ρ the dislocation density and β the boundary friction (summary §5d). Grain sizes to scan run from 1 mm to 100 m; inner-core estimates span this whole range (†).

## 2. State points and cells

### 2.1 State points

- **Primary pressure:** 330 GPa (inner-core boundary). **Secondary:** 360 GPa (centre, 364 GPa), at two temperatures.
- **Temperatures are set by the model's own melting point $T_m$** (A3), because homologous temperature controls defect populations, premelting and diffusion:
  - $T/T_m$ ≈ 0.70, 0.80, 0.90, 0.95, 0.98;
  - provisionally 4400, 5000, 5600, 6000, 6200 K if $T_m$(330 GPa) ≈ 6300 K. Published values are 5500–6400 K (Alfè 2009; Anzellini et al. 2013; Sinmyo et al. 2019) (†).
- **One liquid state** at $T_m$ + 300 K (GK η₀; the counterpart of the MgO and MgSiO₃ liquid branch).
- **Cell geometry.** Each (P, T) is NPT-equilibrated (aniso, c/a free; 50 ps) and then run in NVT at the mean cell. Estimates: V ≈ 6.85 Å³/atom, a ≈ 2.15 Å, c ≈ 3.43 Å at 330 GPa and 5500 K.

### 2.2 Cells

| id | cell | atoms | built by |
|---|---|---|---|
| H0 | perfect hcp, orthohexagonal 16 × 8 × 8 (≈ 34 × 30 × 27 Å) | 4096 | new `build_hcp_cells.py` |
| H1 | hcp + 1 % vacancies, random sites, aged ≈ 200 ps (`T_ladder_job.sh`) | 4055 | `build_hcp_cells.py --vac` |
| H2 | {10$\bar1$2} twin bicrystal, boundary normal z (twinning is the low-stress deformation mode of hcp metals; twin walls move at low stress) | ≈ 4–6 k | `build_hcp_cells.py --twin` |
| H3 | [0001] Σ7 (21.8°) symmetric tilt bicrystal, boundary normal z (general sliding boundary) | ≈ 4–6 k | `build_hcp_cells.py --tilt` |
| H4 | melt-grown polycrystal: liquid cooled at fixed V until it crystallizes (MgO protocol, M §2 step 4); phase and grain check by CNA / q4–q6 | 8192 | existing 2025 start cell `end.pos.start` as a seed, rerun with the new FF |
| H5 | dislocation slabs: ⟨a⟩ edge and screw on basal and prismatic planes (b = a ≈ 2.15 Å) | 10–15 k | new `build_hcp_dislocation.py` (rigid-block drive as `disl_drive.lammps`) |
| H6 | (optional) bcc, 16³ × 2 | 8192 | lattice |

H6, bcc, is there because the existing FF was fitted to bcc. Whether bcc is (dynamically) stable at inner-core conditions is a live question (Belonoshko et al. 2017, 2019 (†)), and a fast-diffusing bcc phase would change the viscosity answer by orders of magnitude.

## 3. Phase A: training and validation of the force field

| step | what | cost |
|---|---|---|
| A0   | **DFT settings and timing (revised 11-18; RC: "for solids we need only small cells to train, 64 atoms max"; "we will do these non-magnetic").** 64-atom cells, ISPIN = 1, Fe_sv: hcp 4 × 4 × 2 hexagonal (2-atom) cells and fcc 4 × 4 × 4 primitive cells, at 0, 150 and 330 GPa near 0.9 $T_m$. (a) Γ-centred k-meshes 2³, 3³ and 4³; (b) ENCUT 500 against 700 eV (ENMAX 391 eV); (c) **$T_{el}$ test**: the same 10 snapshots per state at SIGMA = $k_B\cdot$300 K, 0.5 $T$ and $T$, giving ΔF, Δforces and Δstress (the shear stress especially). If the changes are below the FF error (≈ 0.1 eV/Å, ≈ 1 GPa), one FF is enough; otherwise one FF per T band (decision §8 item 2); (d) seconds per ionic step → the cost of A1. **Revised 11-18 (RC: "use vasp_gam"): A0b, Γ-only (vasp_gam) on all snapshots, with 2³ references on 2 snapshots and 3³/4³ references at 0 and 330 GPa (job 7190356).** (d′) **Consistency with the existing ML_AB** (vasp_gam, ENCUT 900, SIGMA 0.2588 eV at every T, 128 atoms): A0b includes those exact settings, so we can decide between appending with the old settings and recomputing the old set with the new ones. (e) **Reuse (RC: "you can add individual points to training … save them for test states too"):** the single points with the final settings are appended to ML_AB (snapshots s1–s3 of each state) or kept as a held-out test set for A2 (s4–s5). After appending, VASP reselects the local reference configurations (ML_MODE = select) before the refit | ≈ 10–15 node-h |
| A1   | **On-the-fly training** (VASP 6.6.1, ML_MODE = train, ISIF = 3 Langevin NPT with PSTRESS, ISPIN = 1, Fe_sv, SIGMA per A0(c)), continuing from the existing ML_AB (bcc and liquid at ≈ 300 GPa stay in). **Solids only, ≤ 64 atoms:** hcp (64; orthorhombic 4a × 2√3a × 2c, axes as in the LAMMPS production cells) and fcc (64) at P = 0, 50, 100, 150, 200, 250, 300 and 350 GPa, each a temperature ramp from 300 K to ≈ 0.98 $T_m(P)$ of the model (provisional $T_m$ ≈ 1800, 3000, 4000, 4500, 5000, 5500, 6000 and 6400 K (†), refined after A3(c)); 16 ramps of 10–20 k steps (split into T bands if A0(c) requires). **Defects:** hcp vacancy (63 atoms) and a basal stacking fault (I₂; 3 × 3 in-plane × 7 layers, 63 atoms) at 50, 200 and 330 GPa near 0.9 $T_m$ (6 runs). Non-magnetic everywhere by RC's choice: below about 50 GPa this is non-magnetic Fe, not the real magnetic phases, which matters only for comparisons with low-pressure experiments | ≈ 50–250 node-h (22 runs; A0(d) fixes this) |
| A1b  | **Second generation:** boundary, dislocation-core and polycrystal environments from Phase B and C cells, cut into ≤ 64-atom periodic cells, then short on-the-fly runs. Only if the A2 held-out test shows errors there                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | cost                                        |
| A2   | Refit (ML_MODE = refit, LINREG 4 as now) and **held-out DFT test**: the A0 snapshots s4–s5 (12 configurations at the final settings; s1–s3 give 18 training configurations) plus 40 configurations from MD with the new FF (hcp at 4 T, fcc at 2 T, liquid, vacancy, stacking fault, twin). Targets: energy < 3 meV/atom, force rmse < 0.15 eV/Å, stress < 1.5 GPa                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | ≈ 30 node-h                                 |
| A3   | **Validation MD** (CPU LAMMPS, `pair_style vasp`): (a) EOS and c/a(T) at 300–360 GPa against DFT-MD and experiment; (b) $C_{ij}$ at 0 K and at 3 T (stress–strain, 1024 atoms) against Steinle-Neumann et al. 2001, Vočadlo et al. 2009 and Martorell et al. 2013 (†); (c) **melting $T_m$** at 330 and 360 GPa by hcp–liquid coexistence (8192-atom elongated cell, NPH, 4 runs) against Alfè 2009, Anzellini 2013, Sinmyo 2019 (†); (d) **liquid GK** η₀ at 330 GPa / $T_m$ + 300 K (4096 atoms, 0.5 ns NVE) against Alfè, Kresse & Gillan 2000 (≈ 10 mPa s (†)); (e) phonon DOS and the $E_{2g}$ frequency from the velocity autocorrelation; (f) **fcc–hcp–bcc energy differences** at 0 K (300–360 GPa) and the **basal stacking-fault energies** (I₁, I₂, extrinsic) against static DFT on the same cells; (g) fcc–hcp Gibbs energy difference at 2 T by Frenkel–Ladd (the C1 machinery)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | ≈ 100 node-h                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | ≈ 20–50 node-h                              |

**Go/no-go after A3.** Production (B, C) starts only if the A2 targets are met and $T_m$, $C_{ij}$ and η₀(liquid) are within the published spread. This gate is the Fe analogue of the DFT checks done for MgO (summary §5l).

### 3.1 DeePMD route with recomputed configurations (RC 11-19)

RC 11-19: "Yes recomputing configs for deepmd is a good idea. I actually have a whole bunch of tools we have developed for that. I am waiting first for the k-point test." The reasons are in the A0b results (`results_Fe/A0b_summary.txt`): SIGMA must equal $k_BT$, so one VASP MLFF cannot span 300–6400 K, and the existing ML_AB has Γ-only and SIGMA 0.2588 eV errors. The DeePMD model takes fparam $=k_BT$ (as Deng's MgSiO₃ model and Xin Deng's pure-Fe model).

**Workflow (X. Deng's `mldp-master`; readable copy `/central/groups/carnegie_poc/xind/mldp-master`, `/home/xindeng` is private).** Environments (RC 11-19: "My lammps and deepmd and plumed installations work as well as you have run them"): **training, `dp test`, compression, LAMMPS and PLUMED use RC's `deepmd_py311`** (DeePMD-kit 3.2.0, `lmp`, `plumed`; P100 recipe in memory/lammps-gpu-jobs). It has no dpdata or asaplib, so only the mldp data scripts (steps 1–7, 9–10) run with X. Deng's `/central/groups/carnegie_poc/xind/mambaforge/envs/deepmd` python (dpdata) and `mambaforge/bin/asap`. Nothing is installed into `deepmd_py311` (its pip-TF setup is fragile).
1. SOAP descriptors: `asap gen_desc --fxyz NPdT.out soap -e -c 6 -n 6 -l 6 -g 0.44`.
2. Farthest-point selection on the descriptors: `asap/select_frames.py -i ASAP-desc.xyz -n 200`.
3. Extract the selected frames: `extract_deepmd.py -f NPdT.out -fmt dump -id test-frame-select-fps-n-200.index -st -t <T>`.
4. DFT recalculation: `recal_dpdata.py -d deepmd/ -if <inputs_T> -rv no`, with one input set per temperature band (SIGMA = $k_BT$).
5. Checks: `post_recal.py -ss *.sh`; `check_nbands_nelm.py -ip all -v`.
6. Merge: `merge_out.py -o OUTCAR -r y`.
7. To DeePMD format: `extract_deepmd.py -d deepmd -ttr 10000`.
8. `dp test -m ../MLP.pb -d recal`.
9. Split into training and test sets by model error: `model_dev/analysis.py -tf . -mp recal -rf . -euc 10 -fuc 10 -flc 0.44 -elc 0.012`.
10. New training data: `extract_deepmd.py -id recal_id_e_or_f`; copy `type*` into `deepmd/`.

Adaptation for this project:
- Sources of frames: the old 913 ML_AB configurations (bcc, liquid at ≈ 300 GPa, which keeps the liquid for $T_m$ and η₀), VASP-MLFF or DeePMD MD of hcp/fcc 64-atom cells at 0–350 GPa (§3 A1 states), later the defect cells. VASP on-the-fly MLFF serves only as a sampler.
- Recalculation settings: from A0b and the k-mesh test A0c (ENCUT 700, SIGMA $=k_BT$ per band, k-mesh: true shifted MP 2×2×2, 4 k-points listed explicitly with KBLOWUP = .FALSE., from A0c2), Fe_sv, ISPIN 1.
- Xin Deng's existing pure-Fe model (`/central/groups/carnegie_poc/xind/pure_iron/MLP`; 64-atom NPT 0–160 GPa, 3000–7000 K, fparam, rcut 6 Å, 4 iterations) uses PBEsol (`GGA = PS`), Fe_pv, ENCUT 800, Γ-centred 2×2×2, SIGMA = $k_BT$. **Its data cannot be mixed with ours as is.** It uses a different functional. Its Fe_pv RCORE is 2.2 bohr, so 2 × 1.16 Å = 2.33 Å exceeds $d_{nn}$ ≈ 2.12 Å at 330 GPa (PAW spheres overlap), while Fe_sv (RCORE 1.9 bohr, 2.01 Å) does not. Open for RC: PBE (as the old ML_AB and most core-Fe DFT) or PBEsol (as the Deng MgSiO₃ model).

### 3.2 Iterations: DeePMD MD → FPS sample → DFT test → add badly predicted frames (RC 11-20)

RC 11-20: "The plan is to do some MD runs (different structure vacancies twins grain boundaries) with the DP and then sample and test from those and iterate adding badly predicted configurations doing DFT on those and iterating until the potential is stable." This is X. Deng's `mldp-master` loop, §3.1 steps 1–10, applied to each system.

One model per iteration is enough. The error is measured directly against DFT on a sample, so no ensemble of models is needed. RC 11-20 corrected my first draft, which used a 4-model deviation: "you select a set and test those — this was in the workflow I sent you."

**Iteration 00 (submitted 11-20).** Job 7336710 trains `DP/00/graph.pb` and `graph_c.pb`. Its data:
- R1: the old ML_AB frames recomputed (`old`, `old_b`);
- R1b: A1 trajectory FPS frames plus rattled frames (`a1`);
- R1d: vacancies, vacancy jumps, Σ7 tilt and the {10$\bar1$2} twin (`def`).

**Each iteration NN ≥ 01:**
1. **DeePMD MD** with the previous model (P100, RC's `deepmd_py311` LAMMPS, `pair_style deepmd graph_c.pb fparam` $k_BT$). Systems and grid are below.
2. **Sample:** SOAP descriptors (`soap_fps.py`, c 6, n 6, l 6, g 0.44, as §3.1 step 1), then farthest-point selection of $n_{sel}$ frames per run (§3.1 step 2; Xin used 70–200 per trajectory). Equilibration frames are skipped.
3. **DFT** on the selected frames (§3.1 steps 3–5) with the R1 settings:
   - SIGMA = $k_BT$, NBANDS from `fe_r1_old.nbands`;
   - k-points: true shifted 2×2×2 for the 64-atom bulk cells, MP ceil(16 Å/L) for the others;
   - output in `R1/it<NN>/<system>_P<P>_T<T>/`, run with the `fe_r1d_job.sh` layout (2 × 32).
4. **Test:** `dp test` of the current model on these DFT frames (§3.1 step 8).
5. **Split by the true error** (§3.1 step 9, `model_dev/analysis.py`, mode "nn_vasp"). A frame is **badly predicted** if either error lies between its lower and upper cutoff (Eq. 7). The upper cutoffs only drop broken frames.

$$\varepsilon_E=\frac{|E^{DFT}-E^{DP}|}{N}\ \in\ (\varepsilon_E^{lo},\ \varepsilon_E^{hi}),\qquad \varepsilon_F=\sqrt{\frac{1}{3N}\sum_{i}\left\|\mathbf F_i^{DFT}-\mathbf F_i^{DP}\right\|^2}\ \in\ (\varepsilon_F^{lo},\ \varepsilon_F^{hi}) \tag{7}$$

   - **Cutoffs are set per iteration so that only 10–20 % of the sampled DFT frames go into training (RC 11-20).** The lower cutoffs $\varepsilon_E^{lo}$ and $\varepsilon_F^{lo}$ are taken at the 80th–90th percentile of the iteration's errors, per temperature band, so that a hot state does not take all the slots. Upper cutoffs as Xin (10, `-euc`, `-fuc`) only drop broken frames. Xin's 0.012 eV/atom and 0.44 eV/Å (`-elc`, `-flc`) are kept as a reference. Cutoffs, $n_{sel}$ and the MD lengths are tuned from iteration to iteration (RC 11-20: "force cutoff and run sizes can be varied").
   - Badly predicted frames are added to training (§3.1 step 10, `fe_dp_collect.py --sets ... it<NN>` restricted to their ids).
   - The well-predicted frames go to the cumulative test set `DP/test`. They are never trained on, so every DFT frame is used either way.
6. **Retrain** with all the training data:
   - from the previous model, `dp train --init-frz-model`, 200k steps;
   - the final model from scratch, 1.2M steps.

**Exploration MD systems** (cells kept ≤ 128 atoms, so every sampled frame goes to DFT as it is, with no cutting):

| system | atoms | ensemble |
|---|---|---|
| hcp perfect (orthohexagonal 4a × 2√3a × 2c) | 64 | NPT aniso |
| fcc perfect | 64 | NPT aniso |
| hcp, 1 and 2 vacancies | 63, 62 | NPT aniso; vacancies hop at ≥ 0.7 $T_m$ |
| hcp basal stacking fault I₂ (...ABAB\|CACA..., 3a × 2√3a × 6 layers, tilted third vector, one fault per 10 Å) | 72 | NPT aniso |
| Σ7 [0001] tilt bicrystal | 52 (and 104 = 2 × along the normal) | NPT, x, y, z independent; boundaries free to migrate and slide |
| {10$\bar1$2} twin bicrystal | 100 | as Σ7 |
| sheared cells (hcp perfect, vacancy, Σ7, twin) | as above | NVT + `fix deform` shear ±1–3 % (the strains of the anelastic sweeps, §4) |

- **Grid:** P = 0, 100, 200, 300, 350 GPa; T = 300 K, 0.4, 0.7 and 0.95 $T_m$, plus 1.05 $T_m$ (superheated, for premelting and disordered environments).
- **Length:** 20 ps per run, doubled in each iteration that passes.
- **Cost:** the MD is minutes per run on a P100 at 64 atoms. The DFT dominates at ≈ 1 node-h per frame. $n_{sel}$ is therefore set by the DFT budget:
  - 7 systems × 5 P × 5 T = 175 runs;
  - $n_{sel}$ = 2–4 per run gives 350–700 frames per iteration, i.e. ≈ 350–700 node-h.
  - Systems that pass cleanly drop out of later iterations, as in Xin's loop.

**Convergence ("the potential is stable").**
- (a) With the fraction fixed at 10–20 % by construction, convergence is judged by the size of the errors: the cutoffs themselves (the 80th–90th percentile errors) fall below the A2 targets in every system and state. The worst-predicted frames are then already good enough, and adding them stops changing the model.
- (b) The MD is stable (no lost atoms, no blow-up) for the full length.
- (c) The errors on the cumulative test set meet the A2 targets:
  - energy < 3 meV/atom;
  - force RMSE < 0.15 eV/Å at ≤ 0.7 $T_m$, relative force error < 10 % at 0.95 $T_m$;
  - stress < 1.5 GPa;

  and they no longer drop from one iteration to the next.

**Final check on production cells.**
- Run 100 ps at 0.95 $T_m$ on H0–H4 (4096–8192 atoms: H1 aged vacancies, H2 twin, H3 Σ7, H4 polycrystal) and in the sheared B1 runs.
- Local environments from these are cut into ≤ 128-atom periodic cells (A1b, now with DeePMD instead of the VASP MLFF), FPS-sampled, then DFT-tested and added by Eq. (7) as above.
- Then the A3 validation and the go/no-go.

**Tools (written and tested 11-21; procedure in `ML/DP/README.md`):**
- `fe_dp_explore.py`: LAMMPS data files and inputs per system and state, plus the GPU array job and the iteration's train job (P100: ≈ 500 steps/s at 52–100 atoms, ≈ 40 s per 20 ps run).
- `fe_dp_sample.py`: SOAP + FPS on the dumps, and staging of the DFT dirs.
- `fe_dp_split.py`: Eq. (7) from `dp test` output (as `analysis.py`), writing the train ids and the test set.
- `fe_dp_collect.py` and `fe_r1d_job.sh` are reused as they are.

## 4. Phase B: Q from oscillatory NEMD

**Protocol.** As for MgO (M §2):
- γ₀ = ε₀ = 0.01; lag correction (M-Eq. 6); lock-in with block errors and harmonic ratios.
- Shear thermostat τ_T = 0.1 ps with nvt/sllod; the uniaxial τ_T rule (M-Eq. 11) re-derived from $K_S-K_T$ of the FF.
- Finite-size resonance $f_1\approx v_s/L$ (M-Eq. 13). For $v_s$ ≈ 3.6 km/s and L ≈ 30 Å this is ≈ 1.2 THz, the same as in MgO. The 5 THz points are therefore inertial in every Fe cell of this size, and Q is taken at 0.2–1 THz, with 20–50 GHz points for defect and boundary cells.

| step | cells and states | runs per state | steps per state | cost |
|---|---|---|---|---|
| B1 | **H0 perfect** at the 5 primary T, plus 360 GPa at 0.80 and 0.95 $T_m$ | GK 0.5 ns NVE; xz, xy, uniaxial x and uniaxial z at 1 and 0.2 THz (100 and 200 ps) | 1.75 M | 7 × 37 ≈ 260 node-h |
| B2 | **H4 melt-grown polycrystal**: crystallization ladder, then 0.90 and 0.98 $T_m$ | GK; xz and uniaxial x at 1 and 0.2 THz; xz at 50 and 20 GHz with γ₀ = 0.01 and 0.03 (linearity, requirement 9) | 2.9 M (8192 atoms, so 2× per step) | ≈ 20 + 2 × 125 ≈ 270 node-h |
| B3 | **H1 vacancies** at 0.95 $T_m$ | as B2; check PE stationarity and cluster formation (`b1_vacancy_clusters.py`, generalized to hcp) | 2.9 M | ≈ 62 node-h |
| B4 | **H2 twin and H3 Σ7 bicrystals** at 0.95 $T_m$ | as B2, with xz (the sliding direction) and the equilibrium sliding analysis of the GK run (β, summary Eq. 12) and boundary-resolved δD_gb | 2.9 M each | ≈ 2 × 70 ≈ 140 node-h |
| B5 | (optional) H6 bcc at 0.95 $T_m$, if it is stable in the FF | as B1 | 1.75 M (8192 atoms) | ≈ 75 node-h |

The steps-to-cost conversion assumes 4096 atoms at ≈ 13 steps/s per 64-core icelake node, scaled linearly from the measured 6.47 steps/s at 8192 atoms; scan 7166452 will replace it.

**Questions this answers:**
- How Q depends on T/T_m, on channel ($C_{44}$ against $C_{66}$) and on defect type, at the same T. This is the direct counterpart of summary Table 3.1 and the §5i comparison.
- **Premelting.** Does $C_{44}$ (or $G_V$) soften strongly above 0.95 $T_m$, as reported from ab initio MD (Martorell et al. 2013 (†))? Here it is tested with 4096-atom cells and measured loss, not only the static modulus.
- The low-frequency onset in the boundary and vacancy cells (as for the MgO bicrystal at 20–50 GHz and the γ₀ = 0.03 stick–slip).
- The Kramers–Kronig check of every crystal sweep, and the internal-strain resonance in the basal channels.
- **Comparison with MgO and MgSiO₃** at matched T/T_m (the melting points of the MgO and Deng models at the sweep pressures still have to be pinned down for this).

## 5. Phase C: effective viscosity from mechanisms

| step | what | method (existing tool) | cost |
|---|---|---|---|
| C1 | **Vacancy formation free energy** ΔG_f(P, T) in hcp at 330 and 360 GPa and 3 T | Frenkel–Ladd (`fix ti/spring`), forward/backward, 6 replicas, 576-atom cells, as plan FE_DISLOCATIONS Eqs. 1–3 (single species, so no chemical-potential term); ⟨E⟩(T) ladder where hops break the tether (Eq. 5 there) | ≈ 30 node-h |
| C2 | **Vacancy migration** (basal and non-basal jumps; hcp has two) | static NEB (`bdg_vac_neb.py` adapted to ASE + the VASP FF through the LAMMPS calculator) and umbrella integration (A2 tool), checked against direct hop rates in the B3 run; ν* from the jump-projected VACF | ≈ 30 node-h |
| C3 | **D_Fe(P, T)** (basal and c-axis) and the fit of plan FE_DISLOCATIONS Eq. 10; η_NH and η_C (Eq. 4) with δD_gb from B4; Arrhenius against the direct MSD near $T_m$ | analysis | CPU |
| C4 | **Dislocations:** 0 K γ-surfaces (basal, prismatic, pyramidal) and Peierls stresses (minimizations); then drag B(T) for the softest system, edge and screw, at 0.80 and 0.95 $T_m$, 4 stresses (0.1–1 GPa), 100 ps each | rigid-block drive (`disl_drive.lammps`, `disl_velocity.py`); D1-style analysis (summary §5k, §5m) | ≈ 10 + 16 × 6.5 ≈ 115 node-h |
| C5 | **Grain-scale model:** $Q^{-1}(\omega; d, T)$ at 0.01–1 Hz from β (B4), δD_gb (B4), D_Fe (C3) and B (C4) | `gb_grain_model.py` (summary Eq. 13), Granato–Lücke string with B (plan FE_DISLOCATIONS Eq. 13) | CPU |

**Deliverables:**
1. η_eff(d, T/T_m) for the inner core from diffusion, dislocation and boundary routes, with the MD flow bound (M-Eq. 14) as a floor.
2. Q⁻¹ at 1 Hz against seismic inner-core Q (≈ 100–600 (†)) and its depth dependence through T/T_m.

**Comparison table** (†: to collect into `Papers/` and check before any number is quoted):
- Inner-core viscosity: Van Orman 2004 (diffusion and Harper–Dorn creep); Gleason & Mao 2013 (strength); Reaman et al. 2011; Ritterbex & Tsuchiya 2020 (DFT); Belonoshko et al. 2019 (bcc, low η).
- Anelasticity of Fe: Jackson, Fitz Gerald & Kokkonen 2000 (forced torsional oscillation, low P).
- Elasticity and premelting: Steinle-Neumann et al. 2001; Vočadlo et al. 2009; Martorell et al. 2013.

## 6. Cost and order

| phase | content | node-h (64-core icelake) |
|---|---|---|
| A0 | DFT settings, $T_{el}$ test, timing (64-atom cells; 146 single points + 2 short MD) | ≈ 10–15 |
| A1 (+ A1b) | on-the-fly hcp and fcc training, 0–350 GPa, 300 K to $T_m$, ≤ 64 atoms | ≈ 50–250 (+ 20–50) |
| A2–A3 | refit, held-out DFT, validation MD ($T_m$, $C_{ij}$, liquid η, fcc–hcp, stacking faults) | ≈ 130 |
| B1–B4 | Q sweeps | ≈ 730 |
| C1–C4 | defects and dislocations | ≈ 175 |
| **total** | | **≈ 1110–1340 node-h** (70–85 k core-h); B5 adds ≈ 75 |

**A reduced first pass of ≈ 520 node-h** answers the main question (Q against T/T_m, and the diffusion-creep viscosity):
- A0–A3 at the low end;
- B1 at 3 T (0.80, 0.95, 0.98 $T_m$);
- B2 at 0.95 $T_m$;
- C1–C3.

Dislocations, boundaries and 360 GPa follow once those results are in.

**Order:**
1. A0 now (small: a 64-atom DFT test array). This gives the A1 cost and decides the $T_{el}$ question.
2. A1 → A2 → A3, then **go/no-go with RC**.
3. B1 and C1–C2 in parallel.
4. Then B2–B4 and C4, guided by what B1 shows.

**Cheaper production route (to decide at the A3 gate; argued here because it changes the cost of B and C by about 4×).** The A1 DFT labels (with the existing ML_AB) can also train a DeePMD model with fparam $=k_BT$, as Deng did for MgSiO₃:
- The fparam input also solves the electronic-temperature problem (§0 item 2).
- The model runs on P100s, the hardware the requirements prefer.
- The expected speed is 20–25 steps/s at 4096 atoms, as for MgO; it is to be measured.
- Training costs ≈ 1 P100-day.
- Both models would be validated against the same held-out DFT (A2), and the cheaper one used for B and C if it passes.

## 7. New tools needed

- `build_hcp_cells.py`: orthohexagonal perfect cell, vacancies, {10$\bar1$2} twin and [0001] tilt bicrystals with the normal along z; overlap cutoff scaled with a.
- `anelastic_sweep.lammps` and `gk_stress.lammps`:
  - a `PAIR` variable for `pair_style vasp` (they hard-wire `pair_style deepmd`);
  - `MODE shear_xy` and `MODE uniaxial_z`.
- A CPU array job script: icelake constraint (libvaspml is icelake-only), 32 × 2 or the layout chosen from scan 7166452, and the `LD_LIBRARY_PATH` fix (`build_cpu` first; restart 11-17 §7 and `tools/vasp_lammps/README.md`).
- The `anelastic_collect.py` case file `anelastic_cases_Fe_P330.py`, with the hexagonal channels and Eqs. 2–3.
- `build_hcp_dislocation.py`, and the hcp generalization of `b1_vacancy_clusters.py`.
- `fe_dp_explore.py`, `fe_dp_sample.py`, `fe_dp_split.py`: the DeePMD MD → FPS → DFT test → retrain loop (§3.2).

## 8. Decisions for RC

1. **Phase.** hcp as the target, with fcc in training (needed for stacking faults and boundaries, Table 0). Also bcc (B5, and bcc kept in training)? Also fcc as a production phase? *Decided 11-18: training hcp + fcc, 0–350 GPa, 300 K to melting, ≤ 64-atom cells, non-magnetic.*
2. **Electronic temperature.** If A0(c) shows a sensitivity: one FF per temperature band, or the DeePMD fparam route?
3. **Budget.** The full plan (≈ 1110–1340 node-h) or the reduced first pass (≈ 520)?
4. **Pressure.** 330 GPa primary with 360 GPa secondary, or the other way round?
5. **Light elements** (Si, S, O, C, H; superionic alloys, He et al. 2022 (†)) are out of scope for pure Fe. Should they be a later phase?
