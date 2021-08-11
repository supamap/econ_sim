from pop import Pop
from params import Params


class Farmer(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'FAR',size)
    
    def produce(self,verbose):
        qty = self.size*Params.farmer_prod_mod['WHT']*self.prov.local_prod_mod['FAR']
        self.prov.market.sell_good('WHT',qty,self)
        if verbose:
            print(f'FAR PRODUCTED {qty} WHT')
        return ('WHT',qty)
    