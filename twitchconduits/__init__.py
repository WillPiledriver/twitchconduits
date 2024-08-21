import asyncio
from typing import List, Dict
import hashlib
import secrets
import httpx


class Transport():
    """Transport class"""
    def __init__(self, callback_url, key="", secret=None):
        self.method = "webhook"
        self.key = key
        if secret is None:
            self.secret = hashlib.sha256(f"{secrets.token_bytes(32).hex()}:{key}".encode()).hexdigest()
        else:
            self.secret = secret
        self.callback = f"{callback_url}{self.secret}"

    def to_dict(self):
        """Return a dictionary"""
        return {
            "method": self.method,
            "callback": self.callback,
            "secret": self.secret
        }


class Shard():
    """Shard Class"""
    def __init__(self, shard_id, access_token, callback_url, key="", transport=None, session_id=None, status=None):
        self.id = shard_id
        self.key = key
        self.access_token = access_token
        if transport is None:
            self.transport = Transport(callback_url=callback_url, key=key)
        else:
            self.transport = transport
        self.session_id = session_id
        self.status = status

    def update_from_dict(self, data: dict):
        """Update Shard instance from a dictionary."""
        self.id = data.get("id", self.id)
        self.status = data.get("status", self.status)
        self.session_id = data.get("session_id", self.session_id)

        transport_data = data.get("transport", {})
        if transport_data:
            self.transport.method = transport_data.get("method", self.transport.method)
            self.transport.callback = transport_data.get("callback", self.transport.callback)
            self.transport.secret = transport_data.get("secret", self.transport.secret)

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
    def __init__(self, conduit_id, shard_count, access_token, client_id, callback_url):
        self.id = conduit_id
        self.shard_count = shard_count
        self.access_token = access_token
        self.callback_url = callback_url
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

        while True:  # Loop until successful
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.patch(
                        "https://api.twitch.tv/helix/eventsub/conduits",
                        headers=headers,
                        json=data
                    )

                if response.status_code == 200:
                    print(f"Conduit {self.id} shard count updated to {shard_count}")
                    self.shard_count = shard_count
                    return self
                response.raise_for_status()
            except httpx.ConnectTimeout:
                print("Connection timed out. Retrying...")
                await asyncio.sleep(1)

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

    async def get_shards(self, status=""):
        """Retrieve the shard information for a Conduit"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }

        async with httpx.AsyncClient() as client:
            shards_data = []
            after = ""
            while True:
                try:
                    response = await client.get(
                        "https://api.twitch.tv/helix/eventsub/conduits/shards",
                        headers=headers,
                        params={"conduit_id": self.id, "status": status, "after": after}
                    )

                    if response.status_code == 200:
                        r = response.json()
                        shards_data.extend(r["data"])
                        pagination = r.get("pagination", {})

                        # Update `after` if there's a cursor for pagination
                        if "cursor" in pagination:
                            after = pagination["cursor"]
                        else:
                            break  # Exit the loop if no more pages

                    else:
                        response.raise_for_status()

                except httpx.ConnectTimeout:
                    print("Connection timed out. Retrying...")
                    await asyncio.sleep(1)

        # Transform the shard data into Shard objects
        fixed_shards = [
            Shard(
                shard_id=s["id"],
                access_token=self.access_token,
                transport=Transport(callback_url=self.callback_url,
                                    secret=s["transport"]["callback"].rsplit('/', 1)[-1]),
                status=s["status"],
                callback_url=self.callback_url
            )
            for s in shards_data
        ]

        return fixed_shards

    async def create_shard(self, key):
        """Create a new Shard"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }

        if len(self.shards) == self.shard_count:
            await self.update_conduit(self.shard_count+1)
        new_shard = Shard(len(self.shards), self.access_token, key)

        payload = {
            "conduit_id": self.id,
            "shards": [new_shard.to_dict()]
        }

        while True:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.patch(
                        "https://api.twitch.tv/helix/eventsub/conduits/shards",
                        headers=headers,
                        json=payload
                    )

                if response.status_code == 202:
                    print(f"Shards created for conduit {self.id}")
                    new_shard.update_from_dict(response.json())
                    self.shards.append(new_shard)
                    return response.json()
                print(response.json())
                response.raise_for_status()
            except httpx.ConnectTimeout:
                print("Connection timed out. Retrying...")
                await asyncio.sleep(1)

    async def update_shards(self, shards):
        """Update shards for a Conduit"""
        url = "https://api.twitch.tv/helix/eventsub/conduits/shards"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }

        new_shards = []
        for i, s in enumerate(shards):
            cleaned_shard = {key: value for key, value in s.items() if value is not None}
            new_shards.append(cleaned_shard)

        data = {
            "conduit_id": self.id,
            "shards": new_shards
        }

        async with httpx.AsyncClient() as client:
            while True:
                try:
                    response = await client.patch(
                        url,
                        headers=headers,
                        json=data
                    )

                    if response.status_code == 202:
                        print(f"Shards updated for conduit {self.id}")
                        return response.json()
                    else:
                        response.raise_for_status()

                except httpx.ConnectTimeout:
                    print("Connection timed out. Retrying...")
                    await asyncio.sleep(1)


class Conduits():
    """This is for handling Twitch Conduit requests"""
    def __init__(self, client_id, client_secret, callback_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
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
                                  self.access_token, self.client_id, callback_url=self.callback_url)
            new_conduit.on_delete = self._on_conduit_delete
            self.conduits.append(new_conduit)
            return new_conduit
        print(response.json())
        response.raise_for_status()

    async def start(self):
        """Start the conduit."""
        self.access_token = await self.get_app_access_token()
        conduits = await self.get_conduits()

        for conduit in conduits["data"]:
            c = Conduit(conduit["id"], conduit["shard_count"],
                        self.access_token, self.client_id,
                        callback_url=self.callback_url)
            c.on_delete = self._on_conduit_delete
            self.conduits.append(c)
