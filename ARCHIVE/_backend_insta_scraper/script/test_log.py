import logging
import logging.config

# Logger initialisations
logging.config.fileConfig(fname='logging_config.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)


logger.debug('tttt')
