import logging


def initialize_root_logger():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    # suppress logging from requests library to avoid cluttering the output
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.debug("Root logger initialized.")
