import numpy as np
import xarray as xr

from .data import CMBData


class PlanckData(CMBData):

    def _get_dataarray(self, source):
        arr = source.read()[0, :, :].astype(float)
        wcs = source.wcs
        ra, dec = self._get_coord_axes(arr, wcs)
        return xr.DataArray(arr, dims=self._axis_order,
                            coords={'ra': ra, 'dec': dec}, name=source.name)

    def _get_coord_axes(self, arr, wcs):
        ra = (np.arange(arr.shape[1]) - 21601 + 1) / -120.
        dec = (np.arange(arr.shape[0]) - 7561 + 1) / 120.
        return ra, dec
