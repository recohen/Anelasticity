# Anelasticity: questions and proposals waiting for RC

Last updated: 2026-11-19 12:40. RC 11-19: "Maybe make a new file QUESTIONS that I would expect more" (the proposals used to sit in `INPROGRESS.md` §3). Every item here needs a decision from RC; nothing in it is submitted. Running jobs are in `INPROGRESS.md`, history in the restarts and `ANELASTICITY_DONE.md`. When RC answers, the item moves to "Answered" with RC's words and then to the restart/DONE.

## A. Fe at inner-core conditions (`ANELASTICITY_PLAN_FE.md`)

1. **Functional for the DeePMD training data: PBE or PBEsol?**
   - PBE: the old 913-configuration ML_AB and most published DFT on core Fe use it.
   - PBEsol: X. Deng's MgSiO₃ model and her pure-Fe model (`/central/groups/carnegie_poc/xind/pure_iron/MLP`, ≤ 160 GPa) use it. It would make MgO/MgSiO₃–Fe comparisons consistent.
   - Either way, Fe_sv is used, not Fe_pv: the Fe_pv PAW spheres (RCORE 2.2 bohr) overlap at 330 GPa (plan §3.1).
   - Recommendation: PBE, unless the cross-material comparison matters more to you.
2. **k-mesh for the recalculations** (tests A0c and A0c2 done 11-19, `results_Fe/A0c_summary.txt`; 64-atom cells, 500 eV, errors against 3³ ($k_BT$ smearing) / 4³ (300 K smearing), wall time on 64 ranks):

   | mesh | force rms, $k_BT$ (eV/Å) | force rms, 300 K (eV/Å) | ΔP (GPa) | wall (s) |
   |---|---|---|---|---|
   | Γ only | 0.14–0.26 | 0.19–0.46 | 1–7 | 23–45 |
   | one k-point (¼,¼,¼) | 0.06–0.17 | 0.09–0.36 | 0.3–2 | 52–124 |
   | Γ-centred 2×2×2 (8 k) | 0.011–0.025 | 0.036–0.11 | ≤ 0.3; **12.4 at fcc 330 GPa / 300 K** | 250–720 |
   | **true shifted MP 2×2×2** (4 k: one of each ±k pair, KBLOWUP = .FALSE.) | **0.008–0.015** | **0.026–0.087** | **≤ 0.1** (0.01 at fcc 330 GPa / 300 K) | **160–310** |
   | "Monkhorst 2 2 2" as VASP ran it (16 pairs after the lattice point-group blow-up; not a 2×2×2 mesh) | — | 0.005–0.018 | ≤ 0.01 | 790–1090 |

   - **Recommendation: the true shifted 2×2×2 for every band** (RC's proposal, confirmed). It beats the Γ-centred 2×2×2 on every state, removes its 12 GPa error at fcc 330 GPa / 300 K, and costs about 0.6× as much.
   - The remaining error is in the cold limit (300 K smearing: hcp 330 GPa 0.087 eV/Å, deviatoric 0.5 GPa). For 0 K static validation ($C_{ij}$, stacking faults) use 4×4×4.
   - **Cost:** at 700 eV, about 5–12 min per 64-atom configuration on 64 cores, so ≈ 80–200 64-core-h per 1000 configurations.
4. **Budget** (plan §8 item 3): the full plan (≈ 1110–1340 node-h, now an underestimate because of k-points) or the reduced first pass (≈ 520)?
5. **Pressure** (plan §8 item 4): 330 GPa primary with 360 GPa secondary, or the reverse?
6. **Phases** (plan §8 item 1): bcc as a production phase (B5; is it dynamically stable at core conditions?) and fcc as a production phase, beyond training?
7. **Light elements** (plan §8 item 5): out of scope for pure Fe; a later phase?

## B. MgO and MgSiO₃

8. **Σ5 unlocking temperature:** why does it jump between 60 and 90 GPa? Static γ(u) scan or an NEB of one event at 60 and 90 GPa, ≈ 2–4 P100-h.
9. **Dislocation drag B(T)** at 2000 and 5000 K with the rigid-block fix (≈ 40 P100-h). Does a threshold appear at 2000 K?
10. **Bridgmanite boundary energies γ:** anneal + quench of the best shifts (≈ 4 P100-h) and a zoff scan. Bridgmanite boundaries in general wait for your literature check.
11. **Bridgmanite vacancy energies, DFT correction** (optional, A3b (c); ≈ 1000–2000 core-h): VASP single points on DeePMD snapshots of the V_Mg, V_Si, V_O2 and perfect cells at 1–2 states, FEP as for MgO.
12. **Liquids, O-density hypothesis (T26):** matched-$n_O$ Deng runs (≈ 15–25 P100-h) to test whether $D_O$ is a function of the O density.
13. **Optional MgO liquid points** at 7500 and 6500 K.

## Answered

- 11-19, **functional (item 1):** RC "Use PBE".
- 11-19, **k-mesh (item 2), RC's proposal:** "use vasp_gam for MD trajectories and selection, and then recalculation using MP2x2x2". My view is in the 11-19 reply: agreed for sampling, ideally with Γ-only on-the-fly MLFF rather than plain AIMD. The recalculation mesh needs one more test, because the accurate "MP2" was really a 16-point set. A true 4-point shifted 2×2×2 mesh is untested. → A0c2 (7279850) tested it: best accuracy per cost of all meshes; recommended for all bands (item 2).

- 11-19, **electronic temperature / force-field route** (plan §8 item 2): A0b showed that SIGMA must equal $k_BT$. RC: "Yes recomputing configs for deepmd is a good idea. I actually have a whole bunch of tools we have developed for that. I am waiting first for the k-point test." → DeePMD with fparam $=k_BT$, using X. Deng's mldp workflow (plan §3.1).
- 11-19, **first recalculation batch (item 3)**: RC "Go ahead and stage the first recalculation batch and submit" → 100 FPS-selected old configs (R1, 7286822) and 40 constant-T hcp/fcc sampling runs (A1 bands, 7286841); INPROGRESS.
- 11-19, **bridgmanite talk trajectory**: RC "Do the Bridgmanite talk trajectory" → job 7279725, done; movies in `/groups/carnegie_poc/rcohen/LAMMPS/TalkTrajectories/Bdg_vacancy_hops_5000K{,_first50ps}`.
