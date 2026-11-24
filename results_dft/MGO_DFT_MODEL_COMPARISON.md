# MgO models against DFT and experiment: MgO-only DeePMD, Deng DeePMD, and VIB (Ita & Cohen 1997)

*2026-10-14. DFT runs: `/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck` (jobs 4480280 snapshots, 4487158 VASP; README there).
TI runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A0_MgO_Deng` (job 4452757). Figure: `mgo_dft_model_comparison.pdf/png` (this directory).*

## 1. Question

RC (10-13): "The Ita and Cohen was also a model—not full DFT. Even the equation of state (so V at PT) may be different. We should do a DFT spot check."

There are three MgO models in this project:

| model | what it is | used for |
|---|---|---|
| **MgO-only DeePMD** (`graph_c.pb`, md5 6357206b; type map Mg O, no fparam, se_e2_a, r_c = 7 Å) | Trained on 2157 systems, mostly high-T melt and coexistence runs (0–200 GPa, 5000–11000 K; dpgen iterations "highTemp_Melt_Mar2023", "struc_coex", "higher_encut") | All V6.6868 and V9.6397 MgO anelasticity, vacancy, grain-boundary and edge-dislocation runs |
| **Deng DeePMD** (`graph_c.pb`, md5 0e06a7e2; Mg Si O, fparam = k_B T) | X. Deng's MgSiO₃ model, which includes MgO crystal and melt at 20–160 GPa; VASP PBEsol, 800 eV, SIGMA = k_B T | MgSiO₃ runs; A0 free-energy (TI) test for MgO |
| **VIB** (Ita & Cohen, PRL 79, 3198, 1997) | Non-self-consistent Gordon–Kim ionic model built from LDA ion densities (Watson-sphere O²⁻), pair short-range terms, Thomas–Fermi overlap kinetic energy | The literature MgO vacancy formation and migration free energies (used by Cordier et al. 2023) |

The MgO-only model's DFT settings (functional, cutoff, POTCARs) are not stored in the graph. Only the training-set names are; RC to confirm them. The results below suggest PBE (§3); **confirmed by PBE single points in §8.**

## 2. Method

**Snapshots** (`tools/dft_snapshots.lammps`):
- Deng-model NVT MD of the A0 TI cells:
  - perfect cell: 4×4×4 B1, 512 atoms;
  - bound V_Mg + V_O pair: 510 atoms;
  - volumes are the NPT means at 20 GPa / 2000 K and 140 GPa / 3000 K.
- 8 frames per cell, 2 ps apart.

**DFT single points** (`tools/dft_snapshots_poscar.py`, `tools/vasp_array.sh`):
- VASP 6.6.0 with Deng's training settings: PBEsol, ENCUT 800 eV, Γ only, SIGMA = k_B T (Fermi smearing).
- Mermin free energy TOTEN, stress and forces.

**Models on the same frames:**
- Deng model: from the MD itself.
- MgO-only model: re-evaluated on the identical POSCARs (`tools/dp_rescore.py`).
- Re-evaluating with the Deng model reproduces the LAMMPS energy to 10⁻⁶ eV and the pressure to 0.01 bar.

**Comparison** (`tools/dft_compare.py [--tag mgo]`):
- Pressure difference at fixed volume and configuration: $\Delta P = P_{DFT}-P_{model}$, static (virial) part only.
- Force RMSE.
- Model error of the formation free energy, as a free-energy perturbation from the model to the DFT surface:

$$\Delta E = E_{DFT}-E_{model},\qquad dF_X=\langle\Delta E\rangle_X-\frac{\operatorname{var}(\Delta E)_X}{2k_BT} \tag{1}$$

$$\delta\Delta G_f=\Delta G_f^{DFT}-\Delta G_f^{model}=dF_D-\frac{N-L}{N}\,dF_I \qquad (L=2) \tag{2}$$

- A constant energy offset per atom (different POTCAR reference energies) cancels exactly in Eq. 2 for a stoichiometric (Schottky) defect.
- For the MgO-only model the frames are sampled from the Deng model, not from its own ensemble. Its Eq. 2 value is therefore a fixed-configuration comparison, and it ignores the volume change the model's different EOS would cause (§3).

**Experimental EOS:** Tange et al. 2009 (JGR 114, B03208), Vinet + Mie–Grüneisen–Debye, with
- V₀ = 74.698 Å³ (4 f.u.), K₀ = 160.63 GPa, K₀′ = 4.367;
- θ₀ = 761 K, γ₀ = 1.442, a = 0.138, b = 5.4.

*These parameters were quoted from memory; check them against the paper.*

$$P(V,T)=P_{Vinet}(V)+\frac{\gamma(V)}{V}\left[E_{th}(V,T)-E_{th}(V,300\,\mathrm K)\right] \tag{3}$$

## 3. Equation of state

**At fixed volume and configuration** (static pressure; mean over 8 frames, standard errors ≤ 0.02 GPa):

| state | cell | ΔP = P_DFT − P_Deng (GPa) | ΔP = P_DFT − P_MgO-only (GPa) |
|---|---|---|---|
| 20 GPa, 2000 K | perfect | +0.01 | −4.90 |
| | bound pair | +0.07 | −4.85 |
| 140 GPa, 3000 K | perfect | +0.21 | −9.22 |
| | bound pair | +0.27 | −9.13 |

The Deng model reproduces PBEsol essentially exactly. The MgO-only model gives a pressure 5 GPa (20 GPa) to 9 GPa (140 GPa) higher than PBEsol at the same volume. The difference grows with compression, so this is a different energy–volume curve, i.e. a different functional, not a fitting error.

The energy offset per atom also varies with volume (DFT − MgO-only = −330 meV/atom at 20 GPa, −420 meV/atom at 140 GPa); a pure reference-energy shift would be constant. A higher pressure than PBEsol at the same volume (an underbinding functional) is the behaviour expected of PBE.

**Against experiment** (Eq. 3; each model at its own a(P, T)):

| state | Tange a (Å) | VIB a (Å) | Deng ≈ PBEsol a (Å) | MgO-only a (Å) |
|---|---|---|---|---|
| 20 GPa, 2000 K | 4.1381 | 4.1312 | 4.1540 | – |
| 140 GPa, 3000 K | 3.7414 | 3.7210 | 3.7443 | – |
| 175 GPa, 3500 K | 3.6814 | – | – | 3.7044 (edge run NPT) |

| state | P_model − P_Tange, VIB | Deng ≈ PBEsol | MgO-only |
|---|---|---|---|
| 20 GPa, 2000 K | −1.0 GPa | +2.3 GPa | +7.2 GPa |
| 140 GPa, 3000 K | −9.9 GPa | +1.4 GPa | +10.6 GPa |
| 175 GPa, 3500 K | – | – | +12.5 GPa |

The MgO-only values at 20 and 140 GPa are the Deng NPT pressure plus the fixed-volume ΔP above. At 175 GPa the value comes from the MgO-only NPT lattice of the edge-dislocation run.

![model comparison](mgo_dft_model_comparison.png)

*(a) Pressure error of each model against the experimental EOS. (b) Bound-pair formation free energy. The DFT-corrected error bar spans TOTEN/40 ps to E0/20 ps switching (§4).*

- **PBEsol (Deng)** is the most accurate: within 2.3 GPa (0.4 % in a).
- **VIB** is good at 20 GPa but about 10 GPa too soft at 140 GPa (0.55 % too small in a).
- **MgO-only** overestimates pressure by 7–13 GPa (0.6 % too large in a), increasing with pressure.
- VIB and MgO-only bracket experiment with errors of similar size and opposite sign.

## 4. Point defects (bound V_Mg + V_O pair)

**Fixed-configuration accuracy:**

| state | cell | force RMSE, Deng (eV/Å) | force RMSE, MgO-only (eV/Å) | sd(ΔE), Deng (eV) | sd(ΔE), MgO-only (eV) |
|---|---|---|---|---|---|
| 20 GPa, 2000 K | perfect | 0.073 | 0.055 | 0.14 | 0.16 |
| | bound | 0.082 | 0.067 | 0.16 | 0.17 |
| 140 GPa, 3000 K | perfect | 0.066 | 0.054 | 0.15 | 0.18 |
| | bound | 0.073 | 0.074 | 0.19 | 0.14 |

RMS force is 1.6 eV/Å at 20 GPa and 3.0 eV/Å at 140 GPa. Even against PBEsol, the MgO-only model's forces are as good as or better than the Deng model's, about 2–4 % of the RMS force. Neither model was trained on vacancies, and both are slightly worse in the defect cell.

**Formation free-energy error** (Eq. 2; TOTEN, i.e. including the vacancies' electronic entropy):

| state | δΔG_f, DFT − Deng (eV) | δΔG_f, DFT − MgO-only (eV) | MgO-only − Deng (eV) |
|---|---|---|---|
| 20 GPa, 2000 K | +0.95 ± 0.08 | +0.72 ± 0.08 | +0.22 |
| 140 GPa, 3000 K | +1.27 ± 0.09 | +0.96 ± 0.08 | +0.31 |

- Both models put the bound pair too low, by about 1 eV against PBEsol. The MgO-only model is about 0.2–0.3 eV closer.
- Part of the MgO-only error may be PBE against PBEsol rather than model error. A PBE re-run of a few frames would separate the two, once the training settings are known.
- With E0 (no electronic entropy) instead of TOTEN, every δΔG_f in the two DFT columns rises by the same amount: +0.19 eV at 20 GPa and +0.83 eV at 140 GPa.
  - The electronic entropy of the vacancy in-gap states is T·S_el = 0.17 and 0.80 eV.
  - PBEsol's gap is too small (about 4.5–5 eV against 7.8 eV measured), so this is an upper bound.

**Against VIB** (bound-pair ΔG_f, eV):

| state | Deng TI | DFT-corrected (TOTEN) | DFT-corrected (E0) | VIB (Ita & Cohen) | VIB − DFT |
|---|---|---|---|---|---|
| 20 GPa, 2000 K | 5.15 ± 0.21 | 6.10 ± 0.23 | 6.29 | 7.51 ± 0.25 | +1.2 to +1.4 |
| 140 GPa, 3000 K | 11.90 ± 0.24 (TS 40), 12.68 ± 0.30 (TS 20) | 13.17 – 13.95 | 14.00 – 14.78 | 15.79 ± 0.69 | +1.0 to +2.6 |

(VIB values converted from Table I: 12.04 and 25.29 × 10⁻¹⁹ J.)

- VIB is 1.0–2.6 eV (6–19 %) above DFT. The difference is significant at 20 GPa (3.5–4σ, combined errors) and 1.4–3.5σ at 140 GPa.
- **Not the EOS:** VIB's denser lattice changes $P\,v_f$ by ≤ 0.1 eV.
- **Probable causes:**
  1. VIB's rigid, spherical, non-self-consistent ions cannot relax charge around the vacancies or form in-gap states, which makes the defect too expensive.
  2. The TI formation-volume term is not converged: TS 20 against 40 differ by 0.8 eV at 140 GPa.
  3. LDA against PBEsol.

## 5. Implications for earlier results

1. **MgO-only pressures are high by about 7–13 GPa** relative to experiment (about 5–9 GPa relative to PBEsol), increasing with pressure. For every MgO-only run labelled by pressure, the experimental-scale pressure is lower:
   - "≈ 175–193 GPa" for V6.6868 becomes ≈ 162–180 GPa (offset extrapolated as +12 to +13 GPa);
   - "≈ 18–50 GPa" for V9.6397 becomes about 7–8 GPa lower;
   - the 175 GPa / 3500 K edge-dislocation run is at ≈ 162 GPa, still inside Perez et al.'s 175 ± 15 GPa.

   Volumes (V6.6868, V9.6397) are unaffected; only the pressure labels change.
2. **MgO against MgSiO₃ at V = 6.5669 (§5i of the summary):** MgSiO₃ uses the Deng (PBEsol) model, MgO the MgO-only model. Comparisons at equal volume are unaffected, but quoted pressures carry a 5–9 GPa model-dependent offset between the minerals.
3. **Vacancy energetics from the MgO-only model** (§5a–5c of the summary: jump rates, NEB barriers, elastic dipoles) come from a model that underbinds the bound pair by about 0.7–1 eV at fixed volume. Migration barriers were not tested here (next step 3).
4. **Ita & Cohen (and Cordier et al. 2023, who use their D_O fit):**
   - the VIB EOS is accurate to about 1 GPa at 20 GPa but about 10 GPa too soft at 140 GPa;
   - VIB formation free energies are 1–2.6 eV above PBEsol.
   - Taken alone, a lower ΔG_f means more vacancies and faster intrinsic diffusion than the VIB fit predicts. The migration free energies must be checked before drawing a conclusion for D_O.

## 6. Next steps

1. ~~RC to confirm the MgO-only model's DFT settings; PBE re-run.~~ **Done 2026-11-15 (§8): the model is PBE-trained; its ΔG_f error against PBE is 0.5–0.9 eV, and PBEsol − PBE is only 0.05–0.16 eV.**
2. Part 2 (static): relaxed ΔH_f of bound and separated pairs in 64- and 216-atom cells at 0, 20 and 140 GPa. Compare DFT, both DeePMD models and Karki & Khanduja 2006 (†).
3. Snapshot check of the migration saddle (the NEB images of §5b) for both models.
4. Decide between per-state snapshot corrections and retraining with vacancy frames. The roughly 1 eV error is similar in both models and varies by only about 0.3 eV between states, so per-state correction is adequate for now.
5. Recompute the MgO-only offset at the V6.6868 and V9.6397 crystal states directly (a few frames each) and correct the pressure labels in the summary.

## 7. Reproduce

```
D=/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck; cd $D
# Deng-model comparison (DeePMD values written by the snapshot MD)
python ~/Claude/tools/dft_compare.py --gf P20_T2000_perfect P20_T2000_bound --L 2 --temp 2000
python ~/Claude/tools/dft_compare.py --gf P140_T3000_perfect P140_T3000_bound --L 2 --temp 3000
# MgO-only model: re-score the same POSCARs (deepmd_py311 env, CPU), then compare
python ~/Claude/tools/dp_rescore.py md/graph_c_MgOonly.pb mgo P20_T2000_perfect P20_T2000_bound P140_T3000_perfect P140_T3000_bound
python ~/Claude/tools/dft_compare.py --tag mgo --gf P20_T2000_perfect P20_T2000_bound --L 2 --temp 2000
python ~/Claude/tools/dft_compare.py --tag mgo --gf P140_T3000_perfect P140_T3000_bound --L 2 --temp 3000
python ~/Claude/tools/plot_dft_model_comparison.py ~/Claude/Anelasticity/results_dft
```

## 8. PBE check: the MgO-only model was trained with PBE (2026-11-15)

*Job 4520046 (32 single points, finished 10-16): the same 32 frames as §2, with `GGA = PE` and otherwise identical settings. Record: `/resnick/groups/carnegie_poc/rcohen/VASP/MgO_vacancy_DFTcheck/PBE/README.md`; per-state output `PBE/<state>/dft_compare{,_mgo}.txt`.*

**Fixed-configuration comparison** (mean over 8 frames; standard errors ≤ 0.02 GPa and ≤ 0.13 meV/atom):

| state | cell | MgO-only − PBE: ΔE/N (meV/atom) | P_PBE − P_MgO-only (GPa) | force RMSE vs PBE (eV/Å) | P_PBEsol − P_MgO-only (GPa, §3) | P_PBE − P_Deng (GPa) |
|---|---|---|---|---|---|---|
| 20 GPa, 2000 K | perfect | +12.4 | −0.31 | 0.050 | −4.90 | +4.61 |
| | bound | +11.3 | −0.27 | 0.062 | −4.85 | +4.65 |
| 140 GPa, 3000 K | perfect | +10.8 | −1.07 | 0.050 | −9.22 | +8.36 |
| | bound | +9.2 | −1.00 | 0.069 | −9.13 | +8.40 |

- **The MgO-only model reproduces PBE:** its pressure is within 0.3 GPa (20 GPa) and 1.0 GPa (140 GPa) of PBE at the same configuration, against 5–9 GPa from PBEsol. Its energy offset from PBE is almost constant (12.4 → 10.8 meV/atom between the two volumes, a reference-energy shift), against 330 → 420 meV/atom from PBEsol. Its forces match PBE better (0.050–0.069 eV/Å) than PBEsol (0.054–0.074 eV/Å).
- **Conclusion: the MgO-only model (md5 6357206b) is PBE-trained.** Its 7–13 GPa pressure excess over experiment (§3) is the usual PBE underbinding, not a fitting error.
- The Deng model reproduces PBEsol (§3), so between the two models the difference is the functional (PBE − PBEsol ≈ 4.6 GPa at 20 GPa and 8.4 GPa at 140 GPa at fixed V).

**Bound-pair formation free energy** (Eq. 4 of `dft_compare.py`, TOTEN; first order ± error, then second-order cumulant):

| state | PBE − MgO-only (eV) | PBE − Deng (eV) | PBEsol − MgO-only (eV, §4) | PBEsol − Deng (eV, §4) |
|---|---|---|---|---|
| 20 GPa, 2000 K | +0.56 ± 0.06 (0.50) | +0.79 ± 0.10 (0.79) | +0.72 ± 0.08 | +0.95 ± 0.08 |
| 140 GPa, 3000 K | +0.86 ± 0.08 (0.87) | +1.22 ± 0.10 (1.21) | +0.96 ± 0.08 | +1.27 ± 0.09 |

- **The functional matters little for ΔG_f:** PBEsol − PBE = +0.16 eV (20 GPa) and +0.05 to +0.10 eV (140 GPa), from either model.
- **The model error dominates:** against its own functional (PBE), the MgO-only model underbinds the bound pair by 0.5–0.9 eV. This is a true fitting error (no vacancy frames in training), not PBE against PBEsol. It answers §6 item 1.
- Consequence for the MgO-only vacancy work (summary §5a–5c): the pair binding and formation energies there are 0.5–0.9 eV too low against PBE. Migration barriers are still untested (§6 item 3).
