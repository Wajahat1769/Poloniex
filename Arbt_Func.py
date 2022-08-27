import requests
import json
import time
def get_data(url):
    # getting coins and their price from exchange
    req = requests.get(url) #print(req.text) => is used to print data in string form
    json_resp=json.loads(req.text)# converting string from "req.text" to json object
    return json_resp #returning list

def get_tradeables(json_data):
    tradeAble_pairs = []

    for x in json_data:
        is_frozen = json_data[x]["isFrozen"]
        is_postOnly = json_data[x]["postOnly"]
        # printing pairs that are not tradeable
        if is_frozen != "0" or is_postOnly != "0":
            pass
        else:
            # saving tradeable pairs into new list/array
            tradeAble_pairs.append(x)
    return tradeAble_pairs

def structured_pairs(tradeAble_pairs):
    # declaring variables
    triangular_pair_list = []
    remove_duplicate_list = []
    pair_list = []
    # getting pair A
    for pair_a in tradeAble_pairs:
        pair_a_split = pair_a.split("_")  # spliting data on the base of _
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]


        #storing pair a in a box
        pair_a_box=[a_base,a_quote]

        #getting pair b
        for pair_b in tradeAble_pairs:
            if pair_b!=pair_a:
                pair_b_split = pair_b.split("_")  # spliting data on the base of _
                b_base = pair_b_split[0]
                b_quote = pair_b_split[1]
                if b_base in pair_a_box or b_quote in pair_a_box:
                 #getting pair c
                 for pair_c in tradeAble_pairs:
                   #count the number of matching c items
                   if pair_c!=pair_a and pair_c!=pair_b:
                     pair_c_split = pair_c.split("_")  # spliting data on the base of _
                     c_base = pair_c_split[0]
                     c_quote = pair_c_split[1]
                     combine_box=[pair_a,pair_b,pair_c] #combining all
                     pair_box=[a_base,a_quote,b_base,b_quote,c_base,c_quote]

                     count_c_base=0
                     for i in pair_box:
                         if i==c_base:
                             count_c_base += 1

                     count_c_quote=0
                     for j in pair_box:
                         if j==c_quote :
                             count_c_quote += 1

                         #determining triangular pair
                     if count_c_base==2 and count_c_quote==2 and c_base!=c_quote:
                         combined=pair_a+","+pair_b+","+pair_c
                         unique_item=''.join(sorted(combine_box))
                         if unique_item not in remove_duplicate_list:
                             match_dict={
                                 'pair_a': pair_a,
                                 'pair_b': pair_b,
                                 'pair_c': pair_c,
                                 'a_base': a_base,
                                 'b_base': b_base,
                                 'c_base': c_base,
                                 'a_quote': a_quote,
                                 'b_quote': b_quote,
                                 'c_quote': c_quote,
                                 'combined':combined
                             }
                             triangular_pair_list.append(match_dict)

                             remove_duplicate_list.append(unique_item)


    return triangular_pair_list

def get_t_pairs_price(t_pairs,coin_prices):

    #get triangular pairs info
    pair_a = t_pairs["pair_a"]
    pair_b = t_pairs["pair_b"]
    pair_c = t_pairs["pair_c"]

    #get ask and bid info
    pair_a_ask = float(coin_prices[pair_a]["lowestAsk"])
    pair_b_ask = float(coin_prices[pair_b]["lowestAsk"])
    pair_c_ask = float(coin_prices[pair_c]["lowestAsk"])
    pair_a_bid = float(coin_prices[pair_a]["highestBid"])
    pair_b_bid = float(coin_prices[pair_b]["highestBid"])
    pair_c_bid = float(coin_prices[pair_c]["highestBid"])

   #returning dictionary
    return {
        "pair_a_ask": pair_a_ask,
        "pair_a_bid": pair_a_bid,
        "pair_b_ask": pair_b_ask,
        "pair_b_bid": pair_b_bid,
        "pair_c_ask": pair_c_ask,
        "pair_c_bid": pair_c_bid
    }

