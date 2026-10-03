"""Compare numerical integration with SciPy for a Gaussian integral."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad


def gaussian(x):
    """Return exp(-x**2) for a scalar or NumPy array."""
    return np.exp(-(x**2))


def left_riemann(function, lower_bound, upper_bound, n_intervals):
    """Approximate an integral with a left-endpoint Riemann sum."""
    if n_intervals <= 0:
        raise ValueError("n_intervals must be positive")
    if upper_bound <= lower_bound:
        raise ValueError("upper_bound must be greater than lower_bound")

    edges = np.linspace(lower_bound, upper_bound, n_intervals + 1)
    dx = (upper_bound - lower_bound) / n_intervals
    return float(dx * np.sum(function(edges[:-1])))


def convergence_data(function, lower_bound, upper_bound, interval_counts, reference):
    """Return approximations and absolute errors for several grid sizes."""
    approximations = np.array(
        [left_riemann(function, lower_bound, upper_bound, n) for n in interval_counts]
    )
    errors = np.abs(approximations - reference)
    return approximations, errors


def main():
    lower_bound = -5.0
    upper_bound = 5.0
    n_intervals = 500
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    scipy_value, scipy_error = quad(gaussian, lower_bound, upper_bound)
    approximation = left_riemann(gaussian, lower_bound, upper_bound, n_intervals)

    print(f"SciPy quad: {scipy_value:.12f} (estimated error {scipy_error:.2e})")
    print(f"Left Riemann ({n_intervals} intervals): {approximation:.12f}")
    print(f"Absolute difference: {abs(scipy_value - approximation):.3e}")

    x = np.linspace(lower_bound, upper_bound, n_intervals + 1)
    fig, ax = plt.subplots()
    ax.plot(x, gaussian(x), "r--")
    ax.fill_between(x, gaussian(x), color="tab:blue", alpha=0.6)
    ax.set(xlabel="$x$", ylabel="$f(x)$", title="$e^{-x^2}$")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(output_dir / "gaussian_integrand.png", dpi=200)
    plt.close(fig)

    interval_counts = np.arange(10, 501, 10)
    approximations, errors = convergence_data(
        gaussian, lower_bound, upper_bound, interval_counts, scipy_value
    )

    fig, (value_ax, error_ax) = plt.subplots(1, 2, figsize=(11, 4))
    value_ax.plot(interval_counts, approximations, label="Left Riemann sum")
    value_ax.axhline(scipy_value, color="tab:red", label="SciPy quad")
    value_ax.set(xlabel="Number of intervals", ylabel="Integral estimate")
    value_ax.legend()
    value_ax.grid(True)

    error_ax.loglog(interval_counts, errors, marker="o")
    error_ax.set(xlabel="Number of intervals", ylabel="Absolute error")
    error_ax.grid(True, which="both")
    fig.tight_layout()
    fig.savefig(output_dir / "integration_convergence.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
