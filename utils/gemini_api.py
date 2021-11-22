import time

import requests
import urllib3


urllib3.disable_warnings()


class GeminiAPI:
    """
    Convenience object wrapper for interfacing with the Gemini API.
    """
    def __init__(self):
        self.base_url = 'https://api.sandbox.gemini.com/'

    def base_get(self, uri_path, **kwargs):
        url = f"{self.base_url}{uri_path}"
        r = requests.get(url, verify=False, **kwargs)
        time.sleep(1)
        return r

    def get_sym_ticker(self, symbol):
        sym_ticker_uri = f"v2/ticker/{symbol}"
        r = self.base_get(sym_ticker_uri)
        return r

    def get_pub_ticker(self, symbol):
        pub_ticker_uri = f"v1/pubticker/{symbol}"
        r = self.base_get(pub_ticker_uri)
        return r

    def get_last_trade(self, symbol):
        trades_uri = f"v1/trades/{symbol}"
        parameters = {'limit_trades': '1'}
        r = self.base_get(trades_uri, params=parameters)
        return r

    def get_all_symbols(self):
        symbols_uri = f"v1/symbols"
        r = self.base_get(symbols_uri)
        return r
