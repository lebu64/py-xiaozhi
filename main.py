import argparse
import asyncio
import sys

from src.application import Application
from src.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="XiaoZhi AI Client")
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Run mode: gui (graphical interface) or cli (command line)",
    )
    parser.add_argument(
        "--protocol",
        choices=["mqtt", "websocket"],
        default="websocket",
        help="Communication protocol: mqtt or websocket",
    )
    parser.add_argument(
        "--skip-activation",
        action="store_true",
        help="Skip activation process and start application directly (for debugging only)",
    )
    return parser.parse_args()


async def handle_activation(mode: str) -> bool:
    """Handle device activation process, depends on existing event loop.

    Args:
        mode: Run mode, "gui" or "cli"

    Returns:
        bool: Whether activation was successful
    """
    try:
        from src.core.system_initializer import SystemInitializer

        logger.info("Starting device activation process check...")

        system_initializer = SystemInitializer()
        # Use SystemInitializer's activation handling uniformly, adaptive to GUI/CLI
        result = await system_initializer.handle_activation_process(mode=mode)
        success = bool(result.get("is_activated", False))
        logger.info(f"Activation process completed, result: {success}")
        return success
    except Exception as e:
        logger.error(f"Activation process exception: {e}", exc_info=True)
        return False


async def start_app(mode: str, protocol: str, skip_activation: bool) -> int:
    """
    Unified entry point to start the application (executed in the existing event loop).
    """
    logger.info("Starting XiaoZhi AI Client")

    # Handle activation process
    if not skip_activation:
        activation_success = await handle_activation(mode)
        if not activation_success:
            logger.error("Device activation failed, program exiting")
            return 1
    else:
        logger.warning("Skipping activation process (debug mode)")

    # Create and start the application
    app = Application.get_instance()
    return await app.run(mode=mode, protocol=protocol)


if __name__ == "__main__":
    exit_code = 1
    try:
        args = parse_args()
        setup_logging()

        if args.mode == "gui":
            # In GUI mode, create QApplication and qasync event loop uniformly in main
            try:
                import qasync
                from PyQt5.QtWidgets import QApplication
            except ImportError as e:
                logger.error(f"GUI mode requires qasync and PyQt5 libraries: {e}")
                sys.exit(1)

            qt_app = QApplication.instance() or QApplication(sys.argv)

            loop = qasync.QEventLoop(qt_app)
            asyncio.set_event_loop(loop)
            logger.info("Created qasync event loop in main")

            with loop:
                exit_code = loop.run_until_complete(
                    start_app(args.mode, args.protocol, args.skip_activation)
                )
        else:
            # CLI mode uses standard asyncio event loop
            exit_code = asyncio.run(
                start_app(args.mode, args.protocol, args.skip_activation)
            )

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        exit_code = 0
    except Exception as e:
        logger.error(f"Program exited abnormally: {e}", exc_info=True)
        exit_code = 1
    finally:
        sys.exit(exit_code)