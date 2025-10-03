from typing import Any, Optional

from src.constants.constants import AbortReason, DeviceState
from src.plugins.base import Plugin


class UIPlugin(Plugin):
    """UI Plugin - Manages CLI/GUI display"""

    name = "ui"

    # Device state text mapping
    STATE_TEXT_MAP = {
        DeviceState.IDLE: "Standby",
        DeviceState.LISTENING: "Listening...",
        DeviceState.SPEAKING: "Speaking...",
    }

    def __init__(self, mode: Optional[str] = None) -> None:
        super().__init__()
        self.app = None
        self.mode = (mode or "cli").lower()
        self.display = None
        self._is_gui = False
        self.is_first = True

    async def setup(self, app: Any) -> None:
        """Initialize UI plugin"""
        self.app = app

        # Create corresponding display instance
        self.display = self._create_display()

        # Disable in-app console input
        if hasattr(app, "use_console_input"):
            app.use_console_input = False

    def _create_display(self):
        """Create display instance based on mode"""
        if self.mode == "gui":
            from src.display.gui_display import GuiDisplay

            self._is_gui = True
            return GuiDisplay()
        else:
            from src.display.cli_display import CliDisplay

            self._is_gui = False
            return CliDisplay()

    async def start(self) -> None:
        """Start UI display"""
        if not self.display:
            return

        # Bind callbacks
        await self._setup_callbacks()

        # Start display
        self.app.spawn(self.display.start(), name=f"ui:{self.mode}:start")

    async def _setup_callbacks(self) -> None:
        """Set up display callbacks"""
        if self._is_gui:
            # GUI needs to schedule to async tasks
            callbacks = {
                "press_callback": self._wrap_callback(self._press),
                "release_callback": self._wrap_callback(self._release),
                "auto_callback": self._wrap_callback(self._auto_toggle),
                "abort_callback": self._wrap_callback(self._abort),
                "send_text_callback": self._send_text,
            }
        else:
            # CLI directly passes coroutine functions
            callbacks = {
                "auto_callback": self._auto_toggle,
                "abort_callback": self._abort,
                "send_text_callback": self._send_text,
            }

        await self.display.set_callbacks(**callbacks)

    def _wrap_callback(self, coro_func):
        """Wrap coroutine function as schedulable lambda"""
        return lambda: self.app.spawn(coro_func(), name="ui:callback")

    async def on_incoming_json(self, message: Any) -> None:
        """Handle incoming JSON messages"""
        if not self.display or not isinstance(message, dict):
            return

        msg_type = message.get("type")

        # Both tts/stt update text
        if msg_type in ("tts", "stt"):
            if text := message.get("text"):
                await self.display.update_text(text)

        # llm updates emotion
        elif msg_type == "llm":
            if emotion := message.get("emotion"):
                await self.display.update_emotion(emotion)

    async def on_device_state_changed(self, state: Any) -> None:
        """Handle device state changes"""
        if not self.display:
            return

        # Skip first call
        if self.is_first:
            self.is_first = False
            return

        # Update emotion and status
        await self.display.update_emotion("neutral")
        if status_text := self.STATE_TEXT_MAP.get(state):
            await self.display.update_status(status_text, True)

    async def shutdown(self) -> None:
        """Clean up UI resources, close window"""
        if self.display:
            await self.display.close()
            self.display = None

    # ===== Callback functions =====

    async def _send_text(self, text: str):
        """Send text to server"""
        if await self.app.connect_protocol():
            await self.app.protocol.send_wake_word_detected(text)

    async def _press(self):
        """Manual mode: Press to start recording"""
        await self.app.start_listening_manual()

    async def _release(self):
        """Manual mode: Release to stop recording"""
        await self.app.stop_listening_manual()

    async def _auto_toggle(self):
        """Auto mode toggle"""
        await self.app.start_auto_conversation()

    async def _abort(self):
        """Interrupt conversation"""
        await self.app.abort_speaking(AbortReason.USER_INTERRUPTION)
