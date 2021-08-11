from pop import Pop
from params import Params


class Brewer(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'BRW',size)
    
    def produce(self,verbose):
        # forget all the other things, its just, buy WHT, make BER, immediately this couldnt be done before
        wht_mod = Params.brewer_prod_mod['WHT']
        ber_mod = Params.brewer_prod_mod['BER']
        
        wht_consumed = wht_mod*self.size
        ber_prod = ber_mod*self.size
        
        margin = ber_mod * self.market.sell_price('BER',ber_prod) - wht_mod * self.market.buy_price('WHT',wht_consumed)
        
        if margin > 0:
            # BER will be produced
            # CHECK IF YOU WILL NEED TO TAKE A LOAN
            wht_cost = self.market.buy_cost('WHT',wht_consumed)
            if wht_cost > self.funds:
                #take a loan to buy
                loan = (wht_cost - self.funds)
                self.funds += loan
                self.loaned_funds += loan
            # BUY WHT
            bought, real_cost = self.market.buy_good('WHT',wht_consumed,self.funds,self)
            # SELL BER
            ber_prod = bought/wht_mod*ber_mod
            self.market.sell_good('BER',ber_prod,self)
        else:
            ber_prod = 0

        if verbose:  
            print(f'BRW PRODUCED {ber_prod} BER')
        
        return ('BER',ber_prod)
    