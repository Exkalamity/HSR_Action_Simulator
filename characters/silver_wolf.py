from characters.base_character import Character
import numpy as np

class Silver_Wolf(Character):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = "Silver Wolf"
    self.max_energy = 110
    if  self.energy == "MoC":
      self.energy = 0.5*self.max_energy
    self.skill_counter = -1
  
  def basic(self, arena = None, verbose = None):
    if arena is None:
      arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.skill_counter -= 1
    if verbose:
      print("Silver Wolf uses basic! SP +1")
  
  def skill(self, arena = None, verbose = None):
    if arena is None:
      arena = self.arena
    if verbose is None:
      verbose = self.verbose
    self.skill_counter = 2
    arena.sp -= 1
    if verbose:
      print("Silver Wolf uses skill! SP -1")
  def update_stats(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    try:
      self.total_attack = self.base_attack * (1 + self.attack_percent) + self.flat_attack
    except TypeError:
      if verbose:
        print("Warning: Silver Wolf's update_stats failed due to blank stat values")
      else:
        pass