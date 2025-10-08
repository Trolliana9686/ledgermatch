from fastapi import FastAPI
app=FastAPI(title='LedgerMatch')
@app.get('/')
def r(): return {'ok':True,'service':'ledgermatch'}
