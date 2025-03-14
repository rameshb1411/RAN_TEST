import os
import platform

def get_os_info():
    return platform.system(), platform.release()

def get_memory_usage():
    return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3)

def create_directory(path):
    os.makedirs(path, exist_ok=True)

def remove_directory(path):
    os.rmdir(path)