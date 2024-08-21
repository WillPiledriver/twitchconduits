# Twitch EventSub Conduit Manager

This project is a Python-based utility for managing Twitch EventSub Conduits. It allows for the creation, retrieval, and deletion of conduits and their associated shards using Twitch's Helix API.

## Features

- **Conduit Management**: Create, retrieve, and delete Twitch EventSub Conduits.
- **Shard Handling**: Manage shards associated with conduits.
- **Async HTTP Requests**: Utilizes `httpx` for asynchronous API requests to Twitch.

## Classes

### `Shard`
Represents a shard associated with a conduit.

### `Conduit`
Represents a Twitch EventSub Conduit with methods to manage its lifecycle.

- **Attributes**:
  - `conduit_id`: Unique identifier for the conduit.
  - `shard_count`: Number of shards associated with the conduit.
  - `access_token`: OAuth token for API authentication.
  - `client_id`: Client ID for the Twitch app.
  - `shards`: List of `Shard` objects.

- **Methods**:
  - `delete_conduit()`: Deletes the conduit via the Twitch API.

### `Conduits`
Manages multiple `Conduit` objects and handles interactions with the Twitch API.

- **Attributes**:
  - `client_id`: Client ID for the Twitch app.
  - `client_secret`: Client Secret for the Twitch app.
  - `conduits`: List of `Conduit` objects.

- **Methods**:
  - `get_conduits()`: Fetches a list of existing conduits from Twitch.
  - `create_conduit(shard_count)`: Creates a new conduit with the specified number of shards.
  - `start()`: Initializes the manager by fetching conduits and retrieving an access token.

## Usage

1. **Install dependencies**:
    ```bash
    pip install httpx
    ```

2. **Initialize and Start**:

    ```python
    import asyncio
    from conduits import Conduits

    async def main():
        conduits_manager = Conduits(client_id="your_client_id", client_secret="your_client_secret")
        await conduits_manager.start()
    
    asyncio.run(main())
    ```

3. **Create a New Conduit**:
    ```python
    await conduits_manager.create_conduit(shard_count=2)
    ```

4. **Delete a Conduit**:
    ```python
    for conduit in conduits_manager.conduits:
        await conduit.delete_conduit()
    ```

## License

This project is licensed under the MIT License.
