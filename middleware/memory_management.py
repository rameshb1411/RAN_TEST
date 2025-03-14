import gc

def collect_garbage():
    gc.collect()

def get_objects():
    return gc.get_objects()