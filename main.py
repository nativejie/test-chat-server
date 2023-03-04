from fastapi import FastAPI, Body, Header
from V1 import Chatbot
from starlette.responses import StreamingResponse
import time
import redis
from pydantic import BaseModel

app = FastAPI();

r = redis.Redis(host='localhost', port=6379, db=1)
chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..y0I3wSxCPpx-dwPX.Xg5j0Xb3779S28-VGN6lWSBwnzcGATeetQX61lMpk-yq8DzmySLJ1Wsb3r4zdxYVs-uVhb7fY7mgK3f7NUqt8OxDJhuKCsKcogL4ABD2YHGlgSvIYqrHNh4dUgVR0DrFJZ7A_lhKCglJgV9ix_aERSyK82ElqQjvAviSqI7j2ok-E2Ump11YV5x_U2UI4FTVLG1t1oT1uQv-rVJsdjcwyxK82OB9-hq6edi1JP62fUyRfmVMKESfbbrxqj6ygYOi925WinzLE52cJCLNRauzP6ygK6H8_--OO2QqXj8xl_xk8VF716JDtW7hX077xde3KJH5TcM5ZG8WSjk1v5Hrx_OUH266s0Q9N-qafdvrJq84GI1lFhkZPkQq3Vrgr5pu1fmysSqamlVtmMqgxR3SJGDuHSNZNcC-LHGFjJXJG6jJ6vcSDF1EgX_-A4aGGOrKICMMHGCkHKD2FiHEBoQ9iispnzu-jAMsmwoIfTGQ8O2-4RGE0mKCVvNP4IwSbCWUsCUZujyhrN4UooIc2NCXmZrs4eDeTHNiixwjdzGaEhdTojIt7FnjvxjuLKvG2lJOyF22_kLbpoLAltomv6WVJxazcPqpFiJ90HPCdmi4owiWmQ1oro5diVYk_h4IzkWJc73kGfVu9EQKj2N-nd9JC9kU3jJoVnwtMcl8NXy1Ewa-7IOMxwwzpNfkAFxsCywhWUoPPLgRAU7pPb3QvnZRb7gtg2AMcUUM0AEWAinh43rwWwQqJp9VJs_dzVoXLd2VZMxovjEjJpEiLLALH5tjDSgMFmV6a1bBqigo5j83qDtvs6uivgXD-hXTkOGioMQvXehTwsVoSxnQgCHUAMmyT3VAz3fjxPjdowSVq-36h96A6gEmUXf_JGj2_etGmsFi1MkowhkBG-PJ2FImS7K2umH7DMaUyx04FZDfq3Bn0WIHB9XWHNdIItSGKFZoZaUM-j_gtdGMuciJIfmE0S1TxOwHNQ0FvqRMq-q6t5U-ITeTStny3oXEpv0djBPVvNoPx8fUd01wjVX1Rj1BcN65-5qeZHYdm1hImjrKH9MCkdJC5m1bspEpJrd4VpkUD6HiPKbyf1PR6GnVbLqKu5q6SXQDFMpPw2tO__KxaxJzUmbDbHrwSQTyhTxH9AalukE2xTwJZJMHpeMg3Ltj2N6wxvJog8C11CYyiYSQmzca-BNFyjw_fcXbEz-09cLPtvFa640gfqzF5OijP-PX4suH4vPYZWwPsKgqc0Qjqq2s-w9PoDUar2zQfNdHkuxSYO3eC0dmFyWzKpBJd6iNCujnhdBZyIhrpPdwNLplVDW6Hk2vEmrAEsGuBoftflc6-KSZfk06VQo2OorkE8UTi3LfeTq6n0Hk82gY9rt1JSdt3M4taQGlPmDZY4C2D8jlTgVfGDlK1BcCCLfHb2592tuBwWFVgvUol8jgTe5ut570MKFrk4uNRmEF77kDhz_tz-jIQp0H1Zqzv_1UO3QPJCUDiBp4RttJyLWo5_8ZTKDv3a_CGdjL2-cFDNGxVq3Me_ph1l3B8LsYUDelw8sSoWGmg7W-jA-ZibbdBWMQWAGNESOsbyeOE81oqRXvWLQZrP7x1cWgQtvb9UXhQIpJEVgSmezoE3j39iM9pJJUxDDj0aO1MLyopW231j6EQ2Tt7n3WGMTGK3c0SOtW9RCeLrwEfOsURl-rPMnBVtE2Hj9NcBMA1y0_c-QSMEpvZeU-JZzon7NAdR_T5vCgAuayNEAmsDVDQiSPCBFbCnMCbUXlIR7Sp5OMuD-50AbeETTTXDO9m3IY6NTluMpQrIdT-1uLcpWYCi6H4MIz_QcfUj0vYQgeyt255uTAEI7O0QhsdJesMzBmkDSUgYoToU8pF1ZtjqFaxn-RIb6wGG6trpDbyGAxVVjxh2zsDephuZ8AR7n_B-2MqX-fsuJhrh68hR45R8OZyNigEKjLHHNOEIcTZ8DTMzGtAmzKCrxL_noJkbFJecZ1ypG5_IM4pxETpnz1GOYDED6IfaxgTFspRCehFsHjJUfathSwY2o3feFX7_kh5PjmRzJb8oHVQqraELn8IOFob308S3UBnswFipLD6X6U0gJtxc4el9NRVrgkDMu-k6EYQHdniMCEGV65wP6TvEC2H3VvZC8GRLUnOixV4vJkVEDAjQOHmsEhZV56ZmydtF79PNB-1FOxT7xUDvAzZG9nS8YqzXKFnCLJnk9tZLqNXEyZQ96q_v_Yh-0-L9kvzHoi1Cv7lJh1TB2WYMejfEj4BU8Ej4_yruh9Go1Vw3qoR3N7I6v-1QuGsVUEHf7KflWDZ4huGjYsEFlzx5u3d8i36Q3iC8wcSzL2pZeX45UHytZATyoBn6EHtetmf9FFv5ajp44BRkhKKg3X4gE8mTTlS6CS1lM1r19Y3Z0yFqc_2qmcMQU97u0UpzkIhosgnvNV1YGDLcyaPoH4h8HW4adPLqEAlvgAw3-G1Su1k-UzakUtfIi7VQWHttIvaCqU0Mwe-qOnIujvVJoYWm7ljwPIW9WuWhEQimqM_J4HLFlI0Not1bNp9rkcIScVZA3DMg__tVF5njtkAtmL5L5pLDNifQHVDNA7Jihs_ol2N96QWHBi8Hzi55XKITgTeVqrxnr_9XasrUFLMPy9HpvneelUXB2x-sC9P6qky4kBVsXD.r4RWYNuQGTrCiMcsW75wEg"
})

class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hi!"}
    
<<<<<<< HEAD
def ask(question: str):
=======
def ask(question: str, auth_key: str ):
    print("Chatbot: ")
>>>>>>> 1d422db04cc222fade2a0050e6e279cea3f32ad8
    prev_text = ""
    result = ""
    for data in chatbot.ask(
        question,
        auth_key
    ):
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        prev_text = data["message"]
        result += prev_text
        yield message
    return result

@app.get('/get-conversations')
def get_conversations():
    return chatbot.get_conversations(0, 20)

@app.get('/bind')
def bind(key: str, unionid: str):
    if r.exists(key):
        return {"status": "error", "message": "激活码已经被绑定"}
    else:
        r.set(key, unionid, ex=30 * 24 * 60 * 60)
        return {"status": "success", "message": "绑定成功"}
    

@app.post("/events")
def events(message: str = Body(..., embed=True), auth_key: str = Header(default="")):
    if not r.exists(auth_key):
        return {"status": "error", "message": "无效的激活码或者激活码已经过期"}
    return ask(message, auth_key)
#     return StreamingResponse(ask(message), media_type="text/event-stream")
       

if __name__ == "__main__":
    print("Starting server...")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
