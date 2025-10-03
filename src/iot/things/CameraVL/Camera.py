import asyncio
import base64
import threading

import cv2

from src.application import Application
from src.constants.constants import DeviceState
from src.iot.thing import Thing
from src.iot.things.CameraVL import VL
from src.utils.logging_config import get_logger

logger = get_logger("Camera")


class Camera(Thing):
    def __init__(self):
        super().__init__("Camera", "Camera management")
        self.app = None
        """
        Initialize camera manager.
        """
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
        # Load configuration
        self.cap = None
        self.is_running = False
        self.camera_thread = None
        self.result = ""
        from src.utils.config_manager import ConfigManager

        self.config = ConfigManager.get_instance()
        # Camera controller
        VL.ImageAnalyzer.get_instance().init(
            self.config.get_config("CAMERA.VLapi_key"),
            self.config.get_config("CAMERA.Local_VL_url"),
            self.config.get_config("CAMERA.models"),
        )
        self.VL = VL.ImageAnalyzer.get_instance()

        self.add_property_and_method()  # Define device methods and state properties

    def add_property_and_method(self):
        # Define properties
        self.add_property("power", "Whether camera is on", lambda: self.is_running)
        self.add_property("result", "Content of recognized image", lambda: self.result)
        # Define methods
        self.add_method(
            "start_camera", "Turn on camera", [], lambda params: self.start_camera()
        )

        self.add_method(
            "stop_camera", "Turn off camera", [], lambda params: self.stop_camera()
        )

        self.add_method(
            "capture_frame_to_base64",
            "Recognize image",
            [],
            lambda params: self.capture_frame_to_base64(),
        )

    def _camera_loop(self):
        """
        Main loop for camera thread.
        """
        camera_index = self.config.get_config("CAMERA.camera_index")
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            logger.error("Cannot open camera")
            return

        # Set camera parameters
        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH, self.config.get_config("CAMERA.frame_width")
        )
        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT, self.config.get_config("CAMERA.frame_height")
        )
        self.cap.set(cv2.CAP_PROP_FPS, self.config.get_config("CAMERA.fps"))

        self.is_running = True
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                logger.error("Cannot read frame")
                break

            # Display frame
            cv2.imshow("Camera", frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.is_running = False

        # Release camera and close window
        self.cap.release()
        cv2.destroyAllWindows()

    def start_camera(self):
        """
        Start camera thread.
        """
        if self.camera_thread is not None and self.camera_thread.is_alive():
            logger.warning("Camera thread is already running")
            return

        self.camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
        self.camera_thread.start()
        logger.info("Camera thread started")
        return {"status": "success", "message": "Camera thread started"}

    def capture_frame_to_base64(self):
        """
        Capture current frame and convert to Base64 encoding.
        """
        if not self.cap or not self.cap.isOpened():
            logger.error("Camera not opened")
            return None

        ret, frame = self.cap.read()
        if not ret:
            logger.error("Cannot read frame")
            return None

        # Convert frame to JPEG format
        _, buffer = cv2.imencode(".jpg", frame)

        # Convert JPEG image to Base64 encoding
        frame_base64 = base64.b64encode(buffer).decode("utf-8")
        self.result = str(self.VL.analyze_image(frame_base64))
        # Get application instance
        self.app = Application.get_instance()
        logger.info("Image recognized successfully")
        self.app.set_device_state(DeviceState.LISTENING)
        asyncio.create_task(self.app.protocol.send_wake_word_detected("Broadcast recognition result"))
        return {"status": "success", "message": "Recognition successful", "result": self.result}

    def stop_camera(self):
        """
        Stop camera thread.
        """
        self.is_running = False
        if self.camera_thread is not None:
            self.camera_thread.join()  # Wait for thread to end
            self.camera_thread = None
            logger.info("Camera thread stopped")
            return {"status": "success", "message": "Camera thread stopped"}
