from pop import Pop
from params import Params

class Merchant(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'MER',size)
    
    def produce(self,verbose):
        mk = self.prov.market
        qty = 0
        for k in mk.pools.values():
            qty_good = k.cashout_fraction(Params.merchant_cut)
            qty += qty_good
        
        assert qty>=0
        self.receive_income(qty)
        if verbose:
            print(f'MER PRODUCED {qty} FUNDS FROM MARKET')
    