import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv
from requests import Request, Session, Response
import time
import hmac

#https://github.com/ftexchange/ftx/blob/master/rest/client.py

class FtxClient:
    def __init__(self) -> None:
        load_dotenv()
        self._endpoint = os.getenv("API_URI")
        self._session = Session()
        self._api_key = os.getenv("API_KEY")
        self._api_secret = os.getenv("API_SECRET")
        

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._endpoint + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTXUS-KEY'] = self._api_key
        request.headers['FTXUS-SIGN'] = signature
        request.headers['FTXUS-TS'] = str(ts)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']