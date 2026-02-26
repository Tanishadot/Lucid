import logging
import sys
from typing import Optional


class LucidLogger:
    """Centralized logging configuration for LUCID"""
    
    def __init__(self, name: str = "lucid", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup console and file handlers"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        file_handler = logging.FileHandler('lucid.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        return self.logger


# Global logger instance
lucid_logger = LucidLogger()
logger = lucid_logger.get_logger()
