"""Linter appeasement"""
# TODO: Get Shards, Update Conduits, Update Conduit Shards

from typing import List, Dict
import httpx

class Shard():
    """Shard Class"""
    def __init__(self):
        pass

class Conduit():
    """Conduit Class"""
    def __init__(self, conduit_id, shard_count, access_token, client_id):
        self.conduit_id = conduit_id
        self.shard_count = shard_count
        self.access_token = access_token
        self.client_id = client_id
        self.shards : List[Shard] = []
        self.on_delete = None

    def to_dict(self) -> Dict:
        """Convert Conduit object to a dictionary."""
        return {
            "conduit_id": self.conduit_id,
            "shard_count": self.shard_count
        }

    async def update_conduit(self, shard_count):
        """Update a Conduit's shard count"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }
        data = {
            "id": self.conduit_id,
            "shard_count": shard_count
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch("https://api.twitch.tv/helix/eventsub/conduits",
                                          headers=headers, json=data)

        if response.status_code == 200:
            print(f"Conduit {self.conduit_id} shard count updated to {shard_count}")
            self.shard_count = shard_count
            return self
        response.raise_for_status()

    async def delete_conduit(self):
        """Delete a Twitch EventSub conduit."""

        url = f"https://api.twitch.tv/helix/eventsub/conduits?id={self.conduit_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Conduit {self.conduit_id} deleted successfully.")
            if self.on_delete:
                self.on_delete(self)
            return True
        response.raise_for_status()

class Conduits():
    """This is for handling Twitch Conduit requests"""
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.conduits : List[Conduit] = []
        self.access_token = None

    def _on_conduit_delete(self, conduit):
        """Callback for when a conduit is deleted."""
        if conduit in self.conduits:
            self.conduits.remove(conduit)

    async def get_app_access_token(self):
        """Retrieve the client credentials"""
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://id.twitch.tv/oauth2/token", data=payload)

        if response.status_code == 200:
            tokens = response.json()
            return tokens.get('access_token')
        response.raise_for_status()

    async def get_conduits(self):
        """Gets conduits list"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.twitch.tv/helix/eventsub/conduits",
                                        headers=headers)

        if response.status_code == 200:
            return response.json()
        response.raise_for_status()
        
    async def create_conduit(self, shard_count):
        """Create Conduit for webhooks"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }
        payload = {
            'shard_count': shard_count
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.twitch.tv/helix/eventsub/conduits",
                                         headers=headers, json=payload)

        if response.status_code == 200:
            r = response.json()
            new_conduit = Conduit(r["data"][0]["id"], r["data"][0]["shard_count"],
                                  self.access_token, self.client_id)
            new_conduit.on_delete = self._on_conduit_delete
            self.conduits.append(new_conduit)
            return new_conduit
        response.raise_for_status()

    async def start(self):
        """Start the conduit."""
        self.access_token = await self.get_app_access_token()
        print(self.access_token)
        conduits = await self.get_conduits()

        for conduit in conduits["data"]:
            self.conduits.append(Conduit(conduit["id"], conduit["shard_count"],
                                         self.access_token, self.client_id))
