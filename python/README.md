# Python DEED implementation

## Installation and usage

Run from the repository root:

```bash
python -m pip install -r python/requirements.txt
python python/src/main.py
```

The entry point runs `l_mohade.LMOHADE.LMOHADE` on the 5-unit, 24-hour system.

### Script defaults and manuscript settings

The current defaults in `src/main.py` are population 100, 10,000 iterations, archive threshold 100, grid divisions 100, and `NumOfRuns = 5`. The class defaults are `LH=10000` and `L=0.08`. Random seeds are not assigned by the entry point.

The manuscript specifies **30 independent runs unless otherwise stated**, and **20 runs per setting for the parameter-sensitivity and ablation studies**. The script's default of 5 runs is not the manuscript's experimental setting.

## Output

Results are saved in `python/results/DEED_5unit_LMOHADE/`:

- `LMOHADE_fitness<i>.txt`: cost and emission columns.
- `LMOHADE_position<i>.txt`: flattened 24-hour schedules.
- `LMOHADE_compromised_solution<i>.txt`: selected cost–emission pair.

Run indices are 0–4. Running again overwrites matching output files.

## Configuration

System data are in `src/public/constants_*unit.py`. The entry point and shared `init.py`, `update.py`, and `P_objective.py` currently use the 5-unit data. Changing systems requires consistent configuration of all four modules and their cached dimensions; changing only `main.py` is insufficient.

Parameter variants are in `src/l_mohade/` subdirectories. `src/l_mohade_archive_learning/` is a separate implementation. The optional `LMOHADE_MS.py` additionally needs a version of jMetalPy providing `jmetal.operator`.

Plotting and spreadsheet utilities reference external result files. Set their input paths to your own data before use.
