from characters.fu_xuan import Fu_Xuan
from characters.qingque import Qingque
from characters.silver_wolf import Silver_Wolf
from characters.sparkle import Sparkle
from utils.arena import Arena
import numpy as np
import random as rand

def QQ_Mono_Quantum(arena, qq, spk, sw, fx, action_df, prob_df, buffs_df,  cycles = 5, verbose = False):

    if spk.tech:
        arena.sp += 3
        spk.tech = False
    while arena.cycle <= cycles:
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
        if arena.sp >=7:
            arena.sp = 7
        #Determine the next character to act based on who has 0 action gauge
        if fx.action_gauge == 0:
        
        #Fu Xuan's actions
            if verbose:
                print("Fu Xuan takes a turn")
            if arena.sp > 0 and fx.skill_counter < 0 or spk.energy >= spk.max_energy:
                action_df.add_row(arena, fx, "Skill", -1)
                ##TODO: Add FX's 12% CR Buff:
                fx.skill(verbose = verbose)
            else:
                action_df.add_row(arena, fx, "Basic", 1)
                fx.basic(verbose = verbose)
            buffs_df.add_character_buffs(fx.buffs, arena)
            for chara in characters:
                chara.buffs.tick_down(holder = fx.name)
            fx.action_reset()

        elif sw.action_gauge == 0:
        
        #Silver Wolf's actions
            if verbose:
                print("Silver Wolf takes a turn")
            if arena.sp > 0 and sw.skill_counter == 0 or spk.energy >= spk.max_energy:
                action_df.add_row(arena, sw, "Skill", -1)
                sw.skill(verbose = verbose)
            else:
                action_df.add_row(arena, sw, "Basic", 1)
                sw.basic(verbose = verbose)
            buffs_df.add_character_buffs(sw.buffs, arena)
            for chara in characters:
                chara.buffs.tick_down(holder = sw.name)
            sw.action_reset()

        elif spk.action_gauge ==0:
        
        #Sparkle's actions
            print(spk.buffs.df)
            if verbose:
                print("Sparkle takes a turn:")
            if spk.energy >= spk.max_energy:
                action_df.add_row(arena, spk, "Ultimate", 4)
                spk.ult(verbose = verbose)
                spk.apply_ult_buff(characters)
            if arena.sp >= 7:
                arena.sp = 7
            if arena.sp > 0:
                action_df.add_row(arena, spk, "Skill", -1)
                spk.skill(verbose = verbose)
            else:
                action_df.add_row(arena, spk, "Basic", 1)
                spk.basic(verbose = verbose)
            buffs_df.add_character_buffs(spk.buffs, arena)
            for chara in characters:
                chara.buffs.tick_down(holder = spk.name)
            spk.action_reset()

        #Qingque's Actions
        elif qq.action_gauge == 0:
            if qq.tile_battle == True:
                arena.sp += 1
                qq.tile_battle = False
            passive_tiles = qq.tiles
            # qq.check_hh()
            roll = rand.random()
            if verbose:
                print(f"P to beat is {roll}")
            if spk.energy >= spk.max_energy:
                action_df.add_row(arena, spk, "Ultimate", 4)
                spk.ult(verbose = verbose)
                sparkle_ult = True
            else:
                sparkle_ult = False

            for i in range(1, arena.sp + 1):
                check = qq.f_success(sp = i)
                if verbose:
                    print(f"Did QQ win with {check}?")
                if roll < check:
                    sp_consumed = i
                    qq.hidden_hand = True
                    if verbose:
                        print("Success!")
                        print(f"Draws = {i}")
                    break
            else:
                if verbose:
                    print("Failure!")
                sp_consumed = int(arena.sp)
                if qq.eidolon == 6:
                    sp_consumed -=1
                if sp_consumed < 0:
                    sp_consumed = 0
                qq.draws = sp_consumed
                qq.hidden_hand = False
                action_df.add_row(arena, qq, "Basic", -sp_consumed)
            if qq.hidden_hand == True:
                #qq.check_hh(threshold = sp_consumed)
                if sp_consumed > 1:
                    qq.p_low = qq.f_success(sp_consumed -1)
                else:
                    qq.p_low = 0.000
                qq.p_high = qq.f_success(sp_consumed)
                qq.draws = sp_consumed
                if qq.eidolon >= 6:
                    sp_consumed -= 1
                action_df.add_row(arena, qq, "Enhanced Basic", -sp_consumed)
                qq.tiles = 0
            if arena.sp > 7 and sparkle_ult: #Undo Sparkle's Ult if too much SP
                action_df.df.drop(action_df.df.tail(2).index[0], inplace=True)
                spk.energy = 120
                arena.sp -=1
            elif sparkle_ult:
                spk.apply_ult_buff(characters)
           
            prob_df.add_row(arena, qq, passive_tiles, sp_consumed, qq.hidden_hand, roll)
            if verbose:
                print(f"SP Consumed = {sp_consumed}")
            arena.sp -= sp_consumed
            buffs_df.add_character_buffs(qq.buffs, arena)
            for chara in characters:
                chara.buffs.tick_down(holder = qq.name)
            if sparkle_ult:
                qq.buffs.refresh_buff("Cipher", 2)
            sparkle_ult = False
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
  party = [QQ, SW, FX]
  Spk = Sparkle(arena = arena, recipient = QQ, party = party, Spd = sparkle_speed, ER = 1.194, tech = True)
  return arena, QQ, Spk, SW, FX