from collections import namedtuple

import inspect
import warnings
from functools import wraps
from packaging import version

__version__ = "0.22.0-dev"

Stage = namedtuple('Stage', ['name', 'in_version'])


def _sphinx_generator(**kwargs):
    return ".. deprecated :: {deprecated_in} {details}".format(**kwargs)


def _default_generator(**kwargs):
    return "{} since {}. {details}".format(kwargs['current_stage'].name.title(),
                                           kwargs['current_stage'].in_version,
                                           details=kwargs['details'])


def _default_preview_generator(**kwargs):
    if kwargs['next_stage']:
        return "Will be {} in {}.".format(kwargs['next_stage'].name.lower(),
                                          kwargs['next_stage'].in_version)
    else:
        return None


class Deprecator:

    def __init__(self, current_version, stages=None, docstring_generator=None, warning_generator=None,
                 preview_generator=None, parameter_generator=":param {old}: Replaced by {new}"):
        self.stages = stages or ['DEPRECATED', 'UNSUPPORTED', 'REMOVED']
        self.current_version = version.parse(current_version)
        self.docstring_generator = docstring_generator or _default_generator
        self.warning_generator = warning_generator or _default_generator
        self.preview_generator = preview_generator or _default_preview_generator
        self.parameter_generator = parameter_generator

    def _generate_deprecation(self, *version_identifiers):
        stages = list(map(lambda x: Stage(*x), zip(self.stages, map(version.parse, version_identifiers))))

        for current_stage, next_stage in zip(stages, stages[1:]):
            if current_stage.in_version >= next_stage.in_version:
                raise TypeError("Don't schedule {} in {} after {} in {}."
                                .format(current_stage.name.lower(), current_stage.in_version,
                                        next_stage.name.lower(), next_stage.in_version))

        next_stage = None
        for current_stage in reversed(stages):
            if current_stage.in_version <= self.current_version:
                return {"deprecated_in": version_identifiers[0], "current_stage": current_stage,
                        "next_stage": next_stage}
            next_stage = current_stage
        return None

    def _generate_messages(self, f, **kwargs):
        warning_message = " :: ".join([f.__name__, self.warning_generator(**kwargs)])
        docstring_message = self.docstring_generator(**kwargs)
        preview_next_stage = self.preview_generator(**kwargs)
        if preview_next_stage:
            warning_message = ' '.join([warning_message, preview_next_stage])
            docstring_message = ' '.join([docstring_message, preview_next_stage])
        return docstring_message, warning_message

    def deprecated_method(self, *version_identifiers, details=None):
        """Decorator to mark a class, function, staticmethod, classmethod or instancemethod as deprecated

        * Inserts information to the docstring describing the current (and next) deprecation stage.
        * Generates a `DeprecationWarning` if the decorator gets called.

        :parameter version_identifiers:
            Specify versions at which the decorated object is [DEPRECATED, UNSUPPORTED, REMOVED].
        :parameter details:
            Additional information to integrate in docstring
        :exception TypeError:
            If stages not in ascending order.
        """
        deprecation = self._generate_deprecation(*version_identifiers)

        def decorator(f):
            if not deprecation:
                return f

            docstring_message, warning_message = self._generate_messages(f, details=details, **deprecation)

            docstring = f.__doc__ or ""
            docstring = docstring.split('\n', 1)
            docstring.insert(1, docstring_message)
            docstring.insert(1, '\n')
            f.__doc__ = "\n".join(docstring)

            @wraps(f)
            def wrapper(*args, **kwargs):
                warnings.warn(warning_message, DeprecationWarning, stacklevel=3)
                return f(*args, **kwargs)

            return wrapper

        return decorator

    def deprecated_argspec(self, *version_identifiers, parameter_map, details=""):
        """Decorator to mark keyword arguments as deprecated

        * Replaces old keywords with new ones.
        * Generates a `DeprecationWarning` with if a deprecated keyword argument was passed.

        :param version_identifiers:
            Specify versions at which the decorated object is [DEPRECATED, UNSUPPORTED, REMOVED].
        :param parameter_map:
            If keyword arguments got renamed, pass a dict with (old_keyword=new_keyword) items.
            Otherwise pass a function with old_keywords and their default values as parameter which
            returns a dict of new_keywords mapped to new values.
        :param details:
            Additional information to integrate in docstring
        :exception TypeError:
            If stages not in ascending order.

        .. hint :: Valid versions passed to current_version and stages have to follow :pep:`440`

        """

        deprecation = self._generate_deprecation(*version_identifiers)

        def decorator(f):
            if not deprecation:
                return f

            docstring_message, warning_message = self._generate_messages(f, details=details, **deprecation)

            if inspect.isfunction(parameter_map):
                old_params = inspect.getfullargspec(parameter_map).args
                new_params = ', '.join(parameter_map().keys())

                deprecated_params = [self.parameter_generator.format(old=old, new=new_params) for old in old_params]
            elif isinstance(parameter_map, dict):
                deprecated_params = [self.parameter_generator.format(old=k, new=v) for k, v in parameter_map.items()]
            else:
                raise TypeError("parameter_map needs to be a dict or a function")

            f.__doc__ = "\n\n".join([f.__doc__, '\n'.join([docstring_message, '\n'.join(deprecated_params)])])

            @wraps(f)
            def wrapper(*args, **kwargs):
                if inspect.isfunction(parameter_map):
                    signature = inspect.signature(parameter_map)
                    old_kwargs = dict(
                        [(old_key, kwargs[old_key]) for old_key in signature.parameters if old_key in kwargs])
                    new_kwargs = parameter_map(**old_kwargs)
                else:
                    old_kwargs = dict(
                        [(old_key, kwargs[old_key]) for old_key in parameter_map if old_key in kwargs])
                    new_kwargs = dict([(new_key, kwargs[old_key]) for old_key, new_key in parameter_map.items()
                                       if old_key in kwargs])

                for key, value in inspect.signature(f).parameters.items():
                    if key in new_kwargs and new_kwargs[key] is value:
                        del new_kwargs[key]

                for key in old_kwargs.keys():
                    kwargs.pop(key)
                kwargs.update(new_kwargs)

                if old_kwargs:
                    migration_advice = [
                        ', '.join(str(inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, default=value))
                                  for key, value in parameters.items())
                        for parameters in [old_kwargs, new_kwargs]]
                    advice = " Replace ({}) with ({}).".format(*migration_advice)
                else:
                    advice = ""

                warnings.warn("".join([warning_message, advice]), DeprecationWarning, stacklevel=3)
                return f(*args, **kwargs)

            return wrapper

        return decorator

    def deprecated(self, *version_identifiers, parameter_map=None, details=""):
        """
        Calls either :func:`deprecated_method` or :func:`deprecated_argspec` if parameter_map is specified
        """
        if not parameter_map:
            return self.deprecated_method(*version_identifiers, details=details)
        return self.deprecated_argspec(*version_identifiers, parameter_map=parameter_map, details=details)
