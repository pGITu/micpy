from numpy.core.multiarray import normalize_axis_index
from numpy.core.numeric import normalize_axis_tuple
from numpy import AxisError
from .multiarray import array as micarray

def asarray(a, dtype=None, order=None):
    """Convert the input to an array.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major (C-style) or
        column-major (Fortran-style) memory representation.
        Defaults to 'C'.

    Returns
    -------
    out : ndarray
        Array interpretation of `a`.  No copy is performed if the input
        is already an ndarray with matching dtype and order.  If `a` is a
        subclass of ndarray, a base class ndarray is returned.

    See Also
    --------
    asanyarray : Similar function which passes through subclasses.
    ascontiguousarray : Convert input to a contiguous array.
    asfarray : Convert input to a floating point ndarray.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    asarray_chkfinite : Similar function which checks input for NaNs and Infs.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    Convert a list into an array:

    >>> a = [1, 2]
    >>> mp.asarray(a)
    array([1, 2])

    Existing arrays are not copied:

    >>> a = mp.array([1, 2])
    >>> mp.asarray(a) is a
    True

    If `dtype` is set, array is copied only if dtype does not match:

    >>> a = mp.array([1, 2], dtype=np.float32)
    >>> mp.asarray(a, dtype=np.float32) is a
    True
    >>> mp.asarray(a, dtype=np.float64) is a
    False

    Contrary to `asanyarray`, ndarray subclasses are not passed through:

    >>> issubclass(np.matrix, np.ndarray)
    True
    >>> a = mp.matrix([[1, 2]])
    >>> mp.asarray(a) is a
    False
    >>> mp.asanyarray(a) is a
    True

    """
    return micarray(a, dtype, copy=False, order=order)


def rollaxis(a, axis, start=0):
    """
    Roll the specified axis backwards, until it lies in a given position.

    Parameters
    ----------
    a : micpy.ndarray
        Input array.
    axis : int
        The axis to roll backwards.  The positions of the other axes do not
        change relative to one another.
    start : int, optional
        The axis is rolled until it lies before this position.  The default,
        0, results in a "complete" roll.

    Returns
    -------
    res : micpy.ndarray
        a view of `a` is always returned.

    See Also
    --------
    moveaxis : Move array axes to new positions.
    roll : Roll the elements of an array by a number of positions along a
        given axis.

    Examples
    --------
    >>> a = mp.ones((3,4,5,6))
    >>> mp.rollaxis(a, 3, 1).shape
    (3, 6, 4, 5)
    >>> mp.rollaxis(a, 2).shape
    (5, 3, 4, 6)
    >>> mp.rollaxis(a, 1, 4).shape
    (3, 5, 6, 4)

    """
    n = a.ndim
    axis = normalize_axis_index(axis, n)
    if start < 0:
        start += n
    msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
    if not (0 <= start < n + 1):
        raise AxisError(msg % ('start', -n, 'start', n + 1, start))
    if axis < start:
        # it's been removed
        start -= 1
    if axis == start:
        return a.view()
    axes = list(range(0, n))
    axes.remove(axis)
    axes.insert(start, axis)
    return a.transpose(axes)


def moveaxis(a, source, destination):
    """
    Move axes of an array to new positions.

    Other axes remain in their original order.

    .. versionadded::1.11.0

    Parameters
    ----------
    a : np.ndarray
        The array whose axes should be reordered.
    source : int or sequence of int
        Original positions of the axes to move. These must be unique.
    destination : int or sequence of int
        Destination positions for each of the original axes. These must also be
        unique.

    Returns
    -------
    result : np.ndarray
        Array with moved axes. This array is a view of the input array.

    See Also
    --------
    transpose: Permute the dimensions of an array.
    swapaxes: Interchange two axes of an array.

    Examples
    --------

    >>> x = np.zeros((3, 4, 5))
    >>> np.moveaxis(x, 0, -1).shape
    (4, 5, 3)
    >>> np.moveaxis(x, -1, 0).shape
    (5, 3, 4)

    These all achieve the same result:

    >>> np.transpose(x).shape
    (5, 4, 3)
    >>> np.swapaxes(x, 0, -1).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1], [-1, -2]).shape
    (5, 4, 3)
    >>> np.moveaxis(x, [0, 1, 2], [-1, -2, -3]).shape
    (5, 4, 3)

    """
    try:
        # allow duck-array types if they define transpose
        transpose = a.transpose
    except AttributeError:
        a = asarray(a)
        transpose = a.transpose

    source = normalize_axis_tuple(source, a.ndim, 'source')
    destination = normalize_axis_tuple(destination, a.ndim, 'destination')
    if len(source) != len(destination):
        raise ValueError('`source` and `destination` arguments must have '
                         'the same number of elements')

    order = [n for n in range(a.ndim) if n not in source]

    for dest, src in sorted(zip(destination, source)):
        order.insert(dest, src)

    result = transpose(order)
    return result
