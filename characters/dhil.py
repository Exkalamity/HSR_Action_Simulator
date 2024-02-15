from characters.base_character import Character

class DHIL(Character):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = "Dan Heng IL"
    self.skill_charges = 0
    self.max_energy = 140
    self.sp_cost = 0
    if self.energy  == "MoC":
      self.energy = 0.5*self.max_energy
    self.basic_level = 0

  def skill(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    if self.skill_charges + arena.sp >=3:
      self.basic_level = 3
    else:
      self.basic_level = self.skill_charges + arena.sp
    self.sp_cost = self.basic_level - self.skill_charges
    if verbose:
      print(f"DHIL enhances to level {self.basic_level}")

  def enhanced_basic(self, verbose = None):
    arena = self.arena
    if verbose == None:
      verbose = self.verbose
    if self.basic_level == 0:
      arena.sp += 1
      self.energy += 20*self.energy_regen
    else:
      arena.sp -= self.sp_cost
      self.skill_charges = 0
      self.energy += self.energy_regen*(30 + 5*(self.basic_level - 1))
    
    if verbose:
      print(f"DHIL used basic level {self.basic_level}")

  def ult(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    self.energy = 5
    self.skill_charges += 2
    if self.skill_charges >3:
      self.skill_charges = 3
    if verbose:
      print("DHIL uses Ult! +2 skill charges")

