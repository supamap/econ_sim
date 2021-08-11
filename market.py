from params import Params
from utils import clamp

class Market:
    def __init__(self,prov):
        self.prov = prov
        price_margin = Params.base_price_margin
        
        pop_size = prov.total_pop_size
        starting_stock_base = pop_size*Params.starting_stock_base
        
        stock_need_modifier = Params.stock_need_modifier
        
        starting_stocks = {k: starting_stock_base * Params.stock_need_modifier[k] for k in Params.goods}
        self.pools = {k: Pool(starting_stocks[k], starting_stocks[k] * Params.starting_prices[k], price_margin) for k in Params.goods}
        
    @property
    def funds(self):
        return sum([i.f for i in self.pools.values()])
    
    @property
    def stocks(self):
        return {k:self.pools[k].q for k in Params.goods}
    
    @property
    def prices(self):
        return {k:self.pools[k].price for k in Params.goods}
    
    def get_stock(self,k):
        return self.pools[k].q
    
    def get_price(self,k):
        return self.pools[k].price
    
    def buy_price(self,k,q):
        return self.pools[k].buy_cost(q)/q
    
    def buy_cost(self,k,q):
        return self.pools[k].buy_cost(q)
    
    def sell_cost(self,k,q):
        return self.pools[k].sell_cost(q)
    
    def sell_price(self,k,q):
        return self.pools[k].sell_cost(q)/q
        
    def buy_good(self,k,q,av_funds,pop):
        assert k in self.pools, f'good not found {k}'
        assert q>=0, f'cant buy negative goods {(k,q)}'
        assert av_funds>=0, f'cant have negative funds {(k,q,av_funds)}'
        
        #sale is done
        q_real,total_cost = self.pools[k].buy(q,av_funds)
        pop.funds -= total_cost
        
        return (q_real, total_cost)
    
    def sell_good(self,k,q,pop):
        assert q>=0, f'cant sell negative goods {(k,q)}'
        
        #sale is done
        q_real,total_cost = self.pools[k].sell(q)
        pop.receive_income(total_cost)
        
        return (q_real, total_cost)
    
    def status(self):
        print('TOTAL FUNDS:',self.funds)
        for k in self.pools:
            print(k)
            self.pools[k].status()
            


class Pool:
    def __init__(self,q,f,rate=0.01):
        self.q = q
        self.f = f
        self.rate = rate
        
    @property
    def price(self):
        return self.f/self.q
        
    def buy_cost(self,q):
        assert q<self.q
        return (self.q*self.f/(self.q-q)-self.f)*(1+self.rate)
    
    def buy(self,q,lim_f):
        
        f_limited = False
        
        if q>self.q:
            f_limited = True
        else:
            if self.buy_cost(q)>lim_f:
                f_limited = True
        
        if f_limited:
            cost = lim_f
            q_real = self.q - self.f*self.q/(self.f+cost/(1+self.rate))
        else:
            cost = self.buy_cost(q)
            q_real = q
            
        self.q -= q_real
        self.f += cost
        return (q_real,cost)
        
    def sell_cost(self,q):
        return (-self.q*self.f/(self.q+q)+self.f)/(1+self.rate)
        
    def sell(self,q):
        cost = self.sell_cost(q)
        self.q += q
        self.f -= cost
        return (q,cost)
    
    def cashout(self,f):
        assert f<self.f
        self.f -= f
        return f
    
    def cashout_fraction(self,frac):
        assert (frac<1) and (frac>=0), 'fraction must be between 0 and 1'
        f = self.cashout(self.f*frac)
        return f
        
    def status(self):
        print('F',self.f)
        print('Q',self.q)
        print('P',self.price)