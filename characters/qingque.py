from characters.base_character import Character
import numpy as np

class Qingque(Character):
  def __init__(self, behavior = "Agressive", eidolon = 6, **kwargs):
    super().__init__(**kwargs)
    self.name = "Qingque"
    self.max_energy = 140
    if self.energy  == "MoC":
      self.energy = 0.5*self.max_energy
    self.tiles = 0
    self.skill_uses = 0
    self.tile_battle = True
    self.draws = None
    self.autarkey_multiplier = 1
    self.hidden_hand = 8
    self.behavior = behavior #Agressive, Emergency, Auto Battle
    self.eidolon = eidolon
    self.autarkey_chance = 0.25
    self.expected_damage = 0
    self.maximum_damage = 0
    self.ult_expected_damage = 0
    self.ult_max_damage = 0
    
  def basic(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.energy += 20
    if verbose:
      print("QQ uses basic! SP +1")
    mv = 1.1
    avdmg = self.average_damage(mv)
    self.autarkey_multiplier = min(2, 1 + self.autarkey_chance*self.skill_uses)
    self.expected_damage = avdmg*self.autarkey_multiplier
    critdmg = self.max_damage(mv)
    self.maximum_damage = 2 * critdmg

  def enhanced_basic(self, verbose= None):
    if verbose is None:
      verbose = self.verbose
    #add movement values
    #add 1 to SP if E6
    self.energy += 20
    if self.eidolon >= 6:
      self.arena.sp +=1
    if verbose:
      print("QQ uses enhanced basic! SP +1")
    self.tiles = 0
    self.energy += 20
    mv = 4.84
    avdmg = self.average_damage(mv)
    self.autarkey_multiplier = min(2, 1 + self.autarkey_chance*self.skill_uses)
    self.expected_damage = avdmg*self.autarkey_multiplier
    critdmg = self.max_damage(mv)
    self.maximum_damage = 2 * critdmg

  def skill(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    #Draw tiles
    if self.tile_battle:
      arena.sp +=1
      self.tile_battle = False
    if verbose:
      print(f"Attempting to draw {self.hidden_hand - self.tiles} tiles with {arena.sp} SP")
    self.draws = np.ceil((self.hidden_hand - self.tiles)/2)
    self.energy += self.draws
  
  def hidden_hand_failure(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    dmg_bonus = 0.408*arena.sp
    self.skill_uses = arena.sp
    sp_used = arena.sp
    self.damage_percent += dmg_bonus
    self.buffs_list.append({"attribute name":"damage_percent", "recipient":self, "tickdown":self, "value":dmg_bonus, "duration":1})
    arena.sp = 0
    if verbose:
      print("Hidden Hand Failed!")
      print(f"Attempted to use {sp_used} SP to draw {self.draws * 2} tiles")
      print(f"Damage increased by {dmg_bonus * 100}%")
  
  def hidden_hand_success(self,verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    atk_bonus = 0.792
    dmg_bonus = 0.408*self.draws
    self.skill_uses = self.draws
    self.attack_percent += atk_bonus
    self.damage_percent += dmg_bonus
    self.buffs_list.append({"attribute name":"attack_percent", "recipient":self, "tickdown":self, "value":atk_bonus, "duration":1})
    self.buffs_list.append({"attribute name":"damage_percent", "recipient":self, "tickdown":self, "value":dmg_bonus, "duration":1})
    arena.sp -= self.draws
    self.update_stats()
    if verbose:
      print("Hidden Hand Sucess!")
      print(f"{self.draws} SP consumed to draw {self.draws * 2} tiles")
      print(f"Attack increased by {atk_bonus * 100}%, Damage increased by {dmg_bonus * 100}%")
      self.get_stats()
  
  def ult(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    mv = 5*2.16
    self.ult_expected_damage = self.average_damage(mv)
    self.ult_max_damage = self.max_damage(mv)
    if verbose:
      print("Qingque uses ultimate!")
    self.energy = 5

  def update_stats(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    try:
      self.total_attack = self.base_attack * (1 + self.attack_percent) + self.flat_attack
    except TypeError:
      if verbose:
        print("Warning: Qingque's update_stats failed due to blank stat values.")
      else:
        pass

class Qingque_Probabilities():
  pass
  