import requests
from tracer.config import CFG


HEADERS={"Content-Type":"application/json"}
if CFG.SURF_API_KEY:
    HEADERS["Authorization"]=f"Bearer {CFG.SURF_API_KEY}"
def send_surf_prompt(model:str,prompt:str,max_tokens:int|None=None,temperature:float=0.8)->str:
    payload={"model":model,"prompt":prompt,"temperature":temperature}
    if max_tokens:
        payload["max_tokens"]=max_tokens
    r=requests.post(CFG.SURF_URL,headers=HEADERS,json=payload)
    r.raise_for_status()
    return r.json()["choices"][0]["text"]
