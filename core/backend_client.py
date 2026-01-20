import requests
from auth_octopus.auth_octo_flow import AuthClient
from config import BASE_URL

class OctopusClient:
    def __init__(self):
        self.auth_client = AuthClient()
        self.token = self.auth_client.login()
        self.session = requests.Session()
        self._set_token(self.token)

    def _set_token(self, token: str):
        self.session.headers.update({
            "Authorization": token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def refresh_token(self):
        self.token = self.auth_client.login()
        self._set_token(self.token)

    def _request(self, method, url, **kwargs):
        resp = self.session.request(method, url, **kwargs)
        if resp.status_code == 401:
            self.refresh_token()
            resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def resolve_app_id(self, bundle: str) -> int:
        url = f"{BASE_URL}/api/apps"
        params = {
            "search": bundle,
            "status": "active",
            "orderBy": "keyId",
            "orderDirection": "desc"
        }
        resp = self._request("GET", url, params=params)
        apps = resp.json()["data"]["data"]

        for app in apps:
            if app.get("bundle") == bundle:
                return app["id"]
        raise Exception(f"App with bundle {bundle} not found")

    def get_uuid(self, app_id: int) -> str:
        url = f"{BASE_URL}/api/apps/{app_id}/postbacks?orderBy=date&orderDirection=desc"
        resp = self._request("GET", url)
        uuid = resp.json()["data"]["data"]
        uuid_user = uuid[0].get("client_uid")
        if not uuid_user:
            raise Exception(f"No client_uid in first postback for app_id {app_id}")
        return uuid_user

    def get_create_postback(self, app_id: int, uuid_user: str) -> dict | None:
        url = f"{BASE_URL}/api/apps/{app_id}/postbacks?orderBy=date&orderDirection=desc"
        resp = self._request("GET", url)
        postbacks = resp.json()["data"]["data"]
        for pb in postbacks:
            if pb.get("client_uid") != uuid_user:
                continue
            if pb.get("type") == "create":
                return pb
        return None

    def get_receive_postback(self, app_id: int, uuid_user: str) -> dict | None:
        url = f"{BASE_URL}/api/apps/{app_id}/postbacks?orderBy=date&orderDirection=desc"
        resp = self._request("GET", url)
        postbacks = resp.json()["data"]["data"]
        for pb in postbacks:
            if pb.get("client_uid") != uuid_user:
                continue
            if pb.get("type") == "receive":
                return pb
        return None

    def get_token_postback(self, app_id: int, uuid_user: str) -> dict | None:
        url = f"{BASE_URL}/api/apps/{app_id}/postbacks?orderBy=date&orderDirection=desc"
        resp = self._request("GET", url)
        postbacks = resp.json()["data"]["data"]
        for pb in postbacks:
            if pb.get("client_uid") != uuid_user:
                continue
            if pb.get("type") == "token":
                return pb
        return None

    def get_receive_app_instance_id(self, app_id: int, uuid_user: str) -> str | None:
        url = f"{BASE_URL}/api/apps/{app_id}/postbacks?orderBy=date&orderDirection=desc"
        resp = self._request("GET", url)
        postbacks = resp.json()["data"]["data"]
        receive_pb = None
        for pb in postbacks:
            if pb.get("client_uid") == uuid_user and pb.get("type") == "receive":
                receive_pb = pb
                break
        if not receive_pb:
            return None
        body_req = receive_pb.get("body_request", {})
        return body_req.get("app_instance_id") or body_req.get("appInstanceID")