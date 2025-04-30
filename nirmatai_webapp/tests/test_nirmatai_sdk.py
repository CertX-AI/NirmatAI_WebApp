# type: ignore
""""Unit tests for the telemetry module of NirmatAI."""

import numpy as np
import pytest
from nirmatai_sdk.telemetry import Scorer


def test_scorer_valid_labels():
    """Initialize without error if y_true and y_pred contain valid labels."""
    y_true = np.array(
        ["full-compliance", "minor non-conformity", "major non-conformity"]
    )
    y_pred = np.array(
        ["full-compliance", "minor non-conformity", "major non-conformity"]
    )

    scorer = Scorer(y_true, y_pred)
    assert np.array_equal(scorer.y_true, y_true)
    assert np.array_equal(scorer.y_pred, y_pred)


def test_scorer_invalid_y_true_labels():
    """Raise a ValueError if y_true contains invalid labels."""
    y_true = np.array(["C", "B", "B"])
    y_pred = np.array(
        ["full-compliance", "minor non-conformity", "major non-conformity"]
    )

    with pytest.raises(ValueError, match="y_true contains invalid labels"):
        Scorer(y_true, y_pred)
