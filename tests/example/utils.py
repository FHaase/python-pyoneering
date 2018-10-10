from pyoneering import DeprecationDecorators
from tests.example import __version__

_module = DeprecationDecorators(__version__)
deprecated, refactored = _module.deprecated, _module.refactored
