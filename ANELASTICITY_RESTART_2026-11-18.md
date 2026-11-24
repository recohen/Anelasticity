# Anelasticity restart, 2026-11-18 (10:45 PST; updated 11:05: existing ML_AB settings, A0b extended): Fe at core conditions, A0 running, Obsidian/NFS fix

Read first: this file, then `INPROGRESS.md` (§1 running, §3 proposals), `ANELASTICITY_PLAN_FE.md` (the Fe plan: phases A, B, C; decisions in §8) and `ANELASTICITY_TODO.md` (last lines). Previous restart: `ANELASTICITY_RESTART_2026-11-17.md`. Its items 2–5 of §6 (A3b analyses, MgO separated pair, items waiting for RC) are untouched today and still open. Build and run recipes for the VASP MLFF are in `/resnick/home/recohen/Claude/tools/vasp_lammps/README.md`.

## 1. RC requests this session (11-18)
1. "How did the H200 run go? Is the VASP ML faster on GPU or CPUs? … mpi and/or OMP" → §2. MPI × OpenMP scans submitted.
2. "Plan a set of runs for solid Fe at core conditions like you did for MgO and MgSiO₃. We want Q and the effective viscosity" → `ANELASTICITY_PLAN_FE.md` (§3).
3. "I don't think any fcc crystal was included in the training" → confirmed: no fcc and no hcp crystal (§4).
4. "We first need to add training for hcp and fcc from 0 to 350 GPa and 300–7000 K where solid"; "for solids … 64 atoms max"; "we will do these non-magnetic" → Phase A rewritten (§3).
5. "Please start A0" → started (§5). "If you use vasp_gam should be much faster" → A0b, a Γ-only set (§5).
6. The hcp orthorhombic cell (4a × 2√3a × 2c, 64 atoms) has the same k resolution as the hexagonal 4 × 4 × 2 cell (table in §5); it will be used in A1 because its axes match the LAMMPS cells.
7. "You can add individual points to training (by adding to the AB file) … save them for test states too" → A0 snapshots s1–s3 go to ML_AB, s4–s5 form a held-out set (plan A0(e), A2).
8. Obsidian showed stale or garbled files → cause found and fixed with a hook (§6).
9. "Please write restarts" → this file.
10. "What about vasp_gam?" → A0b is mostly vasp_gam; quick Γ timing job 7205894 submitted (§5).
11. "All the earlier runs in ML_AB were done with vasp_gam" → confirmed, with their full settings; A0b extended to test them (§5). "Write restarts" (11:00) → this update.

## 2. VASP MLFF on GPU against CPU (`tools/vasp_lammps/README.md`, log)
- **H200 test 7058548** (8192 atoms, 300 GPa): the GPU path with 1 rank runs at 0.787 steps/s, 2.5× the P100. SM utilization averages 43 %, and host CPU use is 63 %. The CPU path of the same plugin on 16 EPYC cores of that node runs at 3.83 steps/s, 4.9× faster than the GPU path. Step 0 is identical to the P100 run.
- **CPU check 7058477 failed:** `build_cpu/lmp` is a shared build, and the old `~/lib/liblammps.so.0` (Aug 2025, DeePMD) on `LD_LIBRARY_PATH` shadows its RUNPATH, giving "Unrecognized pair style 'vasp'". Fix: put `build_cpu` first on `LD_LIBRARY_PATH` (done in `cpu_scan.sh`).
- **Scans, both still PENDING at 10:40** (`/groups/carnegie_poc/rcohen/LAMMPS/VASP/Fe/plugin_test`):
  - `cpu_scan.sh` 7166452: icelake, 64 × 1, 32 × 2, 16 × 4, 8 × 8.
  - `h200_scan.sh` 7166454: GPU path with 2, 4, 8 ranks and 1 × 8 threads. The plugin has no `-mp`, so threads should do nothing.
- **Conclusion so far:** production uses the CPU build. On cost, the GPU would need ≈ 22× from MPI sharing to win.

## 3. Fe plan (`ANELASTICITY_PLAN_FE.md`; nothing beyond A0 submitted)
- **Phase A, force field:**
  - A0: DFT settings.
  - A1: on-the-fly training, hcp and fcc, 0–350 GPa, 300 K to 0.98 $T_m$, ≤ 64 atoms, non-magnetic, plus vacancy and stacking-fault cells.
  - A2: refit with a held-out test.
  - A3: validation ($T_m$ by coexistence, $C_{ij}(T)$, liquid η against Alfè et al. 2000, fcc–hcp energies, stacking-fault energies, $E_{2g}$). A go/no-go gate with RC follows A3.
