import torch

def check_device_availability(logger, os_type):
    print("Checking device availability...")
    
    if os_type.lower() == 'windows':
        if torch.cuda.is_available():
            print("GPU is available")
            num_gpus = torch.cuda.device_count()
            print(f"Num GPUs Available: {num_gpus}")
            gpu_list = [torch.cuda.get_device_name(i) for i in range(num_gpus)]
            print(f"List of GPUs Available: {gpu_list}")
        else:
            print("GPU is not available")
            num_gpus = 0
            gpu_list = []
        
        print(f"PyTorch version: {torch.__version__}")
        
        # Add information about GPUs to log file
        logger.info(f"Num GPUs Available: {num_gpus}")
        logger.info(f"List of GPUs Available: {gpu_list}")
        logger.info(f"PyTorch version: {torch.__version__}")
    
    elif os_type.lower() == 'mac':
        if torch.backends.mps.is_available():
            print("MPS is available")
        else:
            print("MPS is not available")
        
        print(f"PyTorch version: {torch.__version__}")
        
        # Add information about MPS to log file
        logger.info(f"MPS available: {torch.backends.mps.is_available()}")
        logger.info(f"PyTorch version: {torch.__version__}")

    else:
        print("Unsupported operating system")
        logger.error("Unsupported operating system")