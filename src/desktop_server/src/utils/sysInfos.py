# Check if gpu is available 
# determine max context size for both models

import psutil
import GPUtil
import platform

def collect_system_info():
    info = {}

    # CPU Info
    info['cpu'] = {
        'physical_cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True),
        'frequency': psutil.cpu_freq().max,
        'architecture': platform.machine(),
        'processor': platform.processor(),
    }

    # Memory Info
    virtual_mem = psutil.virtual_memory()
    info['memory'] = {
        'total': virtual_mem.total / (1024.0 ** 3),
        'available': virtual_mem.available / (1024.0 ** 3),
        'used': virtual_mem.used / (1024.0 ** 3),
        'percent': virtual_mem.percent,
        'swap': psutil.swap_memory().total / (1024.0 ** 3),
        'unit': 'GB'
    }

    # GPU Info
    gpus = GPUtil.getGPUs()
    info['gpus'] = [{
        'id': gpu.id,
        'name': gpu.name,
        'memory_total': gpu.memoryTotal,
        'memory_used': gpu.memoryUsed,
        'memory_free': gpu.memoryFree,
    } for gpu in gpus]

    return info

if __name__ == "__main__":
    system_info = collect_system_info()
    print(system_info)