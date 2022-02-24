import csv
import pandas as pd

money_pertner:int = 0
battery_pertner:float = 30
pv_pertner:float = 10
discharge_power_pertner:float = 10
demand_pertner = 10

money:float = 0
battery:float = 35 #バッテリー残量
pv:float = 80 #発電量
discharge_power:float = 30
demand = 20
discharge_power_LIMIT = 10

CHARGE_LIMIT = 10
CAPACITY = 100
SURPLUS_PRICE = 10
GRIDPOWER_BUY = 18
GRIDPOWER_SELL = 8


# print(pv, demand, battery, money, money_pertner)

class Simulate():
    def __init__(self):
        self.idx = 0
        self.pvdf = pd.read_csv('data/PV.csv')
        self.demanddf = pd.read_csv('data/pattern2.csv')
        self.demanddf_pertner = pd.read_csv('data/pattern3.csv')
        self.money_pertner:int = 0
        self.battery_pertner:float = 30
        self.pv_pertner:float = self.pvdf.at[self.idx, 'PV'] / 1.75 /2
        self.discharge_power_pertner:float = 10
        self.demand_pertner = self.demanddf_pertner.at[self.idx, 'demand']
        self.money:float = 0
        self.battery:float = 35 #バッテリー残量
        self.pv:float = self.pvdf.at[self.idx, 'PV'] / 1.75 /2#発電量
        self.discharge_power:float = 30
        self.demand = self.demanddf.at[self.idx, 'demand']
        self.discharge_power_LIMIT = 10
        self.CHARGE_LIMIT = 10
        self.CAPACITY = 100
        self.SURPLUS_PRICE = 10
        self.GRIDPOWER_BUY = 18
        self.GRIDPOWER_SELL = 8
        self.header = ['index', 'pv', 'demand', 'battery', 'money']
        self.data = []


    def onestep(self):
        self.idx = self.idx
        self.pv_pertner:float = self.pvdf.at[self.idx, 'PV']
        self.demand_pertner = self.demanddf_pertner.at[self.idx, 'demand']
        self.pv:float = self.pvdf.at[self.idx, 'PV']
        self.demand = self.demanddf.at[self.idx, 'demand']
        if self.demand >= self.pv:
            self.demand = self.demand - self.pv
            self.pv = 0
            "発電量を供給"
            if self.demand > self.battery:
                self.demand = self.demand - self.battery
                self.battery = 0
            else:
                self.battery = self.battery - self.demand
                self.demand = 0
            "蓄電池放電による供給"
            if self.demand > 0:
                "電力融通リクエスト"
                if self.pv_pertner > self.demand_pertner :#購入許可
                    self.v_pertner = self.pv_pertner - self.demand_pertner
                    if self.battery >= self.pv_pertner:
                        self.money -= self.demand * self.SURPLUS_PRICE
                        self.money_pertner += self.demand * self.SURPLUS_PRICE
                        self.pv_pertner = 0
                        self.demand = 0
                        "電力もらって供給(もらえるだけもらう)"
            if self.demand > 0:
                self.money -= self.demand * self.GRIDPOWER_BUY
                self.demand = 0
        else:
            "発電量で消費量に供給"
            self.pv = self.pv - self.demand
            self.demand = 0
            if self.pv > 0:
                if self.battery > 0:
                    "蓄電池に充電"
                    if self.CAPACITY - self.battery >= self.pv:
                        if self.pv > self.CHARGE_LIMIT:
                            self.pv -= self.CHARGE_LIMIT
                            self.battery += self.CHARGE_LIMIT
                        else:
                            self.battery += self.pv
                            self.pv = 0
                    else:
                        if self.pv > self.CHARGE_LIMIT:
                            self.pv -= self.CHARGE_LIMIT - (self.CAPACITY - self.battery)
                            self.battery = self.CAPACITY
                        else:
                            self.pv -= self.CAPACITY - self.battery
                            self.battery = self.CAPACITY
                    if self.pv > 0:
                        "電力売却リクエスト"
                        if self.CAPACITY - self.battery_pertner > self.pv:#売却許可
                            self.battery_pertner += self.pv
                            self.money_pertner -= self.pv * self.SURPLUS_PRICE
                            self.money += self.pv * self.SURPLUS_PRICE
                            "発電余剰の融通"

                    if self.pv > 0:
                        self.money += self.pv * self.GRIDPOWER_SELL
                        self.pv = 0
                else:
                    "電力売却リクエスト"
                    if self.battery > 0: #販売許可
                        "発電余剰の融通"
                    if self.battery > 0:
                        self.money += self.pv * self.GRIDPOWER_SELL
                        self.pv = 0
        if self.demand > 0:
            self.money -= self.demand * self.GRIDPOWER_BUY
            self.demand = 0
        if self.pv > 0:
            self.money += self.pv * self.GRIDPOWER_SELL
            self.pv = 0
        print(self.pv, self.demand, self.battery, self.money, self.money_pertner) #発電量需要量(前の)充電量放電量融通量etc
        self.data.append([self.idx, self.pv, self.demand, self.battery, self.money])
        self.idx += 1 
    
    def write(self, name: str):
        with open(name, 'w') as f: 
            writer = csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.data)
            f.close()


simu = Simulate()
for i in range(300):
    simu.onestep()
simu.write('result.csv')
# data.insert(0, ['pv', 'demand', 'money'])

# PVとdemandのデータ作る
# 変数更新fix