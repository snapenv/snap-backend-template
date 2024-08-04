"""Test Snap App."""

import snap_app


def test_import() -> None:
    """Test that the app can be imported."""
    assert isinstance(snap_app.__name__, str)
