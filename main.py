import Arbt_Func
import requests
import json

"""
 step 0: we identify the tradeable tokens
 Exchange: poloniex
 link:https://docs.poloniex.com/#introduction
"""
url="https://poloniex.com/public?command=returnTicker"
def step_0():
    # getting coins and their price from exchange
    #get_data will return json responce of data in list form
    json_data=Arbt_Func.get_data(url)

    #tradeAble_pairs will get the list of all the tradeable pairs by providing json_data
    tradeAble_pairs=Arbt_Func.get_tradeables(json_data)

    return tradeAble_pairs

"""
Step:01
structuring triangular pairs
calculation only
"""

def step_1(tradeAble_pairs):
    #getting triangular pairs
    triangular_pairs=Arbt_Func.structured_pairs(tradeAble_pairs)

    #saving triangular_pairs into json file
    with open("Triangular_pairs.json",'w') as fp:
        json.dump(triangular_pairs,fp)


"""
 Step:02 pulling prices to calculate surface rate
 Exchange: poloniex
 link:https://docs.poloniex.com/#introduction    
"""


def step_2():
    #reading data of triangular pairs from json file

    with open("Triangular_pairs.json") as file:
        triangular_pairs=json.load(file)

     #getting  latest surface prices
    coin_prices=Arbt_Func.get_data(url)

    #loop through and get price
    for t_pairs in triangular_pairs:
        price_dict=Arbt_Func.get_t_pairs_price(t_pairs,coin_prices)
        surf_Arb=Arbt_Func.calc_triangular_arb_surface_rate(t_pairs,price_dict)
        if len(surf_Arb)>0:
            print(surf_Arb)

#----------MAIN---------------------------------------

if __name__=="__main__":
    # tradeAble_pairs=step_0() #saving the returned list into list tradeAble_pairs
    # triangular_pairs=step_1(tradeAble_pairs)
    step_2()
#    Arbt_Func.get_depth_from_orderbook()
