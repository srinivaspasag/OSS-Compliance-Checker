import logging


def setup_logger():
    # create a file handler that writes to a separate file
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)

    # create a formatter to set the format of log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # create a logger and add the file handler
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger
