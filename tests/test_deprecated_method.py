import pytest
import warnings
from hypothesis import given
from hypothesis.strategies import one_of, none, text

from deprecator import Deprecator


@pytest.fixture
def default_deprecator():
    return Deprecator('1.0')


@given(docstring_message=text(), preview_message=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", [None, dict(), lambda **_: dict()])
def test_docstring_message_is_included(default_deprecator, parameter_map, docstring_message, preview_message):
    default_deprecator.docstring_generator = lambda **_: docstring_message
    default_deprecator.warning_generator = lambda **_: ''
    default_deprecator.preview_generator = lambda **_: preview_message

    @default_deprecator.deprecated('0.1', parameter_map=parameter_map)
    def func():
        """summary line"""
        pass

    assert docstring_message in func.__doc__
    if preview_message:
        assert preview_message in func.__doc__


@given(warning_message=text(), preview_message=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", [None, dict(), lambda **_: dict()])
def test_warning_message_is_included(default_deprecator, parameter_map, warning_message, preview_message):
    with warnings.catch_warnings(record=True) as w:
        default_deprecator.docstring_generator = lambda **_: ''
        default_deprecator.warning_generator = lambda **_: warning_message
        default_deprecator.preview_generator = lambda **_: preview_message

        @default_deprecator.deprecated('0.1', parameter_map=parameter_map)
        def func():
            """summary line"""
            pass

        func()

        assert DeprecationWarning is w[-1].category
        assert warning_message in str(w[-1].message)
        if preview_message:
            assert preview_message in str(w[-1].message)


@given(docstring_message=text(), preview_message=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", [None, dict(), lambda **_: dict()])
def test_docstring_not_changed_before_deprecated(default_deprecator, parameter_map, docstring_message, preview_message):
    default_deprecator.docstring_generator = lambda **_: docstring_message
    default_deprecator.warning_generator = lambda **_: ''
    default_deprecator.preview_generator = lambda **_: preview_message

    @default_deprecator.deprecated('1.1', parameter_map=parameter_map)
    def func():
        """summary line"""
        pass

    assert func.__doc__ == """summary line"""


@given(warning_message=text(), preview_message=one_of(none(), text()))
@pytest.mark.parametrize("parameter_map", [None, dict(), lambda **_: dict()])
def test_no_warning_before_deprecated(default_deprecator, parameter_map, warning_message, preview_message):
    with warnings.catch_warnings(record=True) as w:
        default_deprecator.docstring_generator = lambda **_: ''
        default_deprecator.warning_generator = lambda **_: warning_message
        default_deprecator.preview_generator = lambda **_: preview_message

        @default_deprecator.deprecated('1.1', parameter_map=parameter_map)
        def func():
            """summary line"""
            pass

        func()

        assert not w


def _migrate_func(old_kwarg=None):
    return dict(new_kwarg=old_kwarg)


@pytest.mark.parametrize("parameter_map", [dict(old_kwarg='new_kwarg'),
                                           lambda old_kwarg=None: dict(new_kwarg=old_kwarg),
                                           _migrate_func])
def test_function_callable_with_old_kwargs(default_deprecator, parameter_map):
    kwarg = '--test--'

    @default_deprecator.deprecated('0.1', parameter_map=parameter_map)
    def func(arg, new_kwarg=None):
        """summary line"""
        return new_kwarg

    result = func('', old_kwarg=kwarg)

    assert result is kwarg


@pytest.mark.parametrize("parameter_map", [dict(old_kwarg='new_kwarg'),
                                           lambda old_kwarg=None: dict(new_kwarg=old_kwarg),
                                           _migrate_func])
def test_docstring_appended_with_old_kwargs(default_deprecator, parameter_map):
    @default_deprecator.deprecated('0.1', parameter_map=parameter_map)
    def func(arg, new_kwarg=None):
        """summary line"""
        pass

    assert ":param old_kwarg: Replaced by new_kwarg" in func.__doc__
