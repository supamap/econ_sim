import numpy as np
import math

from params import Params
from utils import rand_round

class Pop:
    def __init__(self,prov,kind,size):
        self.prov = prov
        self.kind = kind
        self.size = size
        
        self.funds = size*Params.starting_funds[kind]
        self.prev_fpc = self.funds/self.size
        
        self.reserve_factor = Params.reserve_factor
        self.reserved_funds = 0
        
        self.health = 1
        self.status = 1
        self.quality = 1
        
        self.production_type = Params.production_type[self.kind]
        self.rank = Params.pop_rank[kind]
        self.loaned_funds = 0
        
        self.income = 0
        self.cost = 0
        self.av_income = 0
        
    @property
    def market(self):
        return self.prov.market
        
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        assert value > 0, 'SIZE HAS GONE NEGATIVE BOI'
        self._size = value
        
    @property
    def priority(self):
        return self.funds/self.size
    
    def receive_income(self, v):
        assert v >= 0, f'cant receive negative income {v}'
        self.funds += v
        self.income += v
        
    def assume_cost(self, v):
        assert v >= 0, f'cant assume negative cost {v}'
        self.cost += v
    
    def reserve_funds(self):
        funds_to_reserve = max(self.funds * self.reserve_factor - self.reserved_funds,0)
        self.funds -= funds_to_reserve
        self.reserved_funds += funds_to_reserve
        
    def unreserve_funds(self):
        funds_to_unreserve = self.reserved_funds
        self.reserved_funds -= funds_to_unreserve
        self.funds += funds_to_unreserve

    def consume_basic_needs(self,verbose):
        
        sum_needs = 0
        sum_fill = 0
        
        ordered_needs = list(Params.basic_needs.items())
        ordered_needs.sort(key=lambda x:self.prov.market.prices[x[0]])
        
        for k,v in ordered_needs:
            need = v*self.size
            fill = self.market.buy_good(k,need,self.funds,self)[0]
            sum_needs += need
            sum_fill += fill
            if verbose:
                print(f'{self.kind} CONSUMED {fill} {k}')
        
        need_fullfill = sum_fill/sum_needs
        assert need_fullfill<=1
        
        self.basic_needs = need_fullfill
    
    def consume_life_needs(self,verbose):
        if self.basic_needs != 1:
            self.life_needs = 0
            return
        
        sum_needs = 0
        sum_fill = 0
        ordered_needs = list(Params.life_needs.items())
        ordered_needs.sort(key=lambda x:self.prov.market.prices[x[0]])
        for k,v in ordered_needs:
            need = v*self.size*self.quality
            fill = self.market.buy_good(k,need,self.funds,self)[0]
            sum_needs += need
            sum_fill += fill
            if verbose:
                print(f'{self.kind} CONSUMED {fill} {k}')
        
        need_fullfill = sum_fill/sum_needs
        assert need_fullfill<=1
        
        self.life_needs =  need_fullfill
    
    def update(self,verbose):
        #health is affected by basic needs
        alpha = Params.health_alpha
        self.health = self.health*(1-alpha)+self.basic_needs*alpha
        self.status = self.status*(1-alpha)+self.life_needs*alpha
        #quality is affected by life needs

        quality_factor = ((self.status-0.5)*0.05+1)
        quality_factor = quality_factor*(self.quality*0.99 + 0.01)/self.quality
        quality_factor = quality_factor**0.4
        
        #only allow quality to grow if it has more money (funds per capita)
        if self.funds/self.size <= self.prev_fpc:
            quality_factor = min(quality_factor,1)
            
        self.quality = self.quality * quality_factor
        
        self.prev_fpc = self.funds/self.size
        
        min_growth = -0.01
        max_growth = 0.002
        
        self.size = max(1,rand_round(self.size * (1 + self.health*(max_growth-min_growth) + min_growth)))
        
        self.pay_loans()
        

            
    def pay_loans(self,v=None):
        if self.loaned_funds == 0:
            return
        if v is None:
            v = self.loaned_funds
        
        # pay as much loans as one can
        to_pay = min(v,self.funds)
        self.loaned_funds -= to_pay
        self.funds -= to_pay
        
    
    def promote(self,verbose):
        pops = self.prov.pops
        target = np.random.choice(pops)
        target_value = target.quality * target.status
        self_value = self.quality * self.status
        if target_value > (0.95*self_value):
            #should try and switch professions
            factor = 0.01 * self.rank / target.rank
            n = rand_round(math.sqrt(self.size*target.size) * factor)
            if n>0 and target != self:
                n = min(n,self.size-1)
                self.size -= n
                target.size += n
                if verbose:
                    print(f'{n} {self.kind} PROMOTED TO {target.kind}')
        
    
            