import logging
from logstash import TCPLogstashHandler

logger = logging.getLogger("fastapi_logstash")
logger.setLevel(logging.INFO)
logger.addHandler(TCPLogstashHandler("localhost", 50000, version=1))


logger.info("Logstash is working")