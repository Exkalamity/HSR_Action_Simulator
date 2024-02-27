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
        self.df = pd.DataFrame(columns = ["Cycle", "Action Gauge", "Current SP", "Current Tiles", "Hidden Hand", "P(Low)", "P(High)", "QQ Draws", "QQ Roll", "SP Used"])
    def add_row(self, arena, chara, tiles, used, hh, p):
        new_row ={"Cycle":arena.cycle, "Action Gauge":arena.action_gauge, "Current SP":arena.sp, "Current Tiles":tiles, "Hidden Hand":hh, "P(Low)":100*chara.p_low, 
                   "P(High)":100*chara.p_high, "QQ Draws":chara.draws,"QQ Roll":p, "SP Used":used}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index = True)

class Qingque_Statistics_Table(Data_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Sim #", "Turn", "Cycle", "Action Gauge", "Current SP", "Current Tiles", "# Draws", "Hidden Hand Win Rate"])
    def add_row(self, arena, chara, sim, tiles, used):
        new_row = {"Sim #":sim, "Turn":chara.turn, "Cycle":arena.cycle, "Action Gauge":arena.action_gauge, "Current SP":arena.sp, "Current Tiles":tiles, "# Draws":chara.draws, "Hidden Hand Win Rate":chara.hidden_hand}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index = True)