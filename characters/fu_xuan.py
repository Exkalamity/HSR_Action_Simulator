from characters.base_character import Character

class Fu_Xuan(Character):
  def __init__(self, tech = False, **kwargs):
    super().__init__(**kwargs)
    self.name = "Fu Xuan"
    self.max_energy = 135
    if self.energy  == "MoC":
      self.energy = 0.5*self.max_energy
    self.skill_counter = 0
    if tech:
      self.skill_counter = 1

  def basic(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.skill_counter -= 1
    self.energy += 20*self.energy_regen
    if verbose:
      print("Fu Xuan uses basic! SP +1")

  def skill(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    arena = self.arena
    self.skill_counter = 2
    arena.sp -= 1
    if verbose:
      print("Fu Xuan uses skill! SP -1")
  def update_stats(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    try:
      self.total_attack = self.base_attack * (1 + self.attack_percent) + self.flat_attack
    except TypeError:
      if verbose:
        print("Warning: Fu Xuan's update_stats failed due to blank stat values")
      else:
        pass