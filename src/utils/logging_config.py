import logging
from logging.handlers import TimedRotatingFileHandler

from colorlog import ColoredFormatter


def setup_logging():
    """
    Configure logging system.
    """
    from .resource_finder import get_project_root

    # Use resource_finder to get project root directory and create logs directory
    project_root = get_project_root()
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    # Log file path
    log_file = log_dir / "app.log"

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)  # Set root log level

    # Clear existing handlers (avoid duplicate addition)
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Create daily rotating file handler
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",  # Rotate daily at midnight
        interval=1,  # Every 1 day
        backupCount=30,  # Keep 30 days of logs
        encoding="utf-8",
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.suffix = "%Y-%m-%d.log"  # Log file suffix format

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s[%(name)s] - %(levelname)s - %(message)s - %(threadName)s"
    )

    # Console color formatter
    color_formatter = ColoredFormatter(
        "%(green)s%(asctime)s%(reset)s[%(blue)s%(name)s%(reset)s] - "
        "%(log_color)s%(levelname)s%(reset)s - %(green)s%(message)s%(reset)s - "
        "%(cyan)s%(threadName)s%(reset)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={"asctime": {"green": "green"}, "name": {"blue": "blue"}},
    )
    console_handler.setFormatter(color_formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Output logging configuration information
    logging.info("Logging system initialized, log file: %s", log_file)

    return log_file


def get_logger(name):
    """Get uniformly configured logger.

    Args:
        name: Logger name, usually module name

    Returns:
        logging.Logger: Configured logger

    Example:
        logger = get_logger(__name__)
        logger.info("This is an info message")
        logger.error("An error occurred: %s", error_msg)
    """
    logger = logging.getLogger(name)

    # Add some helper methods
    def log_error_with_exc(msg, *args, **kwargs):
        """
        Log error and automatically include exception stack trace.
        """
        kwargs["exc_info"] = True
        logger.error(msg, *args, **kwargs)

    # Add to logger
    logger.error_exc = log_error_with_exc

    return logger
