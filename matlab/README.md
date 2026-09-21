# MATLAB benchmark implementation

## Requirements

- MATLAB with [PlatEMO v4.0](https://github.com/BIMK/PlatEMO).
- Statistics and Machine Learning Toolbox for `pdist2`.

The algorithm is in `LMOHADE/LMOHADE.m`, with helper functions in `LMOHADE/private/`. PlatEMO provides the benchmark problems and platform functions. Third-party attribution is retained in source headers and [upstream information](UPSTREAM_README.md).

## Usage

Add this package's `matlab` directory to the MATLAB path, then call:

```matlab
run_benchmark(platemoRoot, problemName, N, maxFE, seed)
```

- `platemoRoot`: directory containing `platemo.m`.
- `problemName`: `ZDT1`, `ZDT2`, `ZDT3`, `ZDT4`, `ZDT6`, or `DTLZ1`–`DTLZ7`.
- `N`: population size.
- `maxFE`: evaluation budget.
- `seed`: nonnegative integer random seed.

Problem classes provide default objective counts and dimensions. Results are saved through PlatEMO under `Data/LMOHADE`. The entry point restores the MATLAB path and working directory when it exits.
