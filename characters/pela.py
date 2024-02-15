from characters.base_character import Character

class Pela(Character):
  def __init__(self, tech = False, **kwargs):
    super().__init__(**kwargs)
    self.name = "Pela"
    self.max_energy = 110
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
      print("Pela uses basic! SP +1")
  def update_stats(self):
    pass