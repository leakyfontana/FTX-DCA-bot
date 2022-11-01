import os
from dotenv import load_dotenv
from requests import Request, Session
import time
import hmac

def get(endpoint):
    load_dotenv()

    ftx = os.getenv("API_URI")
    apikey = os.getenv("API_KEY")
    apisecret = os.getenv("API_SECRET")

    ts = int(time.time() * 1000)
    session = Session()
    request = Request('GET', ftx+endpoint)
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(apisecret.encode(), signature_payload, 'sha256').hexdigest()

    prepared.headers[f'FTXUS-KEY'] = apikey
    prepared.headers[f'FTXUS-SIGN'] = signature
    prepared.headers[f'FTXUS-TS'] = str(ts)

    response = session.send(prepared)
    return response.json()

def post(endpoint, payload):
    load_dotenv()

    ftx = os.getenv("API_URI")
    apikey = os.getenv("API_KEY")
    apisecret = os.getenv("API_SECRET")

    ts = int(time.time() * 1000)
    session = Session()
    request = Request('POST', ftx+endpoint)
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(apisecret.encode(), signature_payload, 'sha256').hexdigest()

    prepared.headers[f'FTXUS-KEY'] = apikey
    prepared.headers[f'FTXUS-SIGN'] = signature
    prepared.headers[f'FTXUS-TS'] = str(ts)

    response = session.send(prepared)
    return response.json()