import numpy as np
import xarray as xr

from .config import default_map_limit


def get_dataarray(source, limit=default_map_limit):
    """Returns xarray DataArray corresponding to a fits_array data source

    Assumes perfectly rectangular WCS; that is, that it is appropriate to
    treat the pixel axes as ra/dec axes.
    """
    arr = source.read().clip(min=limit * -1, max=limit)
    wcs = source.wcs
    axis0 = wcs.all_pix2world(np.array([[0, i] for i in np.arange(arr.shape[0])]), 0)[:, 1]
    axis1 = wcs.all_pix2world(np.array([[i, 0] for i in np.arange(arr.shape[1])]), 0)[:, 0]
    return xr.DataArray(arr, dims=['dec', 'ra'], coords={'ra': axis1, 'dec': axis0}, name=source.name)


def get_dataset(catalog):
    data_values = {name: get_dataarray(src) for name, src in catalog.items()}
    return xr.Dataset(data_values)

