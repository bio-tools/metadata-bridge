"""
Unit tests for bridge.utils.require_args.

These tests verify that the require_args decorator enforces required keyword
arguments for asynchronous functions.
"""

import inspect

import pytest

from bridge.utils import require_args


@pytest.mark.asyncio
async def test_require_args_happy_path():
    """
    Test that the require_args decorator allows function execution when all
    required arguments are provided.

    Raises
    ------
    AssertionError
        If the function does not return the expected result.
    """

    @require_args("a", "b")
    async def fn(**kwargs):
        return kwargs["a"] + kwargs["b"]

    assert await fn(a=1, b=2) == 3


@pytest.mark.asyncio
async def test_require_args_missing():
    """
    Test that the require_args decorator raises a ValueError when required arguments
    are missing.

    Returns
    -------
    ValueError
        If the function is called without the required arguments.
    """

    @require_args("a")
    async def fn(**kwargs):
        return 1

    with pytest.raises(ValueError, match="Missing required args: a"):
        await fn()


def test_require_args_keeps_name_docstring_and_signature():
    """The decorated function keeps its metadata, so the API docs show the real signature."""

    @require_args("a")
    async def fn(a: int, b: int = 2, **kwargs) -> int:
        """Add things."""
        return a + b

    assert fn.__name__ == "fn"
    assert fn.__doc__ == "Add things."
    assert list(inspect.signature(fn).parameters) == ["a", "b", "kwargs"]


def test_public_handlers_expose_their_docstrings():
    """`bridge.extract_meta_from_repo` and friends aren't hidden behind the decorator."""
    import bridge

    for fn in (bridge.extract_meta_from_repo, bridge.create_pr_issues_from_meta):
        assert fn.__doc__ and "Parameters" in fn.__doc__
        assert "schema" in str(inspect.signature(fn))
