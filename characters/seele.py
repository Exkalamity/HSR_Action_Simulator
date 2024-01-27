from characters.base_character import Character

class Seele(Character):
  def __init__(self, skill_turns = list(range(20)), resurgence_turns = [0,1,2,3],  tech = False, **kwargs):
    super().__init__(**kwargs)
    self.name = "Seele"
    self.max_energy = 120
    if self.energy  == "MoC":
      self.energy = 0.5*self.max_energy
    self.resurgence_procs = 0
    self.resurgence_state = False
    self.speed_buff = False
    self.speed_buff_timer = 2
    self.turn = 0
    self.skill_turns = skill_turns
    self.resurgence_turns = resurgence_turns
    self.base_speed = 113 

  def basic(self, verbose = None):
    arena = self.arena
    if verbose is None:
      verbose = self.verbose
    arena.sp += 1
    self.energy += 20*self.energy_regen
    if verbose:
      print("Seele uses basic! SP +1")

  def skill(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    arena = self.arena
    arena.sp -= 1
    self.energy += 30 * self.energy_regen
    
    self.speed_buff_timer = 2
    
    if self.speed_buff == False: #Check if the skill speed increase has been already applied or not
      self.speed_buff = True
      self.speed = self.speed +  self.base_speed * 0.25
      self.buffs_list.append({"attribute name":"speed", "recipient":self, "tickdown":self, "value":self.base_speed * 0.25, "duration":2})
      if verbose:
        print(f"Seele's speed increased by {self.base_speed * 0.25}")
    else:
      for buff in self.buffs_list:
        if buff.get("attribute name") == "speed" and buff.get("recipient") == self and buff.get("tickdown") == self:
          buff["duration"] = 2
      if verbose:
        print("Seele's speed buff refreshed!")
      
    if verbose:
      print("Seele uses skill! SP -1")
      print(f"Seele's current speed is {self.speed}")
    #at end of turn, make sure to tick down self.speed_buff
  
  def ult(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    if verbose:
      print("Seele uses Ult!")
    self.energy = 5

  def enter_resurgence(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    if verbose:
      print("Seele enters Resurgence!")
    self.resurgence_state = True
    self.resurgence_procs += 1

  def exit_resurgence(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    if verbose:
      print("Seele exits Resurgence.")
    self.resurgence_state = False

  def update_stats(self, verbose = None):
    if verbose is None:
      verbose = self.verbose
    self.speed_buff_timer -= 1
    if self.speed_buff_timer == 0:
      self.speed_buff = False
    self.action_value = 10000/self.speed
    if verbose:
      print(f"Seele's action gauge is now {self.action_value}")
    try:
      self.total_attack = self.base_attack * (1 + self.attack_percent) + self.flat_attack
    except TypeError:
      if verbose:
        print("Warning: Seele's update_stats failed due to blank stat values")
      else:
        pass