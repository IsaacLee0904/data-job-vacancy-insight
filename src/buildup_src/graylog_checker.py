import sys, os

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger

logger = set_logger()
logger.info("This is an info message sent to Graylog for testing")