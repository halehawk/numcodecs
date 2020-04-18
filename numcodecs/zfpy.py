_zfpy = None
try:
    import zfpy as _zfpy
except ImportError:  # pragma: no cover
    pass


if _zfpy:

    from .abc import Codec
    from .compat import ndarray_copy, ensure_contiguous_ndarray

    # noinspection PyShadowingBuiltins
    class ZFPY(Codec):
        """Codec providing compression using zfpy via the Python standard
        library.

        Parameters
        ----------
        mode : integer
            One of the zfpy mode choice, e.g., ``zfpy.FORMAT_XZ``.
        tolerance : double, optional
            A double-precision number, specifying the compression accuracy needed.
        preset : integer, optional
            An integer between 0 and 9 inclusive, specifying the compression
            level.
        filters : list, optional
            A list of dictionaries specifying compression filters. If
            filters are provided, 'preset' must be None.

        """

        codec_id = 'zfpy'

        def __init__(self, mode=_zfpy.mode_fixed_accuracy, tolerance=-1, rate=-1, precision=-1):
            self.mode = mode
            if mode == _zfpy.mode_fixed_accuracy:
               self.compression_kwargs = {
                   "tolerance" : tolerance
               }
            elif mode == _zfpy.mode_fixed_rate:
               self.compression_kwargs = {
                   "rate" : rate
               }
            elif mode == _zfpy.mode_fixed_precision:
               self.compression_kwargs = {
                   "precision" : precision
               }
            self.tolerance = tolerance
            self.rate = rate
            self.precision = precision

        def encode(self, buf):

            # normalise inputs
            buf = ensure_contiguous_ndarray(buf)

            # do compression
            return _zfpy.compress_numpy(buf, write_head=False, **self.compression_kwargs)

        def decode(self, buf, out=None):

            # normalise inputs
            buf = ensure_contiguous_ndarray(buf)
            if out is not None:
                out = ensure_contiguous_ndarray(out)

            # do decompression
            dec = _zfpy._decompress(buf, _zfpy.dtype_to_ztype(out.dtype),
                 out.shape, out=out)

            # handle destination
            return ndarray_copy(dec, out)

        def __repr__(self):
            if self.mode == _zfpy.mode_fixed_accuracy:
                r = '%s(mode=%r, tolerance=%s)' % (type(self).__name__, self.mode, self.tolerance)
            elif self.mode == _zfpy.mode_fixed_rate:
                r = '%s(mode=%r, rate=%s)' % (type(self).__name__, self.mode, self.rate)
            elif self.mode == _zfpy.mode_fixed_precision:
                r = '%s(mode=%r, precision=%s)' % (type(self).__name__, self.mode, self.precision)
            else:
                r="WRONG MODE"
            return r