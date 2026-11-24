# Requirements for the MgO anelasticity project

1. System: MgO, 4096 atoms, constant volume $V=6.6868$ Å$^3$/atom. Do not switch to smaller cells for production.
2. Potential: DeePMD `graph.pb` (Mg, O). Production uses the compressed `graph_c.pb` (checked against `graph.pb`, 2.8× faster). Any new compressed model must be checked the same way.
3. Compute: cheap Tesla P100 GPUs only (`--gres=gpu:p100:1`, partition `gpu`). Never H100, H200, L40S.
4. Job scripts copy the SBATCH header of `8000K/Viscosity/x/R1A1/2267049/1submit_lammps.sh`: `--nodes 1 --ntasks 1 --cpus-per-task 9 --gres=gpu:p100:1 --exclude=hpc-93-36 --partition gpu --mem-per-cpu=2GB`, mail to the user. No `cd` to the working directory, no directory in the slurm output name, no array `%` limits.
5. Cost: estimate from a **measured** speed and present it before submitting anything beyond a short test. Keep total cost small. The user rejected a multi-ten-GPU-day plan.
6. Physics protocol: cool the liquid at constant volume until it crystallizes (it supercools, then crystallizes all at once).
7. Frequency range: aim for 4–5 decades to extrapolate toward MHz. Run sub-10 GHz points only where the relaxation time puts structure there.
8. Analysis: lock-in at the known drive frequency (`anelastic_lockin.py`), never FFT peak picking. Strain is tilt$/L_z$. Stress is $-P_{ab}$ in Pa. Report $G'$, $G''$, $\tan\delta$, $\eta'=G''/\omega$ (Eq. 3 of the plan) with block error bars and harmonic ratios.
9. Linearity must be checked by repeating at least one frequency at a second amplitude.
10. Compare with the user's Green–Kubo $G(t)$ results.
11. Docs: equation numbers always; LaTeX in docs, unicode in the terminal. Tools live in `/resnick/home/recohen/Claude/tools`; docs in `/resnick/home/recohen/Claude/Anelasticity`. Test runs go under `/groups/carnegie_poc/rcohen/` (write paths in this form; it is a symlink to `/resnick/groups`), scratch in `.../rcohen/Downloads`, never `/tmp`.
12. Python: `source /resnick/home/recohen/cohen_env/bin/activate`. The user's notebooks are jupytext `.py` files; do not overwrite them.
13. Queue: jobs of ≤ 30 min (tests, timings) go in the debug QOS, `sbatch -q debug -t 00:30:00` (standing rule from the start; one running debug job per user; it is a QOS, so `sinfo` does not list it). Many short jobs at once can instead run in parallel in the normal queue.
