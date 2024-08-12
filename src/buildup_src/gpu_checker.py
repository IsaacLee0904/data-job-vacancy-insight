import sys, os
import torch

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.gpu_utils import check_device_availability

logger = set_logger()

# Example for Windows
check_device_availability(logger, 'windows')

# Example for macOS
check_device_availability(logger, 'mac')