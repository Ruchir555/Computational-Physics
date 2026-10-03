# Computational-Physics

This repository collects small Python exercises in numerical methods and
computational physics.

## Included examples

- numerical integration of a Gaussian and convergence against `scipy.integrate.quad`
- damped oscillator dynamics
- nanobeam parameter calculations
- Fibonacci numbers, proper divisors and number-base conversions

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Each script can be run independently. For example:

```bash
python integration_methods.py
```

That example prints the numerical estimates and writes its plots to `results/`.
