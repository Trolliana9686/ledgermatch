from fastapi import FastAPI, UploadFile, File
import pandas as pd
from app.reconcile import reconcile_ledgers

app = FastAPI(title='LedgerMatch')

@app.get('/')
def r():
    return {
        'ok': True,
        'service': 'ledgermatch'
    }

@app.post('/reconcile')
async def reconcile(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    df1 = pd.read_csv(file1.file)
    df2 = pd.read_csv(file2.file)

    result = reconcile_ledgers(df1, df2)

    return result
