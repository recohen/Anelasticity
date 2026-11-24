# results_Tdep: how these files were made

Latest run 2026-10-13 (after the MgO perfect-B1 T series, jobs 4407426–8, and the bridgmanite V_Mg + V_O cells,
jobs 4407925–8 and 4408168–9). First collect, then:

    source ~/cohen_env/bin/activate; cd /resnick/home/recohen/Claude; A=$PWD/Anelasticity
    python tools/anelastic_collect.py --cases tools/anelastic_cases_MgSiO3_V6.5669.py
    python tools/anelastic_collect.py --cases tools/anelastic_cases_MgO_V6.6868.py
    python tools/T_dependence.py --case "MgSiO3 V6.5669" $A/results_MgSiO3_V6.5669 --case "MgO V6.6868" $A/results \
      --case "MgO V9.6397" $A/results_V9.6397 \
      --series "MgSiO3 V6.5669" /crystal/ perfect --series "MgSiO3 V6.5669" /crystal_VMgO/ "V_Mg+V_O" \
      --series "MgO V6.6868" FreqSweep_solid melt-grown --series "MgO V6.6868" FreqSweep_B1perfect "perfect B1" \
      --crystal-note "MgO V9.6397" melt-grown --defect-gk "MgSiO3 V6.5669" VMgO "V_Mg+V_O" \
      --out $A/results_Tdep

`--series` is needed because the perfect (`crystal/<T>K/FreqSweep_solid`) and vacancy (`crystal_VMgO/<T>K/FreqSweep_solid`)
bridgmanite sweeps share a directory name; a plain `--crystal-dir FreqSweep_solid` would mix them in one fit.
`--defect-gk` adds D_i from the vacancy-cell GK msd.dat (1.5 ns).

Outputs: T_dependence.md/.csv (tool tables), fig_T_dependence.{pdf,png}, and T_DEPENDENCE_RESULTS.md (written
results and interpretation, 2026-10-13). Discussion: ANELASTICITY_RESULTS_SUMMARY.md §5j.

Earlier run (2026-10-12) used only `--crystal-note` for the three cases; superseded.
