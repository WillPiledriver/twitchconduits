# Twitch Conduits Management

This Python module provides a set of classes and functions for managing Twitch EventSub conduits, shards, and subscriptions. The library uses `httpx` for asynchronous HTTP requests and supports creating, updating, deleting, and retrieving EventSub conduits and shards from the Twitch API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Sending HTTP Requests](#sending-http-requests)
  - [Managing Subscriptions](#managing-subscriptions)
  - [Creating and Managing Conduits](#creating-and-managing-conduits)
- [Classes and Functions](#classes-and-functions)
  - [Subscription](#subscription)
  - [User](#user)
  - [Users](#users)
  - [Transport](#transport)
  - [Shard](#shard)
  - [Conduit](#conduit)
  - [Conduits](#conduits)
- [License](#license)

## Installation

Make sure you have Python 3.7 or higher installed. You also need to install `httpx` for making asynchronous HTTP requests:

```bash
pip install httpx
```

## Usage
### Sending HTTP Requests

The `send_request` function sends an HTTP request with retry logic:

```python

from twitchconduits import send_request

response = await send_request("GET", "https://api.twitch.tv/helix/eventsub/conduits", headers={"Authorization": "Bearer YOUR_TOKEN"})
```

## Managing Subscriptions

The `Subscription` class represents an individual subscription, and you can manage subscriptions by using the `create_subscriptions` and `delete_subscription` methods in the `Conduits` class.

## Creating and Managing Conduits

To create a new Twitch EventSub conduit:
```python
from twitchconduits import Conduits

conduits_manager = Conduits(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET", callback_url="YOUR_CALLBACK_URL")
await conduits_manager.create_conduit(shard_count=1)
```

## Classes and Functions
### Subscription

A class representing a subscription for a user.

- `__init__(sub_id, user_id)`: Initializes the subscription with an ID and user ID.
- `to_dict()`: Converts the subscription instance to a dictionary.

### User

A class representing a user in the Twitch EventSub system.

- `__init__(key, user_id, subscriptions)`: Initializes a user with an optional key, user ID, and subscriptions.

### Users

A class for managing multiple users.

- `add_user(key, user_id, subscriptions)`: Adds a user to the collection.
- `get_user(key)`: Retrieves a user by their key.
- `remove_user(user_id)`: Removes a user by their user ID.

### Transport

Represents the transport configuration for a subscription or conduit.

- `__init__(callback_url, key, secret)`: Initializes the transport with a callback URL, key, and secret.
- `to_dict()`: Returns a dictionary representation of the transport.

### Shard

Represents a single shard in the EventSub system.

- `__init__(shard_id, access_token, callback_url, key, transport, session_id, status)`: Initializes a shard with its configuration details.
- `update_from_dict(data)`: Updates shard instance properties from a dictionary.
- `to_dict()`: Converts the shard instance to a dictionary.

### Conduit

Represents a Twitch EventSub conduit.

- `__init__(conduit_id, shard_count, access_token, client_id, callback_url)`: Initializes a conduit.
- `update_conduit(shard_count)`: Updates the shard count for a conduit.
- `delete_conduit()`: Deletes a conduit.
- `create_shard(key)`: Creates a new shard.

### Conduits

A class for handling multiple conduits.

- `get_access_token()`: Retrieves an access token from Twitch.
- `get_conduits()`: Fetches a list of conduits from Twitch.
- `clean_up_subscriptions()`: Removes all non-enabled subscriptions.
