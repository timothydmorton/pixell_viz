import os
import yaml

from .config import lambda_urlbase

__all__ = ['get_basenames', 'get_yaml', 'write_catalogs']


def get_basenames(ubername='ACTPol', bands=[148], fields=['D5', 'D6', 'D56'],
                  PAs=['PA1', 'PA2'], Ss=['S1', 'S2'], ways=[1, 4]):
    names = []
    for band in bands:
        for field in fields:
            for PA in PAs:
                for S in Ss:
                    if (S == 'S2' or PA == 'PA2') and (field != 'D56'):
                        continue
                    for way in ways:
                        if way == 1:
                            args = [ubername, band, field, PA, S,
                                    '{}way'.format(way)]
                            name = '{}_' * len(args)
                            name = name[:-1].format(*args)
                            names.append(name)
                        else:
                            for i in range(way):
                                split = 'split{}'.format(i)
                                args = [ubername, band, field, PA, S,
                                        '{}way'.format(way), split]
                                name = '{}_' * len(args)
                                name = name[:-1].format(*args)
                                names.append(name)
    return names


def get_yaml(basename,
             maps=['I', 'Q', 'U', 'hits', 'noise', 'I_src_free',
                   'risingscans_hits', 'settingscans_hits'],
             urlbase=lambda_urlbase):
    """YAML string of ActPol intake catalog
    """
    sources = {}
    for m in maps:
        name = basename + '_{}'.format(m)
        d = {'driver': 'fits_array',
             'cache': [{'argkey': 'url', 'type': 'file'}],
             'args': {'url': urlbase + '{}.fits'.format(name)},
             'direct_access': 'force'}
        sources[m] = d

    s = yaml.dump({'sources': sources})
    return s


def write_catalogs(rootdir='.', basenames=None, **kwargs):
    if not os.path.exists(rootdir):
        os.makedirs(rootdir)

    if basenames is None:
        basenames = get_basenames(**kwargs)

    for basename in basenames:
        with open(os.path.join(rootdir, '{}.yaml'.format(basename)), 'w') as fout:
            fout.write(get_yaml(basename))