# def calc_triangular_arb_surface_rates(t_pairs,price_dict):
#
#     #setting variables
#     starting_amount=1
#     minimum_surface_rate=0
#     surface_dict={}
#     contract_1=""
#     contract_2=""
#     contract_3=""
#     direction_trade_1=""
#     direction_trade_2 = ""
#     direction_trade_3 = ""
#     acquired_coin_t1 = 0
#     acquired_coin_t2=0
#     acquired_coin_t3=0
#     calculated=0
#
#     #extracting pair variables
#     pair_a = t_pairs["pair_a"]
#     pair_b = t_pairs["pair_b"]
#     pair_c = t_pairs["pair_c"]
#     a_base = t_pairs["a_base"]
#     b_base = t_pairs["c_base"]
#     c_base = t_pairs["c_base"]
#     a_quote = t_pairs["a_quote"]
#     b_quote = t_pairs["b_quote"]
#     c_quote = t_pairs["c_quote"]
#
#     #extrcting price information
#     a_ask = price_dict["pair_a_ask"]
#     b_ask = price_dict["pair_b_ask"]
#     c_ask = price_dict["pair_c_ask"]
#     a_bid = price_dict["pair_a_bid"]
#     b_bid = price_dict["pair_b_bid"]
#     c_bid = price_dict["pair_c_bid"]
#
#     #set direction and loop through
#
#     direction_list=["forward","reverse"]
#     for direction in direction_list:
#
#         #setting additional variables for swap info
#         swap_1 = 0
#         swap_2 = 0
#         swap_3 = 0
#         swap_1_rate = 0
#         swap_2_rate = 0
#         swap_3_rate = 0
#         """
#                poloniex rules
#                if we are swaping from left(base) to right(quote) then *1/ask
#                if we are swaping from right(quote) to left(base) then * bid
#         """
#         # assume we starting from a_base and swapping it for a_quote
#         if direction == "forward":
#             swap_1=a_base
#             swap_2=a_quote
#             swap_1_rate=1/a_ask
#             direction_trade_1="base_to_quote"
#             acquired_coin_t1 = starting_amount * swap_1_rate
#             contract_1 = pair_a
#
#         #for reverse
#         if direction == "reverse":
#             swap_1=a_quote
#             swap_2=a_base
#             swap_1_rate=a_bid
#             direction_trade_1="quote_to_base"
#             # place first trade
#             contract_1 = pair_a
#             acquired_coin_t1 = starting_amount * swap_1_rate
#         '''
#         FORWARD
#         '''
#
#         if direction == "forward":
#             #we will check if a_quote(acquired_coin_trade_1) is matches to b_quote
#             """ SCENARIO:01 """
#             if a_quote == b_quote and calculated==0:
#                 swap_2=b_quote
#                 swap_2_rate=b_bid
#                 acquired_coin_t2=acquired_coin_t1*swap_2_rate
#
#                 direction_trade_2="quote_to_base"
#                 contract_2=pair_b
#
#                 #if b_base(acquired coin) matches c_base
#                 if b_base==c_base:
#                     swap_3=c_base
#                     swap_3_rate=1/c_ask
#                     direction_trade_3="base_to_quote"
#                     contract_3=pair_c
#                 if b_base==c_quote:
#                     swap_3=c_quote
#                     swap_3_rate=c_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_c
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#
#      # check if a_quote (acquired coin) matches b_base """
#             """ SCENARIO:02 """
#         if direction == "forward":
#             if a_quote == b_base and calculated==0:
#                 swap_2=b_base
#                 swap_2_rate = 1/b_ask
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "base_to_quote"
#                 contract_2 = pair_b
#
#                 # if b_quote(acquired coin) matches c_base
#                 if b_quote == c_base:
#                     swap_3 = c_base
#                     swap_3_rate = 1 / c_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_c
#                 if b_quote == c_quote:
#                     swap_3=c_quote
#                     swap_3_rate = c_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_c
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#
#             """ SCENARIO:03 """
#             # what if a_quote matches c_quote
#         if direction == "forward":
#             if a_quote == c_quote and calculated==0:
#                 swap_2=c_quote
#                 swap_2_rate = c_bid
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "quote_to_base"
#                 contract_2 = pair_c
#
#                 # if c_base(acquired coin) matches b_base
#                 if c_base == b_base:
#                     swap_3 = b_base
#                     swap_3_rate = 1 / b_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_b
#                 # if c_base(acquired coin) matches b_quote
#                 if c_base == b_quote:
#                     swap_2=b_quote
#                     swap_3_rate = b_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_b
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#             """ SCENARIO:04 """
#         if direction == "forward":
#             # what if a_quote matches c_base
#             if a_quote == c_base and calculated==0:
#                 swap_2=c_base
#                 swap_2_rate = 1/c_ask
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "base_to_quote"
#                 contract_2 = pair_c
#
#                 # if c_quote(acquired coin) matches b_base
#                 if c_quote == b_base:
#                     swap_3 = b_base
#                     swap_3_rate = 1 / b_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_b
#                 # if c_quote(acquired coin) matches b_quote
#                 if c_quote == b_quote:
#                     swap_3=b_quote
#                     swap_3_rate = b_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_b
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#             # if acquired_coin_t3 > starting_amount:
#             #     print(direction,pair_a,pair_b,pair_c,starting_amount,acquired_coin_t3)
#         '''
#         Reverse Calculation
#         '''
#
#         if direction == "reverse":
#             # we will check if a_base(acquired_coin_trade_1) is matches to b_quote
#             """ SCENARIO:01 """
#             if a_base == b_quote and calculated == 0:
#                 swap_2=b_quote
#                 swap_2_rate = b_bid
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "quote_to_base"
#                 contract_2 = pair_b
#
#                 # if b_base(acquired coin) matches c_base
#                 if b_base == c_base:
#                     swap_3 = c_base
#                     swap_3_rate = 1 / c_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_c
#                 if b_base == c_quote:
#                     swap_3=c_quote
#                     swap_3_rate = c_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_c
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#
#             # check if a_base (acquired coin) matches b_base """
#             """ SCENARIO:02 """
#         if direction == "reverse":
#             if a_base == b_base and calculated == 0:
#                 swap_2 = b_base
#                 swap_2_rate = 1 / b_ask
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "base_to_quote"
#                 contract_2 = pair_b
#
#                 # if b_quote(acquired coin) matches c_base
#                 if b_quote == c_base:
#                     swap_3 = c_base
#                     swap_3_rate = 1 / c_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_c
#                 if b_quote == c_quote:
#                     swap_3=c_quote
#                     swap_3_rate = c_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_c
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#
#             """ SCENARIO:03 """
#             # what if a_base matches c_quote
#         if direction == "reverse":
#             if a_base == c_quote and calculated == 0:
#                 swap_2=c_quote
#                 swap_2_rate = c_bid
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "quote_to_base"
#                 contract_2 = pair_c
#
#                 # if c_base(acquired coin) matches b_base
#                 if c_base == b_base:
#                     swap_3 = b_base
#                     swap_3_rate = 1 / b_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_b
#                 # if c_base(acquired coin) matches b_quote
#                 if c_base == b_quote:
#                     swap_3=b_quote
#                     swap_3_rate = b_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_b
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#             """ SCENARIO:04 """
#             # what if a_base matches c_base
#         if direction == "reverse":
#             if a_base == c_base and calculated == 0:
#                 swap_2 = c_base
#                 swap_2_rate = 1 / c_ask
#                 acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
#
#                 direction_trade_2 = "base_to_quote"
#                 contract_2 = pair_c
#
#                 # if c_quote(acquired coin) matches b_base
#                 if c_quote == b_base:
#                     swap_3 = b_base
#                     swap_3_rate = 1 / b_ask
#                     direction_trade_3 = "base_to_quote"
#                     contract_3 = pair_b
#                 # if c_quote(acquired coin) matches b_quote
#                 if c_quote == b_quote:
#                     swap_3=b_quote
#                     swap_3_rate = b_bid
#                     direction_trade_3 = "quote_to_base"
#                     contract_3 = pair_b
#
#                 acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
#                 calculated = 1
#
#         """Profit and loss percentage """
#         profit_loss=acquired_coin_t3-starting_amount
#         profit_loss_perc=(profit_loss/starting_amount)*100 if profit_loss!=0 else 0
#         #Trade Descriptions
#
#         if profit_loss_perc > 0:
#             trade_description_1 = f"Start with {swap_1} of {starting_amount}. Swap at {swap_1_rate} for {swap_2} acquiring {acquired_coin_t1}."
#             trade_description_2 = f"Swap {acquired_coin_t1} of {swap_2} at {swap_2_rate} for {swap_3} acquiring {acquired_coin_t2}."
#             trade_description_3 = f"Swap {acquired_coin_t2} of {swap_3} at {swap_3_rate} for {swap_1} acquiring {acquired_coin_t3}."
#             print("New Trade")
#             print(trade_description_1)
#             print(trade_description_2)
#             print(trade_description_3)
#             print(direction, pair_a, pair_b, pair_c, starting_amount, acquired_coin_t3)

