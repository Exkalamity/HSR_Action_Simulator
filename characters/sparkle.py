from characters.base_character import Character
from utils.data_table import Buff_Table

class Sparkle(Character):
  def __init__(self, recipient, party = None, tech = False, broyna_lc = False, t1_skill = True, **kwargs):
    super().__init__(**kwargs)
    self.name = "Sparkle"
    self.max_energy = 110
    self.party = party.append(self)
    self.recipient  = recipient

    self.skill_buff = Buff_Table()
    self.skill_buff.add_row(name="Dreamdiver", holder_name=recipient.name, source_name=self.name, 
                            recipient_name=recipient.name, stat = "Crit Dmg", amount = 100, remaining_turns=1)
    self.ult_buff = Buff_Table()
    for member in party:
      self.ult_buff.add_row(name="Cipher", holder_name=member.name, source_name=self.name, 
                            recipient_name=member.name, stat = "Dmg%", amount = 30, remaining_turns=2)
    

    self.tech = tech
    self.bronya_lc = broyna_lc
    self.ult_counter = 1
    self.t1_skill = t1_skill
    if self.energy == "MoC":
      self.energy = 0.5*self.max_energy

  def basic(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.energy += 30*self.energy_regen
    if verbose:
      print("Sparkle uses basic! SP +1")

  def skill(self, recipient = None, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    if recipient is None:
      recipient = self.recipient
    if recipient.action_gauge > 0.5 * recipient.action_value:
      adv = 0.5 * recipient.action_value - 0.1
    else:
      adv = recipient.action_gauge - 0.0001
    recipient.action_gauge -= adv

    recipient.buffs.concat(self.skill_buff)
    self.energy += 30 *self.energy_regen
    arena.sp -= 1
    if verbose:
      print("Sparkle uses skill! SP -1")
      print(f"{recipient.name} is advanced forward by {adv}!" )
  
  def ult(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    self.energy = 5
    if self.bronya_lc:
      if self.ult_counter == 1:
        arena.sp +=5
        self.ult_counter -=1
        if verbose:
          print("Sparkle uses Ult!")
          print("SP + 5!")
      else:
        arena.sp +=4
        self.ult_counter = 1
        if verbose:
          print("Sparkle uses Ult!")
          print("SP + 4!")
    else:
      arena.sp +=4
      if verbose:
          print("Sparkle uses Ult!")
          print("SP + 4!")

  def apply_ult_buff(self, party):#Manually insert Party
    sparkle_ult_name = "Cipher"
    # if self.buffs.check_buff(sparkle_ult_name):
    #   print(f"Refreshing {sparkle_ult_name} on Sparkle")
    #   self.buffs.refresh_buff(sparkle_ult_name, 2)
    # else:
    #   print(f"Applying {sparkle_ult_name} Sparkle")
    #   self.buffs.concat(self.ult_buff)

    for i in party:
      if i.buffs.check_buff(sparkle_ult_name):
        print(f"Refreshing {sparkle_ult_name} on {i.name}")
        i.buffs.refresh_buff(sparkle_ult_name, 2)
      else:
        print(f"Applying {sparkle_ult_name} on {i.name}")
        i.buffs.concat(self.ult_buff.df.loc[self.ult_buff.df["Holder Name"] == i.name]) ##todo: concat only relavant character's buff


  def update_stats(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    try:
      self.total_attack = self.base_attack * (1 + self.attack_percent) + self.flat_attack
    except TypeError:
      if verbose:
        print("Warning: Sparkle's update_stats failed due to blank stat values")
      else:
        pass