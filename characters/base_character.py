import numpy as np

class Character():
  def __init__(self, arena, Base_HP = None, HPPct = None , Total_HP = None, Base_Atk = None, AtkPct = None, Total_Atk = None, Base_Def = None,
               DefPct = None, Total_Def = None, DmgPct = None, CritRate = None, CritDmg = None, Spd = None, Break = None, ER = 1.0,
               EHR = None, Res = None, E = "MoC", verbose = False):
    self.base_hp = Base_HP
    self.hp_percent = HPPct
    self.total_hp = Total_HP
    self.base_attack = Base_Atk
    try:
      self.attack_percent = AtkPct/100
    except TypeError:
      self.attack_percent = AtkPct
    self.total_attack = Total_Atk
    self.base_defense = Base_Def
    self.defense_percent = DefPct
    self.total_defense = Total_Def
    try:
      self.crit_rate = CritRate/100
    except TypeError:
      self.crit_rate = CritRate
    try:
      self.crit_damage = CritDmg/100
    except TypeError:
      self.crit_damage = CritDmg
    try:
      self.damage_percent = DmgPct/100
    except TypeError:
          self.crit_damage = DmgPct
    self.Break_Effect = Break
    self.effect_hit_rate = EHR
    self.effect_resistance = Res
    self.speed = Spd
    try:
      self.action_value = 10000/self.speed
    except TypeError:
      self.action_value = 100
    self.action_gauge = self.action_value
    self.energy_regen = ER
    self.actions = 0
    self.energy = E
    self.verbose = verbose
    self.arena = arena
    self.buffs_list = [] #Store buffs as a list of dictionaries: {name:"attribute_name", giver:"character name", value:value, duration:duration}
    try:
      self.flat_attack = self.total_attack - self.base_attack - self.base_attack*self.attack_percent
    except TypeError:
      if self.verbose:
        print(f"Cannot calculate character attack due to invalid values for base attack, attack percent, and/or total attack")
  def action_advance(self, AG, verbose = None):
    self.action_gauge -= AG
  def update_buffs(self, verbose = None): #function for counting down buffs from other characters
    if verbose is None:
      verbose = self.verbose
    for buff in self.buffs_list.copy():
      buff["duration"] -= 1
      if buff["duration"] <1:
        current_value = getattr(buff["tickdown"], buff["attribute name"])
        setattr(buff["tickdown"], buff["attribute name"], current_value - buff["value"])
        if verbose:
          print(f"{buff['recipient'].name}'s {buff['value']*100}% {buff['attribute name']} removed")
        self.buffs_list.remove(buff)
    self.update_stats()
  
  def action_reset(self, verbose = None):
    if verbose == None:
      verbose = self.verbose
    self.action_gauge = self.action_value
    if verbose:
      print(f"{self.name}'s action gauge reset to {self.action_value}")
  
  def get_stats(self):
    print(f"Base Attack: {self.base_attack}, Attack Percent: {self.attack_percent * 100}%, Flat Attack: {self.flat_attack}, Total_Attack: {self.total_attack},")
    print(f"Crit Rate: {self.crit_rate * 100}%, Crit Damage: {self.crit_damage*100}%, Damage Percent: {self.damage_percent*100}%, Speed = {self.speed}")
  
  def average_damage(self, mv, enlvl = 95, weak = True, broken = False, def_shred = 0, res_shred = 0):
    base_damage = self.total_attack * mv
    dmg_multiplier = self.damage_percent
    def_mult = 100/((enlvl + 20)*(1 - def_shred) +100)
    if weak == True:
      res = 1
    else:
      res = 0.8
    res -= res_shred
    crit_multiplier = (1 - self.crit_rate) + self.crit_rate * self.crit_damage
    return base_damage * dmg_multiplier * def_mult * res * crit_multiplier
  
  def max_damage(self, mv, enlvl = 95, weak = True, broken = False, def_shred = 0, res_shred = 0):
    base_damage = self.total_attack * mv
    dmg_multiplier = self.damage_percent
    def_mult = 100/((enlvl + 20)*(1 - def_shred) +100)
    if weak == True:
      res = 1
    else:
      res = 0.8
    res -= res_shred
    return base_damage * dmg_multiplier * def_mult * res * self.crit_damage