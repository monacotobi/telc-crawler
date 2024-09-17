import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'message': record.getMessage(),
            'level': record.levelname,
            'time': self.formatTime(record, self.datefmt),
            'module': record.module,
            'line': record.lineno
        }

        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)

        return json.dumps(log_record)
    
# Create a logger
logger = logging.getLogger('wendy_logger')
logger.setLevel(logging.INFO)

# Create a stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JSONFormatter())

# Add the handler to the logger
logger.addHandler(stream_handler)

# Export the logger for use in other modules
__all__ = ['logger']