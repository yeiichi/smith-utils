from __future__ import annotations

import random


def sample_positive_gaussian(
    mean: float,
    approx_upper_bound: float,
    trial_number: int,
) -> list[float]:
    """Sample positive Gaussian values bounded by an approximate upper bound.

    ``approx_upper_bound`` is used as ``mean + 3 * sigma`` to derive the
    Gaussian standard deviation. It is also used as a truncation bound, so
    returned samples are greater than zero and less than or equal to the bound.
    """
    if trial_number < 0:
        raise ValueError("trial_number must be >= 0")
    if mean <= 0:
        raise ValueError("mean must be positive")
    if approx_upper_bound <= mean:
        raise ValueError("approx_upper_bound must be greater than mean")

    sigma = (approx_upper_bound - mean) / 3
    samples: list[float] = []

    while len(samples) < trial_number:
        value = random.gauss(mean, sigma)
        if 0 < value <= approx_upper_bound:
            samples.append(value)

    return samples
