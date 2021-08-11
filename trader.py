from pop import Pop
from params import Params


class Trader(Pop):
    def __init__(self,prov,size):
        Pop.__init__(self,prov,'TRD',size)
        self.bought_inputs = {k:0 for k in Params.goods}
        self.av_provs = self.prov.neighbors
#         self.best_deal_list = None
        self.best_deal = None
#         self.past_deal = {}
#         self.past_past_deal = {}
        self.deal_subdiv = 5
    
    
    def produce(self,verbose):
        # do everything in the same day (maybe add the opportunity to add a delay, but for now, only daily, well weekly)
        # maybe add the multiple goods functionality, but for now, all or nothing of one good
        
        # find all deals
        if verbose:
            print('')
            print(self.prov.name)
        deal_list = []
        q_limit = Params.trader_limit * self.size
        lmk = self.prov.market
        for n in self.av_provs:
            target_prov = self.prov.world.provs[n]
            tmk = target_prov.market
            for k in Params.goods:
                av_good = lmk.get_stock(k)
                q_av = min(q_limit,av_good*0.5)
                for i in range(self.deal_subdiv):
                    subdiv_mod = (i+1)/self.deal_subdiv
                    q_deal = q_av*subdiv_mod
                    
                    local_cost = lmk.buy_cost(k,q_deal)
                    target_cost = tmk.sell_cost(k,q_deal)

                    possible_profit = target_cost - local_cost
                    info_dict = {
                        'n':n,
                        'k':k,
                        'AV:':round(av_good,2),
                        'LP:':round(local_cost/q_deal,2),
                        'TP:':round(target_cost/q_deal,2),
                        'SALE':q_deal,
                        'PROFIT':possible_profit,
                        'PM':possible_profit/q_deal,
                        'SM':subdiv_mod
                    }
                    #display(info_dict)
                    if possible_profit > 0:
                        deal_list.append(info_dict)
        
        # get best deals
        if len(deal_list) == 0:
            if verbose:
                print('NO GOOD DEAL')
            return
        else:
            if verbose:
                print('DEAL LIST')
                display(deal_list)
        
        best_deal = max(deal_list,key=lambda x:x['PROFIT']) 
        
        if verbose:
            print('SELECTED DEAL')
            display(best_deal)
        
        # trade the best deals
        # get loan if needed
        cost = lmk.buy_cost(best_deal['k'],best_deal['SALE'])
        loan = 0
        if cost>self.funds:
            loan = (cost - self.funds)
            if verbose:
                print(f'LOAN OF {loan} NEEDED. COST {cost} FUNDS {self.funds}')
            self.funds += loan
            self.loaned_funds += loan
        
        # buy local
        bought, real_cost = lmk.buy_good(best_deal['k'],best_deal['SALE'],self.funds,self)

        # sell target
        tmk = self.prov.world.provs[best_deal['n']].market
        sold, real_rev = tmk.sell_good(best_deal['k'],bought,self)
        
        # pay back the loan imediately
        if loan>0:
            self.pay_loans(loan)
        
        
        if verbose:
            print(f'BOUGHT {bought} FOR {real_cost}')
            print(f'SOLD {sold} FOR {real_rev}')
            print(f'FUNDS {self.funds} LOANS {self.loaned_funds}')
        

    
#     def find_deals(self,verbose):
#         if verbose:
#             print('')
#             print(self.prov.name)
#         deal_list = []
#         q_limit = Params.trader_limit * self.size
#         for n in self.av_provs:
#             target_prov = self.prov.world.provs[n]
#             lmk = self.prov.market
#             tmk = target_prov.market
#             for k in Params.goods:
#                 # deal info
#                 local_price = lmk.buy_price(k)
#                 target_price = tmk.sell_price(k)
#                 target_demand = tmk.prev_demand[k]
#                 target_supply = tmk.prev_supply[k]
#                 # im missing a way to only consider supply not from me, best way is to check my past deal, if there is any past supplies to that, then subtract it
#                 if (n,k) in self.past_past_deal:
#                     own_supply = self.past_past_deal[(n,k)]
#                     target_supply -= own_supply
#                     if verbose:
#                         print(f'SUBTRACTING {own_supply} {k} {n}')
                        
#                 assert target_supply >= 0, 'TARGET SUPPLY NEGATIVE'

#                 av_good = lmk.prev_supply[k]
#                 max_goods = min(av_good,q_limit,tmk.prev_demand[k])
#                 if max_goods <= 0:
#                     continue
#                 for i in range(5):
#                     q_deal = max_goods*(i+1)/5
#                     expected_price = min(target_demand/(target_supply+q_deal+0.000001),1)*target_price
#                     possible_profit = q_deal*(expected_price-local_price)
#                     info_dict = {
#                         'n':n,
#                         'k':k,
#                         'AV:':round(av_good,2),
#                         'TS:':round(target_supply,2),
#                         'TD:':round(target_demand,2),
#                         'LP:':round(local_price,2),
#                         'TP:':round(target_price,2),
#                         'EP:':round(expected_price,2),
#                         'SALE':q_deal,
#                         'PROFIT':possible_profit,
#                         'PM':possible_profit/q_deal
#                     }
#                     #display(info_dict)
#                     if possible_profit > 0:
#                         deal_list.append(info_dict)

#         if len(deal_list) == 0:
#             if verbose:
#                 print('NO GOOD DEAL')
#             return
#         else:
#             if verbose:
#                 print('DEAL LIST')
#                 display(deal_list)
        

#         # from all the deals in deal_list it has to pick the best ones to trade
#         # first of all it 
#         best_deal_list = []
#         # while there is still space to trade and deals left to evaluate
#         while (q_limit > 0) and (len(deal_list) > 0):
#             # picks the best deal in terms of price margin
#             best_deal_prov_kind = max(deal_list,key=lambda x:x['PM'])
#             # out of that deal, it picks the one with THAT resource and THAT province that maximizes profit
#             used_good = best_deal_prov_kind['k']
#             target_prov = best_deal_prov_kind['n']

#             prov_kind_deal_list = [deal for deal in deal_list if ((deal['k'] == used_good) and (deal['n'] == target_prov))]
#             best_deal = max(prov_kind_deal_list,key=lambda x:x['PROFIT'])

#             deal_list = [deal for deal in deal_list if ((deal['k'] != used_good) or (deal['n'] != target_prov))]
#             q_limit -= best_deal['SALE']

#             best_deal_list.append(best_deal)
        
        
#         if len(best_deal_list) > 0:
#             if verbose:
#                 print('BEST DEAL:')
#                 display(best_deal_list)
#             self.best_deal_list = best_deal_list
#         else:
#             if verbose:
#                 print('NO GOOD DEAL')
    
    
