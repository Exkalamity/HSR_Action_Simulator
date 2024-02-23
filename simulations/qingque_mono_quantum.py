from characters.fu_xuan import Fu_Xuan
from characters.qingque import Qingque
from characters.silver_wolf import Silver_Wolf
from characters.sparkle import Sparkle
from utils.arena import Arena
import numpy as np

def QQ_Mono_Quantum(arena, qq, spk, sw, fx, action_df, prob_df, cycles = 10, verbose = False):

    if spk.tech:
        arena.sp += 3
        spk.tech = False
    while arena.cycle < cycles:
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
        
        #Qingque's Passive Tile Draw
        qq.tiles += 1 
        if arena.sp >7:
            arena.sp = 7
        #Determine the next character to act based on who has 0 action gauge
        if fx.action_gauge == 0:
        
        #Fu Xuan's actions
            if verbose:
                print("Fu Xuan takes a turn")
            if arena.sp > 0 and fx.skill_counter < 0:
                action_df.add_row(arena, fx, "Skill", -1)
                ##TODO: Add FX's 12% CR Buff:
                fx.skill(verbose = verbose)
  
            else:
                action_df.add_row(arena, fx, "Basic", 1)
                fx.basic(verbose = verbose)

            fx.update_buffs()
            fx.action_reset()

        elif sw.action_gauge == 0:
        
        #Silver Wolf's actions
            if verbose:
                print("Silver Wolf takes a turn")
            if arena.sp > 0 and sw.skill_counter <= 0:
                action_df.add_row(arena, sw, "Skill", -1)
                sw.skill(verbose = verbose)

            else:
                action_df.add_row(arena, sw, "Basic", 1)
                sw.basic(verbose = verbose)

            sw.update_buffs()
            sw.action_reset()

        elif spk.action_gauge ==0:
        
        #Sparkle's actions
            if verbose:
                print("Sparkle takes a turn:")
            if arena.sp > 0:
                action_df.add_row(arena, spk, "Skill", -1)
                spk.skill(verbose = verbose)
            else:
                action_df.add_row(arena, spk, "Basic", 1)
                spk.basic(verbose = verbose)
            if spk.energy >= spk.max_energy:
                action_df.add_row(arena, spk, "Ultimate", 4)
                spk.ult(verbose = verbose)
                
            
            spk.update_buffs()
            spk.action_reset()

        elif qq.action_gauge == 0:
            if qq.tile_battle == True:
                arena.sp += 1
                qq.tile_battle = False
            passive_tiles = qq.tiles
            qq.check_hh(threshold=0.7)

            if qq.hidden_hand == True:
                sp_consumed = int(np.round(qq.likely_multiplier))
                if qq.eidolon >= 6:
                    sp_consumed -= 1
                action_df.add_row(arena, qq, "Enhanced Basic", sp_consumed)
                qq.tiles = 0
            else: 
                sp_consumed = int(arena.sp - 1)
                action_df.add_row(arena, qq, "Enhanced Basic", sp_consumed)
            prob_df.add_row(arena, qq, passive_tiles)
            arena.sp -= sp_consumed
            #qq.update_buffs(verbose)
            qq.action_reset()
        
        else:
            print(f"Action Gauge error!")
            print(f"Current AG: {arena.action_gauge}, current SP: {arena.sp}, current cycle: {arena.cycle}")
            print(f"QQ AG: {current_gauges[0]}, Spk AG: {current_gauges[1]}, SW AG: {current_gauges[2]}, FX AG: {current_gauges[3]}")

        del current_gauges




def Initialize_QQ_Mono_Quantum(qingque_speed = None, silver_wolf_speed = None, fu_xuan_speed = None, sparkle_speed = None):
  arena = Arena()
  QQ = Qingque(arena = arena, Spd = qingque_speed)
  SW = Silver_Wolf(arena = arena, Spd = silver_wolf_speed)
  FX = Fu_Xuan(arena = arena, tech = True, Spd = fu_xuan_speed, ER = 1.194)
  Spk = Sparkle(arena = arena, recipient = QQ, Spd = sparkle_speed, ER = 1.194, tech = True)
  return arena, QQ, Spk, SW, FX