from pop import Pop
from params import Params


class Shepherd(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'SHE',size)

    def produce(self,verbose):
        qty = self.size*Params.shepherd_prod_mod['WOL']*self.prov.local_prod_mod['SHE']
        self.prov.market.sell_good('WOL',qty,self)
        
        if verbose:  
            print(f'SHE PRODUCED {qty} WOL')
        return ('WOL',qty)
    