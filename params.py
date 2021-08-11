class Params:
    goods = ['WHT','BER','WOL']
    pop_types = ['FAR','BRW','SHE','MER','GDM','TRD']
    
    trader_limit = 5
    
    starting_pops = [
        ('FAR',600),
        ('BRW',5),
        ('SHE',250),
        ('MER',20),
        ('GDM',10),
        ('TRD',10)
    ]
    
    terrain_prod_mod = {
        'FARMLANDS':{
            'FAR':1.5,
            'SHE':0.8,
            'GDM':1
        },        
        'PLAINS':{
            'FAR':1,
            'SHE':1,
            'GDM':1
        },
        'HILLS':{
            'FAR':0.8,
            'SHE':0.8,
            'GDM':2
        },
        'MOUNTAINS':{
            'FAR':0.5,
            'SHE':0.5,
            'GDM':10
        },
        
    }
    
    starting_market_funds = 5000
    
    reserve_factor = 0.5
    
    farmer_prod_mod = {
        'WHT':1
    }
    brewer_prod_mod = {
        'WHT':1,
        'BER':0.5
    }
    shepherd_prod_mod = {
        'WOL':1
    }
    
    goldminer_prod_mod = 0.1
    
    merchant_cut = 0.0004
    
    starting_funds = {
        'FAR':1,
        'BRW':5,
        'SHE':1,
        'MER':5,
        'GDM':1,
        'TRD':2,
    }
    
    pop_rank = {
        'FAR':1,
        'BRW':3,
        'SHE':1,
        'MER':3,
        'GDM':2,
        'TRD':3,
    }
    
    production_type = {
        'FAR':'PRODUCER',
        'BRW':'PRODUCER',
        'SHE':'PRODUCER',
        'MER':'EARNER',
        'GDM':'EARNER',
        'TRD':'TRADER',
    }
    
    health_alpha = 0.1
    
    basic_needs = {
        'WHT':0.6,
        'WOL':0.2
    }
    life_needs = {
        'WHT':0.1,
        'BER':0.1,
        'WOL':0.1
    }
    
    starting_prices = {
        'WHT':1,
        'BER':4,
        'WOL':1
    }
    
    stock_need_modifier = {'WHT':0.7,'WOL':0.3,'BER':0.1}
    
    starting_stock_base = 25
    
    base_price_margin = 0.02
    