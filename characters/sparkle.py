from characters.base_character import Character

class Sparkle(Character):
  def __init__(self, recipient, tech = False, broyna_lc = False, t1_skill = True, **kwargs):
    super().__init__(**kwargs)
    self.name = "Sparkle"
    self.max_energy = 110
    self.recipient  = recipient
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
      adv = recipient.action_gauge - 0.1
    recipient.action_gauge -= adv
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