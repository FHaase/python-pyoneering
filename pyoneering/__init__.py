__all__ = ['__version__', 'DevUtils']

from pkg_resources import get_distribution, DistributionNotFound

from pyoneering.devutils import DevUtils

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