#Calculate Surface Rate Arbitrage Opportunity

def calc_triangular_arb_surface_rate(t_pair, prices_dict):

    # Set Variables
    starting_amount = 1
    min_surface_rate = 0
    surface_dict = {}
    contract_2 = ""
    contract_3 = ""
    direction_trade_1 = ""
    direction_trade_2 = ""
    direction_trade_3 = ""
    acquired_coin_t2 = 0
    acquired_coin_t3 = 0
    calculated = 0

    # Extract Pair Variables
    a_base = t_pair["a_base"]
    a_quote = t_pair["a_quote"]
    b_base = t_pair["b_base"]
    b_quote = t_pair["b_quote"]
    c_base = t_pair["c_base"]
    c_quote = t_pair["c_quote"]
    pair_a = t_pair["pair_a"]
    pair_b = t_pair["pair_b"]
    pair_c = t_pair["pair_c"]

    # Extract Price Information
    a_ask = prices_dict["pair_a_ask"]
    a_bid = prices_dict["pair_a_bid"]
    b_ask = prices_dict["pair_b_ask"]
    b_bid = prices_dict["pair_b_bid"]
    c_ask = prices_dict["pair_c_ask"]
    c_bid = prices_dict["pair_c_bid"]

    # Set directions and loop through
    direction_list = ["forward", "reverse"]
    for direction in direction_list:

        # Set additional variables for swap information
        swap_1 = 0
        swap_2 = 0
        swap_3 = 0
        swap_1_rate = 0
        swap_2_rate = 0
        swap_3_rate = 0

        """
            Poloniex Rules !!
            If we are swapping the coin on the left (Base) to the right (Quote) then * (1 / Ask)
            If we are swapping the coin on the right (Quote) to the left (Base) then * Bid
        """

        # Assume starting with a_base and swapping for a_quote
        if direction == "forward":
            swap_1 = a_base
            swap_2 = a_quote
            swap_1_rate = 1 / a_ask
            direction_trade_1 = "base_to_quote"

        # Assume starting with a_base and swapping for a_quote
        if direction == "reverse":
            swap_1 = a_quote
            swap_2 = a_base
            swap_1_rate = a_bid
            direction_trade_1 = "quote_to_base"

        # Place first trade
        contract_1 = pair_a
        acquired_coin_t1 = starting_amount * swap_1_rate

        """  FORWARD """
        # SCENARIO 1 Check if a_quote (acquired_coin) matches b_quote
        if direction == "forward":
            if a_quote == b_quote and calculated == 0:
                swap_2_rate = b_bid
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "quote_to_base"
                contract_2 = pair_b

                # If b_base (acquired coin) matches c_base
                if b_base == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 / c_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_c

                # If b_base (acquired coin) matches c_quote
                if b_base == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = c_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_c

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 2 Check if a_quote (acquired_coin) matches b_base
        if direction == "forward":
            if a_quote == b_base and calculated == 0:
                swap_2_rate = 1 / b_ask
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "base_to_quote"
                contract_2 = pair_b

                # If b_quote (acquired coin) matches c_base
                if b_quote == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 / c_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_c

                # If b_quote (acquired coin) matches c_quote
                if b_quote == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = c_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_c

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 3 Check if a_quote (acquired_coin) matches c_quote
        if direction == "forward":
            if a_quote == c_quote and calculated == 0:
                swap_2_rate = c_bid
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "quote_to_base"
                contract_2 = pair_c

                # If c_base (acquired coin) matches b_base
                if c_base == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 / b_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_b

                # If c_base (acquired coin) matches b_quote
                if c_base == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = b_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_b

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 4 Check if a_quote (acquired_coin) matches c_base
        if direction == "forward":
            if a_quote == c_base and calculated == 0:
                swap_2_rate = 1 / c_ask
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "base_to_quote"
                contract_2 = pair_c

                # If c_quote (acquired coin) matches b_base
                if c_quote == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 / b_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_b

                # If c_quote (acquired coin) matches b_quote
                if c_quote == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = b_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_b

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        """  REVERSE """
        # SCENARIO 1 Check if a_base (acquired_coin) matches b_quote
        if direction == "reverse":
            if a_base == b_quote and calculated == 0:
                swap_2_rate = b_bid
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "quote_to_base"
                contract_2 = pair_b

                # If b_base (acquired coin) matches c_base
                if b_base == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 / c_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_c

                # If b_base (acquired coin) matches c_quote
                if b_base == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = c_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_c

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 2 Check if a_base (acquired_coin) matches b_base
        if direction == "reverse":
            if a_base == b_base and calculated == 0:
                swap_2_rate = 1 / b_ask
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "base_to_quote"
                contract_2 = pair_b

                # If b_quote (acquired coin) matches c_base
                if b_quote == c_base:
                    swap_3 = c_base
                    swap_3_rate = 1 / c_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_c

                # If b_quote (acquired coin) matches c_quote
                if b_quote == c_quote:
                    swap_3 = c_quote
                    swap_3_rate = c_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_c

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 3 Check if a_base (acquired_coin) matches c_quote
        if direction == "reverse":
            if a_base == c_quote and calculated == 0:
                swap_2_rate = c_bid
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "quote_to_base"
                contract_2 = pair_c

                # If c_base (acquired coin) matches b_base
                if c_base == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 / b_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_b

                # If c_base (acquired coin) matches b_quote
                if c_base == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = b_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_b

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        # SCENARIO 4 Check if a_base (acquired_coin) matches c_base
        if direction == "reverse":
            if a_base == c_base and calculated == 0:
                swap_2_rate = 1 / c_ask
                acquired_coin_t2 = acquired_coin_t1 * swap_2_rate
                direction_trade_2 = "base_to_quote"
                contract_2 = pair_c

                # If c_quote (acquired coin) matches b_base
                if c_quote == b_base:
                    swap_3 = b_base
                    swap_3_rate = 1 / b_ask
                    direction_trade_3 = "base_to_quote"
                    contract_3 = pair_b

                # If c_quote (acquired coin) matches b_quote
                if c_quote == b_quote:
                    swap_3 = b_quote
                    swap_3_rate = b_bid
                    direction_trade_3 = "quote_to_base"
                    contract_3 = pair_b

                acquired_coin_t3 = acquired_coin_t2 * swap_3_rate
                calculated = 1

        """ PROFIT LOSS OUTPUT """

        # Profit and Loss Calculations
        profit_loss = acquired_coin_t3 - starting_amount
        profit_loss_perc = (profit_loss / starting_amount) * 100 if profit_loss != 0 else 0

        # Trade Descriptions
        trade_description_1 = f"Start with {swap_1} of {starting_amount}. Swap at {swap_1_rate} for {swap_2} acquiring {acquired_coin_t1}."
        trade_description_2 = f"Swap {acquired_coin_t1} of {swap_2} at {swap_2_rate} for {swap_3} acquiring {acquired_coin_t2}."
        trade_description_3 = f"Swap {acquired_coin_t2} of {swap_3} at {swap_3_rate} for {swap_1} acquiring {acquired_coin_t3}."

        # Output Results
        if profit_loss_perc > min_surface_rate:
            surface_dict = {
                "swap_1": swap_1,
                "swap_2": swap_2,
                "swap_3": swap_3,
                "contract_1": contract_1,
                "contract_2": contract_2,
                "contract_3": contract_3,
                "direction_trade_1": direction_trade_1,
                "direction_trade_2": direction_trade_2,
                "direction_trade_3": direction_trade_3,
                "starting_amount": starting_amount,
                "acquired_coin_t1": acquired_coin_t1,
                "acquired_coin_t2": acquired_coin_t2,
                "acquired_coin_t3": acquired_coin_t3,
                "swap_1_rate": swap_1_rate,
                "swap_2_rate": swap_2_rate,
                "swap_3_rate": swap_3_rate,
                "profit_loss": profit_loss,
                "profit_loss_perc": profit_loss_perc,
                "direction": direction,
                "trade_description_1": trade_description_1,
                "trade_description_2": trade_description_2,
                "trade_description_3": trade_description_3
            }

            return surface_dict

    return surface_dict


