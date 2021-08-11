import numpy as np


def rand_round(n):
    e = n-int(n)
    return int(n)+(e>np.random.rand())

def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

def generate_pop(prov,kind,size):
    from farmer import Farmer
    from brewer import Brewer
    from shepherd import Shepherd
    from merchant import Merchant
    from goldminer import GoldMiner
    from trader import Trader
    
    class_dict = {
        'FAR':Farmer,
        'BRW':Brewer,
        'SHE':Shepherd,
        'MER':Merchant,
        'GDM':GoldMiner,
        'TRD':Trader
    }
    pop_class = class_dict[kind]
    return pop_class(prov,size)