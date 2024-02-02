import pandas as pd
import numpy as np

class Data_Table():
    def __init__(self):
        pass
    pass

class Action_Table(Data_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Name", "Cycle", "Action Gauge", "Current SP", "Current Energy", "Action"])
        self.sp_now = None

    def append(self, arena, chara, action):
        new_row = {"Name":chara.name, "Cycle":arena.cycle, "Action Gauge":arena.action_gauge, "Current SP":arena.sp, 
                   "Current Energy":chara.energy, "Action":action}
        self.df = self.df.append(new_row, ignore_index = True)
    # def update_sp(self, arena):
    #     self.sp_now = arena.sp