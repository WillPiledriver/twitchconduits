import asyncio
from typing import List, Dict
import hashlib
import secrets
import httpx
from .sub_versions import sub_dict


async def send_request(method: str, url: str, headers: Dict, json: Dict = None, params: Dict = None, retries: int = 3) -> Dict:
    """Send an HTTP request with retry logic."""
    async with httpx.AsyncClient() as client:
        for attempt in range(retries):
            try:
                response = await client.request(method, url, headers=headers, json=json, params=params)
                if response.status_code in {200, 202, 204}:
                    return response
                else:
                    print(f"Request failed: {response.status_code} - {response.text}")
                    return response
            except httpx.ConnectTimeout:
                if attempt < retries - 1:
                    print(f"Connection timed out. Retrying... (Attempt {attempt + 1}/{retries})")
                    await asyncio.sleep(1)
                else:
                    raise
    return response


class Subscription:
    """Subscription Class"""
    def __init__(self, sub_id, user_id):
        self.id = sub_id
        self.user_id = user_id
        self.status = None

    def to_dict(self):
        """Convert Subscription to dict"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status
        }


class User:
    """User class"""
    def __init__(self, key=None, user_id=None, ws=None, subscriptions=None):
        self.id = user_id
        self.key = key
        self.sub_dict = subscriptions
        self.ws = ws


class Users:
    """Users class"""
    def __init__(self):
        self.users = {}
        self.refresh_tokens = {}
        self.limbo = set()
    
    def add_user(self, key=None, user_id=None, ws=None, subscriptions=None):
        """Add a user to the users collection"""
        new_user = User(key, user_id, ws, subscriptions)
        self.users[user_id] = new_user
    
    def get_user(self, key):
        for k, d in self.users.items():
            if d.key == key:
                return self.users[k]
        return False



class Transport:
    """Transport class"""
    def __init__(self, callback_url, key="", secret=None):
        self.method = "webhook"
        self.key = key
        self.secret = secret or hashlib.sha256(f"{secrets.token_bytes(32).hex()}:{key}".encode()).hexdigest()
        self.callback = f"{callback_url}{self.secret}"

    def to_dict(self):
        """Return a dictionary"""
        return {
            "method": self.method,
            "callback": self.callback,
            "secret": self.secret
        }


class Shard:
    """Shard Class"""
    def __init__(self, shard_id, access_token, callback_url, key="", transport=None, session_id=None, status=None):
        self.id = shard_id
        self.key = key
        self.access_token = access_token
        self.transport = transport or Transport(callback_url=callback_url, key=key)
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


class Conduit:
    """Conduit Class"""
    def __init__(self, conduit_id, shard_count, access_token, client_id, callback_url):
        self.id = conduit_id
        self.shard_count = shard_count
        self.access_token = access_token
        self.callback_url = callback_url
        self.client_id = client_id
        self.shards: List[Shard] = []
        self.shards_dict = {}
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
        url = "https://api.twitch.tv/helix/eventsub/conduits"
        response = await send_request("PATCH", url, headers, json=data)
        if response.status_code == 200:
            print(f"Conduit {self.id} shard count updated to {shard_count}")
            self.shard_count = shard_count
            return self

    def make_dict(self):
        """Map the shards to a dictionary"""
        self.shards_dict = {shard.transport.secret: shard for shard in self.shards}

    async def delete_conduit(self):
        """Delete a Twitch EventSub conduit."""
        url = f"https://api.twitch.tv/helix/eventsub/conduits?id={self.id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        response = await send_request("DELETE", url, headers)
        if response.status_code == 204:
            print(f"Conduit {self.id} deleted successfully.")
            if self.on_delete:
                self.on_delete(self)
            return True

    async def get_shards(self, status=""):
        """Retrieve the shard information for a Conduit"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        url = "https://api.twitch.tv/helix/eventsub/conduits/shards"
        shards_data = []
        after = ""

        while True:
            params = {"conduit_id": self.id, "status": status, "after": after}
            response = await send_request("GET", url, headers, params=params)
            if response.status_code == 200:
                response = response.json()
                shards_data.extend(response.get("data", []))
                pagination = response.get("pagination", {})
                after = pagination.get("cursor")
                if not after:
                    break
            else:
                response.raise_for_status()

        self.shards = [
            Shard(
                shard_id=s["id"],
                access_token=self.access_token,
                transport=Transport(callback_url=self.callback_url, secret=s["transport"]["callback"].rsplit('/', 1)[-1]),
                status=s["status"],
                callback_url=self.callback_url
            )
            for s in shards_data
        ]
        self.make_dict()
        return self.shards

    async def create_shard(self, key):
        """Create a new Shard"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }
        url = "https://api.twitch.tv/helix/eventsub/conduits/shards"
        if len(self.shards) == self.shard_count:
            await self.update_conduit(self.shard_count + 1)

        new_shard = Shard(len(self.shards), self.access_token, callback_url=self.callback_url, key=key)
        payload = {"conduit_id": self.id, "shards": [new_shard.to_dict()]}
        response = await send_request("PATCH", url, headers, json=payload)
        if response.status_code == 202:
            response = response.json()
            print(f"Shards created for conduit {self.id}")
            new_shard.update_from_dict(response)
            self.shards.append(new_shard)
            self.shards_dict[new_shard.transport.secret] = new_shard
            return response
        else:
            response.raise_for_status()

    async def create_subscriptions(self, subscriptions, condition):
        """Create multiple subscriptions concurrently"""
        async def create_single_subscription(subscription):
            """Helper function to create a single subscription"""
            if subscription in sub_dict:
                url = "https://api.twitch.tv/helix/eventsub/subscriptions"
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Client-Id": self.client_id,
                    "Content-Type": "application/json"
                }
                data = {
                    "type": subscription,
                    "version": sub_dict[subscription]["version"],
                    "condition": {k: d for k, d in condition.items() if k in sub_dict[subscription]["conditions"]},
                    "transport": {"method": "conduit", "conduit_id": self.id}
                }
                response = await send_request("POST", url, headers, json=data)
                if response.status_code == 202:
                    # print(f"Subscription '{subscription}' created successfully!")
                    return response.json()
            return (False, subscription)

        # Use asyncio.gather to create all subscriptions concurrently
        results = await asyncio.gather(*(create_single_subscription(sub) for sub in subscriptions))
        return results

    async def update_shards(self, shards):
        """Update shards for a Conduit"""
        url = "https://api.twitch.tv/helix/eventsub/conduits/shards"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }
        new_shards = [{key: value for key, value in s.items() if value is not None} for s in shards]
        data = {"conduit_id": self.id, "shards": new_shards}
        r = await send_request("PATCH", url, headers, json=data)
        if r.status_code == 202:
            return r.json()
        else:
            r.raise_for_status()


class Conduits:
    """This is for handling Twitch Conduit requests"""
    def __init__(self, client_id, client_secret, callback_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = callback_url
        self.conduits: List[Conduit] = []
        self.access_token = None

    def _on_conduit_delete(self, conduit):
        """Handle a Conduit deletion event"""
        self.conduits.remove(conduit)

    async def get_access_token(self):
        """Retrieve an access token from Twitch"""
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = await send_request("POST", url, {}, params=params)
        if response.status_code == 200:
            response = response.json()
            self.access_token = response.get("access_token")
            return self.access_token

    async def get_conduits(self):
        """Retrieve a list of conduits"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        url = "https://api.twitch.tv/helix/eventsub/conduits"

        response = await send_request("GET", url, headers)
        response = response.json()
        conduits_data = response.get("data", [])

        self.conduits = [Conduit(conduit["id"], conduit["shard_count"], self.access_token, self.client_id, self.callback_url)
                         for conduit in conduits_data]

        return self.conduits
    
    async def get_subscriptions(self):
        """Retrieve the list of subscriptions for the current Conduits."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        url = "https://api.twitch.tv/helix/eventsub/subscriptions"
        subscriptions = []
        after = ""

        while True:
            params = {"after": after}
            response = await send_request("GET", url, headers, params=params)
            response = response.json()
            subscriptions.extend(response.get("data", []))
            pagination = response.get("pagination", {})
            after = pagination.get("cursor")
            if not after:
                break

        return subscriptions

    async def delete_subscription(self, sub_id: str):
        """Delete a specific subscription by ID."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id
        }
        url = f"https://api.twitch.tv/helix/eventsub/subscriptions?id={sub_id}"

        response = await send_request("DELETE", url, headers)
        if response.status_code ==  204:
            return True
        else:
            print(f"Failed to delete subscription {sub_id}. Response: {response.json()}")
            return False
        
    async def clean_up_subscriptions(self):
        """Remove all non-enabled subscriptions concurrently."""
        subscriptions = await self.get_subscriptions()
        to_delete = [sub["id"] for sub in subscriptions if sub["status"] != "enabled"]

        # Use asyncio.gather to delete all subscriptions concurrently
        results = await asyncio.gather(*(self.delete_subscription(sub_id) for sub_id in to_delete))

        # Filter and return the list of successfully deleted subscription IDs
        deleted_ids = [sub_id for sub_id, success in zip(to_delete, results) if success]
        return deleted_ids

    async def create_conduit(self, shard_count: int = 1) -> Conduit:
        """Create a Conduit"""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": self.client_id,
            "Content-Type": "application/json"
        }
        url = "https://api.twitch.tv/helix/eventsub/conduits"
        data = {"shard_count": shard_count}
        response = await send_request("POST", url, headers, json=data)
        if response.status_code == 200:
            response = response.json()
            print(f"Conduit created successfully: {response}")
            conduit = Conduit(
                conduit_id=response["data"][0]["id"],
                shard_count=response["data"][0]["shard_count"],
                access_token=self.access_token,
                client_id=self.client_id,
                callback_url=self.callback_url
            )
            conduit.on_delete = self._on_conduit_delete
            self.conduits.append(conduit)
            return conduit
        else:
            response.raise_for_status()

    async def start(self):
        """Start the Conduits management by retrieving and refreshing Conduits and shards."""
        await self.get_access_token()
        await self.get_conduits()
        for conduit in self.conduits:
            await conduit.get_shards()
            conduit.on_delete = self._on_conduit_delete
