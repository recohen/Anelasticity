# Plan: dislocations in the anelastic production runs, THz to Gy (MgO, MgSiO₃, Fe) (2026-11-21)

**RC 11-21:** "We want to predict over all frequencies from THz to Gy. I think we need dislocations, if just to prove them unimportant. So we should add them to our MgO and MgSiO3 production runs and analyze, and include in Fe training as possible."

## 0. Where we are

- **No dislocations in the anelastic production runs so far.** The oscillatory-shear sweeps (summary §3–5) used:
  - perfect crystals;
  - vacancy cells (MgO Schottky, bridgmanite V_Mg + V_O);
  - Σ5 bicrystals;
  - the MgO polycrystal.
- **Dislocations do not appear spontaneously in these cells:**
  - vacancy numbers are fixed, and loops would need tens of vacancies to condense;
  - the sweep stresses (a few GPa) are far below the ideal strength (≈ G/10);
  - nm cells cannot hold a stable loop.
- **One separate dislocation result exists, for MgO:** the driven ½[110](001) edge at ≈ 162 GPa / 3500 K.
  - Phonon drag B = 1.76 × 10⁻⁴ Pa s, with no threshold (summary §5k, §5m).
  - The Granato–Lücke estimate puts the drag peak at ≈ 7 kHz for L = 100 µm.
- **Bridgmanite dislocations** (Guan et al. 2026: [100](010) / [010](100)) were planned (DRIVEN_RHEOLOGY D7) but not run.
- **Fe:** dislocation cores were not yet in the training set.

## 1. Strategy over the whole band

| band | what controls dislocation loss | how we get it |
|---|---|---|
| THz–GHz | glide against drag B, with the long-range back stress of the cell | **periodic dipole cells in the production sweeps** (§2); direct G*(ω), same V, T and protocol as the perfect references |
| GHz–kHz | the same physics; L and ρ set the time scale | scale the §2 result with ρ and L (Eqs. 4–5); check with two cell sizes |
| kHz–mHz (seismic) | string damping with pinning (Granato–Lücke), kink-pair (Peierls) mobility at low stress, unpinning | B(T) and the kink-pair rate law from the driven runs (DRIVEN_RHEOLOGY D1–D6), in the line model (Eqs. 5–6) |
| years–Gy | steady dislocation creep, glide plus climb, climb set by self-diffusion | Weertman/Orowan creep (Eq. 7) with our vacancy ΔG_f, ΔG_m and D (summary §5n), against diffusion creep (FE plan Eq. 4) |

The goal is a Q⁻¹(ω) and η_eff for each band, with an error bar. That is enough to show either that dislocations are negligible or where they dominate.

## 2. Dipole cells in the production sweeps

**Cells (`tools/build_dislocation_dipole.py`, written and tested 11-21).**
- Fully periodic dipole cells: the glide-plane normal is z and b lies along x. The cells are driven by the existing xz sweep (`anelastic_sweep.lammps`, MODE shear).
- The Peach–Koehler force is bσ_xz along the glide direction for both characters:
  - **edge** (line along y): glides along x;
  - **screw** (line along x): glides along y.
- **Edge construction:**
  - remove one column of whole repeat units between the glide planes at Lz/4 and 3Lz/4, so the cell stays stoichiometric;
  - apply the isotropic Volterra field of the dipole with periodic images, removing the spurious linear terms;
  - shrink Lx by b/2, so V/atom is that of the perfect cell.
- **Screw construction:** a quadrupolar dipole, with the plastic strain of Eq. 2 carried in the tilt (xz = xy = b/2).

| id | material, state | system | atoms | ρ (m⁻²) |
|---|---|---|---|---|
| M1 | MgO V6.6868 (≈ 162–180 GPa), 3000/4000/5000 K, MgO-only model (as the B1 references) | ½[110](001) edge, 16 × 4 × 16 | 3968 | 8.0 × 10¹⁶ |
| M2 | same | ½[110](001) screw, 4 × 16 × 16 | 4096 | 7.7 × 10¹⁶ |
| M3 | same (optional) | ½[110](1$\bar1$0) edge | 1984 (×2) | 1.1 × 10¹⁷ |
| B1 | MgSiO₃ V6.5669 bridgmanite, 2000/3000/4000 K, Deng model (as the crystal sweeps) | [100](010) edge, 8 × 2 × 8 | 2400 | 1.5 × 10¹⁷ |
| B2 | same | [010](100) edge | 2400 | 1.5 × 10¹⁷ |
| B3 | same | [100](010) screw | 1920 | 1.3 × 10¹⁷ |

