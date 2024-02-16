from characters.base_character import Character

class Luocha(Character):
  def __init__(self, multiplication = True, **kwargs):
    super().__init__(**kwargs)
    self.name = "Luocha"
    self.max_energy = 110
    self.multuplcation = multiplication
    self.og_action_value = self.action_value
    if self.energy  == "MoC":
      self.energy = 0.5*self.max_energy

  def basic(self, multiplication = None, verbose = None):
    arena = self.arena
    if multiplication is None:
      multiplication = self.multuplcation
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.energy += 20*self.energy_regen
    if multiplication:
        self.action_value = self.og_action_value*0.8
        multiplication = False
    if verbose:
      print("Luocha uses basic! SP +1")
  def update_stats(self):
    pass