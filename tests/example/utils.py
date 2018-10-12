from pyoneering import DevUtils
from tests.example import __version__

_module = DevUtils(__version__)
deprecated, refactored = _module.deprecated, _module.refactored
