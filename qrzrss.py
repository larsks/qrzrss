from typing import Any, Callable

import os
import flask
import requests

from urllib.parse import urljoin


class QrzSession(requests.Session):
    base_url = "https://forums.qrz.com/"
    login_url = "https://www.qrz.com/login"

    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password
        self._authenticated = False

    def login(self):
        res = self.post(
            self.login_url, data={"username": self.username, "password": self.password}
        )
        res.raise_for_status()
        self._authenticated = True

    @property
    def authenticated(self):
        return self._authenticated

    def request(
        self,
        method: str,
        url: str,
        **kwargs,
    ):
        if "://" not in url:
            url = urljoin(self.base_url, url)

        return super().request(method, url, **kwargs)


def create_app():
    app = flask.Flask(__name__)
    proxy = QrzSession(
        username=os.environ["QRZ_USERNAME"], password=os.environ["QRZ_PASSWORD"]
    )

    @app.route("/healthz", methods=["GET"])
    def healthz():
        return flask.Response("OK\r\n", mimetype="text/plain")

    @app.route("/feed/<path:path>", methods=["GET"])
    def proxyrequest(path):
        for i in range(2):
            try:
                res = proxy.get(f"{path}?{flask.request.query_string.decode()}")
                res.raise_for_status()
            except Exception as err:
                if i == 0 and err.response.status_code == 403:
                    proxy.login()
                    continue

                raise

        return flask.Response(res.content, mimetype=res.headers["content-type"])

    return app
