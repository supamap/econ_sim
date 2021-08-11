from pop import Pop
from params import Params

class GoldMiner(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'GDM',size)
    
    def produce(self,verbose):
        qty = self.size*Params.goldminer_prod_mod*self.prov.local_prod_mod['GDM']
        self.receive_income(qty)
        if verbose:
            print(f'PRODUCED {qty} FUNDS FROM MINE')
    