#reformating orderbook for depth calculation
def reformated_orderBook(prices,c_direction):
    price_list_main=[]
    if c_direction=="base_to_quote":
        for p in prices["asks"]:
            ask_price=float(p[0])
            adj_price=1/ask_price if ask_price!=0 else 0
            adj_quantity=float(p[1]) * ask_price
            price_list_main.append([adj_price,adj_quantity])

    if c_direction == "quote_to_base":
        for p in prices["bids"]:
            bid_price = float(p[0])
            adj_price = bid_price if bid_price != 0 else 0
            adj_quantity = float(p[1])
            price_list_main.append([adj_price, adj_quantity])

    return price_list_main


#calculating depth prices
def calculate_acquired_coin( amount_in,depth_prices):

    pass


def get_depth_from_orderbook():
    """
    Challenges
    our whole capital of starting amount maybe eaten at level 1 depth
    our capital maybe eaten in multiple levels
    there may not be enough depth to sell the whole assest(in case of rubbish/shit coins)

    """

    #extract initial variables
    swap_1="USDT"
    starting_amount=1
    starting_amount_dict={
        "USDT":100,
        'BTC':0.5,
        'ETH':1,
        'XRP':200
    }
    if swap_1 in starting_amount_dict:
        starting_amount=starting_amount_dict[swap_1]

    #define pairs
    contract_1='USDT_BTC'
    contract_2='BTC_INJ'
    contract_3='USDT_INJ'

    #pairs direction
    contract_1_direction='base_to_quote'
    contract_2_direction='base_to_quote'
    contract_3_direction='quote_to_base'

    #getting orderbook data for assessment
    url=f"https://poloniex.com/public?command=returnOrderBook&currencyPair={contract_1}&depth=20"
    contract_1_prices=get_data(url)
    contract_1_formated_prices= reformated_orderBook(contract_1_prices,contract_1_direction)
    time.sleep(0.5)
    url2 = f"https://poloniex.com/public?command=returnOrderBook&currencyPair={contract_2}&depth=20"
    contract_2_prices = get_data(url2)
    contract_2_formated_prices = reformated_orderBook(contract_2_prices, contract_2_direction)
    time.sleep(0.5)
    url3 = f"https://poloniex.com/public?command=returnOrderBook&currencyPair={contract_3}&depth=20"
    contract_3_prices = get_data(url3)
    contract_3_formated_prices = reformated_orderBook(contract_3_prices, contract_3_direction)


    #get acquired coins
    acquired_coin_t1=calculate_acquired_coin(starting_amount,contract_1_formated_prices)
    acquired_coin_t2 = calculate_acquired_coin(acquired_coin_t1, contract_2_formated_prices)
    acquired_coin_t3 = calculate_acquired_coin(acquired_coin_t2, contract_3_formated_prices)

