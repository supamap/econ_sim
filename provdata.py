import matplotlib.pyplot as plt
import pandas as pd

class ProvData:
    
    def __init__(self, prov):
        self.prov = prov
        self.price_list = []
        self.quality_list = []
        self.size_list = []
        self.size_frac_list = []
        self.pop_funds_list = []
        self.mk_funds_list = []
        self.total_population_list = []
        self.pop_fpc_list = []
        self.pop_ipc_list = []
    
    def update(self):
        prov = self.prov

        quality = {}
        size = {}
        funds = {}
        fpc = {}
        ipc = {}
        
        total_loans = 0
        
        for p in prov.pops:
            
            p.av_income = 0.9*p.av_income + 0.1*(p.income-p.cost)
            funds[p.kind] = p.funds  - p.loaned_funds
            quality[p.kind] = p.quality
            size[p.kind] = p.size
            fpc[p.kind] = p.funds/p.size
            ipc[p.kind] = p.av_income/p.size
        
        total_size = prov.total_pop_size
        total_funds = prov.total_funds

        size_frac = {k:s/total_size for k,s in size.items()}

        funds['MKT'] = prov.market.funds
        funds['TOT'] = total_funds

        self.price_list.append(prov.market.prices.copy())
        self.mk_funds_list.append(prov.market.funds)
        self.total_population_list.append(total_size)
        self.quality_list.append(quality)
        self.size_list.append(size)
        self.size_frac_list.append(size_frac)
        self.pop_funds_list.append(funds)
        self.pop_fpc_list.append(fpc)
        self.pop_ipc_list.append(ipc)
        
    def plot_prov_data(self):
        if len(self.price_list) == 0:
            print('NO DATA TO PLOT')
            return
        fig, ax = plt.subplots(2, 4,figsize=(24,10))
        
        name = self.prov.name
        
        pd.DataFrame(self.price_list).plot(title=name+': PRICES',logy=True,ax=ax[0][0])
        pd.DataFrame(self.quality_list).plot(title=name+': QUALITIES',ax=ax[0][1],logy=True)
        pd.DataFrame(self.size_list).plot(title=name+': POPULATIONS',ax=ax[0][2],logy=True)
        pd.DataFrame(self.size_frac_list).plot(title=name+': POP FRACTION',ax=ax[0][3])
        pd.DataFrame(self.pop_funds_list).plot(title=name+': POP FUNDS',ax=ax[1][0])
        pd.DataFrame(self.pop_fpc_list).plot(title=name+': POP FPC',ax=ax[1][1],logy=True)
        pd.DataFrame(self.pop_ipc_list).plot(title=name+': POP IPC',ax=ax[1][2])
        pd.DataFrame(self.total_population_list).plot(title=name+': TOTAL POP',ax=ax[1][3],logy=True)
        