Each system is built at two sizes, ρ and about ρ/4 (2× along the two perpendicular directions), to separate the cell back-stress from the physics (Eq. 3).

**Protocol** (`tools/disl_dipole_eq.lammps`, `tools/disl_dipole_cores.py`):
1. Build at the production V/atom.
2. Minimize at fixed box, then 40 ps NVT.
3. Check that the cores are intact and stay on their planes.
4. Sweep at periods of 0.2, 1, 5 and 20 ps (5 THz–50 GHz), γ₀ = 0.5–1 %, 200 ps each, as the B1 references.
5. Check linearity at one period with γ₀/2.

**Analysis.** For the dislocations of density ρ (per area normal to the lines), each moving with drag B against a restoring stiffness k (dipole interaction, Peierls well, and the elastic back stress of the periodic cell):

$$B\,\dot x=b\,\sigma-k\,x,\qquad \gamma_p=\rho\,b\,x \tag{1}$$

The plastic strain of a dipole of cut area vector A (built into the screw cell's tilt):

$$\beta_{ij}=\frac{b_iA_j}{V} \tag{2}$$

Equation 1 at fixed total strain gives a Debye relaxation of the compliance. Its strength and time are

$$J^*(\omega)=J_U+\frac{\Delta J}{1+i\omega\tau},\qquad \Delta J=\frac{\rho b^2}{k},\qquad \tau=\frac{B}{k+\rho b^2G_U} \tag{3}$$

so the dislocation contribution is $J^*_{disl}-J^*_{perfect}$ at the same V and T.
- Two cell sizes give B and k separately. In a periodic cell k scales as $Gb^2/L^2$, with L the cell size perpendicular to the lines.
- The B from Eq. 3 must agree with the driven B (1.76 × 10⁻⁴ Pa s for the MgO edge). That agreement validates both.
- **Expected for M1:** $\rho b^2G\approx$ 2 GPa and B ≈ 1.8 × 10⁻⁴ Pa s, so τ ≈ 0.1 ps; the peak is near 1 THz, inside the sweep band. At ρ/4, τ ≈ 0.4 ps.

## 3. From the cell to Earth (THz → Gy)

1. **Drag-controlled string (Granato–Lücke).** A segment of length L between pins, line tension C ≈ Gb²/2:

$$Q^{-1}(\omega)=\frac{\Omega\,\rho L^2\,\omega\tau_L}{1+\omega^2\tau_L^2},\qquad \tau_L=\frac{B\,L^2}{\pi^2 C} \tag{4}$$

   Ω ≈ 0.1 is the orientation factor. Using B from §2 and network spacing L ≈ ρ^{-1/2}, the peak frequency follows directly:

$$f_{peak}=\frac{\pi C\,\rho}{2B}\quad(L=\rho^{-1/2}) \tag{5}$$

   For MgO (C ≈ 1.1 × 10⁻⁸ N) this gives ≈ 10⁸ Hz at ρ = 10¹² m⁻² and ≈ 10⁴ Hz at 10⁸ m⁻² (the 7 kHz of summary §5k). Seismic frequencies need L ≳ 1 cm (ρ ≲ 10⁴ m⁻²) or a much smaller mobility (item 2).
2. **Lattice friction at low stress.** When the Peierls barrier controls glide (bridgmanite certainly; MgO below the drag regime), B in Eq. 4 is replaced by the linear-response kink-pair mobility $B_{eff}=1/M_0$ (DRIVEN_RHEOLOGY Eq. 3, from the driven runs D1–D4). This can move the peak down by many decades. Guan's slip change at ≈ 1800 K is the test for bridgmanite.
3. **Pinning and unpinning:** vacancies and boundaries at the line (D5) set L and add an unpinning (hysteretic, amplitude-dependent) loss. This is checked against the γ₀ dependence of §2.
4. **Years to Gy: steady creep.** Glide is limited by climb, and climb by self-diffusion of the slowest species:

$$\dot\varepsilon=A\,\frac{D_{sd}Gb}{k_BT}\left(\frac{\sigma}{G}\right)^n,\qquad \eta_{disl}=\frac{\sigma}{2\dot\varepsilon} \tag{6}$$

   - n ≈ 3 for climb-controlled creep; D_sd is from our vacancy free energies (summary §5n; Cordier's O diffusion in MgO).
   - The comparison is with diffusion creep, $\eta_{NH}$ and $\eta_C$ (FE plan Eq. 4), at mantle stresses of 0.1–1 MPa and grain sizes of 0.1–10 mm.
   - This deformation-mechanism map is the Gy end of the answer.
5. **Combined loss:**

$$Q^{-1}_{total}(\omega)=Q^{-1}_{phonon}+Q^{-1}_{vac}+Q^{-1}_{gb}(\omega;d)+Q^{-1}_{disl}(\omega;\rho,L,T) \tag{7}$$

   Each term comes from its own calculation, and the dislocation term is plotted against the others over 10¹²–10⁻¹⁷ Hz.

## 4. Fe

- **Training:** four ⟨a⟩ dipole cells added to the iteration loop (`fe_dp_explore.py` systems `dbe`, `dpe`, `dbs`, `dps`, plus sheared `dbe_sh`, `dbs_sh`):
  - basal edge (176 atoms) and prismatic edge (88);
  - screw gliding on basal and on prism (128 each).
- They sit in the same P–T grid as the other systems. Their DFT frames go through the same sample → DFT → split by error loop (plan FE §3.2).
- **Not included:** ⟨c+a⟩ dislocations are too large for DFT cells and are not planned for training.
- **Production (FE plan H5):** the same builder for the Fe dipole sweeps, with Eqs. 3–6 at 330 GPa once the potential passes the gate.

## 5. Order and cost

1. **Pilot (job 7587907, finished 11-21):** M1 at 4000 K, minimize + 38 ps NVT. Both cores intact on their glide planes; the dipole glides freely as a pair; ⟨P⟩ 145.9 GPa (perfect 144.7), ⟨σ_xz⟩ −1.0 GPa.
   - **M1 sweep submitted 11-21** (job 7614205: 0.2, 1, 5, 20 ps, γ₀ = 0.01, plus the perfect cell at 20 ps; `Dislocations/M1_edge001_4000K`).
   - **M1 sweep finished 11-22** (`results_dislocations/M1_edge001_4000K.md`): nonlinear at γ₀ = 0.01. The dipole flips between its two stable configurations each half cycle (plastic strain ±0.015 = 1.5 γ₀), so G′ < 0 at 5 and 20 ps and G″ < 0 at 1 ps; Eq. 3 does not apply. At 0.2 ps a Maxwell (k ≈ 0) reading gives B ≈ 9 × 10⁻⁵ Pa s (driven 1.76 × 10⁻⁴), but at v ≈ 0.8 c_s. Linear response needs Green–Kubo on a long NVT or γ₀ = 0.001. RC 11-22 chose Green–Kubo: job 7718928, 1 ns NVE (`Dislocations/M1_edge001_4000K_GK`).
   - **B1 pilot submitted 11-21** (job 7615044, P100 debug): bridgmanite [100](010) edge, 2400 atoms, 3000 K, minimize + 40 ps NVT (`MgSiO3/.../V6.5669/crystal/Dislocations/B1_edge100_010_3000K`).
2. If the cores are stable, run the M1 sweep at 4000 K (4 periods, ≈ 10 P100-h). Then a second size and Eq. 3: B against the driven value.
3. **Then:** M1 and M2 at 3000, 4000 and 5000 K, two sizes each (≈ 120 P100-h); B1–B3 at 2000, 3000 and 4000 K (≈ 180 P100-h; first a B1 pilot at 3000 K, since bridgmanite cores may need a longer anneal).
4. The DRIVEN_RHEOLOGY D-runs (kink pairs, pinning) feed §3 steps 2–3; Eq. 6 needs no new MD.

## 6. Decisions for RC

1. Slip systems: MgO ½⟨110⟩{100} (high-P) only, or also {110}? Bridgmanite: Guan's [100](010) and [010](100), plus [001](010)?
2. The full set (≈ 300 P100-h) or the reduced pass: M1, M2 and B1 at one size and 2 T (≈ 60 P100-h), with the second size only at one T?
