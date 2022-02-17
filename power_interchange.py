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
all_energy = battery_remain + pv - discharge_power
discharge_power_LIMIT = 10

CHARGE_LIMIT = 10
CAPACITY = 100


if demand >= pv:
    "発電量を供給"
    "蓄電池放電による供給"
    if demand > 0:
        "電力融通リクエスト"
        if "購入許可":
            "電力もらって供給"
    if demand > 0:
        "系統から電力購入"
else:
    "発電量で消費量に供給"
    if "発電余剰" > 0:
        if "蓄電池空き容量" > 0:
            "蓄電池に充電"
            if "発電余剰" > 0:
                "電力売却リクエスト"
                if "売却許可":
                    "発電余剰の融通"
            if "発電余剰" > 0:
                "系統に電力売却"
        else:
            "電力売却リクエスト"
            if "売却許可":
                "発電余剰の融通"
            if "発電余剰" > 0:
                "系統に電力売却"
if "発電余剰があったとき":
    "系統に全部売る"