# pixell_viz
Interactive visualization of CMB maps

## Dependencies

```
conda install -c pyviz pyviz
conda install -c intake intake-astro
```

## Quickstart

```python
import intake
intake.output_notebook()

from actpol import get_dataset

basename = 'ACTPol_148_D6_PA1_S1_1way'  # e.g.
cat = intake.open_catalog('data/{}.yaml'.format(basename))
dataset = get_dataset(cat)
```

## Visualize

```python
import holoviews as hv
import hvplot.xarray
hv.extension('bokeh')

dataset['I'].hvplot.quadmesh('ra', 'dec', rasterize=True, width=800, height=400, grid=True)
```
