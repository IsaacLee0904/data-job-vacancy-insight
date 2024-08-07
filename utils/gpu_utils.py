import torch

def check_gpu_availability(logger):
    print("Checking GPU availability...")
    
    if torch.cuda.is_available():
        print("GPU is available")
    else:
        print("GPU is not available")
    
    num_gpus = torch.cuda.device_count()
    print(f"Num GPUs Available: {num_gpus}")
    
    gpu_list = [torch.cuda.get_device_name(i) for i in range(num_gpus)]
    print(f"List of GPUs Available: {gpu_list}")
    
    print(f"PyTorch version: {torch.__version__}")

    # add information about GPUs to log file
    logger.info(f"Num GPUs Available: {num_gpus}")
    logger.info(f"List of GPUs Available: {gpu_list}")
    logger.info(f"PyTorch version: {torch.__version__}")