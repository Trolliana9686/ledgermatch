import pandas as pd

def reconcile_ledgers(df1: pd.DataFrame, df2: pd.DataFrame):
    df1['key'] = df1['amount'].astype(str) + df1['date'].astype(str)
    df2['key'] = df2['amount'].astype(str) + df2['date'].astype(str)

    matched = pd.merge(df1, df2, on='key', how='inner', suffixes=('_internal', '_external'))

    unmatched_internal = df1[~df1['key'].isin(df2['key'])]
    unmatched_external = df2[~df2['key'].isin(df1['key'])]

    return {
        "matched": len(matched),
        "unmatched_internal": len(unmatched_internal),
        "unmatched_external": len(unmatched_external)
    }
