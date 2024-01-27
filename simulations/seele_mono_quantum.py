def Seele_Mono_Quantum(enlvl = 95, quantum_weak = True, verbose = False):
  actions_df = pd.DataFrame(columns = ["Cycle", "Action_Gauge", "SP", "Character", "Energy", "Action", "Ultimate"])
  damage_df = pd.DataFrame(columns = ["Cycle", "Action Gauge", "Attack Percent", "Current Attack", "Damage Bonus Percent", "Crit Rate Percent", "Crit Dmg Percent", "Move", "Expected Damage", "Max Damage", "Ult Expected Damage", "Ult Max Damage"])

  arena, seele, spk, sw, fx = Initialize_Seele_Mono_Quantum()
  if spk.tech:
    arena.sp += 3
    spk.tech = False
  while arena.cycle < 5:
    characters = [seele, spk, sw, fx]
    try:
      del current_gauges
    except UnboundLocalError:
      pass
    current_gauges = []
    
    #Make a list of the current action gauges
    for chara in characters:
      current_gauges.append(chara.action_gauge)
    if verbose:
      print(f"Current AG: {arena.action_gauge}, current SP: {arena.sp}, current cycle: {arena.cycle}")
      print(f"Seele AG: {current_gauges[0]}, Spk AG: {current_gauges[1]}, SW AG: {current_gauges[2]}, FX AG: {current_gauges[3]}")
    
    #Find the lowest gauge
    lowest_gauge = min(current_gauges)
    
    #Cycle through all characters and advance them forward by the lowest gauge. Should lead to 1 character with AG of 0
    for chara in characters:
      chara.action_advance(lowest_gauge)
    arena.action_advance(lowest_gauge)
    sp_now = arena.sp
    #Determine the next character to act based on who has 0 action gauge
    if fx.action_gauge == 0:
      
      #Fu Xuan's actions
      ult = None
      if verbose:
        print("Fu Xuan takes a turn")
      if arena.sp > 0 and fx.skill_counter <= 0:
        ##TODO: Add FX's 12% CR Buff:
        fx.skill(verbose = verbose)
        action = "Skill"
      else:
        fx.basic(verbose = verbose)
        action = "Basic"

      Action_List_Update(arena, fx, action, ult, sp_now) 
      fx.update_buffs()
      fx.action_reset()

    elif sw.action_gauge == 0:
      
      #Silver Wolf's actions
      if verbose:
        print("Silver Wolf takes a turn")
      ult = None
      if arena.sp > 0 and sw.skill_counter <= 0:
        sw.skill(verbose = verbose)
        action = "Skill"
      else:
        sw.basic(verbose = verbose)
        action = "Basic"
      Action_List_Update(arena, sw, action, ult, sp_now) 
      sw.update_buffs()
      sw.action_reset()

    elif spk.action_gauge ==0:
      
      #Sparkle's actions
      ult = None
      if verbose:
        print("Sparkle takes a turn:")
      if arena.sp > 0:
        spk.skill(verbose = verbose)
        action = "Skill"
      else:
        spk.basic(verbose = verbose)
        action = "Basic"
      if spk.energy >= spk.max_energy:
        spk.ult(verbose = verbose)
        ult = True
      
      Action_List_Update(arena, spk, action, ult, sp_now) 
      spk.update_buffs()
      spk.action_reset()

    elif seele.action_gauge == 0:
      
      #Seele's actions
      ult = None
      if arena.sp > 0 and seele.turn in seele.skill_turns:
        seele.skill(verbose = verbose)
        action = "Skill"
      else:
        seele.basic(verbose = verbose)
        action = "basic"
      if seele.energy >= seele.max_energy:
        seele.ult(verbose = verbose)
        ult = True
      Action_List_Update(arena, seele, action, ult, sp_now)
      sp_now = arena.sp

      if seele.turn in seele.resurgence_turns:
        seele.enter_resurgence(verbose = verbose)
        if arena.sp > 0:
          seele.skill(verbose = verbose)
          action = "Skill"
        else:
          seele.basic(verbose = verbose)
          action = "Basic"
        if seele.energy >= seele.max_energy:
          seele.ult(verbose = verbose)
          ult = True
        Action_List_Update(arena, seele, action, ult, sp_now) 
        seele.exit_resurgence(verbose = verbose)
      seele.update_stats()
      seele.speed_buff_timer -=1
      seele.update_buffs(verbose = verbose)
      seele.action_reset(verbose = verbose)

    else:
      print(f"Action Gauge error!")
      print(f"Current AG: {arena.action_gauge}, current SP: {arena.sp}, current cycle: {arena.cycle}")
      print(f"QQ AG: {current_gauges[0]}, Spk AG: {current_gauges[1]}, SW AG: {current_gauges[2]}, FX AG: {current_gauges[3]}")

    del current_gauges


