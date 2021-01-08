
import logging
def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/opt/source/mylogs.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
