# Twitch EventSub Conduit Manager

This project provides a Python-based solution to manage Twitch EventSub Conduits and their associated shards. The system allows for creating, updating, and deleting conduits and shards, and automates interactions with the Twitch API.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Classes and Methods](#classes-and-methods)
  - [Transport](#transport)
  - [Shard](#shard)
  - [Conduit](#conduit)
  - [Conduits](#conduits)
- [License](#license)

## Features

- **Manage Twitch EventSub Conduits:** Create, update, and delete conduits using the Twitch API.
- **Shard Management:** Dynamically create and update shards within conduits.
- **Retry Mechanism:** Automatic retries for API requests that experience timeouts.
- **Callback Handling:** Supports custom callback handling when conduits are deleted.

## Requirements

- Python 3.8+
- `httpx` for making asynchronous HTTP requests

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/twitch-conduit-manager.git
   cd twitch-conduit-manager
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   - `TWITCH_CLIENT_ID`: Your Twitch Client ID
   - `TWITCH_CLIENT_SECRET`: Your Twitch Client Secret

## Usage

To start using the Conduit Manager, you can follow the example below:

```python
import asyncio
from your_module import Conduits

async def main():
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    shard_count = 5

    conduits = Conduits(client_id, client_secret)
    await conduits.start()
    new_conduit = await conduits.create_conduit(shard_count)
    await new_conduit.create_shard("shard_key")

asyncio.run(main())
```

## Classes and Methods

### `Transport`

- **Attributes:**
  - `method`: The method used for the transport (default: `webhook`).
  - `key`: A unique key for identifying the transport.
  - `secret`: A generated SHA-256 hash secret.
  - `callback`: A URL callback for the transport.

- **Methods:**
  - `to_dict()`: Returns the transport data as a dictionary.

### `Shard`

- **Attributes:**
  - `id`: The shard ID.
  - `key`: A unique key for identifying the shard.
  - `access_token`: Twitch API access token.
  - `transport`: A `Transport` instance for the shard.
  - `session_id`: The session ID for the shard.
  - `status`: The status of the shard.

- **Methods:**
  - `update_from_dict(data)`: Updates the shard attributes from a dictionary.
  - `to_dict()`: Converts the shard object to a dictionary.

### `Conduit`

- **Attributes:**
  - `id`: The conduit ID.
  - `shard_count`: The number of shards in the conduit.
  - `access_token`: Twitch API access token.
  - `client_id`: The Twitch client ID.
  - `shards`: A list of `Shard` objects associated with the conduit.
  - `on_delete`: A callback function to be called when the conduit is deleted.

- **Methods:**
  - `to_dict()`: Converts the conduit object to a dictionary.
  - `update_conduit(shard_count)`: Updates the shard count for the conduit.
  - `delete_conduit()`: Deletes the conduit.
  - `get_shards(status)`: Retrieves the shard information.
  - `create_shard(key)`: Creates a new shard.
  - `update_shards()`: Placeholder method for updating shards.

### `Conduits`

- **Attributes:**
  - `client_id`: The Twitch client ID.
  - `client_secret`: The Twitch client secret.
  - `conduits`: A list of `Conduit` objects.
  - `access_token`: Twitch API access token.

- **Methods:**
  - `_on_conduit_delete(conduit)`: A callback function that removes the conduit from the list when deleted.
  - `get_app_access_token()`: Retrieves the Twitch application access token.
  - `get_conduits()`: Retrieves the list of conduits.
  - `create_conduit(shard_count)`: Creates a new conduit with the specified shard count.
  - `start()`: Initializes the Conduit Manager by retrieving the access token and existing conduits.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
