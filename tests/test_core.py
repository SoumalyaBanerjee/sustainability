"""Tests for core module."""

import pytest
from sustainability.core import initialize


def test_initialize():
    """Test that initialization works without errors."""
    try:
        initialize()
        assert True
    except Exception as e:
        pytest.fail(f"Initialization failed: {e}")
