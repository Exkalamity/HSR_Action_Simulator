import pandas as pd
import numpy as np

class Data_Table():
    def __init__(self):
        pass
    pass

class Action_Table(Data_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Name", "Cycle", "Action Gauge", "Current SP", "Current Energy", "Action", "SP Gain"])
        self.sp_now = None

    def add_row(self, arena, chara, action, sp_change):
        new_row = {"Name":chara.name, "Cycle":arena.cycle, "Action Gauge":arena.action_gauge, "Current SP":arena.sp, 
                   "Current Energy":chara.energy, "Action":action, "SP Gain":sp_change}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index = True)
    # def update_sp(self, arena):
    #     self.sp_now = arena.sp
class Qingque_Probability_Table(Data_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Cycle", "Action Gauge", "Current SP", "Current Tiles", "P(Success)", "Average # Skills", "Most Likely # Skills", "SP Consumed"])
    def add_row(self, arena, chara, tiles):
        new_row ={"Cycle":arena.cycle, "Action Gauge":arena.action_gauge, "Current SP":arena.sp, "Current Tiles":tiles, "P(Success)":chara.success_chance, 
                    "Average # Skills":chara.average_multiplier, "Most Likely # Skills":chara.likely_multiplier, "SP Consumed":np.round(chara.likely_multiplier)}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index = True)
    