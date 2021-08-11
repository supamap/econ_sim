import matplotlib.pyplot as plt
import pandas as pd

class WorldData:
    
    def __init__(self, world):
        goods = ['WHT','WOL','BER']
        
        self.world = world
        self.prov_pops = []
        self.prov_quality = []
        self.prov_funds = []
        self.prov_price_list = {t:[] for t in goods}
        
    def update(self):
        world = self.world
        goods = ['WHT','WOL','BER']
        
        prov_size = {}
        prov_quality = {}
        prov_funds = {}
        prov_price = {t:{} for t in goods}
        
        for prov in world.provs:
            prov_size[prov.name] = prov.provdata.total_population_list[-1]
            prov_quality[prov.name] = prov.average_quality
            prov_funds[prov.name] = prov.provdata.pop_funds_list[-1]['TOT']
            for t in goods:
                prov_price[t][prov.name] = prov.market.get_price(t)
        
        self.prov_pops.append(prov_size)
        self.prov_quality.append(prov_quality)
        self.prov_funds.append(prov_funds)
        for t in goods:
            self.prov_price_list[t].append(prov_price[t])
    
    def plot_world_data(self):
        if len(self.prov_pops) == 0:
            print('NO DATA TO PLOT')
            return
        
        fig, ax = plt.subplots(2, 4,figsize=(24,10))
        pd.DataFrame(self.prov_pops).plot(title='PROV TOTAL POP',ax=ax[0][0],logy=True)
        pd.DataFrame(self.prov_quality).plot(title='QUALITIES',ax=ax[0][1],logy=True)
        pd.DataFrame(self.prov_funds).plot(title='PROV TOTAL FUNDS',ax=ax[0][2],logy=True)
#         pd.DataFrame(self.size_frac_list).plot(title='POP FRACTION',ax=ax[0][3])
        pd.DataFrame(self.prov_price_list['WHT']).plot(title='WHT PRICE',ax=ax[1][0],logy=True)
        pd.DataFrame(self.prov_price_list['WOL']).plot(title='WOL PRICE',ax=ax[1][1],logy=True)
        pd.DataFrame(self.prov_price_list['BER']).plot(title='BER PRICE',ax=ax[1][2],logy=True)
#         pd.DataFrame(self.total_population_list).plot(title='BE',ax=ax[1][3],logy=True)