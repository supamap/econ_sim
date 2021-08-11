from prov import Prov
from worlddata import WorldData
from maps import Maps

# basic_map = [
#     ('P0','FARMLANDS',[1,2]), #P0
#     ('P1','PLAINS',[0,2,3]), #P1
#     ('P2','PLAINS',[0,1,3,4]), #P2
#     ('P3','HILLS',[1,2,4]), #P3
#     ('P4','MOUNTAINS',[2,3]), #P4
# ]

#basic_map = Maps.basicmap

countries_map = [
    
]

class World:
    def __init__(self,preset_name):
        self.provs = []
        self.worlddata = WorldData(self)
#         self.provs = [
#             Prov(self,'PLAINS','P0',[1]),
#             Prov(self,'GRASSLANDS','P1',[0])
#         ]
        map_preset = Maps.get_preset(preset_name)
        i=0
        for t in map_preset:
            p = Prov(self,t[1],t[0],t[2],i)
            i+=1
            self.provs.append(p)
    
    def step(self,verbose=False):
        for prov in self.provs:
            prov.clean_state()
            
#         for prov in self.provs:
#             for pop in prov.pops:
#                 if pop.production_priority == 'TRADER':
#                     # let traders sell their shit
#                     pop.trade(verbose)
#                     # let traders find their new deal
#                     pop.find_deals(verbose)
            
        for prov in self.provs:
            prov.step(verbose)
            
        for prov in self.provs:
            prov.provdata.update()
        
        self.worlddata.update()
        
        if verbose:
            print('')