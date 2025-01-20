# BYOSnap Rewards

An example byosnap that rewards users on certain actions using Snapsers eventbus.

## Commands

Sync Snap

```bash
snapctl byosnap sync byosnap-rewards --path . --version v1.0.0 --snapend-id SNAPEND_ID
```


## Event Flow

Setup:
- `byosnap-rewards` registers a custom event of type `snapser.services.lobbies.joined`

1. A player joins a Lobby which triggers an event of type `snapser.services.lobbies.joined`
2. The `byosnap-rewards` listens for this event in it's event handler and 