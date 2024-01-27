class Arena():
  def __init__(self, AG = 0, SP = 3):
    self.action_gauge = AG
    self.sp = SP
    self.cycle = 0
  def action_advance(self, AA):
    self.action_gauge += AA
    self.cycle = ((self.action_gauge - 150)// 100)+1
    # ADDED HEREgitgit 

