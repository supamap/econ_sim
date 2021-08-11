from market import Market
from utils import generate_pop

from provdata import ProvData
from params import Params

class Prov:
    
    def __init__(self,world,terrain,name,neighbors,index):
        self.name = name
        self.index = index
        self.world = world
        self.neighbors = neighbors
        self.terrain = terrain
        
        self.pops = [generate_pop(self,kind,size) for kind, size in Params.starting_pops]
        self.market = Market(self)
        
        self.local_prod_mod = Params.terrain_prod_mod[terrain].copy()
        self.provdata = ProvData(self)
        
        self.land_size = 10000
        self.land_use = 0
        self.land_use_factor = 1
        
    @property
    def total_pop_size(self):
        return sum([pop.size for pop in self.pops])
    
    @property
    def total_funds(self):
        pop_funds = sum([pop.funds for pop in self.pops])
        market_funds = self.market.funds
        loaned_funds = sum([pop.loaned_funds for pop in self.pops])
        
        total_funds = pop_funds + market_funds - loaned_funds
        return total_funds
    
    @property
    def average_quality(self):
        quality_sum = sum([pop.quality*pop.size for pop in self.pops])
        return quality_sum/self.total_pop_size
    
    def produce_pops(self,verbose):
        for pop in self.pops:
            pop.produce(verbose)
        
    def step(self,verbose):
        if verbose:
            print('PROV',self.name)
        
        ordered_pops = list(self.pops)
        ordered_pops.sort(key = lambda x: -x.priority)
        
        self.produce_pops(verbose)
        
        # reserve funds
        for pop in self.pops:
            pop.reserve_funds()
        
        # consume basic needs
        if verbose:
            print('--BASIC NEEDS')  
        for pop in ordered_pops:
            pop.consume_basic_needs(verbose)
          
        # consume life needs
        if verbose:
            print('--LIFE NEEDS')   
        for pop in ordered_pops:
            pop.consume_life_needs(verbose)    
            
        for pop in self.pops:
            pop.unreserve_funds()
            
        # update pops
        for pop in self.pops:
            pop.update(verbose)
        
        # promote
        for pop in self.pops:
            pop.promote(verbose)
        
        self.update_land_use_factor(verbose)
        
        if verbose:
            print('PRICES:', self.market.prices)
#             print('EFFECTIVE PRICES:', self.market.modified_effective_prices)
            print('MARKET STOCKS:',self.market.stocks)
            print('MARKET FUNDS:',self.market.funds)

            for p in self.pops:
                print('---',p.kind,p.size)
                print('--F:',p.funds)
                print('--H:',p.health)
                print('--Q:',p.quality) 
            print('')
            
    def update_land_use_factor(self,verbose):
        if verbose:
            print(f'LAND USE {self.land_use}')
                
    def clean_state(self):
        for pop in self.pops:
            pop.income = 0
            pop.cost = 0
#         self.market.clean_state()
        