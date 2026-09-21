# L-MOHADE

**A Learning-driven Hunger-based Adaptive Differential Evolution for Dynamic Economic Emission Dispatch**

**Authors:** Hui Chen, Liming Xin, and Jinlin Peng  
**Manuscript status:** Submitted to *Applied Soft Computing*.

## Overview

L-MOHADE addresses dynamic economic emission dispatch (DEED), which schedules generator output over time while considering fuel cost and emissions as two objectives. The method combines hunger-driven search, a time-varying cooperation mechanism, and archive-guided learning to explore cost–emission trade-offs.

This repository contains the Python DEED implementation, comparison algorithms, parameter variants, and a MATLAB implementation for multi-objective benchmark problems using PlatEMO. System data for 5, 6, 10, 20, and 40 generating units are included. The Python entry point is configured for the 5-unit system.

## Repository structure

```text
python/
  src/main.py          Python DEED entry point
  src/l_mohade/        L-MOHADE and parameter variants
  src/public/          System data and shared routines
  requirements.txt     Python dependencies
matlab/
  run_benchmark.m      PlatEMO benchmark entry point
  LMOHADE/             MATLAB algorithm and helper functions
figures/               PDF figure assets
CITATION.cff           Manuscript title and author information
```

Additional comparison algorithms and plotting utilities are included under `python/src/`. See the [Python instructions](python/README.md), [MATLAB instructions](matlab/README.md), and [figure index](figures/README.md) for details.

## Quick start

### Python: DEED

Clone the repository and install the dependencies:

```bash
git clone https://github.com/Bailey-iChen/L-MOHADE-DEED.git
cd L-MOHADE-DEED
python -m pip install -r python/requirements.txt
```

Run the configured 5-unit, 24-hour case:

```bash
python python/src/main.py
```

The Python entry point is configured for the 5-unit DEED system. See the [Python instructions](python/README.md) for configuration and output details.

### MATLAB: benchmark problems

Install PlatEMO v4.0 and add this repository's `matlab` directory to the MATLAB path. Then call:

```matlab
run_benchmark(platemoRoot, problemName, N, maxFE, seed)
```

The supported problems are ZDT1–4, ZDT6, and DTLZ1–7. The [MATLAB instructions](matlab/README.md) explain the arguments and dependencies.

## Configuration and results

Python results are saved in `python/results/DEED_5unit_LMOHADE/`, including cost–emission vectors, generator schedules, and selected compromise solutions. Repeated runs of the entry point overwrite matching output files.

To use another system, configure the entry point and shared data-dependent routines consistently; changing only the import in `main.py` is insufficient. See the [configuration notes](python/README.md#configuration). MATLAB benchmark results are saved through PlatEMO under `Data/LMOHADE`.

## Citation and acknowledgments

If you use this code, please cite the manuscript named above. Author and title information is provided in [CITATION.cff](CITATION.cff).

The MATLAB implementation requires [PlatEMO](https://github.com/BIMK/PlatEMO). See the [MATLAB instructions](matlab/README.md#attribution) for its citation and third-party attribution.
