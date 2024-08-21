"""Linter appeasement"""
# TODO: Update Conduit Shards

from typing import List, Dict
import hashlib
import secrets
import httpx

class Transport():
    """Transport class"""
    def __init__(self, key):
        self.method = "webhook"
        self.key = key
        self.secret = hashlib.sha256(f"{secrets.token_bytes(32).hex()}:{key}".encode()).hexdigest()
        self.callback = f"https://willpile.com/streamscripts/callback/{self.secret}"

    def to_dict(self):
        """Return a dictionary"""
        return {
            "method": self.method,
            "callback": self.callback,
            "secret": self.secret
        }

class Shard():
    """Shard Class"""
    def __init__(self, shard_id, access_token, key):
        self.id = shard_id
        self.key = key
        self.access_token = access_token
        self.transport = Transport(key)
        self.session_id = None
        self.status = None
    
    def to_dict(self):
        """Convert Shard object to a dictionary."""
        return {
            "id": self.id,
            "transport": self.transport.to_dict(),
            "status": self.status,
            "session_id": self.session_id,
        }

class Conduit():
    """Conduit Class"""
    def __init__(self, conduit_id, shard_count, access_token, client_id):
        self.id = conduit_id
        self.shard_count = shard_count
        self.access_token = access_token
        self.client_id = client_id
        self.shards : List[Shard] = []
        self.on_delete = None

    def to_dict(self) -> Dict:
        """Convert Conduit object to a dictionary."""
        return {
            "conduit_id": self.id,
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
            "id": self.id,
            "shard_count": shard_count
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch("https://api.twitch.tv/helix/eventsub/conduits",
                                          headers=headers, json=data)

        if response.status_code == 200:
            print(f"Conduit {self.id} shard count updated to {shard_count}")
            self.shard_count = shard_count
            return self
        print(response.json())
        response.raise_for_status()

    async def delete_conduit(self):
        """Delete a Twitch EventSub conduit."""

        url = f"https://api.twitch.tv/helix/eventsub/conduits?id={self.id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Conduit {self.id} deleted successfully.")
            if self.on_delete:
                self.on_delete(self)
            return True
        print(response.json())
        response.raise_for_status()

    async def get_shards(self, status="", after=""):
        """Retrieve the shard information for a Conduit"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.twitch.tv/helix/eventsub/conduits/shards?conduit_id={self.id}&status={status}&after={after}",
                headers=headers
            )

        if response.status_code == 200:
            shards_data = response.json()
            print(f"Shard information for conduit {self.id}: {shards_data}")
            return shards_data
        print(response.json())
        response.raise_for_status()
    
    async def create_shard(self):
        """Create a new Shard"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }

        new_shard = Shard(self.shard_count-1, self.access_token, "key")

        payload = {
            "conduit_id": self.id,
            "shards": [new_shard.to_dict()]
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                "https://api.twitch.tv/helix/eventsub/conduits/shards",
                headers=headers,
                json=payload
            )

        if response.status_code == 202:
            print(f"Shards created for conduit {self.id}")
            self.shard_count += 1
            return response.json()
        print(response.json())
        response.raise_for_status()

    async def update_shards(self):
        """Update Conduit Shards"""
        pass


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
        print(response.json())
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
        print(response.json())
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
        print(response.json())
        response.raise_for_status()

    async def start(self):
        """Start the conduit."""
        self.access_token = await self.get_app_access_token()
        print(self.access_token)
        conduits = await self.get_conduits()

        for conduit in conduits["data"]:
            self.conduits.append(Conduit(conduit["id"], conduit["shard_count"],
                                         self.access_token, self.client_id))
