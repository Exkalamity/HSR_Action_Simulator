def QQ_Mono_Quantum(enlvl = 95, quantum_weak = True, verbose = False):
  actions_df = pd.DataFrame(columns = ["Cycle", "Action_Gauge", "SP", "Character", "Energy", "Action", "Ultimate"])
  damage_df = pd.DataFrame(columns = ["Cycle", "Action Gauge", "Attack Percent", "Current Attack", "Damage Bonus Percent", "Crit Rate Percent", "Crit Dmg Percent", "Move", "Expected Damage", "Max Damage", "Ult Expected Damage", "Ult Max Damage"])

  arena, qq, spk, sw, fx = Initialize_QQ_Mono_Quantum()
  if spk.tech:
    arena.sp += 3
    spk.tech = False
  while arena.cycle < 5:
    characters = [qq, spk, sw, fx]
    current_gauges = []
    
    #Make a list of the current action gauges
    for chara in characters:
      current_gauges.append(chara.action_gauge)
    if verbose:
      print(f"Current AG: {arena.action_gauge}, current SP: {arena.sp}, current cycle: {arena.cycle}")
      print(f"QQ AG: {current_gauges[0]}, Spk AG: {current_gauges[1]}, SW AG: {current_gauges[2]}, FX AG: {current_gauges[3]}")
    
    #Find the lowest gauge
    lowest_gauge = min(current_gauges)
    
    #Cycle through all characters and advance them forward by the lowest gauge. Should lead to 1 character with AG of 0
    for chara in characters:
      chara.action_advance(lowest_gauge)
    arena.action_advance(lowest_gauge)
    sp_now = arena.sp
    qq.tiles += 1
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

    elif qq.action_gauge == 0:
      
      #QQ's Actions
      ult = None
      qq.ult_expected_damage = 0
      qq.ult_max_damage = 0
      if qq.tile_battle == True:
        draws = arena.sp + 1
      else:
        draws = arena.sp
      qq.skill(verbose)
      if qq.draws <= arena.sp:
        qq.hidden_hand_success(verbose)
        draws = qq.draws
        if qq.energy >= qq.max_energy and qq.behavior == "Aggressive":
          qq.ult(verbose)
          ult = "Unga Bunga"
        qq.enhanced_basic(verbose)
        print(qq.expected_damage, qq.maximum_damage, qq.ult_expected_damage, qq.ult_max_damage)
        Damage_List_Update(qq.expected_damage, qq.maximum_damage, qq.ult_expected_damage, qq.ult_max_damage, "Enhanced Basic + Unga Bunga Ult", arena, qq)
        qq_attack = "Enhanced Basic"
      else:
        qq.hidden_hand_failure(verbose)
        if qq.energy >= qq.max_energy and qq.behavior == "Emergency":
          ult = "Emergency"
          qq.ult(verbose)
          atk_bonus = 0.798
          qq.attack_percent += atk_bonus
          qq.buffs.append({"attribute name":"attack_percent", "recipient":qq, "tickdown":qq, "value":atk_bonus, "duration":1})
          qq.enhanced_basic(verbose)
          Damage_List_Update(qq.expected_damage, qq.maximum_damage, qq.ult_expected_damage, qq.ult_max_damage, "Enhanced Basic + Emergency Ult", arena, qq)
          qq_attack = "Enhanced Basic"
        else:
          qq.basic(verbose)
          qq_attack = "Basic"
          Damage_List_Update(qq.expected_damage, qq.maximum_damage, qq.ult_expected_damage, qq.ult_max_damage, "Sad Basic", arena, qq)
      Action_List_Update(arena, qq, action, ult, sp_now) 
      qq.update_buffs(verbose)
      qq.action_reset()
    
    else:
      print(f"Action Gauge error!")
      print(f"Current AG: {arena.action_gauge}, current SP: {arena.sp}, current cycle: {arena.cycle}")
      print(f"QQ AG: {current_gauges[0]}, Spk AG: {current_gauges[1]}, SW AG: {current_gauges[2]}, FX AG: {current_gauges[3]}")

    del current_gauges


