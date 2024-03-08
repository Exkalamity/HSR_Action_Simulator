import pandas as pd
import numpy as np

class Data_Table():
    def __init__(self):
        pass
    pass

    def get_chara(self, name):
        output = self.df.loc[self.df["Name"] == name]
        output
        return output
    
    def get_cycles(self, cycle):
        output = self.df.loc[self.df["Cycle"] == cycle]
        output
        return output
    
    def get_turns(self, turn):
        output = self.df.loc[self.df["Turn"] == turn]
        output
        return output



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

class Buff_Table(Data_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Name", "Holder Name", "Source Name", "Recipient Name", 
             "Stat", "Amount", "Remaining Turns"])
        
    def add_row(self, name, holder_name, source_name, recipient_name, stat, amount, remaining_turns):    
        new_row = {"Name":name, "Holder Name":holder_name, "Source Name":source_name, "Recipient Name":recipient_name, 
             "Stat":stat, "Amount":amount, "Remaining Turns":remaining_turns}
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
  
    def concat(self, buff):
        try:
            new_entry = buff.df.copy()
        except AttributeError:
            new_entry = buff.copy()
        self.df = pd.concat([self.df, new_entry], ignore_index=True)

    def refresh_buff(self, name, duration):
        self.df.loc[self.df["Name"] == name, "Remaining Turns"] = duration
    
    def check_buff(self, name):
        return (self.df["Name"] == name).any()
        
    def tick_down(self, holder):
        self.df.loc[self.df["Holder Name"] == holder, "Remaining Turns"] -= 1
        self.df = self.df[self.df["Remaining Turns"] != 0].copy()

class Battle_Buffs_Tracker(Buff_Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = pd.DataFrame(columns = ["Cycle", "Action Gauge", "Name", "Holder Name", "Source Name", "Recipient Name", 
             "Stat", "Amount", "Remaining Turns"])
        
    def add_character_buffs(self, buffs, arena):
        new_entry = buffs.df.copy()
        new_entry["Cycle"] = arena.cycle
        new_entry["Action Gauge"] = arena.action_gauge
        self.df = pd.concat([self.df, new_entry], ignore_index=True)

    def get_chara(self, name):
        output = self.df.loc[self.df["Holder Name"] == name]
        output
        return output