- **Phase B, Q from NEMD:** perfect hcp in 4 channels ($C_{44}$, $C_{66}$, $C_{11}$, $C_{33}$); melt-grown polycrystal; vacancies; {10$\bar1$2} twin and Σ7 tilt bicrystals. Temperatures are T/T_m = 0.70–0.98 at 330 GPa, plus 360 GPa. Q is taken at ≤ 1 THz in the basal channels because of the internal-strain ($E_{2g}$) term.
- **Phase C, effective viscosity:** vacancy formation and migration, diffusion creep, dislocation drag, and the grain-scale model for Q at 1 Hz.
- **Cost:** ≈ 1110–1340 node-h for the full plan, ≈ 520 for the reduced plan. **These numbers are now too low.** A0 shows DFT is slower than assumed, so the A1 cost must be redone from the A0 timing (§5).
- **Open RC decisions (plan §8):**
  - bcc as a production phase, and fcc as one;
  - electronic-temperature strategy: T bands or DeePMD with fparam (also cheaper on P100);
  - budget;
  - primary pressure;
  - light elements later.

## 4. Training set of the current FF: no fcc, no hcp (plan Table 0)
- **Tool:** `tools/mlab_structure.py` (adaptive CNA, Stukowski 2012; validated on ideal and noisy fcc/hcp/bcc), run on all 913 ML_AB configurations of `/groups/carnegie_poc/rcohen/VASP/Fe/bcc/ML/Orthogonal/P300GPa`. The per-configuration table is `ML_AB_structure_cna.txt` there.
- **Result:** configurations 1–200 are bcc and 501–913 are liquid. 401–500 have 12–17 % hcp-like fragments in disordering bcc. The maximum fcc fraction is 0.12 and the maximum hcp fraction 0.29, and no configuration is mainly close-packed.
- **The 2025 crystallized start cell** (`plugin_test/start8192.data`) is 16 % fcc, 23 % hcp, 2 % bcc and 60 % other: the current FF freezes the melt into stacking-disordered close-packed Fe it never saw in training.

## 5. A0: DFT settings test (`/groups/carnegie_poc/rcohen/VASP/Fe/hcp_fcc/ML/A0`)
- **Snapshots** (`tools/fe_a0_setup.py`): 64-atom hcp (hexagonal 4 × 4 × 2) and fcc (primitive 4 × 4 × 4), non-magnetic, Fe_sv, at V = 10.30, 7.70, 6.85 Å³/atom ("0, 150, 330 GPa"). Gaussian displacements with σ = 0.06 d_nn give 5 snapshots per state. "Thot" = 0.9 $T_m$ provisional: 1600, 4050, 5600 K.
- **Smoke test 7177261_1** (hcp_P0/s1, NBANDS 768, 2 nodes): TIMEOUT at 1 h after 4 of 6 calculations; the k3_E700 run is incomplete and k4 never started.

  | calculation | wall (s) | F (eV / 64 atoms) |
  |---|---|---|
  | k2, SIGMA = $k_B$·1600 K | 557 | −512.99335 |
  | k3, $k_B$·1600 K | 926 | −512.98264 |
  | k3, $k_B$·800 K | 927 | −510.68459 |
  | k3, $k_B$·300 K | 907 | −510.05948 |

  - k2 against k3 at Thot: ΔF = 0.17 meV/atom, so 2³ is converged in F at 0 GPa / 1600 K. Forces and stresses are not compared yet.
  - The "0 GPa" volume gives P ≈ 10 GPa.
  - Band 768 lies 20 eV above E_F, so NBANDS = 600 is enough.
  - The full staging (146 single points) would cost ≈ 90 node-h, so it was **not** submitted beyond task 1.
- **A0b, Γ-only main path** (`tools/fe_a0b_setup.py`, `tasks_b.txt`, `b/`; job **7190356_1–31**, PENDING):
  - vasp_gam on all 30 snapshots at SIGMA = $k_B$T, $k_B$·300 K and $k_B$T/2, and ENCUT 700 on 2 snapshots;
  - 2³ references on 2 snapshots per state;
  - 3³ (T and 300 K) and 4³ (300 K) references at P0 and P330, snapshot s1;
  - NBANDS 600; `GAMMA_ONLY` file → vasp_gam in `fe_a0_job.sh`;
  - estimated ≈ 15 node-h.
- **Existing ML_AB settings (RC 11-18: "all the earlier runs in ML_AB were done with vasp_gam"; checked):** vasp_gam 6.4.3, 128-atom cells, ENCUT 900, NBANDS 1400, **SIGMA = 0.2588 eV (3000 K) at every T** (ramps 10 → 7000 and 7000 → 10000 K), ISPIN 1, PSTRESS 300 GPa (`PRE.*/INCAR`, `slurm_vasp*.sh`). New data appended to the same ML_AB must use the same settings, or the old set must be recomputed. So A0b now also has, at Γ, ENCUT 900 at SIGMA = $k_B$T, and the exact old settings (900 eV, 0.2588 eV) on s1–s2, plus 500 eV / 0.2588 eV on all snapshots (193 calculations in all). The 128-atom bcc cube (L = 9.65 Å, |b| = 0.65 Å⁻¹) samples k more finely at Γ than the 64-atom cells (0.85–0.92 Å⁻¹).
- **Quick Γ timing job 7205894** (1 node, 30 min): one Γ single point (hcp P330 s1) and a 10-step Γ AIMD (`A0/gam_quick`).
- **AIMD timing for the A1 cost:** Γ (A0b task 31, 40 steps, 330 GPa) and k2 (**7183764_31**, PENDING). The k3 MD was cancelled.
- **Γ resolution** (64-atom cells at 330 GPa, reciprocal |b_i| in Å⁻¹):

  | cell | \|b_i\| (Å⁻¹) |
  |---|---|
  | hcp hexagonal 4 × 4 × 2 | 0.85, 0.85, 0.92 |
  | hcp orthorhombic 4a × 2√3a × 2c | 0.73, 0.85, 0.92 |
  | fcc primitive 4 × 4 × 4 | 0.90 |

