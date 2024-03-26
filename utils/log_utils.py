import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import graypy

def set_logger(level=logging.INFO):
    """
    Set up and initialize the logger based on the current script name.
    
    Returns:
    - logger: logging.Logger
        Configured logger instance.
    """
    # Get the current script name (without file extension)
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    # Create log file path
    log_file_path = os.path.join("log", f"{script_name}.log")

    # create log
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # log handle 
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(level)
    file_format = logging.Formatter('%(asctime)s %(levelname)s - %(filename)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # log center handle 
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter('%(asctime)s %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # setup graylog
    graylog_host = 'data_vacancy_insight.graylog.server.ip'
    graylog_port = 12201  # GELF UDP port

    gelf_handler = graypy.GELFUDPHandler(graylog_host, graylog_port)
    gelf_handler.setLevel(logging.DEBUG) 
    logger.addHandler(gelf_handler)

    return logger
