import asyncio
from typing import Any


class Plugin:
    """
    Minimal plugin base class: Provides asynchronous lifecycle hooks. Override as needed.
    """

    name: str = "plugin"

    def __init__(self) -> None:
        self._started = False

    async def setup(self, app: Any) -> None:
        """
        Plugin preparation phase (called early in application run).
        """
        await asyncio.sleep(0)

    async def start(self) -> None:
        """
        Plugin startup (typically called after protocol connection is established).
        """
        self._started = True
        await asyncio.sleep(0)

    async def on_protocol_connected(self, protocol: Any) -> None:
        """
        Notification when protocol channel is established.
        """
        await asyncio.sleep(0)

    async def on_incoming_json(self, message: Any) -> None:
        """
        Notification when JSON message is received.
        """
        await asyncio.sleep(0)

    async def on_incoming_audio(self, data: bytes) -> None:
        """
        Notification when audio data is received.
        """
        await asyncio.sleep(0)

    async def on_device_state_changed(self, state: Any) -> None:
        """
        Device state change notification (broadcast by application).
        """
        await asyncio.sleep(0)

    async def stop(self) -> None:
        """
        Plugin stop (called before application shutdown).
        """
        self._started = False
        await asyncio.sleep(0)

    async def shutdown(self) -> None:
        """
        Plugin final cleanup (called during application shutdown process).
        """
        await asyncio.sleep(0)
