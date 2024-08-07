import sys, os
import torch

# setup project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from utils.log_utils import set_logger
from utils.gpu_utils import check_gpu_availability

logger = set_logger()
check_gpu_availability(logger)