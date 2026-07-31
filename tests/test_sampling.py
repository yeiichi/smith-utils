import pytest

from src.smith_utils.numeric.sampling import sample_positive_gaussian


def test_sample_positive_gaussian_returns_requested_number(monkeypatch):
    values = iter([-1.0, 12.5, 6.0, 7.5, 8.0])

    monkeypatch.setattr("src.smith_utils.numeric.sampling.random.gauss", lambda mean, sigma: next(values))

    assert sample_positive_gaussian(mean=5.0, approx_upper_bound=10.0, trial_number=3) == [
        6.0,
        7.5,
        8.0,
    ]


def test_sample_positive_gaussian_zero_trials_returns_empty_list():
    assert sample_positive_gaussian(mean=5.0, approx_upper_bound=10.0, trial_number=0) == []


def test_sample_positive_gaussian_validates_trial_number():
    with pytest.raises(ValueError, match="trial_number must be >= 0"):
        sample_positive_gaussian(mean=5.0, approx_upper_bound=10.0, trial_number=-1)


def test_sample_positive_gaussian_validates_positive_mean():
    with pytest.raises(ValueError, match="mean must be positive"):
        sample_positive_gaussian(mean=0.0, approx_upper_bound=10.0, trial_number=1)


def test_sample_positive_gaussian_validates_upper_bound_greater_than_mean():
    with pytest.raises(ValueError, match="approx_upper_bound must be greater than mean"):
        sample_positive_gaussian(mean=5.0, approx_upper_bound=5.0, trial_number=1)
