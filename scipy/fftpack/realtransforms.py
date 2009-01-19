"""
Real spectrum tranforms (DCT, DST, MDCT)
"""

__all__ = ['dct1', 'dct2']

import numpy as np
from scipy.fftpack import _fftpack

import atexit
atexit.register(_fftpack.destroy_ddct1_cache)
atexit.register(_fftpack.destroy_ddct2_cache)

def dct1(x, n=None, axis=-1, norm=None):
    """
    Return the Discrete Cosine Transform (type I) of arbitrary type sequence x.

    Parameters
    ----------
    x : array-like
        input array.
    n : int, optional
        Length of the transform.
    axis : int, optional
        axis over which to compute the transform.

    Returns
    -------
    y : real ndarray
    """
    return _dct(x, 1, n, axis, normalize=norm)

def dct2(x, n=None, axis=-1, norm=None):
    """
    Return the Discrete Cosine Transform (type II) of an arbitrary type
    sequence x.

    This is the most commonly used DCT, and corresponds to what is called 'the'
    DCT; in particular, dct2(x, norm='ortho') gives the same result as Matlab
    dct function

    Parameters
    ----------
    x : array-like
        input array.
    n : int, optional
        Length of the transform.
    axis : int, optional
        axis over which to compute the transform.
    norm : {None, 'ortho'}
        normalization mode (see Notes).

    Returns
    -------
    y : real ndarray

    Notes
    -----
    There are several definitions, we use the following (for norm=None):

                  N-1
        y[k] = 2* sum x[n]*cos(pi*k*(2n+1)/(2*N)), 0 <= k < N.
                  n=0

    If norm='ortho', y[k] is multiplied by a scaling factor f:

        f = sqrt(1/(4*N)) if k = 0
        f = sqrt(1/(2*N)) otherwise

    Which makes the corresponding matrix of coefficients orthonormal (OO' = Id).

    References
    ----------

    http://en.wikipedia.org/wiki/Discrete_cosine_transform

    'A Fast Cosine Transform in One and Two Dimensions', by J. Makhoul, in IEEE
    Transactions on acoustics, speech and signal processing.
    """
    return _dct(x, 2, n, axis, normalize=norm)

def dct3(x, n=None, axis=-1, norm=None):
    """
    Return Discrete Cosine Transform (type III) of arbitrary type sequence x.

    This is also called 'the' inverse DCT (IDCT) - dct3(x, norm='ortho') is
    exactly the same as the idct function of Matlab.
    
    Parameters
    ----------
    x : array-like
        input array.
    n : int, optional
        Length of the transform.
    axis : int, optional
        axis over which to compute the transform.
    norm : {None, 'ortho'}
        normalization mode (see Notes).

    Returns
    -------
    y : real ndarray

    Notes
    -----
    There are several definitions, we use the following (norm=None):

                          N-1
        y[k] = x[0] + 2 * sum x[n]*cos(pi*(k+0.5)*n/N), 0 <= k < N.
                          n=0

    Or (norm='ortho'), for 0 <= k < N:

                                            N-1
        y[k] = x[0] / sqrt(N) + sqrt(1/N) * sum x[n]*cos(pi*(k+0.5)*n/N)
                                            n=0

    The (unnormalized) DCT-III is the inverse of the (unnormalized) DCT-II, up
    to a factor 2*N. The orthonormalized DCT-III is exactly the inverse of the
    orthonormalized DCT-II.

    Examples
    --------
    >>> x = np.linspace(0, 9, 10)
    >>> np.testing.assert_array_almost_equal(dct3(dct2(x)) / 20, x)
    """
    return _dct(x, 3, n, axis, normalize=norm)

def _dct(x, type, n=None, axis=-1, overwrite_x=0, normalize=None):
    """
    Return Discrete Cosine Transform of arbitrary type sequence x.

    Parameters
    ----------
    x : array-like
        input array.
    n : int, optional
        Length of the transform.
    axis : int, optional
        Axis along which the dct is computed. (default=-1)
    overwrite_x : bool, optional
        If True the contents of x can be destroyed. (default=False)

    Returns
    -------
    z : real ndarray

    """
    tmp = np.asarray(x)
    if not np.isrealobj(tmp):
        raise TypeError,"1st argument must be real sequence"

    if n is None:
        n = tmp.shape[axis]
    else:
        raise NotImplemented("Padding/truncating not yet implemented")

    if tmp.dtype == np.double:
        if type == 1:
            f = _fftpack.ddct1
        elif type == 2:
            f = _fftpack.ddct2
        elif type == 3:
            f = _fftpack.ddct3
        else:
            raise ValueError("Type %d not understood" % type)
    elif tmp.dtype == np.float32:
        if type == 1:
            f = _fftpack.dct1
        elif type == 2:
            f = _fftpack.dct2
        elif type == 3:
            f = _fftpack.dct3
        else:
            raise ValueError("Type %d not understood" % type)
    else:
        raise ValueError("dtype %s not supported" % tmp.dtype)

    if normalize:
        if normalize == "ortho":
            nm = 1
        else:
            raise ValueError("Unknown normalize mode %s" % normalize)
    else:
        nm = 0

    if axis == -1 or axis == len(tmp.shape) - 1:
        return f(tmp, n, nm, overwrite_x)
    #else:
    #    raise NotImplementedError("Axis arg not yet implemented")

    tmp = np.swapaxes(tmp, axis, -1)
    tmp = f(tmp, n, nm, overwrite_x)
    return np.swapaxes(tmp, axis, -1)