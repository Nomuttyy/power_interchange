import pandas as pd

# timestamps = pd.date_range('2020-01-01 00:00:00', '2020-12-31 23:30:00', freq='30T').to_pydatetime()
# timestamps = pd.Series(timestamps)
# timestamps.to_csv("test.csv", index=None)


money_pertner:int = 0
battery_remain_pertner:float = 100
pv_pertner:float = 20
discharge_power_pertner:float = 10
money:float = 0
battery_remain:float = 35
pv:float = 5
discharge_power:float = 30
all_energy = battery_remain + pv - discharge_power
discharge_power_LIMIT = 10
CHARGE_LIMIT = 10
CAPACITY = 100
for n in range(50):
    battery_remain = battery_remain + pv - discharge_power
    battery_remain_pertner = battery_remain_pertner + pv_pertner - discharge_power_pertner
    if battery_remain < 0 :
        if battery_remain_pertner + pv_pertner - discharge_power_pertner >= 0: # 相手方のバッテリーと太陽光発電量が需要を超えない場合
            pertner_surplus = discharge_power_pertner + pv_pertner
            battery_remain += pertner_surplus
            money -= pertner_surplus * 10
        if battery_remain <= 0 :# パートナーから買って尚電力が足りなかった場合
            pay = all_energy * -1 * 18
            money -= pay
            battery_remain = 0
    else:
        pass
    print(battery_remain, money)