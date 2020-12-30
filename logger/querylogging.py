import logging
from pythonjsonlogger import jsonlogger


#Returns the logger object which can be used for general logging
def get_general_logger():
    logger = logging.getLogger("GeneralLogger")
    logger.setLevel(logging.INFO)
    json_handler = logging.FileHandler('general.log')
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(json_handler)
    return logger

#Returns the logger object which can be used for event logging
def get_event_logger():
    logger = logging.getLogger("EventLogger")
    logger.setLevel(logging.INFO)
    json_handler = logging.FileHandler('event.log')
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    json_handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(json_handler)
    return logger
