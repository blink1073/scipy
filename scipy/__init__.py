"""
SciPy: A scientific computing package for Python
================================================

Documentation is available in the docstrings and
online at http://docs.scipy.org.

Contents
--------
SciPy imports all the functions from the NumPy namespace, and in
addition provides:

Subpackages
-----------
Using any of these subpackages requires an explicit import.  For example,
``import scipy.cluster``.

::

 cluster                      --- Vector Quantization / Kmeans
 fftpack                      --- Discrete Fourier Transform algorithms
 integrate                    --- Integration routines
 interpolate                  --- Interpolation Tools
 io                           --- Data input and output
 lib                          --- Python wrappers to external libraries
 lib.lapack                   --- Wrappers to LAPACK library
 linalg                       --- Linear algebra routines
 misc                         --- Various utilities that don't have
                                  another home.
 ndimage                      --- n-dimensional image package
 odr                          --- Orthogonal Distance Regression
 optimize                     --- Optimization Tools
 signal                       --- Signal Processing Tools
 sparse                       --- Sparse Matrices
 sparse.linalg                --- Sparse Linear Algebra
 sparse.linalg.dsolve         --- Linear Solvers
 sparse.linalg.dsolve.umfpack --- :Interface to the UMFPACK library:
                                  Conjugate Gradient Method (LOBPCG)
 sparse.linalg.eigen.lobpcg   --- Locally Optimal Block Preconditioned
                                  Conjugate Gradient Method (LOBPCG) [*]
 special                      --- Airy Functions [*]
 lib.blas                     --- Wrappers to BLAS library [*]
 sparse.linalg.eigen          --- Sparse Eigenvalue Solvers [*]
 stats                        --- Statistical Functions [*]
 lib                          --- Python wrappers to external libraries
                                  [*]
 lib.lapack                   --- Wrappers to LAPACK library [*]
 integrate                    --- Integration routines [*]
 ndimage                      --- n-dimensional image package [*]
 linalg                       --- Linear algebra routines [*]
 spatial                      --- Spatial data structures and algorithms
 special                      --- Airy Functions
 stats                        --- Statistical Functions

Utility tools
-------------
::

 test              --- Run scipy unittests
 show_config       --- Show scipy build configuration
 show_numpy_config --- Show numpy build configuration
 __version__       --- Scipy version string
 __numpy_version__ --- Numpy version string

"""
from __future__ import division, print_function, absolute_import

__all__ = ['test']

import os as _os

if _os.name == 'nt':
    # prevent interference with KeyboardInterrupt on Windows
    # due to Fortran libraries
    # See stackoverflow for explanation:
    # http://stackoverflow.com/questions/15457786/ctrl-c-crashes-python-after-importing-scipy-stats
    import imp as _imp
    import ctypes as _ctypes

    def handler(sig):
        try:
            import _thread
        except ImportError:
            import thread as _thread
        _thread.interrupt_main()
        return 1

    # load numpy  math and fortran libraries (but do not import numpy)
    basepath = _imp.find_module('numpy')[1]
    _ctypes.CDLL(_os.path.join(basepath, 'core', 'libmmd.dll'))
    _ctypes.CDLL(_os.path.join(basepath, 'core', 'libifcoremd.dll'))
    # install handler
    routine = _ctypes.WINFUNCTYPE(_ctypes.c_int, _ctypes.c_uint)(handler)
    _ctypes.windll.kernel32.SetConsoleCtrlHandler(routine, 1)

    del _imp, _ctypes

del _os

from numpy import show_config as show_numpy_config
if show_numpy_config is None:
    raise ImportError("Cannot import scipy when running from numpy source directory.")
from numpy import __version__ as __numpy_version__

# Import numpy symbols to scipy name space
import numpy as _num
linalg = None
from numpy import *
from numpy.random import rand, randn
from numpy.fft import fft, ifft
from numpy.lib.scimath import *


__all__ += _num.__all__
__all__ += ['randn', 'rand', 'fft', 'ifft']

del _num
# Remove the linalg imported from numpy so that the scipy.linalg package can be
# imported.
del linalg
__all__.remove('linalg')

# We first need to detect if we're being called as part of the scipy
# setup procedure itself in a reliable manner.
try:
    __SCIPY_SETUP__
except NameError:
    __SCIPY_SETUP__ = False


if __SCIPY_SETUP__:
    import sys as _sys
    _sys.stderr.write('Running from scipy source directory.\n')
    del _sys
else:
    try:
        from scipy.__config__ import show as show_config
    except ImportError:
        msg = """Error importing scipy: you cannot import scipy while
        being in scipy source directory; please exit the scipy source
        tree first, and relaunch your python intepreter."""
        raise ImportError(msg)

    from scipy.version import version as __version__
    from scipy.lib._version import NumpyVersion as _NumpyVersion
    if _NumpyVersion(__numpy_version__) < '1.5.1':
        import warnings
        warnings.warn("Numpy 1.5.1 or above is recommended for this version of "
                      "scipy (detected version %s)" % __numpy_version__,
                      UserWarning)

    del _NumpyVersion

    from numpy.testing import Tester
    test = Tester().test
    bench = Tester().bench
