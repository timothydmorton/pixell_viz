import os

import numpy as np
import xarray as xr
import hvplot.xarray
import intake


class CMBData(object):
    _axis_order = ('dec', 'ra')

    def __init__(self, catalog_file):

        self.catalog_file = catalog_file
        self.catalog = intake.open_catalog(catalog_file)

        self._dataset = None

    def _get_coord_axes(self, arr, wcs):
        axis0 = wcs.all_pix2world(np.array([[0, i] for i in np.arange(arr.shape[0])]), 0)[:, 1]
        axis1 = wcs.all_pix2world(np.array([[i, 0] for i in np.arange(arr.shape[1])]), 0)[:, 0]

        if self._axis_order == ('ra', 'dec'):
            return (axis0, axis1)
        elif self._axis_order == ('dec', 'ra'):
            return (axis1, axis0)

    def _get_dataarray(self, source):
        arr = source.read().astype(float)
        wcs = source.wcs
        ra, dec = self._get_coord_axes(arr, wcs)
        return xr.DataArray(arr, dims=self._axis_order,
                            coords={'ra': ra, 'dec': dec}, name=source.name)

    @property
    def dataset(self):
        if self._dataset is None:
            data_values = {name: self._get_dataarray(src)
                           for name, src in self.catalog.items()}
            return xr.Dataset(data_values)

    def view(self, name=None, width=1000, height=400, **kwargs):
        if name is None:
            name = list(self.dataset.data_vars.keys())[0]
        if kwargs.get('datashade', False):
            rasterize = False
        else:
            rasterize = True
        image_kwargs = dict(rasterize=rasterize, width=width, height=height)
        image_kwargs.update(kwargs)
        return self.dataset[name].hvplot.image('ra', 'dec', **image_kwargs)

