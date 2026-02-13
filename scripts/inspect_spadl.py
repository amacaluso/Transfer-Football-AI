import h5py
import numpy as np

path = 'notebooks/spadl.h5'
print('opening', path)
with h5py.File(path,'r') as f:
    def print_tree(g, indent=0):
        for k,v in g.items():
            t = 'dataset' if isinstance(v, h5py.Dataset) else 'group'
            print('  '*indent + f"- {k} ({t})")
            if isinstance(v, h5py.Group):
                print_tree(v, indent+1)
    print_tree(f)
    print('\nTop-level datasets info:')
    for name, obj in f.items():
        if isinstance(obj, h5py.Dataset):
            print(name, 'shape', obj.shape, 'dtype', obj.dtype)

    candidates = [k for k in f.keys() if 'label' in k.lower() or 'type' in k.lower() or 'action' in k.lower()]
    print('\nCandidate label datasets:', candidates)
    for c in candidates:
        try:
            data = f[c][:]
            print(f"\nDataset: {c}")
            print('  shape', data.shape, 'dtype', data.dtype)
            try:
                uniq = np.unique(data)
                print('  unique (first 50):', uniq[:50])
            except Exception as e:
                print('  Could not compute unique:', e)
        except Exception as e:
            print('  Could not read', c, e)

    def find_labels(g, path='/'):
        found = []
        for k,v in g.items():
            full = path + k
            if isinstance(v, h5py.Dataset) and ('label' in k.lower() or 'type' in k.lower() or 'action' in k.lower()):
                found.append((full, v))
            if isinstance(v, h5py.Group):
                found.extend(find_labels(v, full + '/'))
        return found

    labels = find_labels(f)
    if labels:
        print('\nLocated label-like datasets:')
        for p, ds in labels:
            print(' -', p, 'shape', ds.shape, 'dtype', ds.dtype)
    else:
        print('\nNo label-like datasets found in groups.')
