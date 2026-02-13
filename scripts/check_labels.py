import pandas as pd
import os, sys

fp = 'notebooks/labels.h5'
if not os.path.exists(fp):
    print(f"ERROR: file not found: {fp}")
    sys.exit(2)

with pd.HDFStore(fp) as s:
    keys = s.keys()
    print('HDF5 keys:')
    for k in keys:
        print(' -', k)
    print('\nSummary per key:')
    for k in keys:
        df = s[k]
        print(f'== {k}  rows={len(df)} cols={df.shape[1]}')
        all_constant = True
        for col in df.columns:
            try:
                nunique = df[col].nunique(dropna=False)
            except Exception:
                nunique = -1
            if nunique > 1:
                all_constant = False
            if pd.api.types.is_numeric_dtype(df[col]):
                ssum = int(df[col].sum())
            else:
                ssum = 'NA'
            vc = df[col].value_counts(dropna=False)
            top_vals = vc.index.tolist()[:5]
            top_counts = vc.tolist()[:5]
            print(f"  {col}: unique={nunique} sum={ssum} top={top_vals} counts={top_counts}")
        if all_constant:
            print('  -> ALL COLUMNS CONSTANT (identical values for all rows)')
        print()
