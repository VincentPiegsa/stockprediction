"""
__init__.py -> Logger
"""
import logging


def init_logger():
    """Startet den Logger
    
    Returns:
        logger: Logger Objekt
    """
    logger = logging.getLogger(name=__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s:%(module)s:%(lineno)s:%(levelname)s] %(message)s')
    
    filehandler = logging.FileHandler('server.log')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(formatter)

    logger.addHandler(filehandler)

    return logger