- **Next:**
  1. Tabulate ΔE, Δforces and Δσ of Γ and k2 against k3/k4 at 300 K and hot smearing, and the SIGMA sensitivity of the forces and the shear stress.
  2. Choose Γ or k2 (possibly Γ hot, k2 cold) and decide on T bands.
  3. Measure s per MD step → the A1 cost, to RC.
  4. Write the OUTCAR → ML_AB converter, checked against a block VASP writes itself (which energy is stored: F or E₀; stress order and units), and append s1–s3.

## 6. Obsidian and NFS (memory note `obsidian-sync-docs`)
- **Symptom:** `ANELASTICITY_PLAN_FE.md` was garbled twice: an old row and a new row merged into one line, then duplicated A0–A3 rows.
- **Cause:** `~/Claude` is on NFS (VAST). RC's Obsidian (AppImage in the OnDemand desktop; hpc-22-14 this week; vault `~/Claude`; Obsidian Sync on) watches with inotify, which only sees changes made on its own node. My edits from login3 were invisible to it until restart. Sync then re-sent its stale copies and merged them with mine. Files opened in editing mode on other devices added rewrites; RC set Reading view as the default.
- **Test:** a note written on login3 was invisible, one written on hpc-22-14 appeared at once, and a login3 note merely `touch`ed on hpc-22-14 also appeared.
- **Fix:** a **user-level PostToolUse hook** (`~/.claude/settings.json`; matcher Write|Edit|MultiEdit|NotebookEdit|Bash) runs `tools/obsidian_poke_recent.sh` in the background.
  - It finds `~/Claude` files newer than a stamp and discovers the Obsidian node from the bc_desktop job (cached 10 min, so a different node next week is fine).
  - It runs `tools/obsidian_poke.sh` there, which does `touch`. Copy-and-rename was dropped: it would orphan files held open by writers.
  - Log: `~/.cache/obsidian_poke/log`.
- **Deletions are not covered by the hook.** Delete vault files with `tools/obsidian_poke.sh --rm FILE` (removes them on the Obsidian node), never with rm on a login node.
- The "conflicted copy" files in `~/Claude/.obsidian` are old Dropbox leftovers (RC no longer uses Dropbox).

## 7. Tools added or changed today
| tool | purpose |
|---|---|
| `tools/mlab_structure.py` | adaptive CNA for ML_AB, LAMMPS data or POSCAR |
| `tools/fe_a0_setup.py`, `tools/fe_a0b_setup.py` | A0 and A0b staging |
| `A0/fe_a0_job.sh` | array job; `TASKS=` selects the task list; `GAMMA_ONLY` selects vasp_gam |
| `tools/obsidian_poke.sh`, `tools/obsidian_poke_recent.sh` | Obsidian refresh (§6) |
| `plugin_test/cpu_scan.sh`, `plugin_test/h200_scan.sh` | MPI × OpenMP scans |

## 8. Jobs (11:02; all PENDING)
| job | what | state |
|---|---|---|
| 7205894_1 | quick Γ timing (`A0/gam_quick`, 1 node, 30 min) | PENDING |
| 7166452 | CPU MPI × OpenMP scan | PENDING |
| 7166454 | H200 MPI scan | PENDING |
| 7190356_1–31 | A0b, 193 calculations (157 Γ) after the 11:00 extension | PENDING |
| 7183764_31 | k2 AIMD timing | PENDING |
| 7177261_1 | A0 smoke test | TIMEOUT, 4/6 done, analysed above |

Earlier jobs still unanalysed are listed in `INPROGRESS.md` §1–2 (A3b follow-ups, MgO separated-pair DFT, older items).

## 9. Priorities for the next session
1. A0b results → settings, T-band decision, A1 cost (§5 next) → RC. **Key decision:** append to the existing ML_AB with its settings (Γ, 900 eV, SIGMA 0.2588 eV at every T), or recompute the 913 old configurations with new settings. A0b's G_E900_S02588 against G_E500_Thot / G_E900_Thot gives the ENCUT and SIGMA effects on E, F, σ.
   - Quick Γ timing (7205894) gives the s per Γ step → the A1 cost even before A0b runs.
2. Scans 7166452 / 7166454 → steps/s → rescale the plan's B and C costs.
3. Then A1 staging (64-atom orthorhombic hcp and primitive fcc, ramps per pressure) once RC approves the A1 cost.
4. Restart 11-17 §6 items 2–5 (A3b (a)/(b) analyses, MgO separated-pair FEP and DFT binding curve, items waiting for RC).
