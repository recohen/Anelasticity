# Bridgmanite vacancy formation and migration free energies, Deng model (A3, analysed 2026-11-16)

Runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A3_Bdg_Deng` (README there; jobs 6957232 perfect, 6957233 defects, 6957324 migration, 6957279/80 direct hops). Raw output: `A3_analysis.txt` in the run directory (copied here). Plan: `ANELASTICITY_PLAN_FE_DISLOCATIONS.md` §1–2. MgO counterpart: `MGO_VACANCY_FREE_ENERGIES.md`.

**Summary.**
- **The O vacancy in bridgmanite is very mobile.** Its migration barrier is 0.9–1.9 eV along the cheapest octahedron edge, over 30–120 GPa.
  - It hops 10¹⁰–10¹¹ times per second at the Cordier states, about 10⁴ times faster than the O vacancy in periclase at the same (P, T).
  - Direct MD confirms the transition-state rates to within a factor of 2: κ = 0.6, Eq. 3.
- **That mobility spoils most of the Frenkel–Ladd formation runs.** The O vacancies hop during the λ ≈ 0 stage, and some already hopped during the averaging that defines the tether sites.
  - Only hop-free replicas are usable. They give provisional values at 60–120 GPa (Table 1) and almost nothing at 30 GPa.
  - The method has to change for cells containing V_O (§4).
- **Mg vacancies are slow:** ΔG_m = 4.7–6.0 eV at 60–120 GPa.
- **The Si migration runs failed.** The O vacancies in the Si cell hopped in most windows.

## 1. Formation (Frenkel–Ladd, defect cells at the perfect cell's box)

$$\Delta G=G_D-G_I+\mu,\qquad \mu_{MgO}=g_{per},\ \ \mu_{SiO_2}=g_{Bdm}-g_{per},\ \ \mu_{full}=g_{Bdm} \tag{1}$$

$$\Delta G(\text{full})=\Delta G(\text{MgO})+\Delta G(\text{SiO}_2)\quad\text{(non-interacting separated defects)} \tag{2}$$

(Eqs. 1–3c of `tools/bdg_schottky_analyze.py`; periclase-saturated μ from the A1 perfect MgO at the same P, T.)

**Hops.**
- In most defect cells, one or more replicas show a displacement of 2.0–2.8 Å from a tether site. That is one O jump (2.3–2.5 Å).
- The timeline of P30_T2000_mgo_sep shows when it happens: the O vacancy hops during the 10 ps equilibration at λ = 0. The spring then pulls the atom back at λ ≈ 0.05–0.1, and that pull-back is irreversible work.
  - The per-replica dissipation becomes 1–7 eV, against 0.05–0.3 eV in the perfect cells.
  - The forward/backward estimate is then biased by up to about half of that.
- **The tether sites are also affected.** I compared `sites.data` with the ideal lattice by assigning each tether site to the nearest lattice site.
  - In 8 of the 18 defect cells, one O tether sits 0.9–1.2 Å off a lattice site, because a hop happened during the averaging.
  - At 30 GPa the defects rearranged before switching started:
    - the "bound" V_Mg + V_O pair had dissociated (V_O 13 Å away);
    - in the SiO₂ cell both V_O moved next to V_Si (1.7–1.8 Å), forming a V_Si + 2 V_O cluster;
    - in the full-Schottky cell a Mg left its site (2.8 Å).
- New option: `bdg_schottky_analyze.py --maxdr 1.5` (and `ti_einstein_analyze.py --maxdr`) keeps only the replicas whose maximum displacement stayed below 1.5 Å.

**Table 1.** ΔG (eV), hop-free replicas only (`--maxdr 1.5`; number kept of 6 in brackets). "All" gives the 6-replica value. Errors are statistical only.

| P, T | MgO partial, bound | MgO partial, separated | SiO₂ partial, separated | full Schottky | Eq. 2 check |
|---|---|---|---|---|---|
| 30 GPa, 2000 K | – (0; all 4.36 ± 0.93, pair dissociated) | – (0; all 4.29 ± 0.40) | 7.91 ± 0.20 (2) **= bound V_Si + 2 V_O cluster** | – (0) | – |
| 60 GPa, 2300 K | 6.63 ± 0.19 (2) | 8.52 ± 0.19 (3); 2000 atoms: 8.92 ± 0.22 (4) | 15.76 ± 0.5 (1) | – (0; all 19.1 ± 1.3) | all replicas: 19.1 vs 23.4 ± 1.4 (fails, 2.3σ) |
| 90 GPa, 2500 K | 9.63 ± 0.33 (4) | 10.58 ± 0.24 (5) | 19.87 ± 0.19 (3) | 30.24 ± 0.5 (1) | 30.24 vs 30.45 ± 0.62 (passes) |
| 120 GPa, 2800 K | 10.98 ± 0.29 (5) | 11.78 ± 0.24 (4) | 22.42 ± 0.25 (2) | – (0; all 31.3 ± 1.2) | – |

- **Provisional.** Even the hop-free replicas scatter by ±0.5 eV per replica, against ±0.2 eV in the perfect cells. Some of them use tether sites that were affected by earlier hops. I put a systematic uncertainty of about ±0.5 eV on these values.
- **V_Mg–V_O binding** (separated − bound): 1.9 (60 GPa), 0.9 (90 GPa), 0.8 eV (120 GPa).
  - The 30 GPa bound pair dissociated by itself within the first 50 ps, so the binding there is weak or the pair escaped thermally (V_O makes ≈ 10 hops per 20 ps at 30/2000; rates in §2).
  - V_O binds strongly to V_Si at 30 GPa: the cluster value of 7.9 eV is about half of the separated value at 60 GPa.
- **Against periclase** (A1, separated pair at the same P, T): 10.01 / 12.13 / 13.61 eV at 60 / 90 / 120 GPa. Removing MgO from bridgmanite costs 1.5–1.8 eV less, under the short-range model and without a DFT check.
- **Size check:** MgO partial (separated) at 60/2300 is 8.92 ± 0.22 eV in 2000 atoms and 8.52 ± 0.19 eV in 960 atoms, which agree within 1.4σ.

## 2. Migration (umbrella integration, independent windows, full paths 0 → l)

$$\Delta G_m=G(s^*)-\min_{s<s^*}G,\qquad \Gamma=\nu^*e^{-\Delta G_m/k_BT}\ \ \text{(one jump path)} \tag{3}$$

Figure `bdg_migration.{pdf,png}` (tool `tools/bdg_mig_plot.py`): G(s) for the O1e, O2e, O2x and Mg paths at every state. Windows with another atom displaced by more than 1.4 Å are skipped (`vac_mig_analyze.py`). The table gives ΔG_m in eV, with the number of usable windows out of 41 (61 for Si) in brackets.

| state | O1e: O1 → V(O2), edge, l 2.3 Å | O2e: O2 → V(O2), edge | O2x: O2 → V(O2), open path, l 2.5 Å | Mg | Si |
|---|---|---|---|---|---|
| 30 GPa, 2000 K | 0.87 (27) | 0.93 (31) | 2.58 (24) | (2.90, 7 windows: unusable) | none usable |
| 60 GPa, 2300 K | 1.26 (38) | 1.52 (36) | 2.84 (34) | 4.65 (23; 6 windows missing at the saddle) | 4.6 (8, up to s = 1.1 Å only: unusable) |
| 90 GPa, 2500 K | 1.61 (39) | 1.74 (38) | 2.87 (37) | 5.46 (33) | 7.6 (12: unusable) |
| 120 GPa, 2800 K | 1.92 (36) | 1.99 (38) | 2.92 (38) | 6.04 (33) | 8.8 (12; G(end) − G(0) = 3.4 eV: unusable) |
| V6.5669, 3021 K | 1.70 (34) | 2.02 (34) | 2.84 (35) | 5.49 (19) | – |

- ν* = 7–17 THz. The statistical errors are 0.01–0.02 eV.
- **O1 versus O2 vacancy sites:** G(end) − G(start) of the O1e path gives G(V on O1) − G(V on O2) = 0.00–0.07 eV, so the two sites are nearly degenerate.
  - The O2e path joins equivalent sites, so its value of −0.01 to −0.22 eV should be zero. That sets the accuracy of the end-point differences at about 0.1–0.2 eV.
- **Mg and Si runs:** the cells held the other vacancies too (V_O in the Mg cell; 2 V_O in the Si cell), and their hops removed the windows. Mg at 90 and 120 GPa is usable; the 60 GPa value interpolates across the saddle. **Si needs cells without V_O.**

**Per-vacancy O hop rate from TST**, using the neighbour shells of the cell's jump list:
- A vacancy on O2 can be filled by 4 O1 edge jumps, 4 O2 edge jumps and 2 O2x jumps.
- A vacancy on O1 can be filled by 8 O2 edge jumps.
- The sites are occupied in the ratio 4 O1 : 8 O2, weighted by e^{−ΔG_site/k_BT}.

$$\langle\Gamma_v\rangle=p_1\,8\Gamma_{O1e}e^{\Delta G_{12}/k_BT}+(1-p_1)\left(4\Gamma_{O1e}+4\Gamma_{O2e}+2\Gamma_{O2x}\right) \tag{4}$$

| state | ⟨Γ_v⟩ TST (s⁻¹) | direct MD (s⁻¹) | κ = MD/TST | vacancy D_v ≈ Γ l²/6 (m²/s) | periclase V_O, 12 Γ (A2) (s⁻¹) |
|---|---|---|---|---|---|
| 30 / 2000 | 4.6×10¹¹ | – | – | 4×10⁻⁹ | 2.7×10⁷ |
| 60 / 2300 | 1.3×10¹¹ | – | – | 1×10⁻⁹ | 9×10⁶ |
| 90 / 2500 | 4.2×10¹⁰ | – | – | 4×10⁻¹⁰ | 3×10⁶ |
| 120 / 2800 | 3.1×10¹⁰ | 1.7×10¹⁰ (5 hops, 300 ps) | 0.54 ± 0.24 | 3×10⁻¹⁰ | 3.6×10⁶ |
| V6.5669 / 3021 | 9.6×10¹⁰ | 6.0×10¹⁰ (12 hops, 200 ps) | 0.63 ± 0.18 | 9×10⁻¹⁰ | – |

- **TST checks out:** κ ≈ 0.6, the same at both states. The predicted share of O2 → O2 hops (15 %) matches what MD sees (2 of 12, 17 %).
- **At 4020 K** (V6.5669) the direct rate is 3.1×10¹¹ s⁻¹. The 3021 K barriers predict 4.9×10¹¹ s⁻¹ (κ = 0.64) if ΔG_m does not depend on T.
- **Bridgmanite against periclase:** O vacancies hop about 10⁴ times faster in bridgmanite at the same (P, T); compare the barriers 0.9–1.9 eV here with 2.7–4.3 eV in periclase. V_Mg is the opposite (4.7–6.0 eV here against 2.4–3.7 eV in periclase).

## 3. What holds and what does not
- **Holds:**
  - the O-vacancy barriers, the site energetics and the hop rates (validated against MD);
  - the Mg barriers at 90 and 120 GPa (a straight path, with transverse relaxation free);
  - the conclusion that V_O is fast and V_Mg slow, consistent with the 1268-atom MD (`results_Tdep/T_DEPENDENCE_RESULTS.md` §2.3).
- **Does not hold yet:**
  - every formation free energy of a cell containing V_O (Table 1 is provisional; nothing usable at 30 GPa);
  - all Si migration;
  - Mg at 30 and 60 GPa.
- **So no bridgmanite D (plan Eq. 8) is given yet.** The O vacancy diffusivity D_v is known; the vacancy concentration is not.

## 4. Proposed fix (not submitted; for RC)
1. **Single-vacancy cells.** One cell each for V_Mg, V_Si, V_O(O1) and V_O(O2), at the 4 states. The DeePMD model carries no charge, so non-stoichiometric cells are allowed. This removes association (V_O–V_Si clusters, pair dissociation). The full Schottky energy and the partial energies then come from sums of the single-vacancy values plus μ; binding energies come separately.
2. **Formation of mobile vacancies by temperature integration.**
   - Frenkel–Ladd at a low T₀ (≈ 800–1000 K), where an O hop during a 100 ps replica is unlikely, at the target box and with fparam fixed at the target k_BT.
   - Then integrate ⟨E⟩ from NVT MD up to T:

$$\frac{F(V,T)}{T}=\frac{F(V,T_0)}{T_0}-\int_{T_0}^{T}\frac{\langle E\rangle_{V,T'}}{T'^2}\,dT' \tag{5}$$

   - ⟨E⟩ does not change when a vacancy hops between equivalent sites, so Eq. 5 is immune to hops.
   - The perfect cell is treated the same way, so systematic errors cancel.
3. **Mg and Si migration in single-vacancy cells** (no V_O to hop).
4. **Cost:** formation 20 cells × ≈ 2.3 h ≈ 46 P100-h; migration 8 tasks ≈ 15 P100-h; ≈ 60 P100-h in all.

## 5. A3b: the redo with single-vacancy cells (RC 2026-11-16 "Yes, run the A3 redo"; analysed 2026-11-17)
Runs: `/groups/carnegie_poc/rcohen/LAMMPS/FreeEnergy/A3b_Bdg_single` (README; jobs 7000466 Frenkel–Ladd, 7000467 ladders, 7000468 migration; all 32 COMPLETED). Raw output `A3b_analysis.txt` (here). Tool `tools/bdg_tint_analyze.py`.

**Method.**
- One vacancy per cell (V_Mg, V_Si, V_O on O2), each in the A3 perfect cell's mean box.
- V_Mg and V_Si: Frenkel–Ladd directly at T.
- Perfect and V_O2: Frenkel–Ladd at T₁ = 800 / 1200 / 1500 / 1800 K, with fparam fixed at k_B T, then a 7-point ladder of ⟨E⟩(T′) up to T:

$$\frac{F(T)}{T}=\frac{F(T_1)}{T_1}+\int_{1/T_1}^{1/T}\left(\langle U\rangle+\tfrac32Nk_BT'\right)d(1/T') \tag{5}$$

- Per-vacancy terms D_X = F_X − F_I − (P_X − P_I)²V_I/2K_T, both cells at V_I. They are combined with the periclase-saturated μ:

$$\Delta G_{MgO}=D_{Mg}+D_O+g_{per},\quad \Delta G_{SiO_2}=D_{Si}+2D_O+(g_{Bdm}-g_{per}),\quad \Delta G_{full}=D_{Mg}+D_{Si}+3D_O+g_{Bdm} \tag{6}$$

**No hops anywhere.** All 96 Frenkel–Ladd replicas are hop-free: max |dr| ≤ 0.65 Å at T₁ and ≤ 1.03 Å for V_Mg / V_Si at T. Dissipation is 0.05–0.46 eV. The single-vacancy D_X are large and of mixed sign (D_O ≈ −28.3, D_Mg ≈ +44, D_Si ≈ +91 eV) because of the model's per-species reference energies. Only the sums of Eq. 6 are physical.

**Check (Eq. 2 of the tool): the ladder F_I(T) of the perfect crystal against the direct Frenkel–Ladd F_I(T) of A3.** The ladder is lower by 0.83 / 0.77 / 0.46 / 0.37 eV at 30 / 60 / 90 / 120 GPa, i.e. 0.4–0.9 meV/atom. The statistical errors are 0.1–0.3 eV.
- *Correction (2026-11-17):* I first attributed 0.16–0.24 eV of this to a 3N vs 3N − 3 kinetic-energy convention. That is wrong. The Frenkel–Ladd F, with the centre-of-mass correction F_CM, has all 3N momenta and a free centre of mass, so its energy is ⟨U⟩ + (3N/2) k_BT, exactly as in Eq. 5. The whole offset is unexplained so far.
- It grows with the length of the ladder (T/T₁). The candidate is a switching bias of the direct Frenkel–Ladd at high T, the same size as the TS 20-vs-40 ps difference seen in A0. **Test submitted 2026-11-17:** direct Frenkel–Ladd with TS 80 ps for the 4 perfect cells and for V_Mg, V_Si at 30 GPa (job 7045833).
- It does not affect the formation energies. Each D_X is a difference taken within one route (V_O: ladder minus ladder; V_Mg, V_Si: direct minus direct), and the μ's enter per formula unit (≤ 0.005 eV).
- If TS 80 ps moves the direct F toward the ladder and D_Mg, D_Si stay put, the formation energies stand. If D_Mg, D_Si move too, V_Mg and V_Si need ladders.

**Table 2.** Separated-defect formation Gibbs energies, A3b (eV; Deng model, raw). The A3 hop-free values (Table 1) are in brackets.

| P, T | MgO partial (V_Mg + V_O) | SiO₂ partial (V_Si + 2 V_O) | full Schottky | per vacancy (full/5) |
|---|---|---|---|---|
| 30 GPa, 2000 K | 6.22 ± 0.32 | 12.32 ± 0.54 | 18.54 ± 0.81 | 3.71 |
| 60 GPa, 2300 K | 8.40 ± 0.37 [8.52 ± 0.19] | 16.15 ± 0.70 [15.76 ± 0.5] | 24.55 ± 1.04 | 4.91 |
| 90 GPa, 2500 K | 10.25 ± 0.33 [10.58 ± 0.24] | 19.53 ± 0.55 [19.87 ± 0.19] | 29.78 ± 0.81 [30.24 ± 0.5] | 5.96 |
| 120 GPa, 2800 K | 12.17 ± 0.32 [11.78 ± 0.24] | 22.64 ± 0.51 [22.42 ± 0.25] | 34.81 ± 0.75 | 6.96 |

- **A3b agrees with the hop-free A3 subset within 0.2–0.4 eV** at 60–120 GPa, and it now gives 30 GPa as well. The errors come mostly from the ladders (D_O ± 0.23–0.34 eV, which enters 3× in the full Schottky energy).
- **Against periclase** (A1, separated pair): 7.66 / 10.01 / 12.13 / 13.61 eV. The MgO partial Schottky in bridgmanite is 1.4–1.9 eV cheaper at every state.
- **The SiO₂ partial costs about twice the MgO partial** (12.3–22.6 eV).

**Migration in single-vacancy cells (7000468).**
- **V_Mg:** ΔG_m = 3.86 / 4.77 / 5.47 / 6.07 eV at 30 / 60 / 90 / 120 GPa. All 41 windows are usable at every state; ν* = 7.9–10.0 THz. The A3 values (5.46, 6.04 eV at 90, 120 GPa) are reproduced.
- **V_Si: still unresolved.** With no V_O present, the windows beyond s ≈ 1.2 Å (of l = 4.2–4.7 Å) are lost anyway, because other atoms (O) move 2–3 Å.
  - So the straight Si jump along a_o is not a single-atom hop. It drags the O neighbours along, i.e. it is a cooperative rearrangement.
  - The partial profiles give no barrier (4.3–9.7 eV, meaningless).
  - Si needs a path search: a 0 K NEB over the candidate paths, or high-T MD of the V_Si cell to see what actually happens. **Both submitted 2026-11-17** (RC: "Yes do a and b"): static NEB, new `tools/bdg_vac_neb.py`, smoke 7045831; V_Si MD at 30 GPa / 2600, 3000 K and 120 GPa / 3600, 4200 K, 500 ps each (job 7045834).

## 6. Intrinsic vacancy concentrations and diffusion in bridgmanite (Deng model, raw)
Mass action with formal-charge neutrality (2 c_Mg + 4 c_Si = 2 · 3 c_O per formula unit), periclase-saturated:

$$c_{Mg}c_O=e^{-\Delta G_{MgO}/k_BT},\qquad c_{Si}c_O^2=e^{-\Delta G_{SiO_2}/k_BT},\qquad c_{Mg}+2c_{Si}=3c_O \tag{7}$$

$$D_O=c_O\,\frac{\langle\Gamma_v\rangle l_O^2}{6},\qquad D_{Mg}=c_{Mg}\,\frac{Z_{Mg}\Gamma_{Mg}l_{Mg}^2}{6} \tag{8}$$

with ⟨Γ_v⟩ from Eq. 4 (l_O = 2.37 Å), Z_Mg ≈ 4 (the 4 of the 6 A-site neighbours with clearance ≥ 1.2 Å), and no correlation factor.

| P, T | c_O | c_Mg | c_Si | D_O bridgmanite (m²/s) | D_O periclase (A1/A2) | ratio | D_Mg bridgmanite (m²/s) |
|---|---|---|---|---|---|---|---|
| 30 / 2000 | 8×10⁻⁹ | 2.5×10⁻⁸ | 1×10⁻¹⁵ | 4×10⁻¹⁷ | 8.5×10⁻²³ | 4×10⁵ | 3×10⁻²⁴ |
| 60 / 2300 | 4×10⁻¹⁰ | 1.1×10⁻⁹ | 3×10⁻¹⁷ | 4×10⁻¹⁹ | 1.3×10⁻²⁴ | 3×10⁵ | 3×10⁻²⁶ |
| 90 / 2500 | 3×10⁻¹¹ | 8×10⁻¹¹ | 6×10⁻¹⁹ | 1×10⁻²⁰ | 2.4×10⁻²⁶ | 4×10⁵ | 5×10⁻²⁸ |
| 120 / 2800 | 6×10⁻¹² | 1.9×10⁻¹¹ | 4×10⁻¹⁹ | 2×10⁻²¹ | 2.4×10⁻²⁶ | 8×10⁴ | 1×10⁻²⁸ |

- **The intrinsic defect population is MgO partial Schottky** (c_Mg ≈ 3 c_O). Si vacancies are 10⁷ times rarer.
- **O diffuses 10⁵ times faster in bridgmanite than in periclase** at the same (P, T). The factor comes from both a lower formation energy (1.5–2 eV) and a much lower migration barrier (0.9–1.9 vs 2.7–4.3 eV).
- **Mg is 10⁷–10⁹ times slower than O in bridgmanite.**
- **Caveats** (as for MgO, `MGO_VACANCY_FREE_ENERGIES.md` §3–4):
  - raw Deng values, with no DFT correction yet;
  - charged defects in a short-range model (no long-range electrostatics);
  - real bridgmanite is extrinsic: Fe³⁺ and Al³⁺ fix c_O through charge-coupled substitution, typically far above these intrinsic values. So for O this table is a lower bound on c_O and an upper bound on the activation energy.
- **For Cordier et al. 2023:** they use Si (the slowest species) for bridgmanite creep, and that is still not computed here (§5). The O and Mg results do not change their bridgmanite strength. They show that O is not rate-limiting in bridgmanite, but is in periclase.
