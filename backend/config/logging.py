import logging
from logging import Formatter

from flask import current_app, has_request_context, request
from flask.logging import default_handler


class RequestFormatter(Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url or 'N/A'
            record.remote_addr = request.remote_addr or 'N/A'
        else:
            record.url = 'N/A'
            record.remote_addr = 'N/A'

        return super().format(record)

def configure_logger(debug = False):
  if (debug):
    logger = logging.getLogger('run')
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh_formatter = RequestFormatter('[%(asctime)s] -- request at %(url)s -- %(levelname)s in %(module)s: %(message)s')
    sh.setFormatter(sh_formatter)
    logger.addHandler(sh)
    logger.propagate = False
    return logger
  else:
     pass  # TODO set up when closer to deployment
    