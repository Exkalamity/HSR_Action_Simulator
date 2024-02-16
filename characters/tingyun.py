from characters.base_character import Character

class Tingyun(Character):
  def __init__(self, recipient, eidolon = 0, tech = False, **kwargs):
    super().__init__(**kwargs)
    self.name = "Tingyun"
    self.max_energy = 130
    self.recipient  = recipient
    self.tech = tech
    self.skill_counter = 0
    if eidolon >= 6:
      self.ult_energy = 60
    else:
      self.ult_energy = 50
    self.energy_regen = 1.194 + 0.05

    if self.energy == "MoC":
      self.energy = 0.5*self.max_energy
    if tech is not False:
      self.energy += tech*50

  def basic(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.energy += 28*self.energy_regen
    self.skill_counter -= 1
    if verbose:
      print("Tingyun uses basic! SP +1")

  def skill(self, recipient = None, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    if recipient is None:
      recipient = self.recipient
    self.energy += 38 *self.energy_regen
    self.skill_counter = 2
    arena.sp -= 1
    if verbose:
      print("Tingyun uses skill! SP -1")
  
  def ult(self, recipient = None, verbose = None):
    if verbose is None:
      verbose = self.verbose
    if recipient is None:
      recipient = self.recipient
    self.energy = 5*self.energy_regen
    recipient.energy += self.ult_energy
    if verbose:
      print("Tingyun uses Ult!")
      print(f"{recipient.name} gains {self.ult_energy} energy")

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