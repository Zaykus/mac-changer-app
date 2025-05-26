import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, name: str = "MAC_Changer"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create file handler
        log_file = os.path.join(log_dir, f"mac_changer_{datetime.now():%Y%m%d}.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(fh)

    def set_log_level(self, level: str) -> None:
        """Set the log level dynamically."""
        level = level.upper()
        if level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            self.logger.setLevel(getattr(logging, level))
            for handler in self.logger.handlers:
                handler.setLevel(getattr(logging, level))
        else:
            self.logger.warning(f"Invalid log level: {level}")

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)

    def get_log_file(self) -> str:
        """Return the current log file path."""
        return self.logger.handlers[0].baseFilename
