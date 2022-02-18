money_pertner:int = 0
battery_remain_pertner:float = 100
pv_pertner:float = 20
discharge_power_pertner:float = 10
demand_pertner = 10

money:float = 0
battery_remain:float = 35 #バッテリー残量
pv:float = 5 #発電量
discharge_power:float = 30
demand = 10
discharge_power_LIMIT = 10

CHARGE_LIMIT = 10
CAPACITY = 100
SURPLUS_PRICE = 10
GRIDPOWER_BUY = 18
GRIDPOWER_SELL = 8


if demand >= pv:
    demand_remain = demand - pv
    "発電量を供給"
    if demand_remain > battery_remain:
        demand_remain = demand_remain - battery_remain
        battery_remain = 0
    else:
        battery_remain = battery_remain - demand_remain
        demand_remain = 0
    "蓄電池放電による供給"
    if demand_remain > 0:
        "電力融通リクエスト"
        if pv_pertner > demand_pertner :#購入許可
            pv_remain_pertner = pv_pertner - demand_pertner
            if battery_remain >= pv_remain_pertner:
                money -= demand_remain * SURPLUS_PRICE #処理別に書く
                pv_remain_pertner
                demand_remain = 0
                "電力もらって供給(もらえるだけもらう)"
    if demand_remain > 0:
        money -= demand_remain * GRIDPOWER_BUY
        demand_remain = 0
else:
    "発電量で消費量に供給"
    pv_remain = pv - demand
    demand_remain = 0
    if pv_remain > 0:
        if battery_remain > 0:
            "蓄電池に充電"
            if battery_remain >= pv_remain:
                battery_remain = battery_remain - pv_remain
                pv_remain = 0
            else:
                battery_remain = CHARGE_LIMIT
                pv_remain -= CHARGE_LIMIT - battery_remain
            if pv_remain > 0:
                "電力売却リクエスト"
                if battery_remain_pertner > 0 :#売却許可
                    "発電余剰の融通"
            if pv_remain > 0:
                money += pv_remain * GRIDPOWER_SELL
                pv_remain = 0
        else:
            "電力売却リクエスト"
            if battery_remain > 0: #販売許可
                "発電余剰の融通"
            if battery_remain > 0:
                money += pv_remain * GRIDPOWER_SELL
                pv_remain = 0
if demand_remain > 0:
    money -= demand_remain * GRIDPOWER_BUY
    demand_remain = 0
if pv_remain > 0:
    money += pv_remain * GRIDPOWER_SELL
    pv_remain = 0