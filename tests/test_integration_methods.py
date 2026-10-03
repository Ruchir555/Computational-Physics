import unittest

import numpy as np

from integration_methods import convergence_data, gaussian, left_riemann


class IntegrationMethodTests(unittest.TestCase):
    def test_left_riemann_integrates_a_constant_exactly(self):
        value = left_riemann(lambda x: np.full_like(x, 3.0), -2.0, 4.0, 17)
        self.assertAlmostEqual(value, 18.0, places=12)

    def test_left_riemann_converges_for_quadratic(self):
        interval_counts = np.array([20, 40, 80, 160])
        approximations, errors = convergence_data(
            lambda x: x**2,
            0.0,
            1.0,
            interval_counts,
            1.0 / 3.0,
        )
        self.assertEqual(approximations.shape, interval_counts.shape)
        self.assertTrue(np.all(np.diff(errors) < 0.0))
        self.assertLess(errors[-1], errors[0] / 7.0)

    def test_gaussian_is_vectorized_and_even(self):
        points = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])
        values = gaussian(points)
        np.testing.assert_allclose(values, values[::-1])
        self.assertAlmostEqual(values[2], 1.0)

    def test_invalid_bounds_and_interval_counts_are_rejected(self):
        with self.assertRaises(ValueError):
            left_riemann(np.sin, 0.0, 1.0, 0)
        with self.assertRaises(ValueError):
            left_riemann(np.sin, 1.0, 1.0, 10)
        with self.assertRaises(ValueError):
            left_riemann(np.sin, 2.0, 1.0, 10)


if __name__ == "__main__":
    unittest.main()
