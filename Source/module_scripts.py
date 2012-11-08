# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
import types


####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

##delay script system begin
def set_num_of_params_in_each_script():
  contents = []
  for i_script in xrange(len(scripts)):
    statement_block = scripts[i_script][1]
    param_num = 0
    for statement in statement_block:
      if ((type(statement) != types.ListType) and (type(statement) != types.TupleType)):
        continue
      operation = statement[0]
      if operation == store_script_param_1 and param_num < 1:
        param_num = 1
      elif operation == store_script_param_2 and param_num < 2:
        param_num = 2
      elif operation == store_script_param and param_num < statement[2]:
        param_num = statement[2]
    contents.append((item_set_slot,"itm_param_num_of_script",i_script,param_num))
  return contents

def generate_call_script_scripts(num):
  result = []
  for i in xrange(num):
    statement_block = []
    call_script_statement = [call_script,":script_id"]
    statement_block.append((store_script_param_1,":script_id"))
    for j in xrange(i):
      statement_block.append((assign,":param_"+str(j+1),0))
      statement_block.append((item_get_slot,":param_"+str(j+1),"itm_param_list",j))
      call_script_statement.append(":param_"+str(j+1))
    statement_block.append(call_script_statement[:])
    result.append(("call_script_"+str(i),statement_block[:]))
  return result
##delay script system end
scripts = [
  #script_game_get_use_string
  # This script is called from the game engine for getting using information text
  # INPUT: used_scene_prop_id  
  # OUTPUT: s0
  ("game_get_use_string",
   [
     (store_script_param, ":instance_id", 1),

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
     
     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),   

     (scene_prop_get_slot, ":item_situation", ":instance_id", scene_prop_open_or_close_slot),
   
     (try_begin), #opening/closing portcullis
       (eq, ":effected_object", "spr_portcullis"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_gate"),
       (else_try), 
         (str_store_string, s0, "str_close_gate"),
       (try_end),
     (else_try), #opening/closing door
       (this_or_next|eq, ":effected_object", "spr_door_destructible"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
       (this_or_next|eq, ":effected_object", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":effected_object", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":effected_object", "spr_viking_keep_destroy_sally_door_right"),
       (eq, ":effected_object", "spr_castle_f_door_a"),

       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_open_door"),
       (else_try),
         (str_store_string, s0, "str_close_door"),
       (try_end),
     (else_try), #raising/dropping ladder
       (try_begin),
         (eq, ":item_situation", 0),
         (str_store_string, s0, "str_raise_ladder"),
       (else_try),
         (str_store_string, s0, "str_drop_ladder"),
       (try_end),
     (try_end),
   ]),

  #script_game_set_multiplayer_mission_end
  # This script is called from the game engine when a multiplayer map is ended in clients (not in server).
  # INPUT:
  # none
  # OUTPUT:
  # none
  ("game_set_multiplayer_mission_end",
    [
      (assign, "$g_multiplayer_mission_end_screen", 1),
  ]),

  #script_add_kill_death_counts
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("add_kill_death_counts",
   [
      (store_script_param, ":killer_agent_no", 1),
      (store_script_param, ":dead_agent_no", 2),
      
#      (try_begin),
#        (ge, ":killer_agent_no", 0),
#        (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
#      (else_try),
#        (assign, ":killer_agent_team", -1),
#      (try_end),

      (try_begin),
        (ge, ":dead_agent_no", 0),
        (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
      (else_try),
        (assign, ":dead_agent_team", -1),
      (try_end),

        (try_begin), 
          (ge, ":dead_agent_no", 0),
          (agent_is_human, ":dead_agent_no"),
          (try_begin),
            (agent_is_non_player, ":dead_agent_no"), #if dead agent is bot then increase bot kill counts of dead agent's team by one.
            (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
            (team_get_bot_death_count, ":dead_agent_team_bot_death_count", ":dead_agent_team"),
            (val_add, ":dead_agent_team_bot_death_count", 1),
            (team_set_bot_death_count, ":dead_agent_team", ":dead_agent_team_bot_death_count"),
          (else_try), #if dead agent is not bot then increase death counts of dead agent's player by one.
            (agent_get_player_id, ":dead_agent_player", ":dead_agent_no"),
            (player_is_active, ":dead_agent_player"),
            (player_get_death_count, ":dead_agent_player_death_count", ":dead_agent_player"),
            (val_add, ":dead_agent_player_death_count", 1),
            (player_set_death_count, ":dead_agent_player", ":dead_agent_player_death_count"),
          (try_end),

          (try_begin),
            (assign, ":continue", 0),
      
            (try_begin),
              (this_or_next|lt, ":killer_agent_no", 0), #if he killed himself (1a(team change) or 1b(self kill)) then decrease kill counts of killer player by one.
              (eq, ":killer_agent_no", ":dead_agent_no"),
              (assign, ":continue", 1),
            (try_end),

            (eq, ":continue", 1),
                    
            (try_begin),
              (ge, ":killer_agent_no", 0),
              (assign, ":responsible_agent", ":killer_agent_no"),                
            (else_try),
              (assign, ":responsible_agent", ":dead_agent_no"),
            (try_end),

            (try_begin),
              (ge, ":responsible_agent", 0),
              (neg|agent_is_non_player, ":responsible_agent"),
              (agent_get_player_id, ":responsible_player", ":responsible_agent"),
              (ge, ":responsible_player", 0),
              (player_get_kill_count, ":dead_agent_player_kill_count", ":responsible_player"),
              (val_add, ":dead_agent_player_kill_count", -1),
              (player_set_kill_count, ":responsible_player", ":dead_agent_player_kill_count"),
            (try_end),
          (try_end),               
        (try_end),
      (try_end),
    ]),

  #script_warn_player_about_auto_team_balance
  # INPUT: none
  # OUTPUT: none
  ("warn_player_about_auto_team_balance",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
     (start_presentation, "prsnt_multiplayer_message_2"),
     ]),

  #script_check_team_balance
  # INPUT: none
  # OUTPUT: none
  ("check_team_balance",
   [
     (try_begin),
       (multiplayer_is_server),
  
       (assign, ":number_of_players_at_team_1", 0),
       (assign, ":number_of_players_at_team_2", 0),
       (get_max_players, ":num_players"),
       (try_for_range, ":cur_player", 0, ":num_players"),
         (player_is_active, ":cur_player"),
         (player_get_team_no, ":player_team", ":cur_player"),
         (try_begin),
           (eq, ":player_team", 0),
           (val_add, ":number_of_players_at_team_1", 1),
         (else_try),
           (eq, ":player_team", 1),
           (val_add, ":number_of_players_at_team_2", 1),
         (try_end),         
       (try_end),
 
       (store_sub, ":difference_of_number_of_players", ":number_of_players_at_team_1", ":number_of_players_at_team_2"),
       (assign, ":number_of_players_will_be_moved", 0),
       (try_begin),
         (try_begin),
           (store_mul, ":checked_value", "$g_multiplayer_auto_team_balance_limit", -1),
           (le, ":difference_of_number_of_players", ":checked_value"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", -2),
           (assign, ":team_with_more_players", 1),
           (assign, ":team_with_less_players", 0),
         (else_try),
           (ge, ":difference_of_number_of_players", "$g_multiplayer_auto_team_balance_limit"),
           (store_div, ":number_of_players_will_be_moved", ":difference_of_number_of_players", 2),
           (assign, ":team_with_more_players", 0),
           (assign, ":team_with_less_players", 1),
         (try_end),          
       (try_end),         
       #team balance checks are done
       (try_begin),
         (gt, ":number_of_players_will_be_moved", 0),
         (try_begin),
           (eq, "$g_team_balance_next_round", 1), #if warning is given
           
           #auto team balance starts
           (try_for_range, ":unused", 0, ":number_of_players_will_be_moved"), 
             (assign, ":max_player_join_time", 0),
             (assign, ":latest_joined_player_no", -1),
             (get_max_players, ":num_players"),                               
             (try_for_range, ":player_no", 0, ":num_players"),
               (player_is_active, ":player_no"),
               (player_get_team_no, ":player_team", ":player_no"),
               (eq, ":player_team", ":team_with_more_players"),
               (player_get_slot, ":player_join_time", ":player_no", slot_player_join_time),
               (try_begin),
                 (gt, ":player_join_time", ":max_player_join_time"),
                 (assign, ":max_player_join_time", ":player_join_time"),
                 (assign, ":latest_joined_player_no", ":player_no"),
               (try_end),
             (try_end),
             (try_begin),
               (ge, ":latest_joined_player_no", 0),
               (try_begin),
                 #if player is living add +1 to his kill count because he will get -1 because of team change while living.
                 (player_get_agent_id, ":latest_joined_agent_id", ":latest_joined_player_no"), 
                 (ge, ":latest_joined_agent_id", 0),
                 (agent_is_alive, ":latest_joined_agent_id"),

                 (player_get_kill_count, ":player_kill_count", ":latest_joined_player_no"), #adding 1 to his kill count, because he will lose 1 undeserved kill count for dying during team change
                 (val_add, ":player_kill_count", 1),
                 (player_set_kill_count, ":latest_joined_player_no", ":player_kill_count"),

                 (player_get_death_count, ":player_death_count", ":latest_joined_player_no"), #subtracting 1 to his death count, because he will gain 1 undeserved death count for dying during team change
                 (val_sub, ":player_death_count", 1),
                 (player_set_death_count, ":latest_joined_player_no", ":player_death_count"),

                 (player_get_score, ":player_score", ":latest_joined_player_no"), #adding 1 to his score count, because he will lose 1 undeserved score for dying during team change
                 (val_add, ":player_score", 1),
                 (player_set_score, ":latest_joined_player_no", ":player_score"),

                 (try_for_range, ":player_no", 1, ":num_players"), #0 is server so starting from 1
                   (player_is_active, ":player_no"),
                   (multiplayer_send_4_int_to_player, ":player_no", multiplayer_event_set_player_score_kill_death, ":latest_joined_player_no", ":player_score", ":player_kill_count", ":player_death_count"),
                 (try_end),

                 (player_get_value_of_original_items, ":old_items_value", ":latest_joined_player_no"),
                 (player_get_gold, ":player_gold", ":latest_joined_player_no"),
                 (val_add, ":player_gold", ":old_items_value"),
                 (player_set_gold, ":latest_joined_player_no", ":player_gold", multi_max_gold_that_can_be_stored),
               (end_try),

               (player_set_troop_id, ":latest_joined_player_no", -1),
               (player_set_team_no, ":latest_joined_player_no", ":team_with_less_players"),
               (multiplayer_send_message_to_player, ":latest_joined_player_no", multiplayer_event_force_start_team_selection),
             (try_end),
           (try_end),
     
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_done, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------     
           (get_max_players, ":num_players"),                               
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_done), 
           (try_end),
           (assign, "$g_team_balance_next_round", 0),
           #auto team balance done
         (else_try),
           #tutorial message (next round there will be auto team balance)
           (assign, "$g_team_balance_next_round", 1),
     
           #for only server itself-----------------------------------------------------------------------------------------------
           (call_script, "script_show_multiplayer_message", multiplayer_message_type_auto_team_balance_next, 0), #0 is useless here
           #for only server itself-----------------------------------------------------------------------------------------------     
           (get_max_players, ":num_players"),                               
           (try_for_range, ":player_no", 1, ":num_players"),
             (player_is_active, ":player_no"),
             (multiplayer_send_int_to_player, ":player_no", multiplayer_event_show_multiplayer_message, multiplayer_message_type_auto_team_balance_next), 
           (try_end),
         (try_end),
       (else_try),
         (assign, "$g_team_balance_next_round", 0),
       (try_end),
     (try_end),
   ]),


  #script_money_management_after_agent_death
  # INPUT: arg1 = killer_agent_no, arg2 = dead_agent_no
  # OUTPUT: none
  ("money_management_after_agent_death",
   [
     (store_script_param, ":killer_agent_no", 1),
     (store_script_param, ":dead_agent_no", 2),

#     (assign, ":dead_agent_player_id", -1),
#
#     (try_begin),
#       (multiplayer_is_server),
#       (ge, ":killer_agent_no", 0),
#       (ge, ":dead_agent_no", 0),
#       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
#       (agent_is_human, ":killer_agent_no"), #if killer agent is not horse
#       (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
#       (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
#     
#       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch),
#       (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel),
#       (neq, ":killer_agent_team", ":dead_agent_team"), #if these agents are enemies
#
#       (neq, ":dead_agent_no", ":killer_agent_no"), #if agents are different, do not remove it is needed because in deathmatch mod, self killing passes here because of this or next.
#     
#       (try_begin),
#         (neg|agent_is_non_player, ":dead_agent_no"), 
#         (agent_get_player_id, ":dead_player_no", ":dead_agent_no"),
#         (player_get_slot, ":dead_agent_equipment_value", ":dead_player_no", slot_player_total_equipment_value),             
#       (else_try),
#         (assign, ":dead_agent_equipment_value", 0),
#       (try_end),
#
#       (assign, ":dead_agent_team_human_players_count", 0),
#       (get_max_players, ":num_players"),
#       (try_for_range, ":player_no", 0, ":num_players"),
#         (player_is_active, ":player_no"),
#         (player_get_team_no, ":player_team", ":player_no"),
#         (eq, ":player_team", ":dead_agent_team"),
#         (val_add, ":dead_agent_team_human_players_count", 1),
#       (try_end),
#         
#       (try_for_range, ":player_no", 0, ":num_players"),
#         (player_is_active, ":player_no"),
#          
#         (try_begin), 
#           (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#           (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#           (assign, ":one_spawn_per_round_game_type", 1),            
#         (else_try),
#           (assign, ":one_spawn_per_round_game_type", 0),
#         (try_end),
#         
#         (this_or_next|eq, ":one_spawn_per_round_game_type", 0),
#         (this_or_next|player_slot_eq, ":player_no", slot_player_spawned_this_round, 0),
#         (player_slot_eq, ":player_no", slot_player_spawned_this_round, 1),
#         
#         (player_get_agent_id, ":agent_no", ":player_no"),
#         (try_begin),
#           (eq, ":agent_no", ":dead_agent_no"), #if this agent is dead agent then get share from total loot. (20% of total equipment value)                 
#           (player_get_gold, ":player_gold", ":player_no"),
#
#           (assign, ":dead_agent_player_id", ":player_no"),
#          
#           #dead agent loot share (32%-48%-64%, norm : 48%)
#           (store_mul, ":share_of_dead_agent", ":dead_agent_equipment_value", multi_dead_agent_loot_percentage_share),
#           (val_div, ":share_of_dead_agent", 100),
#           (val_mul, ":share_of_dead_agent", "$g_multiplayer_battle_earnings_multiplier"),
#           (val_div, ":share_of_dead_agent", 100),
#           (try_begin),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
#             (val_mul, ":share_of_dead_agent", 4),
#             (val_div, ":share_of_dead_agent", 3),
#             (val_add, ":player_gold", ":share_of_dead_agent"), 
#           (else_try),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
#             (val_mul, ":share_of_dead_agent", 2),
#             (val_div, ":share_of_dead_agent", 3),
#             (val_add, ":player_gold", ":share_of_dead_agent"),
#           (else_try),
#             (val_add, ":player_gold", ":share_of_dead_agent"), #(3/3x) share if current mod is siege
#           (try_end),
#           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
#         (else_try),
#           (eq, ":agent_no", ":killer_agent_no"), #if this agent is killer agent then get share from total loot. (10% of total equipment value)
#           (player_get_gold, ":player_gold", ":player_no"),           
#
#           #killer agent standart money (100-150-200, norm : 150)
#           (assign, ":killer_agent_standard_money_addition", multi_killer_agent_standard_money_add),
#           (val_mul, ":killer_agent_standard_money_addition", "$g_multiplayer_battle_earnings_multiplier"),
#           (val_div, ":killer_agent_standard_money_addition", 100),
#           (try_begin),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
#             (val_mul, ":killer_agent_standard_money_addition", 4),
#             (val_div, ":killer_agent_standard_money_addition", 3),
#             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), 
#           (else_try),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
#             (val_mul, ":killer_agent_standard_money_addition", 2),
#             (val_div, ":killer_agent_standard_money_addition", 3),
#             (val_add, ":player_gold", ":killer_agent_standard_money_addition"),
#           (else_try),
#             (val_add, ":player_gold", ":killer_agent_standard_money_addition"), #(3/3x) share if current mod is siege
#           (try_end),
#
#           #killer agent loot share (8%-12%-16%, norm : 12%)
#           (store_mul, ":share_of_killer_agent", ":dead_agent_equipment_value", multi_killer_agent_loot_percentage_share),
#           (val_div, ":share_of_killer_agent", 100),
#           (val_mul, ":share_of_killer_agent", "$g_multiplayer_battle_earnings_multiplier"),
#           (val_div, ":share_of_killer_agent", 100),
#           (try_begin),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_deathmatch), #(4/3x) share if current mod is deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_duel), #(4/3x) share if current mod is duel
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_team_deathmatch), #(4/3x) share if current mod is team_deathmatch
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_capture_the_flag), #(4/3x) share if current mod is capture the flag
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #(4/3x) share if current mod is headquarters
#             (val_mul, ":share_of_killer_agent", 4),
#             (val_div, ":share_of_killer_agent", 3),
#             (val_add, ":player_gold", ":share_of_killer_agent"), 
#           (else_try),
#             (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #(2/3x) share if current mod is battle 
#             (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #(2/3x) share if current mod is fight and destroy
#             (val_mul, ":share_of_killer_agent", 2),
#             (val_div, ":share_of_killer_agent", 3),
#             (val_add, ":player_gold", ":share_of_killer_agent"),
#           (else_try),
#             (val_add, ":player_gold", ":share_of_killer_agent"), #(3/3x) share if current mod is siege
#           (try_end),
#           (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
#         (try_end),
#       (try_end),
#     (try_end),
#
#     #(below lines added new at 25.11.09 after Armagan decided new money system)
#     (try_begin),
#       (multiplayer_is_server),
#       (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#       (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#
#       (ge, ":dead_agent_no", 0),
#       (agent_is_human, ":dead_agent_no"), #if dead agent is not horse
#       (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
#       (ge, ":dead_agent_player_id", 0),
#     
#       (player_get_gold, ":player_gold", ":dead_agent_player_id"),
#       (try_begin),
#         (store_mul, ":minimum_gold", "$g_multiplayer_initial_gold_multiplier", 10),
#         (lt, ":player_gold", ":minimum_gold"),
#         (assign, ":player_gold", ":minimum_gold"),
#       (try_end),
#       (player_set_gold, ":dead_agent_player_id", ":player_gold"),
#     (try_end),
#     #new money system addition end          
     ]),

  #script_initialize_all_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_all_scene_prop_slots",
   [
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_e_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_sally_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_earth_sally_gate_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_left"),
     (call_script, "script_initialize_scene_prop_slots", "spr_viking_keep_destroy_sally_door_right"),
     (call_script, "script_initialize_scene_prop_slots", "spr_castle_f_door_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_a"),
     (call_script, "script_initialize_scene_prop_slots", "spr_belfry_b"),
     (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),
    ]),

  #script_initialize_scene_prop_slots
  # INPUT: arg1 = scene_prop_no
  # OUTPUT: none
  ("initialize_scene_prop_slots",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", ":scene_prop_no"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", ":scene_prop_no", ":cur_instance"),
       (try_for_range, ":cur_slot", 0, scene_prop_slots_end),
         (scene_prop_set_slot, ":cur_instance_id", ":cur_slot", 0),
       (try_end),
     (try_end),
     ]),
           

  #script_use_item
  # INPUT: arg1 = agent_id, arg2 = instance_id
  # OUTPUT: none
  ("use_item",
   [
     (store_script_param, ":instance_id", 1),
     (store_script_param, ":user_id", 2),

     (try_begin),
       (game_in_multiplayer_mode),
       (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
       (eq, ":scene_prop_id", "spr_winch_b"),
                      
       (multiplayer_get_my_player, ":my_player_no"),

       (this_or_next|gt, ":my_player_no", 0),
       (neg|multiplayer_is_dedicated_server),

       (ge, ":my_player_no", 0),
       (player_get_agent_id, ":my_agent_id", ":my_player_no"),
       (ge, ":my_agent_id", 0),
       (agent_is_active, ":my_agent_id"),
       (agent_get_team, ":my_team_no", ":my_agent_id"),
       (eq, ":my_team_no", 0),
                             
       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (ge, ":user_id", 0),
       (agent_is_active, ":user_id"),
       (agent_get_player_id, ":user_player", ":user_id"),
       (str_store_player_username, s7, ":user_player"),
            
       (try_begin),
         (eq, ":opened_or_closed", 0),
         (display_message, "@{s7} opened the gate"),
       (else_try),  
         (display_message, "@{s7} closed the gate"),
       (try_end),
     (try_end),  

     (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),
     
     (try_begin),
       (this_or_next|eq, ":scene_prop_id", "spr_winch_b"),
       (eq, ":scene_prop_id", "spr_winch"),
       (assign, ":effected_object", "spr_portcullis"),
     (else_try),
       (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
       (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),
       (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
       (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
       (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
       (assign, ":effected_object", ":scene_prop_id"),
     (try_end),

     (assign, ":smallest_dist", -1),
     (prop_instance_get_position, pos0, ":instance_id"),
     (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
       (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions, ":dist", pos0, pos1),
       (this_or_next|eq, ":smallest_dist", -1),
       (lt, ":dist", ":smallest_dist"),
       (assign, ":smallest_dist", ":dist"),
       (assign, ":effected_object_instance_id", ":cur_instance_id"),
     (try_end),

     (try_begin),
       (ge, ":instance_id", 0),
       (ge, ":smallest_dist", 0),

       (try_begin),     
         (eq, ":effected_object", "spr_portcullis"),
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0), #open gate
     
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, 375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, 72000),
           (try_end),
         (else_try), #close gate     
           (scene_prop_enable_after_time, ":instance_id", 400), #4 seconds
           (try_begin),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos0, ":effected_object_instance_id"),
             (position_move_z, pos0, -375),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 400),
           (try_end),
           (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 0),

           (try_begin),
             (eq, ":scene_prop_id", "spr_winch_b"),
             (this_or_next|multiplayer_is_server),
             (neg|game_in_multiplayer_mode),
             (prop_instance_get_position, pos1, ":instance_id"),
             (prop_instance_rotate_to_position, ":instance_id", pos1, 400, -72000),
           (try_end),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_6m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_8m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_10m"),
         (this_or_next|eq, ":effected_object", "spr_siege_ladder_move_12m"),
         (eq, ":effected_object", "spr_siege_ladder_move_14m"),

         (try_begin),
           (eq, ":effected_object", "spr_siege_ladder_move_6m"),
           (assign, ":animation_time_drop", 120),
           (assign, ":animation_time_elevate", 240),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_8m"),
           (assign, ":animation_time_drop", 140),
           (assign, ":animation_time_elevate", 280),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_10m"),
           (assign, ":animation_time_drop", 160),
           (assign, ":animation_time_elevate", 320),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_12m"),
           (assign, ":animation_time_drop", 190),
           (assign, ":animation_time_elevate", 360),
         (else_try),
           (eq, ":effected_object", "spr_siege_ladder_move_14m"),
           (assign, ":animation_time_drop", 230),
           (assign, ":animation_time_elevate", 400),
         (try_end),
     
         (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_elevate"), #3 seconds in average
           (eq, ":opened_or_closed", 0), #ladder at ground           
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
           (prop_instance_enable_physics, ":effected_object_instance_id", 0),
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 300),
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1), 
         (else_try), #ladder at wall
           (scene_prop_enable_after_time, ":effected_object_instance_id", ":animation_time_drop"), #1.5 seconds in average
           (prop_instance_get_position, pos0, ":instance_id"),

           (assign, ":smallest_dist", -1),
           (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
             (entry_point_get_position, pos1, ":entry_point_no"),
             (get_sq_distance_between_positions, ":dist", pos0, pos1),
             (this_or_next|eq, ":smallest_dist", -1),
             (lt, ":dist", ":smallest_dist"),
             (assign, ":smallest_dist", ":dist"),
             (assign, ":nearest_entry_point", ":entry_point_no"),
           (try_end),

           (try_begin),
             (ge, ":smallest_dist", 0),
             (lt, ":smallest_dist", 22500), #max 15m distance
             (entry_point_get_position, pos1, ":nearest_entry_point"),
             (position_rotate_x, pos1, -90),
             (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_smoke_effect_done, 0),
             (prop_instance_enable_physics, ":effected_object_instance_id", 0),
             (prop_instance_animate_to_position, ":effected_object_instance_id", pos1, 130),
           (try_end),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (else_try),
         (this_or_next|eq, ":effected_object", "spr_door_destructible"),
         (this_or_next|eq, ":effected_object", "spr_castle_f_door_b"),
         (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),     
         (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),     
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),     
         (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),     
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),     
         (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),     
         (eq, ":scene_prop_id", "spr_castle_f_door_a"),
     
         (assign, ":effected_object_instance_id", ":instance_id"),
         (scene_prop_get_slot, ":opened_or_closed", ":effected_object_instance_id", scene_prop_open_or_close_slot),

         (try_begin),
           (eq, ":opened_or_closed", 0),

           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (try_begin),
             (neg|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),
             (neg|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),
             
             (position_rotate_z, pos0, -85),
           (else_try),  
             (position_rotate_z, pos0, 85),
           (try_end),
           
           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),
          
           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 1),
         (else_try),          
           (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),

           (scene_prop_enable_after_time, ":effected_object_instance_id", 100),

           (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 100),

           (scene_prop_set_slot, ":effected_object_instance_id", scene_prop_open_or_close_slot, 0),
         (try_end),
       (try_end),
     (try_end),
     ]),
           
  #script_determine_team_flags
  # INPUT: none
  # OUTPUT: none
  ("determine_team_flags",
   [
     (store_script_param, ":team_no", 1),          
   
       (try_begin),
         (eq, ":team_no", 0),
     
         (team_get_faction, ":team_faction_no", 0),
         (try_begin),
           (eq, ":team_faction_no", "fac_1"),   
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_swadian"),
         (else_try),
           (eq, ":team_faction_no", "fac_2"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_vaegir"),
         (else_try),
           (eq, ":team_faction_no", "fac_3"), 
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_khergit"),
         (else_try),
           (eq, ":team_faction_no", "fac_4"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_nord"),
         (else_try),
           (eq, ":team_faction_no", "fac_5"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_rhodok"),
         (else_try),
           (eq, ":team_faction_no", "fac_6"),
           (assign, "$team_1_flag_scene_prop", "spr_headquarters_flag_sarranid"),
         (try_end),
       (else_try),
         (team_get_faction, ":team_faction_no", 1),
         (try_begin),    
           (eq, ":team_faction_no", "fac_1"),   
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_swadian"),
         (else_try),
           (eq, ":team_faction_no", "fac_2"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_vaegir"),
         (else_try),
           (eq, ":team_faction_no", "fac_3"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_khergit"),
         (else_try),
           (eq, ":team_faction_no", "fac_4"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_nord"),
         (else_try),
           (eq, ":team_faction_no", "fac_5"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_rhodok"),
         (else_try),
           (eq, ":team_faction_no", "fac_6"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_sarranid"),
         (try_end),  
       
         (try_begin),       
           (eq, "$team_1_flag_scene_prop", "$team_2_flag_scene_prop"),
           (assign, "$team_2_flag_scene_prop", "spr_headquarters_flag_rebel"),
         (try_end),
       (try_end),
   ]),


  #script_move_death_mode_flags_down
  # INPUT: none
  # OUTPUT: none
  ("move_death_mode_flags_down",
   [
     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (position_move_z, pos0, -2000), 
       (prop_instance_set_position, ":pole_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (position_move_z, pos1, -2000), 
       (prop_instance_set_position, ":pole_2_id", pos1),
     (try_end),
    
     (try_begin),
       (scene_prop_get_instance, ":pole_1_id", "spr_headquarters_pole_code_only", 0),
       (prop_instance_get_position, pos0, ":pole_1_id"),
       (scene_prop_get_instance, ":flag_1_id", "$team_1_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_1_id"),
       (position_move_z, pos0, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_1_id", pos0),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_2_id", "spr_headquarters_pole_code_only", 1),
       (prop_instance_get_position, pos1, ":pole_2_id"),
       (scene_prop_get_instance, ":flag_2_id", "$team_2_flag_scene_prop", 0),
       (prop_instance_stop_animating, ":flag_2_id"),
       (position_move_z, pos1, multi_headquarters_flag_initial_height),
       (prop_instance_set_position, ":flag_2_id", pos1),
     (try_end),
   ]),


  #script_move_headquarters_flags
  # INPUT: arg1 = current_owner, arg2 = number_of_agents_around_flag_team_1, arg3 = number_of_agents_around_flag_team_2
  # OUTPUT: none
  ("move_headquarters_flags",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":number_of_agents_around_flag_team_1", 2),
     (store_script_param, ":number_of_agents_around_flag_team_2", 3),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":current_owner", "trp_multiplayer_data", ":cur_flag_slot"),

     (scene_prop_get_num_instances, ":num_instances", "spr_headquarters_flag_gray_code_only"),
     (try_begin),
       (assign, ":visibility", 0),
       (lt, ":flag_no", ":num_instances"),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_get_visibility, ":visibility", ":flag_id"),
     (try_end),

     (try_begin),
       (eq, ":visibility", 1),
       (assign, ":shown_flag", 0),
       (assign, ":shown_flag_id", ":flag_id"),
     (else_try),
       (scene_prop_get_num_instances, ":num_instances", "$team_1_flag_scene_prop"),
       (try_begin),
         (assign, ":visibility", 0),
         (lt, ":flag_no", ":num_instances"),
         (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (scene_prop_get_visibility, ":visibility", ":flag_id"),
       (try_end),

       #(scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       #(scene_prop_get_visibility, ":visibility", ":flag_id"),       
       (try_begin),
         (eq, ":visibility", 1),
         (assign, ":shown_flag", 1),
         (assign, ":shown_flag_id", ":flag_id"),
       (else_try),
         (scene_prop_get_num_instances, ":num_instances", "$team_2_flag_scene_prop"),
         (try_begin),
           (assign, ":visibility", 0),
           (lt, ":flag_no", ":num_instances"),
           (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
           (scene_prop_get_visibility, ":visibility", ":flag_id"),
         (try_end),

         #(scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         #(scene_prop_get_visibility, ":visibility", ":flag_id"),              
         (try_begin),
           (eq, ":visibility", 1),
           (assign, ":shown_flag", 2),
           (assign, ":shown_flag_id", ":flag_id"),
         (try_end),
       (try_end),
     (try_end),

     (try_begin),
       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
     (try_end),

     (try_begin),       
       (eq, ":shown_flag", ":current_owner"), #situation 1 : (current owner is equal shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),         
         (assign, ":flag_movement", 0), #0:stop
       (else_try),  
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", 1), #1:rise (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (eq, ":current_owner", 1),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (eq, ":current_owner", 2),
           (assign, ":flag_movement", 1), #1:rise (fast)
         (else_try),
           (assign, ":flag_movement", -1), #-1:drop (fast)
         (try_end),
       (try_end),
     (else_try), #situation 2 : (current owner is different than shown flag)
       (try_begin),
         (ge, ":number_of_agents_around_flag_team_1", 1),
         (ge, ":number_of_agents_around_flag_team_2", 1),
         (assign, ":flag_movement", 0), #0:stop
       (else_try),  
         (eq, ":number_of_agents_around_flag_team_1", 0),
         (eq, ":number_of_agents_around_flag_team_2", 0),
         (assign, ":flag_movement", -1), #-1:drop (slow)
       (else_try),
         (try_begin),
           (ge, ":number_of_agents_around_flag_team_1", 1),
           (eq, ":number_of_agents_around_flag_team_2", 0),
           (try_begin),
             (eq, ":shown_flag", 1),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 1),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (else_try),
           (eq, ":number_of_agents_around_flag_team_1", 0),
           (ge, ":number_of_agents_around_flag_team_2", 1),
           (try_begin),
             (eq, ":shown_flag", 2),
             (assign, ":flag_movement", 1), #1:rise (fast)
           (else_try),
             (neq, ":current_owner", 2),
             (assign, ":flag_movement", -1), #-1:drop (fast)
           (try_end),
         (try_end),
       (try_end),
     (try_end),

     (store_add, ":number_of_total_agents_around_flag", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),

     (try_begin),
       (eq, ":flag_movement", 0),
       (assign, reg0, 0),
     (else_try),
       (eq, ":flag_movement", 1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (position_move_z, pos0, multi_headquarters_pole_height),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (else_try),  
       (eq, ":flag_movement", -1),
       (prop_instance_get_position, pos1, ":shown_flag_id"),
       (prop_instance_get_position, pos0, ":pole_id"),
       (get_distance_between_positions, ":dist_between_flag_and_its_target", pos0, pos1),
       (call_script, "script_calculate_flag_move_time", ":number_of_total_agents_around_flag", ":dist_between_flag_and_its_target"),
     (try_end),

     (call_script, "script_move_flag", ":shown_flag_id", reg0), #pos0 : target position
     ]),

  #script_set_num_agents_around_flag
  # INPUT: arg1 = flag_no, arg2 = owner_code
  # OUTPUT: none
  ("set_num_agents_around_flag",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":current_owner_code", 2),

     (store_div, ":number_of_agents_around_flag_team_1", ":current_owner_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":current_owner_code", 100),

     (store_add, ":cur_flag_owner_counts_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_owner_counts_slot", ":current_owner_code"),

     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
  ]),
  
  #script_change_flag_owner
  # INPUT: arg1 = flag_no, arg2 = owner_code
  # OUTPUT: none
  ("change_flag_owner",
   [
     (store_script_param, ":flag_no", 1),
     (store_script_param, ":owner_code", 2),

     (try_begin),
       (lt, ":owner_code", 0),
       (val_add, ":owner_code", 1),
       (val_mul, ":owner_code", -1),
     (try_end),
  
     (store_div, ":owner_team_no", ":owner_code", 100),
     (store_mod, ":shown_flag_no", ":owner_code", 100),
  
     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_get_slot, ":older_owner_team_no", "trp_multiplayer_data", ":cur_flag_slot"),

     (store_add, ":cur_flag_slot", multi_data_flag_owner_begin, ":flag_no"),
     (troop_set_slot, "trp_multiplayer_data", ":cur_flag_slot", ":owner_team_no"),

     #senchronizing flag positions
     (try_begin),
       #(this_or_next|eq, ":initial_flags", 0), #moved after auto-animating
       (multiplayer_is_server),

       (scene_prop_get_instance, ":pole_id", "spr_headquarters_pole_code_only", ":flag_no"),
       (try_begin),
         (eq, ":owner_team_no", 0), #if new owner team is 0 then flags are at bottom
         (neq, ":older_owner_team_no", -1), #clients
         (assign, ":continue", 1),
         (try_begin),
           (multiplayer_is_server),
           (eq, "$g_placing_initial_flags", 1),
           (assign, ":continue", 0),
         (try_end),
         (eq, ":continue", 1),
         (prop_instance_get_position, pos0, ":pole_id"),
         (position_move_z, pos0, multi_headquarters_distance_to_change_flag),      
       (else_try),
         (prop_instance_get_position, pos0, ":pole_id"), #if new owner team is not 0 then flags are at top
         (position_move_z, pos0, multi_headquarters_pole_height),
       (try_end),
  
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),
  
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),
  
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
         (prop_instance_stop_animating, ":flag_id"),
       (prop_instance_set_position, ":flag_id", pos0),          
     (try_end),

     #setting visibilities of flags
     (try_begin), 
       (eq, ":shown_flag_no", 0),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
     (else_try),
       (eq, ":shown_flag_no", 1),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (else_try),
       (eq, ":shown_flag_no", 2),
       (scene_prop_get_instance, ":flag_id", "$team_1_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
       (scene_prop_get_instance, ":flag_id", "$team_2_flag_scene_prop", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 1),
       (scene_prop_get_instance, ":flag_id", "spr_headquarters_flag_gray_code_only", ":flag_no"),
       (scene_prop_set_visibility, ":flag_id", 0),
     (try_end),

     #other
     (store_add, ":cur_flag_players_around_slot", multi_data_flag_players_around_begin, ":flag_no"),
     (troop_get_slot, ":players_around_code", "trp_multiplayer_data", ":cur_flag_players_around_slot"),
 
     (store_div, ":number_of_agents_around_flag_team_1", ":players_around_code", 100),
     (store_mod, ":number_of_agents_around_flag_team_2", ":players_around_code", 100),
  
     (call_script, "script_move_headquarters_flags", ":flag_no", ":number_of_agents_around_flag_team_1", ":number_of_agents_around_flag_team_2"),
   ]),

  #script_move_object_to_nearest_entry_point
  # INPUT: none
  # OUTPUT: none
  ("move_object_to_nearest_entry_point",
   [
     (store_script_param, ":scene_prop_no", 1),

     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (prop_instance_get_position, pos0, ":instance_id"),

       (assign, ":smallest_dist", -1),
       (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
         (entry_point_get_position, pos1, ":entry_point_no"),
         (get_sq_distance_between_positions, ":dist", pos0, pos1),
         (this_or_next|eq, ":smallest_dist", -1),
         (lt, ":dist", ":smallest_dist"),
         (assign, ":smallest_dist", ":dist"),
         (assign, ":nearest_entry_point", ":entry_point_no"),
       (try_end),

       (try_begin),
         (ge, ":smallest_dist", 0),
         (lt, ":smallest_dist", 22500), #max 15m distance
         (entry_point_get_position, pos1, ":nearest_entry_point"),
         (position_rotate_x, pos1, -90),
         (prop_instance_animate_to_position, ":instance_id", pos1, 1),
       (try_end),
     (try_end),
   ]),


  #script_multiplayer_server_on_agent_spawn_common
  # INPUT: arg1 = agent_no
  # OUTPUT: none
  ("multiplayer_server_on_agent_spawn_common",
   [
     (store_script_param, ":agent_no", 1),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, -1),
     (try_begin),
       (agent_is_non_player, ":agent_no"),
       (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
     (try_end),
     ]),

  #script_multiplayer_server_player_joined_common
  # INPUT: arg1 = player_no
  # OUTPUT: none
  ("multiplayer_server_player_joined_common",
   [
     (store_script_param, ":player_no", 1),
     (try_begin),
       (this_or_next|player_is_active, ":player_no"),
       (eq, ":player_no", 0),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (store_mission_timer_a, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_join_time, ":player_join_time"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1),
       #fight and destroy only
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_1, 0),
       (player_set_slot, ":player_no", slot_player_damage_given_to_target_2, 0),
       #fight and destroy only end
       (try_begin),
         (multiplayer_is_server),
         (assign, ":initial_gold", multi_initial_gold_value),
         (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
         (val_div, ":initial_gold", 100),
         (player_set_gold, ":player_no", ":initial_gold"),
         (call_script, "script_multiplayer_send_initial_information", ":player_no"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_server_before_mission_start_common
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_server_before_mission_start_common",
   [
     (try_begin),
       (scene_allows_mounted_units),
       (assign, "$g_horses_are_avaliable", 1),
     (else_try),
       (assign, "$g_horses_are_avaliable", 0),
     (try_end),
     (scene_set_day_time, 15),
     (assign, "$g_multiplayer_mission_end_screen", 0),

     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (call_script, "script_multiplayer_init_player_slots", ":player_no"),
       (assign, ":initial_gold", multi_initial_gold_value),
       (val_mul, ":initial_gold", "$g_multiplayer_initial_gold_multiplier"),
       (val_div, ":initial_gold", 100),
       (player_set_gold, ":player_no", ":initial_gold"),
       (player_set_slot, ":player_no", slot_player_first_spawn, 1), #not required in siege, bt, fd
     (try_end),
     ]),

  #script_multiplayer_server_on_agent_killed_or_wounded_common
  # INPUT: arg1 = dead_agent_no, arg2 = killer_agent_no
  # OUTPUT: none
  ("multiplayer_server_on_agent_killed_or_wounded_common",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),

     (call_script, "script_multiplayer_event_agent_killed_or_wounded", ":dead_agent_no", ":killer_agent_no"),
     #adding 1 score points to agent which kills enemy agent at server
     (try_begin),
       (multiplayer_is_server),
       (try_begin), #killing myself because of some reason (friend hit, fall, team change)
         (lt, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (neg|agent_is_non_player, ":dead_agent_no"),
         (agent_get_player_id, ":dead_agent_player_id", ":dead_agent_no"),
         (player_is_active, ":dead_agent_player_id"),
         (player_get_score, ":dead_agent_player_score", ":dead_agent_player_id"),
         (val_add, ":dead_agent_player_score", -1),
         (player_set_score, ":dead_agent_player_id", ":dead_agent_player_score"),
       (else_try), #killing teammate
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_get_team, ":killer_team_no", ":killer_agent_no"),
         (agent_get_team, ":dead_team_no", ":dead_agent_no"),
         (eq, ":killer_team_no", ":dead_team_no"),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (val_add, ":killer_agent_player_score", -1),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
         #(player_get_kill_count, ":killer_agent_player_kill_count", ":killer_agent_player_id"),
         #(val_add, ":killer_agent_player_kill_count", -2),
         #(player_set_kill_count, ":killer_agent_player_id", ":killer_agent_player_kill_count"),
       (else_try), #killing enemy
         (ge, ":killer_agent_no", 0),
         (ge, ":dead_agent_no", 0),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_human, ":killer_agent_no"),
         (neg|agent_is_non_player, ":killer_agent_no"),
         (agent_get_player_id, ":killer_agent_player_id", ":killer_agent_no"),
         (player_is_active, ":killer_agent_player_id"),
         (player_get_score, ":killer_agent_player_score", ":killer_agent_player_id"),
         (agent_get_team, ":killer_agent_team", ":killer_agent_no"),
         (agent_get_team, ":dead_agent_team", ":dead_agent_no"),
         (try_begin),
           (neq, ":killer_agent_team", ":dead_agent_team"),
           (val_add, ":killer_agent_player_score", 1),
         (else_try),
           (val_add, ":killer_agent_player_score", -1),
         (try_end),
         (player_set_score, ":killer_agent_player_id", ":killer_agent_player_score"),
       (try_end),
     (try_end),

     (call_script, "script_add_kill_death_counts", ":killer_agent_no", ":dead_agent_no"),
     #money management
     (call_script, "script_money_management_after_agent_death", ":killer_agent_no", ":dead_agent_no"),
     ]),

  #script_multiplayer_close_gate_if_it_is_open
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_close_gate_if_it_is_open",
   [
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_winch_b"),
     (try_for_range, ":cur_prop_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":prop_instance_id", "spr_winch_b", ":cur_prop_instance"),
       (scene_prop_slot_eq, ":prop_instance_id", scene_prop_open_or_close_slot, 1),
       (scene_prop_get_instance, ":effected_object_instance_id", "spr_portcullis", ":cur_prop_instance"),
       (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),      
       (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
     (try_end),
   ]),  

  #script_multiplayer_move_moveable_objects_initial_positions
  # INPUT: none
  # OUTPUT: none
  ("multiplayer_move_moveable_objects_initial_positions",
   [
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_6m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_8m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_10m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_12m"),
     (call_script, "script_move_object_to_nearest_entry_point", "spr_siege_ladder_move_14m"),
   ]),

  #script_move_belfries_to_their_first_entry_point
  # INPUT: none
  # OUTPUT: none
  ("move_belfries_to_their_first_entry_point",
   [
    (store_script_param, ":belfry_body_scene_prop", 1),
     
    (set_fixed_point_multiplier, 100),    
    (scene_prop_get_num_instances, ":num_belfries", ":belfry_body_scene_prop"),
    
    (try_for_range, ":belfry_no", 0, ":num_belfries"),
      #belfry 
      (scene_prop_get_instance, ":belfry_scene_prop_id", ":belfry_body_scene_prop", ":belfry_no"),
      (prop_instance_get_position, pos0, ":belfry_scene_prop_id"),

      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_platform_a", ":belfry_no"),
        #belfry platform_b
        (scene_prop_get_instance, ":belfry_platform_b_scene_prop_id", "spr_belfry_platform_b", ":belfry_no"),
      (else_try),
        #belfry platform_a
        (scene_prop_get_instance, ":belfry_platform_a_scene_prop_id", "spr_belfry_b_platform_a", ":belfry_no"),
      (try_end),
    
      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),    
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),    
      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_2
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
      #belfry wheel_3
      (val_add, ":wheel_no", 1),
      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),

      (store_add, ":belfry_first_entry_point_id", 11, ":belfry_no"), #belfry entry points are 110..119 and 120..129 and 130..139
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),
        (val_add, ":belfry_first_entry_point_id", ":number_of_belfry_a"),
      (try_end),    
      (val_mul, ":belfry_first_entry_point_id", 10),
      (entry_point_get_position, pos1, ":belfry_first_entry_point_id"),

      #this code block is taken from module_mission_templates.py (multiplayer_server_check_belfry_movement)
      #up down rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), 
      (position_get_distance_to_terrain, ":height_to_terrain_1", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at left part of belfry

      (init_position, pos9),
      (position_set_y, pos9, -500), #go 5.0 meters back
      (position_set_x, pos9, 300), #go 3.0 meters right
      (position_transform_position_to_parent, pos10, pos1, pos9), 
      (position_get_distance_to_terrain, ":height_to_terrain_2", pos10), #learn distance between 5 meters back of entry point(pos10) and ground level at right part of belfry

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),
      (val_mul, ":height_to_terrain", 100), #because of fixed point multiplier

      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 2 degrees. #ac sonra
      (init_position, pos20),    
      (position_rotate_x_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos23, pos1, pos20),

      #right left rotation of belfry's next entry point
      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_1", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (init_position, pos9),
      (position_set_x, pos9, -300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in -x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_left", pos10), #learn distance between 3.0 meters left of entry point(pos10) and ground level
      (init_position, pos9),
      (position_set_x, pos9, 300), #go 3.0 meters left
      (position_set_y, pos9, -500), #go 5.0 meters forward
      (position_transform_position_to_parent, pos10, pos1, pos9), #applying 3.0 meters in x to position of next entry point target, final result is in pos10
      (position_get_distance_to_terrain, ":height_to_terrain_at_right", pos10), #learn distance between 3.0 meters right of entry point(pos10) and ground level
      (store_sub, ":height_to_terrain_2", ":height_to_terrain_at_left", ":height_to_terrain_at_right"),

      (store_add, ":height_to_terrain", ":height_to_terrain_1", ":height_to_terrain_2"),    
      (val_mul, ":height_to_terrain", 100), #100 is because of fixed_point_multiplier
      (store_div, ":rotate_angle_of_next_entry_point", ":height_to_terrain", 24), #if there is 1 meters of distance (100cm) then next target position will rotate by 25 degrees. 
      (val_mul, ":rotate_angle_of_next_entry_point", -1),

      (init_position, pos20),
      (position_rotate_y_floating, pos20, ":rotate_angle_of_next_entry_point"),
      (position_transform_position_to_parent, pos22, pos23, pos20),

      (copy_position, pos1, pos22),
      #end of code block

      #belfry 
      (prop_instance_stop_animating, ":belfry_scene_prop_id"),
      (prop_instance_set_position, ":belfry_scene_prop_id", pos1),
    
      #belfry platforms
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_a"),

        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
     
          (init_position, pos20),
          (position_rotate_x, pos20, 90),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),    
        #belfry platform_b
        (prop_instance_get_position, pos6, ":belfry_platform_b_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (prop_instance_stop_animating, ":belfry_platform_b_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_b_scene_prop_id", pos8),
      (else_try),
        #belfry platform_a
        (prop_instance_get_position, pos6, ":belfry_platform_a_scene_prop_id"),
        (position_transform_position_to_local, pos7, pos0, pos6),
        (position_transform_position_to_parent, pos8, pos1, pos7),
        (try_begin),
          (neg|scene_prop_slot_eq, ":belfry_scene_prop_id", scene_prop_belfry_platform_moved, 0),
     
          (init_position, pos20),
          (position_rotate_x, pos20, 50),
          (position_transform_position_to_parent, pos8, pos8, pos20),
        (try_end),
        (prop_instance_stop_animating, ":belfry_platform_a_scene_prop_id"),
        (prop_instance_set_position, ":belfry_platform_a_scene_prop_id", pos8),    
      (try_end),
    
      #belfry wheel_1
      (store_mul, ":wheel_no", ":belfry_no", 3),
      (try_begin),
        (eq, ":belfry_body_scene_prop", "spr_belfry_b"),
        (scene_prop_get_num_instances, ":number_of_belfry_a", "spr_belfry_a"),    
        (store_mul, ":number_of_belfry_a_wheels", ":number_of_belfry_a", 3),
        (val_add, ":wheel_no", ":number_of_belfry_a_wheels"),
      (try_end),
      (prop_instance_get_position, pos6, ":belfry_wheel_1_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_1_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_1_scene_prop_id", pos8),
      #belfry wheel_2
      (prop_instance_get_position, pos6, ":belfry_wheel_2_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_2_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_2_scene_prop_id", pos8),
      #belfry wheel_3
      (prop_instance_get_position, pos6, ":belfry_wheel_3_scene_prop_id"),
      (position_transform_position_to_local, pos7, pos0, pos6),
      (position_transform_position_to_parent, pos8, pos1, pos7),
      (prop_instance_stop_animating, ":belfry_wheel_3_scene_prop_id"),
      (prop_instance_set_position, ":belfry_wheel_3_scene_prop_id", pos8),
    (try_end),
    ]),

  #script_team_set_score
  # INPUT: arg1 = team_no, arg2 = score
  # OUTPUT: none
  ("team_set_score",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":score", 2),
     
     (team_set_score, ":team_no", ":score"),
   ]),


  #script_set_attached_scene_prop
  # INPUT: arg1 = agent_id, arg2 = flag_id
  # OUTPUT: none
  ("set_attached_scene_prop",
   [
     (store_script_param, ":agent_id", 1),
     (store_script_param, ":flag_id", 2),

     (try_begin), #if current mod is capture the flag and attached scene prop is flag then change flag situation of flag owner team.
       (scene_prop_get_instance, ":red_flag_id", "spr_tutorial_flag_red", 0),
       (scene_prop_get_instance, ":blue_flag_id", "spr_tutorial_flag_blue", 0),
       (assign, ":flag_owner_team", -1),
       (try_begin),
         (ge, ":red_flag_id", 0),
         (eq, ":flag_id", ":red_flag_id"),
         (assign, ":flag_owner_team", 0),
       (else_try),
         (ge, ":blue_flag_id", 0),
         (eq, ":flag_id", ":blue_flag_id"),
         (assign, ":flag_owner_team", 1),
       (try_end),
       (ge, ":flag_owner_team", 0),
       (team_set_slot, ":flag_owner_team", slot_team_flag_situation, 1), #1-stolen flag
     (try_end),
        
     (agent_set_attached_scene_prop, ":agent_id", ":flag_id"),
     (agent_set_attached_scene_prop_x, ":agent_id", 20),
     (agent_set_attached_scene_prop_z, ":agent_id", 50),
   ]),  

  #script_set_team_flag_situation
  # INPUT: arg1 = team_no, arg2 = score
  # OUTPUT: none
  ("set_team_flag_situation",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":flag_situation", 2),

     (team_set_slot, ":team_no", slot_team_flag_situation, ":flag_situation"),
   ]),

  #script_start_death_mode
  # INPUT: none
  # OUTPUT: none
  ("start_death_mode",
   [
     (assign, "$g_multiplayer_message_type", multiplayer_message_type_start_death_mode),
     (start_presentation, "prsnt_multiplayer_message_1"),
   ]),

  #script_calculate_new_death_waiting_time_at_death_mod
  # INPUT: none
  # OUTPUT: none
  ("calculate_new_death_waiting_time_at_death_mod",
   [
     (assign, ":num_living_players", 0), #count number of living players to find out death wait time
     (try_begin),
       (try_for_agents, ":agent_no"),
         (agent_is_human, ":agent_no"),
         (agent_is_alive, ":agent_no"),
         (val_add, ":num_living_players", 1),
       (try_end),
     (try_end),

     (val_add, ":num_living_players", multiplayer_battle_formula_value_a),
     (set_fixed_point_multiplier, 100),
     (store_mul, ":num_living_players", ":num_living_players", 100),
     (store_sqrt, ":sqrt_num_living_players", ":num_living_players"),
     (store_div, "$g_battle_waiting_seconds", multiplayer_battle_formula_value_b, ":sqrt_num_living_players"),
     (store_mission_timer_a, "$g_death_mode_part_1_start_time"),
   ]),
  
  #script_calculate_number_of_targets_destroyed
  # INPUT: none
  # OUTPUT: none

  ("calculate_number_of_targets_destroyed",
   [
     (assign, "$g_number_of_targets_destroyed", 0),
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),    

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_get_position, pos1, ":cur_instance_id"),
       (get_sq_distance_between_positions_in_meters, ":dist", pos0, pos1),
       (gt, ":dist", 2), #this can be 0 or 1 too.
       (val_add, "$g_number_of_targets_destroyed", 1),
     (try_end),    
     ]),

  #script_initialize_objects
  # INPUT: none
  # OUTPUT: none
  ("initialize_objects",
   [
     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (val_add, ":number_of_players", 1),
     (try_end),

     #1 player = (Sqrt(1) - 1) * 200 + 1200 = 1200, 1800 (minimum)
     #4 player = (Sqrt(4) - 1) * 200 + 1200 = 1400, 2100
     #9 player = (Sqrt(9) - 1) * 200 + 1200 = 1600, 2400
     #16 player = (Sqrt(16) - 1) * 200 + 1200 = 1800, 2700 (general used)
     #25 player = (Sqrt(25) - 1) * 200 + 1200 = 2000, 3000 (average)
     #36 player = (Sqrt(36) - 1) * 200 + 1200 = 2200, 3300
     #49 player = (Sqrt(49) - 1) * 200 + 1200 = 2400, 3600
     #64 player = (Sqrt(49) - 1) * 200 + 1200 = 2600, 3900

     (set_fixed_point_multiplier, 100),
     (val_mul, ":number_of_players", 100),
     (store_sqrt, ":number_of_players", ":number_of_players"),
     (val_sub, ":number_of_players", 100),
     (val_max, ":number_of_players", 0),
     (store_mul, ":effect_of_number_of_players", ":number_of_players", 2),
     (store_add, ":health_catapult", multi_minimum_target_health, ":effect_of_number_of_players"),     
     (store_mul, ":health_trebuchet", ":health_catapult", 15), #trebuchet's health is 1.5x of catapult's     
     (val_div, ":health_trebuchet", 10),
     (store_mul, ":health_sally_door", ":health_catapult", 18), #sally door's health is 1.8x of catapult's     
     (val_div, ":health_sally_door", 10),
     (store_mul, ":health_sally_door_double", ":health_sally_door", 2),

     (assign, "$g_number_of_targets_destroyed", 0),
     
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),     
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_catapult"),
     (try_end),    

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_trebuchet"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_e_sally_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_e_sally_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),
     
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_sally_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_sally_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_left"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_left", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_right"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_right", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_left"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_left", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),     

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_right"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_right", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),     

     (store_div, ":health_sally_door_div_3", ":health_sally_door", 3),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_a", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),     

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_b"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_b", ":cur_instance"),
       (prop_instance_get_starting_position, pos0, ":cur_instance_id"),
       (prop_instance_stop_animating, ":cur_instance_id"),
       (prop_instance_set_position, ":cur_instance_id", pos0),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),     
     ]),
  
  #script_initialize_objects_clients
  # INPUT: none
  # OUTPUT: none
  ("initialize_objects_clients",
   [
     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),
     (try_for_range, ":player_no", 0, ":num_players"),
       (player_is_active, ":player_no"),
       (val_add, ":number_of_players", 1),
     (try_end),

     #1 player = (Sqrt(1) - 1) * 200 + 1200 = 1200, 1800 (minimum)
     #4 player = (Sqrt(4) - 1) * 200 + 1200 = 1400, 2100
     #9 player = (Sqrt(9) - 1) * 200 + 1200 = 1600, 2400
     #16 player = (Sqrt(16) - 1) * 200 + 1200 = 1800, 2700 (general used)
     #25 player = (Sqrt(25) - 1) * 200 + 1200 = 2000, 3000 (average)
     #36 player = (Sqrt(36) - 1) * 200 + 1200 = 2200, 3300
     #49 player = (Sqrt(49) - 1) * 200 + 1200 = 2400, 3600
     #64 player = (Sqrt(49) - 1) * 200 + 1200 = 2600, 3900

     (set_fixed_point_multiplier, 100),
     (val_mul, ":number_of_players", 100),
     (store_sqrt, ":number_of_players", ":number_of_players"),
     (val_sub, ":number_of_players", 100),
     (val_max, ":number_of_players", 0),
     (store_mul, ":effect_of_number_of_players", ":number_of_players", 2),
     (store_add, ":health_catapult", multi_minimum_target_health, ":effect_of_number_of_players"),     
     (store_mul, ":health_trebuchet", ":health_catapult", 15), #trebuchet's health is 1.5x of catapult's
     (val_div, ":health_trebuchet", 10),
     (store_mul, ":health_sally_door", ":health_catapult", 18), #trebuchet's health is 1.8x of trebuchet's
     (val_div, ":health_sally_door", 10),
     (store_mul, ":health_sally_door_double", ":health_sally_door", 2),

     (assign, "$g_number_of_targets_destroyed", 0),
     
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_catapult_destructible"),
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_catapult_destructible", ":cur_instance"),     
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_catapult"),
     (try_end),    

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_trebuchet_destructible"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_trebuchet_destructible", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_trebuchet"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_e_sally_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_e_sally_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),
     
     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_sally_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_sally_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_left"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_left", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_earth_sally_gate_right"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_earth_sally_gate_right", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_double"),
     (try_end),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_left"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_left", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),             

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_viking_keep_destroy_sally_door_right"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_viking_keep_destroy_sally_door_right", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door"),
     (try_end),             

     (store_div, ":health_sally_door_div_3", ":health_sally_door", 3),

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_a"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_a", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),     

     (scene_prop_get_num_instances, ":num_instances_of_scene_prop", "spr_castle_f_door_b"),     
     (try_for_range, ":cur_instance", 0, ":num_instances_of_scene_prop"),
       (scene_prop_get_instance, ":cur_instance_id", "spr_castle_f_door_b", ":cur_instance"),
       (prop_instance_enable_physics, ":cur_instance_id", 1),
       (scene_prop_set_hit_points, ":cur_instance_id", ":health_sally_door_div_3"),
     (try_end),     
     ]),

  #script_show_multiplayer_message
  # INPUT: arg1 = multiplayer_message_type
  # OUTPUT: none
  ("show_multiplayer_message",
   [
    (store_script_param, ":multiplayer_message_type", 1),
    (store_script_param, ":value", 2),

    (assign, "$g_multiplayer_message_type", ":multiplayer_message_type"),

    (try_begin),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
      
      (try_begin), #end of round in clients
        (neg|multiplayer_is_server),
        (assign, "$g_battle_death_mode_started", 0),
      (try_end),  
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_done),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_2"),
      (assign, "$g_team_balance_next_round", 0), 
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_next),
      (assign, "$g_team_balance_next_round", 1),
      (call_script, "script_warn_player_about_auto_team_balance"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_auto_team_balance_no_need),
      (assign, "$g_team_balance_next_round", 0),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_score),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_returned_home),
      (assign, "$g_multiplayer_message_value_1", ":value"),    
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_capture_the_flag_stole),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_poll_result),
      (assign, "$g_multiplayer_message_value_3", ":value"),
      (start_presentation, "prsnt_multiplayer_message_3"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_neutralized),      
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_captured),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_flag_is_pulling),
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_target_destroyed),
    
      (try_begin), #destroy score (condition : a target destroyed)
        (eq, "$g_defender_team", 0),
        (assign, ":attacker_team_no", 1),
      (else_try),
        (assign, ":attacker_team_no", 0),
      (try_end),
       
      (team_get_score, ":team_score", ":attacker_team_no"),
      (val_add, ":team_score", 1),
      (call_script, "script_team_set_score", ":attacker_team_no", ":team_score"), #destroy score end

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_defenders_saved_n_targets),      
      (assign, "$g_multiplayer_message_value_1", ":value"),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":multiplayer_message_type", multiplayer_message_type_attackers_won_the_round),
      (try_begin),
        (eq, "$g_defender_team", 0),
        (assign, "$g_multiplayer_message_value_1", 1),
      (else_try),
        (assign, "$g_multiplayer_message_value_1", 0),
      (try_end),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    ]),

  #script_get_headquarters_scores
  # INPUT: none
  # OUTPUT: reg0 = team_1_num_flags, reg1 = team_2_num_flags
  ("get_headquarters_scores",
   [
     (assign, ":team_1_num_flags", 0),
     (assign, ":team_2_num_flags", 0),
     (try_for_range, ":flag_no", 0, "$g_number_of_flags"),
       (store_add, ":cur_flag_owner_slot", multi_data_flag_owner_begin, ":flag_no"),
       (troop_get_slot, ":cur_flag_owner", "trp_multiplayer_data", ":cur_flag_owner_slot"),
       (neq, ":cur_flag_owner", 0),
       (try_begin),
         (eq, ":cur_flag_owner", 1),
         (val_add, ":team_1_num_flags", 1),
       (else_try),
         (val_add, ":team_2_num_flags", 1),
       (try_end),
     (try_end),
     (assign, reg0, ":team_1_num_flags"),
     (assign, reg1, ":team_2_num_flags"),
     ]),


  #script_draw_this_round
  # INPUT: arg1 = value
  ("draw_this_round",
   [
    (store_script_param, ":value", 1),
    (try_begin),
      (eq, ":value", -9), #destroy mod round end
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      #(assign, "$g_multiplayer_message_value_1", -1),
      #(assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      #(start_presentation, "prsnt_multiplayer_message_1"),
    (else_try),
      (eq, ":value", -1), #draw
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
      (assign, "$g_multiplayer_message_value_1", -1),
      (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_draw),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try), 
      (eq, ":value", 0), #defender wins
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
        
      (team_get_faction, ":faction_of_winner_team", 0),
      (team_get_score, ":team_1_score", 0),
      (val_add, ":team_1_score", 1),
      (team_set_score, 0, ":team_1_score"),
      (assign, "$g_winner_team", 0),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (else_try), 
      (eq, ":value", 1), #attacker wins
      (assign, "$g_round_ended", 1),
      (store_mission_timer_a, "$g_round_finish_time"),
  
      (team_get_faction, ":faction_of_winner_team", 1),
      (team_get_score, ":team_2_score", 1),
      (val_add, ":team_2_score", 1),
      (team_set_score, 1, ":team_2_score"),
      (assign, "$g_winner_team", 1),
      (str_store_faction_name, s1, ":faction_of_winner_team"),

      (assign, "$g_multiplayer_message_value_1", ":value"),
      (assign, "$g_multiplayer_message_type", multiplayer_message_type_round_result_in_battle_mode),
      (start_presentation, "prsnt_multiplayer_message_1"),
    (try_end),
    ]),   

  #script_find_most_suitable_bot_to_control
  # INPUT: arg1 = value
  ("find_most_suitable_bot_to_control",
   [
      (set_fixed_point_multiplier, 100),
      (store_script_param, ":player_no", 1),
      (player_get_team_no, ":player_team", ":player_no"),

      (player_get_slot, ":x_coor", ":player_no", slot_player_death_pos_x),
      (player_get_slot, ":y_coor", ":player_no", slot_player_death_pos_y),
      (player_get_slot, ":z_coor", ":player_no", slot_player_death_pos_z),

      (init_position, pos0),
      (position_set_x, pos0, ":x_coor"),
      (position_set_y, pos0, ":y_coor"),
      (position_set_z, pos0, ":z_coor"),

      (assign, ":most_suitable_bot", -1),
      (assign, ":max_bot_score", -1),

      (try_for_agents, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_non_player, ":cur_agent"),
        (agent_get_team ,":cur_team", ":cur_agent"),
        (eq, ":cur_team", ":player_team"),
        (agent_get_position, pos1, ":cur_agent"),

        #getting score for distance of agent to death point (0..3000)
        (get_distance_between_positions_in_meters, ":dist", pos0, pos1),

        (try_begin),
          (lt, ":dist", 500),
          (store_sub, ":bot_score", 500, ":dist"),
        (else_try),
          (assign, ":bot_score", 0),
        (try_end),
        (val_mul, ":bot_score", 6),

        #getting score for distance of agent to enemy & friend agents (0..300 x agents)
        (try_for_agents, ":cur_agent_2"),
          (agent_is_alive, ":cur_agent_2"),
          (agent_is_human, ":cur_agent_2"),
          (neq, ":cur_agent", ":cur_agent_2"),      
          (agent_get_team ,":cur_team_2", ":cur_agent_2"),
          (try_begin),
            (neq, ":cur_team_2", ":player_team"),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":enemy_near_score", ":dist_2"),
            (else_try),
              (assign, ":enemy_near_score", 300),
            (try_end),
            (val_add, ":bot_score", ":enemy_near_score"),
          (else_try),
            (agent_get_position, pos1, ":cur_agent_2"),
            (get_distance_between_positions, ":dist_2", pos0, pos1),
            (try_begin),
              (lt, ":dist_2", 300),
              (assign, ":friend_near_score", 300, ":dist_2"),
            (else_try),
              (assign, ":friend_near_score", 0),
            (try_end),
            (val_add, ":bot_score", ":friend_near_score"),
          (try_end),
        (try_end),

        #getting score for health (0..200)
        (store_agent_hit_points, ":agent_hit_points", ":cur_agent"),
        (val_mul, ":agent_hit_points", 2),
        (val_add, ":bot_score", ":agent_hit_points"),

        (ge, ":bot_score", ":max_bot_score"),
        (assign, ":max_bot_score", ":bot_score"),
        (assign, ":most_suitable_bot", ":cur_agent"),
      (try_end),

      (assign, reg0, ":most_suitable_bot"),
    ]),

  #script_game_receive_url_response
  #response format should be like this:
  #  [a number or a string]|[another number or a string]|[yet another number or a string] ...
  # here is an example response:
  # 12|Player|100|another string|142|323542|34454|yet another string
  # INPUT: arg1 = num_integers, arg2 = num_strings
  # reg0, reg1, reg2, ... up to 128 registers contain the integer values
  # s0, s1, s2, ... up to 128 strings contain the string values
  ("game_receive_url_response",
    [
      #here is an example usage
##      (store_script_param, ":num_integers", 1),
##      (store_script_param, ":num_strings", 2),
##      (try_begin),
##        (gt, ":num_integers", 4),
##        (display_message, "@{reg0}, {reg1}, {reg2}, {reg3}, {reg4}"),
##      (try_end),
##      (try_begin),
##        (gt, ":num_strings", 4),
##        (display_message, "@{s0}, {s1}, {s2}, {s3}, {s4}"),
##      (try_end),
      ]),

  #script_game_receive_network_message
  # This script is called from the game engine when a new network message is received.
  # INPUT: arg1 = player_no, arg2 = event_type, arg3 = value, arg4 = value_2, arg5 = value_3, arg6 = value_4
  ("game_receive_network_message",
    [
      (store_script_param, ":player_no", 1),
      (store_script_param, ":event_type", 2),
      (try_begin),
        ###############
        #SERVER EVENTS#
        ###############
        (eq, ":event_type", multiplayer_event_set_item_selection),
        (store_script_param, ":slot_no", 3),
        (store_script_param, ":value", 4),
        (try_begin),
          #valid slot check
          (is_between, ":slot_no", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
          #valid item check
          (assign, ":valid_item", 0),
          (try_begin),
            (eq, ":value", -1),
            (assign, ":valid_item", 1),
          (else_try),
            (ge, ":value", 0),
            (player_get_troop_id, ":player_troop_no", ":player_no"),
            (is_between, ":player_troop_no", multiplayer_troops_begin, multiplayer_troops_end),
            (store_sub, ":troop_index", ":player_troop_no", multiplayer_troops_begin),
            (val_add, ":troop_index", slot_item_multiplayer_availability_linked_list_begin),
            (item_get_slot, ":prev_next_item_ids", ":value", ":troop_index"),
            (gt, ":prev_next_item_ids", 0), #0 if the item is not valid for the multiplayer mode
            (assign, ":valid_item", 1),
            (try_begin),
              (neq, "$g_horses_are_avaliable", 1),
              (item_get_slot, ":item_class", ":value", slot_item_multiplayer_item_class),
              (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
              (assign, ":valid_item", 0),
            (try_end),
            (try_begin),
              (eq, "$g_multiplayer_disallow_ranged_weapons", 1),
              (item_get_slot, ":item_class", ":value", slot_item_multiplayer_item_class),
              (is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
              (assign, ":valid_item", 0),
            (try_end),
          (try_end),
          (eq, ":valid_item", 1),
          #condition checks are done
          (player_set_slot, ":player_no", ":slot_no", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_set_bot_selection),
        (store_script_param, ":slot_no", 3),
        (store_script_param, ":value", 4),
        (try_begin),
          #condition check
          (is_between, ":slot_no", slot_player_bot_type_1_wanted, slot_player_bot_type_4_wanted + 1),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (player_set_slot, ":player_no", ":slot_no", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_change_team_no),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_get_team_no, ":player_team", ":player_no"),
          (neq, ":player_team", ":value"),

          #condition checks are done
          (try_begin),
#            #check if available
#            (call_script, "script_cf_multiplayer_team_is_available", ":player_no", ":value"),
#            #reset troop_id to -1
#            (player_set_troop_id, ":player_no", -1),
#            (player_set_team_no, ":player_no", ":value"),
#            (try_begin),
#              (neq, ":value", multi_team_spectator),
#              (neq, ":value", multi_team_unassigned),
#      
#              (store_mission_timer_a, ":player_last_team_select_time"),         
#              (player_set_slot, ":player_no", slot_player_last_team_select_time, ":player_last_team_select_time"),
#      
#              (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_confirmation),
#            (try_end),
#          (else_try),
            #reject request
            (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_rejection),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_change_troop_id),
        (store_script_param, ":value", 3),
        #troop-faction validity check
        (try_begin),
          (eq, ":value", -1),
          (player_set_troop_id, ":player_no", -1),
        (else_try),
          (is_between, ":value", multiplayer_troops_begin, multiplayer_troops_end),
          (player_get_team_no, ":player_team", ":player_no"),
          (is_between, ":player_team", 0, multi_team_spectator),
          (team_get_faction, ":team_faction", ":player_team"),
          (store_troop_faction, ":new_troop_faction", ":value"),
          (eq, ":new_troop_faction", ":team_faction"),
          (player_set_troop_id, ":player_no", ":value"),
          (call_script, "script_multiplayer_clear_player_selected_items", ":player_no"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_start_map),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", multiplayer_scenes_begin, multiplayer_scenes_end),
          (is_between, ":value_2", 0, multiplayer_num_game_types),
          (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (this_or_next|eq, "$g_multiplayer_changing_game_type_allowed", 1),
          (eq, "$g_multiplayer_game_type", ":value_2"),
          (call_script, "script_multiplayer_fill_map_game_types", ":value_2"),
          (assign, ":num_maps", reg0),
          (assign, ":is_valid", 0),
          (store_add, ":end_cond", multi_data_maps_for_game_type_begin, ":num_maps"),
          (try_for_range, ":i_map", multi_data_maps_for_game_type_begin, ":end_cond"),
            (troop_slot_eq, "trp_multiplayer_data", ":i_map", ":value"),
            (assign, ":is_valid", 1),
            (assign, ":end_cond", 0),
          (try_end),
          (eq, ":is_valid", 1),
          #condition checks are done
          (assign, "$g_multiplayer_game_type", ":value_2"),
          (assign, "$g_multiplayer_selected_map", ":value"),
          (team_set_faction, 0, "$g_multiplayer_next_team_1_faction"),
          (team_set_faction, 1, "$g_multiplayer_next_team_2_faction"),
          (call_script, "script_game_multiplayer_get_game_type_mission_template"),
          (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 1),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_max_num_players),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 2, 65),
          #condition checks are done
          (server_set_max_num_players, ":value"),      
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_num_bots_in_team),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 1, 3),
          (is_between, ":value_2", 0, "$g_multiplayer_max_num_bots"),
          #condition checks are done
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_num_bots_team_1", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_num_bots_team_2", ":value_2"),
          (try_end),
          (get_max_players, ":num_players"),                               
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, ":value", ":value_2"),
          (try_end),            
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_anti_cheat),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_anti_cheat, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_friendly_fire, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_melee_friendly_fire),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_melee_friendly_fire, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire_damage_self_ratio),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 101),
          #condition checks are done
          (server_set_friendly_fire_damage_self_ratio, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_friendly_fire_damage_friend_ratio),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 101),
          #condition checks are done
          (server_set_friendly_fire_damage_friend_ratio, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_ghost_mode),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 4),
          #condition checks are done
          (server_set_ghost_mode, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_control_block_dir),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (server_set_control_block_dir, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_combat_speed),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 5),
          #condition checks are done
          (server_set_combat_speed, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_respawn_count),
        (store_script_param, ":value", 3),
        #validity check
        (player_is_admin, ":player_no"),
        (is_between, ":value", 0, 6),
        #condition checks are done       
        (assign, "$g_multiplayer_number_of_respawn_count", ":value"),
        (get_max_players, ":num_players"),
        (try_for_range, ":cur_player", 1, ":num_players"),
          (player_is_active, ":cur_player"),
          (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_count, ":value"),
        (try_end),                  
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_add_to_servers_list),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_add_to_game_servers_list, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_respawn_period), 
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 3, 31),
          #condition checks are done
          (assign, "$g_multiplayer_respawn_period", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_respawn_period, ":value"),
          (try_end),            
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_max_minutes),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 5, 121),
          #condition checks are done
          (assign, "$g_multiplayer_game_max_minutes", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_round_max_seconds),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 60, 901),
          #condition checks are done
          (assign, "$g_multiplayer_round_max_seconds", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_round_max_seconds, ":value"),
          (try_end),            
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_player_respawn_as_bot),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_player_respawn_as_bot", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_player_respawn_as_bot, ":value"),
          (try_end),            
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_max_points),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 3, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_game_max_points", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_point_gained_from_flags),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 25, 401),
          #condition checks are done
          (assign, "$g_multiplayer_point_gained_from_flags", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_point_gained_from_capturing_flag),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 11),
          #condition checks are done
          (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_initial_gold_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_initial_gold_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_battle_earnings_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_battle_earnings_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_round_earnings_multiplier),
        (store_script_param, ":value", 3),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 1001),
          #condition checks are done
          (assign, "$g_multiplayer_round_earnings_multiplier", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_server_name),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (eq, "$g_multiplayer_renaming_server_allowed", 1),
          #condition checks are done
          (server_set_name, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_game_password),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_password, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_welcome_message),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_set_welcome_message, s0), #validity is checked inside this function
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_team_faction),
        (store_script_param, ":value", 3),
        (store_script_param, ":value_2", 4),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 1, 3),
          (is_between, ":value_2", multiplayer_factions_begin, multiplayer_factions_end),
##          (assign, ":is_valid", 0),
##          (try_begin),
##            (eq, ":value", 1),
##            (neq, ":value_2", "$g_multiplayer_next_team_2_faction"),
##            (assign, ":is_valid", 1),
##          (else_try),
##            (neq, ":value_2", "$g_multiplayer_next_team_1_faction"),
##            (assign, ":is_valid", 1),
##          (try_end),
##          (eq, ":is_valid", 1),
          #condition checks are done
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_next_team_1_faction", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_next_team_2_faction", ":value_2"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_open_game_rules),
        (try_begin),
          #no validity check
          (server_get_max_num_players, ":max_num_players"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_players, ":max_num_players"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 1, "$g_multiplayer_next_team_1_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 2, "$g_multiplayer_next_team_2_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
          (server_get_anti_cheat, ":server_anti_cheat"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_anti_cheat, ":server_anti_cheat"),
          (server_get_friendly_fire, ":server_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire, ":server_friendly_fire"),
          (server_get_melee_friendly_fire, ":server_melee_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_melee_friendly_fire, ":server_melee_friendly_fire"),
          (server_get_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (server_get_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (server_get_ghost_mode, ":server_ghost_mode"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ghost_mode, ":server_ghost_mode"),
          (server_get_control_block_dir, ":server_control_block_dir"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_control_block_dir, ":server_control_block_dir"),
          (server_get_combat_speed, ":server_combat_speed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_combat_speed, ":server_combat_speed"),
          (server_get_add_to_game_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_add_to_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_minutes, "$g_multiplayer_game_max_minutes"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_points, "$g_multiplayer_game_max_points"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_flags, "$g_multiplayer_point_gained_from_flags"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_capturing_flag, "$g_multiplayer_point_gained_from_capturing_flag"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_initial_gold_multiplier, "$g_multiplayer_initial_gold_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_battle_earnings_multiplier, "$g_multiplayer_battle_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_earnings_multiplier, "$g_multiplayer_round_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_valid_vote_ratio, "$g_multiplayer_valid_vote_ratio"),
          (str_store_server_name, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_server_name, s0),
          (multiplayer_send_message_to_player, ":player_no", multiplayer_event_return_open_game_rules),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_open_admin_panel),
        (try_begin),
          #validity check
          (player_is_admin, ":player_no"),
          #condition checks are done
          (server_get_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_renaming_server_allowed, "$g_multiplayer_renaming_server_allowed"),
          (server_get_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_changing_game_type_allowed, "$g_multiplayer_changing_game_type_allowed"),
          (server_get_max_num_players, ":max_num_players"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_players, ":max_num_players"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 1, "$g_multiplayer_next_team_1_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_next_team_faction, 2, "$g_multiplayer_next_team_2_faction"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
          (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
          (server_get_anti_cheat, ":server_anti_cheat"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_anti_cheat, ":server_anti_cheat"),
          (server_get_friendly_fire, ":server_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire, ":server_friendly_fire"),
          (server_get_melee_friendly_fire, ":server_melee_friendly_fire"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_melee_friendly_fire, ":server_melee_friendly_fire"),
          (server_get_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_self_ratio, ":friendly_fire_damage_self_ratio"),
          (server_get_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_friendly_fire_damage_friend_ratio, ":friendly_fire_damage_friend_ratio"),
          (server_get_ghost_mode, ":server_ghost_mode"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ghost_mode, ":server_ghost_mode"),
          (server_get_control_block_dir, ":server_control_block_dir"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_control_block_dir, ":server_control_block_dir"),
          (server_get_combat_speed, ":server_combat_speed"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_combat_speed, ":server_combat_speed"),
          (server_get_add_to_game_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_add_to_servers_list, ":server_add_to_servers_list"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_minutes, "$g_multiplayer_game_max_minutes"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_max_points, "$g_multiplayer_game_max_points"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_flags, "$g_multiplayer_point_gained_from_flags"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_point_gained_from_capturing_flag, "$g_multiplayer_point_gained_from_capturing_flag"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_initial_gold_multiplier, "$g_multiplayer_initial_gold_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_battle_earnings_multiplier, "$g_multiplayer_battle_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_earnings_multiplier, "$g_multiplayer_round_earnings_multiplier"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_valid_vote_ratio, "$g_multiplayer_valid_vote_ratio"),
          (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_max_num_bots, "$g_multiplayer_max_num_bots"),
          (str_store_server_name, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_server_name, s0),
          (str_store_server_password, s0),
          (multiplayer_send_string_to_player, ":player_no", multiplayer_event_return_game_password, s0),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_start_new_poll),
        (try_begin),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
           #validity check
          (eq, "$g_multiplayer_poll_running", 0),
          (store_mission_timer_a, ":mission_timer"),
          (player_get_slot, ":poll_disable_time", ":player_no", slot_player_poll_disabled_until_time),
          (ge, ":mission_timer", ":poll_disable_time"),
          (assign, ":continue", 0),
          (try_begin),
            (eq, ":value", 1), # kicking a player
            (try_begin),
              (eq, "$g_multiplayer_kick_voteable", 1),
              (player_is_active, ":value_2"),
              (assign, ":continue", 1),
            (try_end),
          (else_try),
            (eq, ":value", 2), # banning a player
            (try_begin),
              (eq, "$g_multiplayer_ban_voteable", 1),
              (player_is_active, ":value_2"),
              (save_ban_info_of_player, ":value_2"),
              (assign, ":continue", 1),
            (try_end),
          (else_try), # vote for map
            (eq, ":value", 0),
            (try_begin),
              (eq, "$g_multiplayer_maps_voteable", 1),
              (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
              (assign, ":num_maps", reg0),
              (try_for_range, ":i_map", 0, ":num_maps"),
                (store_add, ":map_slot", ":i_map", multi_data_maps_for_game_type_begin),
                (troop_slot_eq, "trp_multiplayer_data", ":map_slot", ":value_2"),
                (assign, ":continue", 1),
                (assign, ":num_maps", 0), #break
              (try_end),
            (try_end),
          (else_try),
            (eq, ":value", 3), #vote for map and factions
            (try_begin),
              (eq, "$g_multiplayer_factions_voteable", 1),
              (store_script_param, ":value_3", 5),
              (store_script_param, ":value_4", 6),
              (call_script, "script_multiplayer_fill_map_game_types", "$g_multiplayer_game_type"),
              (assign, ":num_maps", reg0),
              (try_for_range, ":i_map", 0, ":num_maps"),
                (store_add, ":map_slot", ":i_map", multi_data_maps_for_game_type_begin),
                (troop_slot_eq, "trp_multiplayer_data", ":map_slot", ":value_2"),
                (assign, ":continue", 1),
                (assign, ":num_maps", 0), #break
              (try_end),
              (try_begin),
                (eq, ":continue", 1),
                (this_or_next|neg|is_between, ":value_3", multiplayer_factions_begin, multiplayer_factions_end),
                (this_or_next|neg|is_between, ":value_4", multiplayer_factions_begin, multiplayer_factions_end),
                (eq, ":value_3", ":value_4"),
                (assign, ":continue", 0),
              (try_end),
            (try_end),
          (else_try),
            (eq, ":value", 4), #vote for number of bots
            (store_script_param, ":value_3", 5),
            (store_add, ":upper_limit", "$g_multiplayer_num_bots_voteable", 1),
            (is_between, ":value_2", 0, ":upper_limit"),
            (is_between, ":value_3", 0, ":upper_limit"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          #condition checks are done
          (str_store_player_username, s0, ":player_no"),
          (try_begin),
            (eq, ":value", 1), #kicking a player
            (str_store_player_username, s1, ":value_2"),
            (server_add_message_to_log, "str_poll_kick_player_s1_by_s0"),
          (else_try),
            (eq, ":value", 2), #banning a player
            (str_store_player_username, s1, ":value_2"),
            (server_add_message_to_log, "str_poll_ban_player_s1_by_s0"),
          (else_try),
            (eq, ":value", 0), #vote for map
            (store_sub, ":string_index", ":value_2", multiplayer_scenes_begin),
            (val_add, ":string_index", multiplayer_scene_names_begin),
            (str_store_string, s1, ":string_index"),
            (server_add_message_to_log, "str_poll_change_map_to_s1_by_s0"),
          (else_try),
            (eq, ":value", 3), #vote for map and factions
            (store_sub, ":string_index", ":value_2", multiplayer_scenes_begin),
            (val_add, ":string_index", multiplayer_scene_names_begin),
            (str_store_string, s1, ":string_index"),
            (str_store_faction_name, s2, ":value_3"),
            (str_store_faction_name, s3, ":value_4"),
            (server_add_message_to_log, "str_poll_change_map_to_s1_and_factions_to_s2_and_s3_by_s0"),
          (else_try),
            (eq, ":value", 4), #vote for number of bots
            (assign, reg0, ":value_2"),
            (assign, reg1, ":value_3"),
            (server_add_message_to_log, "str_poll_change_number_of_bots_to_reg0_and_reg1_by_s0"),
          (try_end),
          (assign, "$g_multiplayer_poll_running", 1),
          (assign, "$g_multiplayer_poll_ended", 0),
          (assign, "$g_multiplayer_poll_num_sent", 0),
          (assign, "$g_multiplayer_poll_yes_count", 0),
          (assign, "$g_multiplayer_poll_no_count", 0),
          (assign, "$g_multiplayer_poll_to_show", ":value"),
          (assign, "$g_multiplayer_poll_value_to_show", ":value_2"),
          (try_begin),
            (eq, ":value", 3),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", ":value_4"),
          (else_try),
            (eq, ":value", 4),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", -1),
          (else_try),
            (assign, "$g_multiplayer_poll_value_2_to_show", -1),
            (assign, "$g_multiplayer_poll_value_3_to_show", -1),
          (try_end),
          (store_add, ":poll_disable_until", ":mission_timer", multiplayer_poll_disable_period),
          (player_set_slot, ":player_no", slot_player_poll_disabled_until_time, ":poll_disable_until"),
          (store_add, "$g_multiplayer_poll_end_time", ":mission_timer", 60),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 0, ":num_players"),
            (player_is_active, ":cur_player"),
            (player_set_slot, ":cur_player", slot_player_can_answer_poll, 1),
            (val_add, "$g_multiplayer_poll_num_sent", 1),
            (multiplayer_send_4_int_to_player, ":cur_player", multiplayer_event_ask_for_poll, "$g_multiplayer_poll_to_show", "$g_multiplayer_poll_value_to_show", "$g_multiplayer_poll_value_2_to_show", "$g_multiplayer_poll_value_3_to_show"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_answer_to_poll),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (eq, "$g_multiplayer_poll_running", 1),
          (is_between, ":value", 0, 2),
          (player_slot_eq, ":player_no", slot_player_can_answer_poll, 1),
          #condition checks are done
          (player_set_slot, ":player_no", slot_player_can_answer_poll, 0),
          (try_begin),
            (eq, ":value", 0),
            (val_add, "$g_multiplayer_poll_no_count", 1),
          (else_try),
            (eq, ":value", 1),
            (val_add, "$g_multiplayer_poll_yes_count", 1),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_kick_player),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (player_is_active, ":value"),
          #condition checks are done
          (kick_player, ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_ban_player),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (player_is_active, ":value"),
          #condition checks are done
          (ban_player, ":value", 0, ":player_no"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_valid_vote_ratio),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 50, 101),
          #condition checks are done
          (assign, "$g_multiplayer_valid_vote_ratio", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_auto_team_balance_limit),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (this_or_next|is_between, ":value", 2, 7),
          (eq, ":value", 1000),
          #condition checks are done
          (assign, "$g_multiplayer_auto_team_balance_limit", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_auto_team_balance_limit, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_num_bots_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 51),
          (is_between, ":value", "$g_multiplayer_max_num_bots"),
          #condition checks are done
          (assign, "$g_multiplayer_num_bots_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_num_bots_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_factions_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_factions_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_factions_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_maps_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_maps_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_maps_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_kick_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_kick_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_kick_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_ban_voteable),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_ban_voteable", ":value"),
          (get_max_players, ":num_players"),
          (try_for_range, ":cur_player", 1, ":num_players"),
            (player_is_active, ":cur_player"),
            (multiplayer_send_int_to_player, ":cur_player", multiplayer_event_return_ban_voteable, ":value"),
          (try_end),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_allow_player_banners),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_allow_player_banners", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_force_default_armor),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_force_default_armor", ":value"),
        (try_end),
      (else_try),
        (eq, ":event_type", multiplayer_event_admin_set_disallow_ranged_weapons),
        (try_begin),
          (store_script_param, ":value", 3),
          #validity check
          (player_is_admin, ":player_no"),
          (is_between, ":value", 0, 2),
          #condition checks are done
          (assign, "$g_multiplayer_disallow_ranged_weapons", ":value"),
        (try_end),
      (else_try),
        ###############
        #CLIENT EVENTS#
        ###############
        (neg|multiplayer_is_dedicated_server),
        (try_begin),      
          (eq, ":event_type", multiplayer_event_return_renaming_server_allowed),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_renaming_server_allowed", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_changing_game_type_allowed),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_changing_game_type_allowed", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_max_num_players),
          (store_script_param, ":value", 3),
          (server_set_max_num_players, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_next_team_faction),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_next_team_1_faction", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_next_team_2_faction", ":value_2"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_num_bots_in_team),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (try_begin),
            (eq, ":value", 1),
            (assign, "$g_multiplayer_num_bots_team_1", ":value_2"),
          (else_try),
            (assign, "$g_multiplayer_num_bots_team_2", ":value_2"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_anti_cheat),
          (store_script_param, ":value", 3),
          (server_set_anti_cheat, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_melee_friendly_fire),
          (store_script_param, ":value", 3),
          (server_set_melee_friendly_fire, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire_damage_self_ratio),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire_damage_self_ratio, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_friendly_fire_damage_friend_ratio),
          (store_script_param, ":value", 3),
          (server_set_friendly_fire_damage_friend_ratio, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_ghost_mode),
          (store_script_param, ":value", 3),
          (server_set_ghost_mode, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_control_block_dir),
          (store_script_param, ":value", 3),
          (server_set_control_block_dir, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_add_to_servers_list),
          (store_script_param, ":value", 3),
          (server_set_add_to_game_servers_list, ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_respawn_period),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_respawn_period", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_max_minutes),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_max_minutes", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_round_max_seconds),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_round_max_seconds", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_player_respawn_as_bot),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_player_respawn_as_bot", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_max_points),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_max_points", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_point_gained_from_flags),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_point_gained_from_flags", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_point_gained_from_capturing_flag),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_point_gained_from_capturing_flag", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_initial_gold_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_initial_gold_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_battle_earnings_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_battle_earnings_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_round_earnings_multiplier),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_round_earnings_multiplier", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_respawn_count),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_number_of_respawn_count", ":value"),          
        (else_try),
          (eq, ":event_type", multiplayer_event_return_server_name),
          (server_set_name, s0),
#        (else_try),
#          (eq, ":event_type", multiplayer_event_return_game_password),
#          (server_set_password, s0),
#          #this is the last option in admin panel, so start the presentation
#          (start_presentation, "prsnt_game_multiplayer_admin_panel"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_open_game_rules),
          #this is the last message for game rules, so start the presentation
          (assign, "$g_multiplayer_show_server_rules", 1),
          (start_presentation, "prsnt_multiplayer_welcome_message"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_game_type),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_game_type", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_valid_vote_ratio),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_valid_vote_ratio", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_max_num_bots),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_max_num_bots", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_server_mission_timer_while_player_joined),
          (store_script_param, ":value", 3),
          (assign, "$server_mission_timer_while_player_joined", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_auto_team_balance_limit),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_auto_team_balance_limit", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_num_bots_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_num_bots_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_factions_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_factions_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_maps_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_maps_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_kick_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_kick_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_ban_voteable),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_ban_voteable", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_allow_player_banners),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_allow_player_banners", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_force_default_armor),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_force_default_armor", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_disallow_ranged_weapons),
          (store_script_param, ":value", 3),
          (assign, "$g_multiplayer_disallow_ranged_weapons", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_confirmation),
          (assign, "$g_confirmation_result", 1),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_rejection),
          (assign, "$g_confirmation_result", -1),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_multiplayer_message),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_show_multiplayer_message", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_draw_this_round),
          (store_script_param, ":value", 3),          
          (call_script, "script_draw_this_round", ":value"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_attached_scene_prop),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_set_attached_scene_prop", ":value", ":value_2"),  
        (else_try),
          (eq, ":event_type", multiplayer_event_set_team_flag_situation),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_set_team_flag_situation", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_team_score),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_team_set_score", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_player_score_kill_death), 
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (store_script_param, ":value_3", 5),
          (store_script_param, ":value_4", 6),
          (call_script, "script_player_set_score", ":value", ":value_2"),
          (call_script, "script_player_set_kill_count", ":value", ":value_3"),
          (call_script, "script_player_set_death_count", ":value", ":value_4"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_num_agents_around_flag),
          (store_script_param, ":flag_no", 3),
          (store_script_param, ":current_owner_code", 4),
          (call_script, "script_set_num_agents_around_flag", ":flag_no", ":current_owner_code"),
        (else_try),
          (eq, ":event_type", multiplayer_event_ask_for_poll),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (store_script_param, ":value_3", 5),
          (store_script_param, ":value_4", 6),
          (assign, ":continue_to_poll", 0),
          (try_begin),
            (this_or_next|eq, ":value", 1),
            (eq, ":value", 2),
            (player_is_active, ":value_2"), #might go offline before here
            (assign, ":continue_to_poll", 1),
          (else_try),
            (assign, ":continue_to_poll", 1),
          (try_end),
          (try_begin),
            (eq, ":continue_to_poll", 1),
            (assign, "$g_multiplayer_poll_to_show", ":value"),
            (assign, "$g_multiplayer_poll_value_to_show", ":value_2"),
            (assign, "$g_multiplayer_poll_value_2_to_show", ":value_3"),
            (assign, "$g_multiplayer_poll_value_3_to_show", ":value_4"),
            (store_mission_timer_a, ":mission_timer"),
            (store_add, "$g_multiplayer_poll_client_end_time", ":mission_timer", 60),
            (start_presentation, "prsnt_multiplayer_poll"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_change_flag_owner),
          (store_script_param, ":flag_no", 3),
          (store_script_param, ":owner_code", 4),
          (call_script, "script_change_flag_owner", ":flag_no", ":owner_code"),
        (else_try),
          (eq, ":event_type", multiplayer_event_use_item),
          (store_script_param, ":value", 3),
          (store_script_param, ":value_2", 4),
          (call_script, "script_use_item", ":value", ":value_2"),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_scene_prop_open_or_close),
          (store_script_param, ":instance_id", 3),       
        
          (scene_prop_set_slot, ":instance_id", scene_prop_open_or_close_slot, 1),

          (prop_instance_get_scene_prop_kind, ":scene_prop_id", ":instance_id"),

          (try_begin),
            (eq, ":scene_prop_id", "spr_winch_b"),
            (assign, ":effected_object", "spr_portcullis"),
          (else_try),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),     
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),     
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),     
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),                             
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),                             
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_b"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_6m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_8m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_10m"),
            (this_or_next|eq, ":scene_prop_id", "spr_siege_ladder_move_12m"),
            (eq, ":scene_prop_id", "spr_siege_ladder_move_14m"),
            (assign, ":effected_object", ":scene_prop_id"),
          (try_end),

          (try_begin),
            (eq, ":effected_object", "spr_portcullis"),

            (assign, ":smallest_dist", -1),
            (prop_instance_get_position, pos0, ":instance_id"),
            (scene_prop_get_num_instances, ":num_instances_of_effected_object", ":effected_object"),     
            (try_for_range, ":cur_instance", 0, ":num_instances_of_effected_object"),
              (scene_prop_get_instance, ":cur_instance_id", ":effected_object", ":cur_instance"),
              (prop_instance_get_position, pos1, ":cur_instance_id"),
              (get_sq_distance_between_positions, ":dist", pos0, pos1),
              (this_or_next|eq, ":smallest_dist", -1),
              (lt, ":dist", ":smallest_dist"),
              (assign, ":smallest_dist", ":dist"),
              (assign, ":effected_object_instance_id", ":cur_instance_id"),
            (try_end),

            (ge, ":smallest_dist", 0),
            (prop_instance_is_animating, ":is_animating", ":effected_object_instance_id"),
            (eq, ":is_animating", 0),

            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),      
            (position_move_z, pos0, 375),
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
          (else_try),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_e_sally_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_sally_door_a"),     
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_left"),     
            (this_or_next|eq, ":scene_prop_id", "spr_earth_sally_gate_right"),     
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_left"),     
            (this_or_next|eq, ":scene_prop_id", "spr_viking_keep_destroy_sally_door_right"),     
            (this_or_next|eq, ":scene_prop_id", "spr_castle_f_door_a"),
            (this_or_next|eq, ":scene_prop_id", "spr_door_destructible"),
            (eq, ":scene_prop_id", "spr_castle_f_door_b"),
            (assign, ":effected_object_instance_id", ":instance_id"),  
            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),
            (position_rotate_z, pos0, -80),
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),
          (else_try),
            (assign, ":effected_object_instance_id", ":instance_id"),
            (prop_instance_is_animating, ":is_animating", ":effected_object_instance_id"),
            (eq, ":is_animating", 0),
            (prop_instance_get_starting_position, pos0, ":effected_object_instance_id"),      
            (prop_instance_animate_to_position, ":effected_object_instance_id", pos0, 1),          
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_set_round_start_time),
          (store_script_param, ":value", 3),

          (try_begin),
            (neq, ":value", -9999),
            (assign, "$g_round_start_time", ":value"),
          (else_try),
            (store_mission_timer_a, "$g_round_start_time"),

            #if round start time is assigning to current time (so new round is starting) then also initialize moveable object slots too.
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_6m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_8m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_10m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_12m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_siege_ladder_move_14m"),
            (call_script, "script_initialize_scene_prop_slots", "spr_winch_b"),         
          (try_end),
#        (else_try),
#          (eq, ":event_type", multiplayer_event_force_start_team_selection),
#          (try_begin),
#            (is_presentation_active, "prsnt_multiplayer_item_select"),
#            (assign, "$g_close_equipment_selection", 1),
#          (try_end),
#          (start_presentation, "prsnt_multiplayer_troop_select"),
        (else_try),     
          (eq, ":event_type", multiplayer_event_start_death_mode),
          (assign, "$g_battle_death_mode_started", 2),
          (start_presentation, "prsnt_multiplayer_flag_projection_display_bt"),
          (call_script, "script_start_death_mode"),
        (else_try),
          (eq, ":event_type", multiplayer_event_return_player_respawn_spent),
          (store_script_param, ":value", 3),
          (try_begin),
            (gt, "$g_my_spawn_count", 0),
            (store_add, "$g_my_spawn_count", "$g_my_spawn_count", ":value"),
          (else_try),
            (assign, "$g_my_spawn_count", ":value"),      
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_duel_request),
          (store_script_param, ":value", 3),
          (try_begin),
            (agent_is_active, ":value"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_s0_offers_a_duel_with_you"),
            (try_begin),
              (get_player_agent_no, ":player_agent"),
              (agent_is_active, ":player_agent"),
              (agent_add_offer_with_timeout, ":player_agent", ":value", 10000), #10 second timeout
            (try_end),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_start_duel),
          (store_script_param, ":value", 3),
          (store_mission_timer_a, ":mission_timer"),
          (try_begin),
            (agent_is_active, ":value"),
            (get_player_agent_no, ":player_agent"),
            (agent_is_active, ":player_agent"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_a_duel_between_you_and_s0_will_start_in_3_seconds"),
            (assign, "$g_multiplayer_duel_start_time", ":mission_timer"),
            (start_presentation, "prsnt_multiplayer_duel_start_counter"),
            (agent_set_slot, ":player_agent", slot_agent_in_duel_with, ":value"),
            (agent_set_slot, ":value", slot_agent_in_duel_with, ":player_agent"),
            (agent_set_slot, ":player_agent", slot_agent_duel_start_time, ":mission_timer"),
            (agent_set_slot, ":value", slot_agent_duel_start_time, ":mission_timer"),
            (agent_clear_relations_with_agents, ":player_agent"),
            (agent_clear_relations_with_agents, ":value"),
##            (agent_add_relation_with_agent, ":player_agent", ":value", -1),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_cancel_duel),
          (store_script_param, ":value", 3),
          (try_begin),
            (agent_is_active, ":value"),
            (agent_get_player_id, ":value_player_no", ":value"),
            (try_begin),
              (player_is_active, ":value_player_no"),
              (str_store_player_username, s0, ":value_player_no"),
            (else_try),
              (str_store_agent_name, s0, ":value"),
            (try_end),
            (display_message, "str_your_duel_with_s0_is_cancelled"),
          (try_end),
          (try_begin),
            (get_player_agent_no, ":player_agent"),
            (agent_is_active, ":player_agent"),
            (agent_set_slot, ":player_agent", slot_agent_in_duel_with, -1),
            (agent_clear_relations_with_agents, ":player_agent"),
          (try_end),
        (else_try),
          (eq, ":event_type", multiplayer_event_show_server_message),
          (display_message, "str_server_s0", 0xFFFF6666),
        (try_end),
     ]),

  # script_cf_multiplayer_evaluate_poll
  # Input: none
  # Output: none (can fail)
  ("cf_multiplayer_evaluate_poll",
   [
     (assign, ":result", 0),
     (assign, "$g_multiplayer_poll_ended", 1),
     (store_add, ":total_votes", "$g_multiplayer_poll_yes_count", "$g_multiplayer_poll_no_count"),
     (store_sub, ":abstain_votes", "$g_multiplayer_poll_num_sent", ":total_votes"),
     (store_mul, ":nos_from_abstains", 3, ":abstain_votes"),
     (val_div, ":nos_from_abstains", 10), #30% of abstains are counted as no
     (val_add, ":total_votes", ":nos_from_abstains"),
     (val_max, ":total_votes", 1), #if someone votes and only 1-3 abstain occurs?
     (store_mul, ":vote_ratio", 100, "$g_multiplayer_poll_yes_count"),
     (val_div, ":vote_ratio", ":total_votes"),
     (try_begin),
       (ge, ":vote_ratio", "$g_multiplayer_valid_vote_ratio"),
       (assign, ":result", 1),
       (try_begin),
         (eq, "$g_multiplayer_poll_to_show", 1), #kick player
         (try_begin),
           (player_is_active, "$g_multiplayer_poll_value_to_show"),
           (kick_player, "$g_multiplayer_poll_value_to_show"),
         (try_end),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 2), #ban player
         (ban_player_using_saved_ban_info), #already loaded at the beginning of the poll
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
         (team_set_faction, 0, "$g_multiplayer_poll_value_2_to_show"),
         (team_set_faction, 1, "$g_multiplayer_poll_value_3_to_show"),
       (else_try),
         (eq, "$g_multiplayer_poll_to_show", 4), #change number of bots
         (assign, "$g_multiplayer_num_bots_team_1", "$g_multiplayer_poll_value_to_show"),
         (assign, "$g_multiplayer_num_bots_team_2", "$g_multiplayer_poll_value_2_to_show"),
         (get_max_players, ":num_players"),                               
         (try_for_range, ":cur_player", 1, ":num_players"),
           (player_is_active, ":cur_player"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
           (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
         (try_end),
       (try_end),
     (else_try),
       (assign, "$g_multiplayer_poll_running", 0), #end immediately if poll fails. but end after some time if poll succeeds (apply the results first)
     (try_end),
     (get_max_players, ":num_players"),
     #for only server itself-----------------------------------------------------------------------------------------------
     (call_script, "script_show_multiplayer_message", multiplayer_message_type_poll_result, ":result"), #0 is useless here
     #for only server itself-----------------------------------------------------------------------------------------------     
     (try_for_range, ":cur_player", 1, ":num_players"),
       (player_is_active, ":cur_player"),
       (multiplayer_send_2_int_to_player, ":cur_player", multiplayer_event_show_multiplayer_message, multiplayer_message_type_poll_result, ":result"),
     (try_end),
     (eq, ":result", 1),
     ]),

  # script_multiplayer_accept_duel
  # Input: arg1 = agent_no, arg2 = agent_no_offerer
  # Output: none
  ("multiplayer_accept_duel",
   [
     (store_script_param, ":agent_no", 1),
     (store_script_param, ":agent_no_offerer", 2),
     (try_begin),
       (agent_slot_ge, ":agent_no", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (agent_get_player_id, ":player_no", ":ex_duelist"),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (try_begin),
       (agent_slot_ge, ":agent_no_offerer", slot_agent_in_duel_with, 0),
       (agent_get_slot, ":ex_duelist", ":agent_no_offerer", slot_agent_in_duel_with),
       (agent_is_active, ":ex_duelist"),
       (agent_clear_relations_with_agents, ":ex_duelist"),
       (agent_set_slot, ":ex_duelist", slot_agent_in_duel_with, -1),
       (try_begin),
         (player_is_active, ":player_no"), #might be AI
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_cancel_duel, ":agent_no_offerer"),
       (else_try),
         (agent_force_rethink, ":ex_duelist"),
       (try_end),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_in_duel_with, ":agent_no_offerer"),
     (agent_set_slot, ":agent_no_offerer", slot_agent_in_duel_with, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no"),
     (agent_clear_relations_with_agents, ":agent_no_offerer"),
##     (agent_add_relation_with_agent, ":agent_no", ":agent_no_offerer", -1),
##     (agent_add_relation_with_agent, ":agent_no_offerer", ":agent_no", -1),
     (agent_get_player_id, ":player_no", ":agent_no"),
     (store_mission_timer_a, ":mission_timer"),
     (try_begin),
       (player_is_active, ":player_no"), #might be AI
       (multiplayer_send_int_to_player, ":player_no", multiplayer_event_start_duel, ":agent_no_offerer"),
     (else_try),
       (agent_force_rethink, ":agent_no"),
     (try_end),
     (agent_set_slot, ":agent_no", slot_agent_duel_start_time, ":mission_timer"),
     (agent_get_player_id, ":agent_no_offerer_player", ":agent_no_offerer"),
     (try_begin),
       (player_is_active, ":agent_no_offerer_player"), #might be AI
       (multiplayer_send_int_to_player, ":agent_no_offerer_player", multiplayer_event_start_duel, ":agent_no"),
     (else_try),
       (agent_force_rethink, ":agent_no_offerer"),
     (try_end),
     (agent_set_slot, ":agent_no_offerer", slot_agent_duel_start_time, ":mission_timer"),
     ]),

  # script_game_get_multiplayer_server_option_for_mission_template
  # Input: arg1 = mission_template_id, arg2 = option_index
  # Output: trigger_result = 1 for option available, 0 for not available
  # reg0 = option_value
  ("game_get_multiplayer_server_option_for_mission_template",
   [
     (store_script_param, ":mission_template_id", 1),
     (store_script_param, ":option_index", 2),
     (try_begin),
       (eq, ":option_index", 0),
       (assign, reg0, "$g_multiplayer_team_1_faction"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 1),
       (assign, reg0, "$g_multiplayer_team_2_faction"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 2),
       (assign, reg0, "$g_multiplayer_num_bots_team_1"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 3),
       (assign, reg0, "$g_multiplayer_num_bots_team_2"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 4),
       (server_get_friendly_fire, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 5),
       (server_get_melee_friendly_fire, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 6),
       (server_get_friendly_fire_damage_self_ratio, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 7),
       (server_get_friendly_fire_damage_friend_ratio, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 8),
       (server_get_ghost_mode, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 9),
       (server_get_control_block_dir, reg0),       
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 10),
       (server_get_combat_speed, reg0),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 11),
       (assign, reg0, "$g_multiplayer_game_max_minutes"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 12),
       (assign, reg0, "$g_multiplayer_round_max_seconds"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 13),
       (assign, reg0, "$g_multiplayer_player_respawn_as_bot"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 14),
       (assign, reg0, "$g_multiplayer_number_of_respawn_count"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 15),
       (assign, reg0, "$g_multiplayer_game_max_points"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 16),
       (assign, reg0, "$g_multiplayer_point_gained_from_flags"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 17),
       (assign, reg0, "$g_multiplayer_point_gained_from_capturing_flag"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 18),
       (assign, reg0, "$g_multiplayer_respawn_period"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 19),
       (assign, reg0, "$g_multiplayer_initial_gold_multiplier"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 20),
       (assign, reg0, "$g_multiplayer_battle_earnings_multiplier"),
       (set_trigger_result, 1),
     (else_try),
       (eq, ":option_index", 21),
       (assign, reg0, "$g_multiplayer_round_earnings_multiplier"),
       (set_trigger_result, 1),
     (try_end),     
     ]),

  # script_game_multiplayer_server_option_for_mission_template_to_string
  # Input: arg1 = mission_template_id, arg2 = option_index, arg3 = option_value
  # Output: s0 = option_text
  ("game_multiplayer_server_option_for_mission_template_to_string",
   [
     (store_script_param, ":mission_template_id", 1),
     (store_script_param, ":option_index", 2),
     (store_script_param, ":option_value", 3),
     (str_clear, s0),
     (try_begin),
       (eq, ":option_index", 0),
       (assign, reg1, 1),
       (str_store_string, s0, "str_team_reg1_faction"),
       (str_store_faction_name, s1, ":option_value"),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 1),
       (assign, reg1, 2),
       (str_store_string, s0, "str_team_reg1_faction"),
       (str_store_faction_name, s1, ":option_value"),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 2),
       (assign, reg1, 1),
       (str_store_string, s0, "str_number_of_bots_in_team_reg1"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 3),
       (assign, reg1, 2),
       (str_store_string, s0, "str_number_of_bots_in_team_reg1"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 4),
       (str_store_string, s0, "str_allow_friendly_fire"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 5),
       (str_store_string, s0, "str_allow_melee_friendly_fire"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 6),
       (str_store_string, s0, "str_friendly_fire_damage_self_ratio"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 7),
       (str_store_string, s0, "str_friendly_fire_damage_friend_ratio"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 8),
       (str_store_string, s0, "str_spectator_camera"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_free"),
       (else_try),
         (eq, ":option_value", 1),
         (str_store_string, s1, "str_stick_to_any_player"),
       (else_try),
         (eq, ":option_value", 2),
         (str_store_string, s1, "str_stick_to_team_members"),
       (else_try),
         (str_store_string, s1, "str_stick_to_team_members_view"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 9),
       (str_store_string, s0, "str_control_block_direction"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_automatic"),
       (else_try),
         (str_store_string, s1, "str_by_mouse_movement"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 10),
       (str_store_string, s0, "str_combat_speed"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_combat_speed_0"),
       (else_try),
         (eq, ":option_value", 1),
         (str_store_string, s1, "str_combat_speed_1"),
       (else_try),
         (eq, ":option_value", 2),
         (str_store_string, s1, "str_combat_speed_2"),
       (else_try),
         (eq, ":option_value", 3),
         (str_store_string, s1, "str_combat_speed_3"),
       (else_try),
         (str_store_string, s1, "str_combat_speed_4"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 11),
       (str_store_string, s0, "str_map_time_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 12),
       (str_store_string, s0, "str_round_time_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 13),
       (str_store_string, s0, "str_players_take_control_of_a_bot_after_death"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_no_wo_dot"),
       (else_try),
         (str_store_string, s1, "str_yes_wo_dot"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 14),
       (str_store_string, s0, "str_defender_spawn_count_limit"),
       (try_begin),
         (eq, ":option_value", 0),
         (str_store_string, s1, "str_unlimited"),
       (else_try),
         (assign, reg1, ":option_value"),
         (str_store_string, s1, "str_reg1"),
       (try_end),
       (str_store_string, s0, "str_s0_s1"),
     (else_try),
       (eq, ":option_index", 15),
       (str_store_string, s0, "str_team_points_limit"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 16),
       (str_store_string, s0, "str_point_gained_from_flags"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 17),
       (str_store_string, s0, "str_point_gained_from_capturing_flag"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 18),
       (str_store_string, s0, "str_respawn_period"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 19),
       (str_store_string, s0, "str_initial_gold_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 20),
       (str_store_string, s0, "str_battle_earnings_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (else_try),
       (eq, ":option_index", 21),
       (str_store_string, s0, "str_round_earnings_multiplier"),
       (assign, reg0, ":option_value"),
       (str_store_string, s0, "str_s0_reg0"),
     (try_end),
     ]),

  # script_find_number_of_agents_constant
  # Input: none
  # Output: reg0 = 100xconstant (100..500)
  ("find_number_of_agents_constant",
   [
     (assign, ":num_dead_or_alive_agents", 0),
     
     (try_for_agents, ":cur_agent"),
       (agent_is_human, ":cur_agent"),
       (val_add, ":num_dead_or_alive_agents", 1),     
     (try_end),

     (try_begin),
       (le, ":num_dead_or_alive_agents", 2), #2
       (assign, reg0, 100),
     (else_try),
       (le, ":num_dead_or_alive_agents", 4), #2+2
       (assign, reg0, 140),
     (else_try),
       (le, ":num_dead_or_alive_agents", 7), #2+2+3
       (assign, reg0, 180),
     (else_try),
       (le, ":num_dead_or_alive_agents", 11), #2+2+3+4
       (assign, reg0, 220),
     (else_try),
       (le, ":num_dead_or_alive_agents", 17), #2+2+3+4+6
       (assign, reg0, 260),
     (else_try),
       (le, ":num_dead_or_alive_agents", 25), #2+2+3+4+6+8
       (assign, reg0, 300),
     (else_try),
       (le, ":num_dead_or_alive_agents", 36), #2+2+3+4+6+8+11
       (assign, reg0, 340),
     (else_try),
       (le, ":num_dead_or_alive_agents", 50), #2+2+3+4+6+8+11+14
       (assign, reg0, 380),
     (else_try),
       (le, ":num_dead_or_alive_agents", 68), #2+2+3+4+6+8+11+14+18
       (assign, reg0, 420),
     (else_try),
       (le, ":num_dead_or_alive_agents", 91), #2+2+3+4+6+8+11+14+18+23
       (assign, reg0, 460),
     (else_try),
       (assign, reg0, 500),
     (try_end),
     ]),

  # script_game_multiplayer_event_duel_offered
  # Input: arg1 = agent_no
  # Output: none
  ("game_multiplayer_event_duel_offered",
   [
     (store_script_param, ":agent_no", 1),
     (get_player_agent_no, ":player_agent_no"),
     (try_begin),
       (agent_is_active, ":player_agent_no"),
       (this_or_next|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, -1),
       (agent_check_offer_from_agent, ":player_agent_no", ":agent_no"),
       (neg|agent_slot_eq, ":player_agent_no", slot_agent_in_duel_with, ":agent_no"), #don't allow spamming duel offers during countdown
       (multiplayer_send_int_to_server, multiplayer_event_offer_duel, ":agent_no"),
       (agent_get_player_id, ":player_no", ":agent_no"),
       (try_begin),
         (player_is_active, ":player_no"),
         (str_store_player_username, s0, ":player_no"),
       (else_try),
         (str_store_agent_name, s0, ":agent_no"),
       (try_end),
       (display_message, "str_a_duel_request_is_sent_to_s0"),
     (try_end),
     ]),
	 
  # script_game_get_multiplayer_game_type_enum
  # Input: none
  # Output: reg0:first type, reg1:type count
  ("game_get_multiplayer_game_type_enum",
   [
     (assign, reg0, multiplayer_game_type_conquest),
	 (assign, reg1, multiplayer_num_game_types),
	 ]),

  # script_game_multiplayer_get_game_type_mission_template
  # Input: arg1 = game_type
  # Output: mission_template 
  ("game_multiplayer_get_game_type_mission_template",
   [
     (assign, reg0, "mt_conquest"),
     ]),

  # script_multiplayer_get_mission_template_game_type
  # Input: arg1 = mission_template_no
  # Output: game_type 
  ("multiplayer_get_mission_template_game_type",
   [
     (assign, reg0, multiplayer_game_type_conquest),
     ]),


  # script_multiplayer_fill_available_factions_combo_button
  # Input: arg1 = overlay_id, arg2 = selected_faction_no, arg3 = opposite_team_selected_faction_no
  # Output: none 
  ("multiplayer_fill_available_factions_combo_button",
   [
     (store_script_param, ":overlay_id", 1),
     (store_script_param, ":selected_faction_no", 2),
##     (store_script_param, ":opposite_team_selected_faction_no", 3),
##     (try_for_range, ":cur_faction", "fac_1", "fac_kingdoms_end"),
##       (try_begin),
##         (eq, ":opposite_team_selected_faction_no", ":cur_faction"),
##         (try_begin),
##           (gt, ":selected_faction_no", ":opposite_team_selected_faction_no"),
##           (val_sub, ":selected_faction_no", 1),
##         (try_end),
##       (else_try),
##         (str_store_faction_name, s0, ":cur_faction"),
##         (overlay_add_item, ":overlay_id", s0),
##       (try_end),
##     (try_end),
##     (val_sub, ":selected_faction_no", "fac_1"),
##     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     (try_for_range, ":cur_faction", multiplayer_factions_begin, multiplayer_factions_end),
       (str_store_faction_name, s0, ":cur_faction"),
       (overlay_add_item, ":overlay_id", s0),
     (try_end),
     (val_sub, ":selected_faction_no", "fac_1"),
     (overlay_set_val, ":overlay_id", ":selected_faction_no"),
     ]),
  

  # script_multiplayer_get_troop_class
  # Input: arg1 = troop_no
  # Output: reg0: troop_class 
  ("multiplayer_get_troop_class",
   [
     (store_script_param_1, ":troop_no"),
     (assign, ":troop_class", multi_troop_class_other),
     (try_begin),
       (this_or_next|eq, ":troop_no", "trp_recruit"),
       (eq, ":troop_no", "trp_infantry"),
       (assign, ":troop_class", multi_troop_class_infantry),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_horseman"),
       (this_or_next|eq, ":troop_no", "trp_cavalry"),
       (eq, ":troop_no", "trp_boss"),
       (assign, ":troop_class", multi_troop_class_cavalry),
     (else_try),
       (eq, ":troop_no", "trp_engineer"),
       (assign, ":troop_class", multi_troop_class_engineer),
     (else_try),
       (eq, ":troop_no", "trp_navy"),
       (assign, ":troop_class", multi_troop_class_sailor),
     (else_try),
       (eq, ":troop_no", "trp_farmer"),
       (assign, ":troop_class", multi_troop_class_civilian),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_driver"),
       (this_or_next|eq, ":troop_no", "trp_police"),
       (this_or_next|eq, ":troop_no", "trp_city_inspector"),
       (eq, ":troop_no", "trp_pilot"),
       (assign, ":troop_class", multi_troop_class_driver),
     (else_try),
       (this_or_next|eq, ":troop_no", "trp_supporter"),
       (this_or_next|eq, ":troop_no", "trp_signalman"),
       (this_or_next|eq, ":troop_no", "trp_medic"),
       (eq, ":troop_no", "trp_artillerist"),
       (assign, ":troop_class", multi_troop_class_supporter),
     (try_end),
     (assign, reg0, ":troop_class"),
     ]),

  #script_multiplayer_clear_player_selected_items
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_clear_player_selected_items",
   [
     (store_script_param, ":player_no", 1),
     (try_for_range, ":slot_no", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_set_slot, ":player_no", ":slot_no", -1),
     (try_end),
     ]),
  

  #script_multiplayer_init_player_slots
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_init_player_slots",
   [
     (store_script_param, ":player_no", 1),
     (call_script, "script_multiplayer_clear_player_selected_items", ":player_no"),
     (player_set_slot, ":player_no", slot_player_spawned_this_round, 0),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (player_set_slot, ":player_no", slot_player_poll_disabled_until_time, 0),

     (player_set_slot, ":player_no", slot_player_bot_type_1_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_2_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_3_wanted, 0),
     (player_set_slot, ":player_no", slot_player_bot_type_4_wanted, 0),
     ]),

  #script_multiplayer_initialize_belfry_wheel_rotations
  # Input: none
  # Output: none
  ("multiplayer_initialize_belfry_wheel_rotations",
   [
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_a"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_mul, ":wheel_no", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),   
##    (try_end),
##
##    (scene_prop_get_num_instances, ":num_belfries_a", "spr_belfry_a"),
##
##    (scene_prop_get_num_instances, ":num_belfries", "spr_belfry_b"),
##    (try_for_range, ":belfry_no", 0, ":num_belfries"),
##      (store_add, ":wheel_no_plus_num_belfries_a", ":wheel_no", ":num_belfries_a"),
##      (store_mul, ":wheel_no_plus_num_belfries_a", ":belfry_no", 3),
##      (scene_prop_get_instance, ":belfry_wheel_1_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_1_scene_prop_id"),
##      #belfry wheel_2
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_2_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_2_scene_prop_id"),
##      #belfry wheel_3
##      (val_add, ":wheel_no_plus_num_belfries_a", 1),
##      (scene_prop_get_instance, ":belfry_wheel_3_scene_prop_id", "spr_belfry_wheel", ":wheel_no_plus_num_belfries_a"),
##      (prop_instance_initialize_rotation_angles, ":belfry_wheel_3_scene_prop_id"),   
##    (try_end),

      (scene_prop_get_num_instances, ":num_wheel", "spr_belfry_wheel"),
      (try_for_range, ":wheel_no", 0, ":num_wheel"),
        (scene_prop_get_instance, ":wheel_id", "spr_belfry_wheel", ":wheel_no"),
        (prop_instance_initialize_rotation_angles, ":wheel_id"),   
      (try_end),

      (scene_prop_get_num_instances, ":num_winch", "spr_winch"),
      (try_for_range, ":winch_no", 0, ":num_winch"),
        (scene_prop_get_instance, ":winch_id", "spr_winch", ":winch_no"),
        (prop_instance_initialize_rotation_angles, ":winch_id"),   
      (try_end),

      (scene_prop_get_num_instances, ":num_winch_b", "spr_winch_b"),
      (try_for_range, ":winch_b_no", 0, ":num_winch_b"),
        (scene_prop_get_instance, ":winch_b_id", "spr_winch_b", ":winch_b_no"),
        (prop_instance_initialize_rotation_angles, ":winch_b_id"),   
      (try_end),
     ]),

  #script_send_open_close_information_of_object
  # Input: arg1 = mission_object_id
  # Output: none
  ("send_open_close_information_of_object",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":scene_prop_no", 2),
     
     (scene_prop_get_num_instances, ":num_instances", ":scene_prop_no"),

     (try_for_range, ":instance_no", 0, ":num_instances"),
       (scene_prop_get_instance, ":instance_id", ":scene_prop_no", ":instance_no"),
       (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),
       (try_begin),
         (eq, ":opened_or_closed", 1),
         (multiplayer_send_int_to_player, ":player_no", multiplayer_event_set_scene_prop_open_or_close, ":instance_id"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_send_initial_information
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_send_initial_information",
   [
     (store_script_param, ":player_no", 1),
          
     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 1, "$g_multiplayer_num_bots_team_1"),
     (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_return_num_bots_in_team, 2, "$g_multiplayer_num_bots_team_2"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_auto_team_balance_limit, "$g_multiplayer_auto_team_balance_limit"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_num_bots_voteable, "$g_multiplayer_num_bots_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_factions_voteable, "$g_multiplayer_factions_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_maps_voteable, "$g_multiplayer_maps_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_kick_voteable, "$g_multiplayer_kick_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_ban_voteable, "$g_multiplayer_ban_voteable"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_allow_player_banners, "$g_multiplayer_allow_player_banners"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_force_default_armor, "$g_multiplayer_force_default_armor"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_disallow_ranged_weapons, "$g_multiplayer_disallow_ranged_weapons"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_respawn_period, "$g_multiplayer_respawn_period"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_round_max_seconds, "$g_multiplayer_round_max_seconds"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_game_type, "$g_multiplayer_game_type"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_player_respawn_as_bot, "$g_multiplayer_player_respawn_as_bot"),
     
     (store_mission_timer_a, ":mission_timer"),
     (multiplayer_send_int_to_player, ":player_no", multiplayer_event_return_server_mission_timer_while_player_joined, ":mission_timer"),

     (try_for_agents, ":cur_agent"), #send if any agent is carrying any scene object
       (agent_is_human, ":cur_agent"),
       (agent_get_attached_scene_prop, ":attached_scene_prop", ":cur_agent"),
       (ge, ":attached_scene_prop", 0),
       (multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_attached_scene_prop, ":cur_agent", ":attached_scene_prop"),
     (try_end),

     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_6m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_8m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_10m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_12m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_siege_ladder_move_14m"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_winch_b"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_e_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_sally_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_left"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_earth_sally_gate_right"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_left"),     
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_viking_keep_destroy_sally_door_right"),     
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_a"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_door_destructible"),
     (call_script, "script_send_open_close_information_of_object", ":player_no", "spr_castle_f_door_b"),

     #(multiplayer_send_2_int_to_player, ":player_no", multiplayer_event_set_day_time, "$g_round_day_time"),
    ]),


  #script_multiplayer_remove_destroy_mod_targets
  # Input: none
  # Output: none
  ("multiplayer_remove_destroy_mod_targets",
   [
       (replace_scene_props, "spr_catapult_destructible", "spr_empty"),
       (replace_scene_props, "spr_trebuchet_destructible", "spr_empty"),
     ]),
  
  #script_multiplayer_init_mission_variables
  ("multiplayer_init_mission_variables",
   [
     (assign, "$g_multiplayer_team_1_first_spawn", 1),
     (assign, "$g_multiplayer_team_2_first_spawn", 1),
     (assign, "$g_multiplayer_poll_running", 0),
##     (assign, "$g_multiplayer_show_poll_when_suitable", 0),
     (assign, "$g_waiting_for_confirmation_to_terminate", 0),
     (assign, "$g_confirmation_result", 0),
     (assign, "$g_team_balance_next_round", 0),
     (team_get_faction, "$g_multiplayer_team_1_faction", 0),
     (team_get_faction, "$g_multiplayer_team_2_faction", 1),
     (assign, "$g_multiplayer_next_team_1_faction", "$g_multiplayer_team_1_faction"),
     (assign, "$g_multiplayer_next_team_2_faction", "$g_multiplayer_team_2_faction"),

     (assign, "$g_multiplayer_bot_type_1_wanted", 0),
     (assign, "$g_multiplayer_bot_type_2_wanted", 0),
     (assign, "$g_multiplayer_bot_type_3_wanted", 0),
     (assign, "$g_multiplayer_bot_type_4_wanted", 0),

#     (call_script, "script_music_set_situation_with_culture", mtf_sit_multiplayer_fight),
     ]),

  #script_multiplayer_event_mission_end
  # Input: none
  # Output: none
  ("multiplayer_event_mission_end",
   [
     #EVERY_BREATH_YOU_TAKE achievement
     (try_begin),
       (multiplayer_get_my_player, ":my_player_no"),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_kill_count, ":kill_count", ":my_player_no"),
       (player_get_death_count, ":death_count", ":my_player_no"),
       (gt, ":kill_count", ":death_count"),
       (unlock_achievement, ACHIEVEMENT_EVERY_BREATH_YOU_TAKE),
     (try_end),
     #EVERY_BREATH_YOU_TAKE achievement end
     ]),
  

  #script_multiplayer_event_agent_killed_or_wounded
  # Input: arg1 = dead_agent_no, arg2 = killer_agent_no
  # Output: none
  ("multiplayer_event_agent_killed_or_wounded",
   [
     (store_script_param, ":dead_agent_no", 1),
     (store_script_param, ":killer_agent_no", 2),
     
     (multiplayer_get_my_player, ":my_player_no"),
     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":my_player_agent", ":my_player_no"),
       (ge, ":my_player_agent", 0),
       (try_begin),
         (eq, ":my_player_agent", ":dead_agent_no"),
         (store_mission_timer_a, "$g_multiplayer_respawn_start_time"),
       (try_end),
       (try_begin),
         (eq, ":my_player_agent", ":killer_agent_no"),
         (neq, ":my_player_agent", ":dead_agent_no"),
         (agent_is_human, ":dead_agent_no"),
         (agent_is_alive, ":my_player_agent"),
         (neg|agent_is_ally, ":dead_agent_no"),
         (agent_get_horse, ":my_horse_agent", ":my_player_agent"),
         (agent_get_wielded_item, ":my_wielded_item", ":my_player_agent", 0),
         (assign, ":my_item_class", -1),
         (try_begin),
           (ge, ":my_wielded_item", 0),
           (item_get_slot, ":my_item_class", ":my_wielded_item", slot_item_multiplayer_item_class),
         (try_end),
         #SPOIL_THE_CHARGE achievement
         (try_begin),
           (lt, ":my_horse_agent", 0),
           (agent_get_horse, ":dead_agent_horse_agent", ":dead_agent_no"),
           (ge, ":dead_agent_horse_agent", 0),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SPOIL_THE_CHARGE, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SPOIL_THE_CHARGE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_SPOIL_THE_CHARGE),
         (try_end),
         #SPOIL_THE_CHARGE achievement end
         #HARASSING_HORSEMAN achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_bow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_crossbow),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_HARASSING_HORSEMAN, 0),
           (lt, ":achievement_stat", 100),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_HARASSING_HORSEMAN, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 100),
           (unlock_achievement, ACHIEVEMENT_HARASSING_HORSEMAN),
         (try_end),
         #HARASSING_HORSEMAN achievement end
         #THROWING_STAR achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_throwing),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THROWING_STAR, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THROWING_STAR, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_THROWING_STAR),
         (try_end),
         #THROWING_STAR achievement end
         #SHISH_KEBAB achievement
         (try_begin),
           (ge, ":my_horse_agent", 0),
           (eq, ":my_item_class", multi_item_class_type_lance),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_SHISH_KEBAB, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_SHISH_KEBAB, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_SHISH_KEBAB),
         (try_end),
         #SHISH_KEBAB achievement end
         #CHOPPY_CHOP_CHOP achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_axe),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_cleavers),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_sword),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_two_handed_axe),
           (this_or_next|eq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (eq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_CHOPPY_CHOP_CHOP, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_CHOPPY_CHOP_CHOP),
         (try_end),
         #CHOPPY_CHOP_CHOP achievement end
         #MACE_IN_YER_FACE achievement
         (try_begin),
           (this_or_next|eq, ":my_item_class", multi_item_class_type_blunt),
           (eq, ":my_wielded_item", "itm_sarranid_two_handed_mace_1"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_b"), #sarranid item exception
           (neq, ":my_wielded_item", "itm_sarranid_axe_a"), #sarranid item exception
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_MACE_IN_YER_FACE, 0),
           (lt, ":achievement_stat", 25),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_MACE_IN_YER_FACE, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 25),
           (unlock_achievement, ACHIEVEMENT_MACE_IN_YER_FACE),
         (try_end),
         #MACE_IN_YER_FACE achievement end
         #THE_HUSCARL achievement
         (try_begin),
           (eq, ":my_item_class", multi_item_class_type_throwing_axe),
           (get_achievement_stat, ":achievement_stat", ACHIEVEMENT_THE_HUSCARL, 0),
           (lt, ":achievement_stat", 50),
           (val_add, ":achievement_stat", 1),
           (set_achievement_stat, ACHIEVEMENT_THE_HUSCARL, 0, ":achievement_stat"),
           (ge, ":achievement_stat", 50),
           (unlock_achievement, ACHIEVEMENT_THE_HUSCARL),
         (try_end),
         #THE_HUSCARL achievement end
       (try_end),
     (try_end),

     (try_begin),
       (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
       (player_get_agent_id, ":player_agent", ":my_player_no"),
       (eq, ":dead_agent_no", ":player_agent"),
     
       (assign, ":show_respawn_counter", 0),
       (try_begin),        
         (eq, "$g_multiplayer_player_respawn_as_bot", 1),
         (player_get_team_no, ":my_player_team", ":my_player_no"),
         (assign, ":is_found", 0),
         (try_for_agents, ":cur_agent"),
           (eq, ":is_found", 0),
           (agent_is_alive, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_get_team ,":cur_team", ":cur_agent"),
           (eq, ":cur_team", ":my_player_team"),
           (assign, ":is_found", 1),
         (try_end),
         (eq, ":is_found", 1),
         (assign, ":show_respawn_counter", 1),
       (try_end),
       
       (try_begin),
         (assign, "$g_show_no_more_respawns_remained", 0),
       (try_end),

       (eq, ":show_respawn_counter", 1),             

       (start_presentation, "prsnt_multiplayer_respawn_time_counter"),
     (try_end),
     ]),
     
  #script_multiplayer_get_item_value_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: item_value
  ("multiplayer_get_item_value_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (try_begin),
       (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":item_no", ":troop_no"),
       (assign, ":item_value", 0),
     (else_try),
       (store_item_value, ":item_value", ":item_no"),
       (store_troop_faction, ":faction_no", ":troop_no"),
       (store_sub, ":faction_slot", ":faction_no", multiplayer_factions_begin),
       (val_add, ":faction_slot", slot_item_multiplayer_faction_price_multipliers_begin),
       (item_get_slot, ":price_multiplier", ":item_no", ":faction_slot"),
       (val_mul, ":item_value", ":price_multiplier"),
       (val_div, ":item_value", 100),
     (try_end),
     (assign, reg0, ":item_value"),
     ]),

  #script_multiplayer_get_previous_item_for_item_and_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: previous_item_no (-1 if it is the root item, 0 if the item is invalid) 
  ("multiplayer_get_previous_item_for_item_and_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
     (call_script, "script_multiplayer_get_item_value_for_troop", ":item_no", ":troop_no"),
     (assign, ":item_value", reg0),
     (store_sub, ":troop_index", ":troop_no", multiplayer_troops_begin),
     (val_add, ":troop_index", slot_item_multiplayer_availability_linked_list_begin),
     (assign, ":max_item_no", -1),
     (assign, ":max_item_value", -1),
     (try_for_range, ":i_item", all_items_begin, all_items_end),
       (item_slot_eq, ":i_item", slot_item_multiplayer_item_class, ":item_class"),
       (item_slot_ge, ":i_item", ":troop_index", 1),
       (call_script, "script_multiplayer_get_item_value_for_troop", ":i_item", ":troop_no"),
       (assign, ":i_item_value", reg0),
       (try_begin),
         (eq, ":i_item_value", 0),
         (eq, ":max_item_value", 0),
         #choose between 2 default items
         (store_item_value, ":i_item_real_value", ":i_item"),
         (store_item_value, ":max_item_real_value", ":max_item_no"),
         (try_begin),
           (gt, ":i_item_real_value", ":max_item_real_value"),
           (assign, ":max_item_value", ":i_item_value"),
           (assign, ":max_item_no", ":i_item"),
         (try_end),
       (else_try),
         (gt, ":i_item_value", ":max_item_value"),
         (lt, ":i_item_value", ":item_value"),
         (assign, ":max_item_value", ":i_item_value"),
         (assign, ":max_item_no", ":i_item"),
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":max_item_no", -1),
       (assign, ":item_upper_class", -1),
       (try_begin),
         (is_between, ":item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
         (assign, ":item_upper_class", 0),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_shields_begin, multi_item_class_type_shields_end),
         (assign, ":item_upper_class", 1),
       (else_try),
         (eq, ":item_class", multi_item_class_type_bow),
         (assign, ":item_upper_class", 2),
       (else_try),
         (eq, ":item_class", multi_item_class_type_crossbow),
         (assign, ":item_upper_class", 3),
       (else_try),
         (eq, ":item_class", multi_item_class_type_arrow),
         (assign, ":item_upper_class", 4),
       (else_try),
         (eq, ":item_class", multi_item_class_type_bolt),
         (assign, ":item_upper_class", 5),
       (else_try),
         (eq, ":item_class", multi_item_class_type_throwing),
         (assign, ":item_upper_class", 6),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
         (assign, ":item_upper_class", 7),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
         (assign, ":item_upper_class", 8),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
         (assign, ":item_upper_class", 9),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
         (assign, ":item_upper_class", 10),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
         (assign, ":item_upper_class", 11),
       (try_end),
       (neq, ":item_upper_class", 0),
       #search for the default item for non-weapon classes (only 1 slot is easy to fill)
       (assign, ":end_cond", all_items_end),
       (try_for_range, ":i_item", all_items_begin, ":end_cond"),
         (item_slot_ge, ":i_item", ":troop_index", 1),
         (item_get_slot, ":i_item_class", ":i_item", slot_item_multiplayer_item_class),
         (try_begin),
           (is_between, ":i_item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
           (assign, ":i_item_upper_class", 0),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_shields_begin, multi_item_class_type_shields_end),
           (assign, ":i_item_upper_class", 1),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_bow),
           (assign, ":i_item_upper_class", 2),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_crossbow),
           (assign, ":i_item_upper_class", 3),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_arrow),
           (assign, ":i_item_upper_class", 4),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_bolt),
           (assign, ":i_item_upper_class", 5),
         (else_try),
           (eq, ":i_item_class", multi_item_class_type_throwing),
           (assign, ":i_item_upper_class", 6),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
           (assign, ":i_item_upper_class", 7),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
           (assign, ":i_item_upper_class", 8),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
           (assign, ":i_item_upper_class", 9),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
           (assign, ":i_item_upper_class", 10),
         (else_try),
           (is_between, ":i_item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
           (assign, ":i_item_upper_class", 11),
         (try_end),
         (eq, ":i_item_upper_class", ":item_upper_class"),
         (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_item", ":troop_no"),
         (assign, ":max_item_no", ":i_item"),
         (assign, ":end_cond", 0), #break
       (try_end),
     (try_end),
     (assign, reg0, ":max_item_no"),
     ]),

  #script_cf_multiplayer_is_item_default_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: reg0: total_cost
  ("cf_multiplayer_is_item_default_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (assign, ":default_item", 0),
     (try_begin),
       (is_between, ":item_no", horses_begin, horses_end),
#       (neq, ":item_no", "itm_warhorse_sarranid"),
#       (neq, ":item_no", "itm_warhorse_steppe"),

       (troop_get_inventory_capacity, ":end_cond", ":troop_no"), #troop no can come -1 here error occured at friday
       (try_for_range, ":i_slot", 0, ":end_cond"),
         (troop_get_inventory_slot, ":default_item_id", ":troop_no", ":i_slot"),
         (eq, ":item_no", ":default_item_id"),
         (assign, ":default_item", 1),
         (assign, ":end_cond", 0), #break
       (try_end),
     (try_end),
     (eq, ":default_item", 1),
     ]),
  
  #script_multiplayer_calculate_cur_selected_items_cost
  # Input: arg1 = player_no
  # Output: reg0: total_cost
  ("multiplayer_calculate_cur_selected_items_cost",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":calculation_type", 2), #0 for normal calculation
     (assign, ":total_cost", 0),
     (player_get_troop_id, ":troop_no", ":player_no"),

     (try_begin),
       (eq, ":calculation_type", 0),
       (assign, ":begin_cond", slot_player_cur_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_cur_selected_item_indices_end),
     (else_try),
       (assign, ":begin_cond", slot_player_selected_item_indices_begin),
       (assign, ":end_cond", slot_player_selected_item_indices_end),
     (try_end),
     
     (try_for_range, ":i_item", ":begin_cond", ":end_cond"),
       (player_get_slot, ":item_id", ":player_no", ":i_item"),
       (ge, ":item_id", 0), #might be -1 for horses etc.
       (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":troop_no"),
       (val_add, ":total_cost", reg0),
     (try_end),
     (assign, reg0, ":total_cost"),
     ]),

  #script_multiplayer_set_item_available_for_troop
  # Input: arg1 = item_no, arg2 = troop_no
  # Output: none
  ("multiplayer_set_item_available_for_troop",
   [
     (store_script_param, ":item_no", 1),
     (store_script_param, ":troop_no", 2),
     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),
     (item_set_slot, ":item_no", ":item_troop_slot", 1),
     ]),

  #script_multiplayer_send_item_selections
  # Input: none
  # Output: none
  ("multiplayer_send_item_selections",
   [
     (multiplayer_get_my_player, ":my_player_no"),
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":item_id", ":my_player_no", ":i_item"),
       (multiplayer_send_2_int_to_server, multiplayer_event_set_item_selection, ":i_item", ":item_id"),
     (try_end),
     ]),

  #script_multiplayer_set_default_item_selections_for_troop
  # Input: arg1 = troop_no
  # Output: none
  ("multiplayer_set_default_item_selections_for_troop",
   [
     (store_script_param, ":troop_no", 1),
     (multiplayer_get_my_player, ":my_player_no"),
     (call_script, "script_multiplayer_clear_player_selected_items", ":my_player_no"),
     (assign, ":cur_weapon_slot", 0),
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
       (troop_get_inventory_slot, ":item_id", ":troop_no", ":i_slot"),
       (ge, ":item_id", 0),
       (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
       (try_begin),
         (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
         (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
         (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, ":cur_weapon_slot"),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
         (val_add, ":cur_weapon_slot", 1),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_heads_begin, multi_item_class_type_heads_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 4),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_bodies_begin, multi_item_class_type_bodies_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 5),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_feet_begin, multi_item_class_type_feet_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 6),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_gloves_begin, multi_item_class_type_gloves_end),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 7),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (else_try),
         (is_between, ":item_class", multi_item_class_type_horses_begin, multi_item_class_type_horses_end),
         (eq, "$g_horses_are_avaliable", 1),
         (store_add, ":selected_item_slot", slot_player_selected_item_indices_begin, 8),
         (player_set_slot, ":my_player_no", ":selected_item_slot", ":item_id"),
       (try_end),
     (try_end),
     ]),

  #script_multiplayer_display_available_items_for_troop_and_item_classes
  # Input: arg1 = troop_no, arg2 = item_classes_begin, arg3 = item_classes_end, arg4 = pos_x_begin, arg5 = pos_y_begin
  # Output: none
  ("multiplayer_display_available_items_for_troop_and_item_classes",
   [
     (store_script_param, ":troop_no", 1),
     (store_script_param, ":item_classes_begin", 2),
     (store_script_param, ":item_classes_end", 3),
     (store_script_param, ":pos_x_begin", 4),
     (store_script_param, ":pos_y_begin", 5),

     (assign, ":x_adder", 100),
     (try_begin),
       (gt, ":pos_x_begin", 500),
       (assign, ":x_adder", -100),
     (try_end),

     (store_sub, ":item_troop_slot", ":troop_no", multiplayer_troops_begin),
     (val_add, ":item_troop_slot", slot_item_multiplayer_availability_linked_list_begin),

     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, multi_data_item_button_indices_end),
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot", -1),
     (try_end),

     (assign, ":num_available_items", 0),
     
     (try_for_range, ":item_no", all_items_begin, all_items_end),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (is_between, ":item_class", ":item_classes_begin", ":item_classes_end"),
       (this_or_next|eq, "$g_multiplayer_disallow_ranged_weapons", 0),
       (neg|is_between, ":item_class", multi_item_class_type_ranged_weapons_begin, multi_item_class_type_ranged_weapons_end),
       (item_slot_ge, ":item_no", ":item_troop_slot", 1),
       (store_add, ":cur_slot_index", ":num_available_items", multi_data_item_button_indices_begin),
       #using the result array for item_ids
       (troop_set_slot, "trp_multiplayer_data", ":cur_slot_index", ":item_no"),
       (val_add, ":num_available_items", 1),
     (try_end),

     #sorting
     (store_add, ":item_slots_end", ":num_available_items", multi_data_item_button_indices_begin),
     (store_sub, ":item_slots_end_minus_one", ":item_slots_end", 1),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end_minus_one"),
       (store_add, ":cur_slot_2_begin", ":cur_slot", 1),
       (try_for_range, ":cur_slot_2", ":cur_slot_2_begin", ":item_slots_end"),
         (troop_get_slot, ":item_1", "trp_multiplayer_data", ":cur_slot"),
         (troop_get_slot, ":item_2", "trp_multiplayer_data", ":cur_slot_2"),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_1", ":troop_no"),
         (assign, ":item_1_point", reg0),
         (call_script, "script_multiplayer_get_item_value_for_troop", ":item_2", ":troop_no"),
         (assign, ":item_2_point", reg0),
         (item_get_slot, ":item_1_class", ":item_1", slot_item_multiplayer_item_class),
         (item_get_slot, ":item_2_class", ":item_2", slot_item_multiplayer_item_class),
         (val_mul, ":item_1_class", 1000000), #assuming maximum item price is 1000000
         (val_mul, ":item_2_class", 1000000), #assuming maximum item price is 1000000
         (val_add, ":item_1_point", ":item_1_class"),
         (val_add, ":item_2_point", ":item_2_class"),
         (lt, ":item_2_point", ":item_1_point"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot", ":item_2"),
         (troop_set_slot, "trp_multiplayer_data", ":cur_slot_2", ":item_1"),
       (try_end),
     (try_end),

     (troop_get_slot, ":last_item_no", "trp_multiplayer_data", multi_data_item_button_indices_begin),
     (assign, ":num_item_classes", 0),
     (try_begin),
       (ge, ":last_item_no", 0),
       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),

       (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
         (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
         (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
         (neq, ":item_class", ":last_item_class"),
         (val_add, ":num_item_classes", 1),
         (assign, ":last_item_class", ":item_class"),
       (try_end),

       (try_begin),
         (store_mul, ":required_y", ":num_item_classes", 100),
         (gt, ":required_y", ":pos_y_begin"),
         (store_sub, ":dif", ":required_y", ":pos_y_begin"),
         (val_div, ":dif", 100),
         (val_add, ":dif", 1),
         (val_mul, ":dif", 100),
         (val_add, ":pos_y_begin", ":dif"),
       (try_end),

       (item_get_slot, ":last_item_class", ":last_item_no", slot_item_multiplayer_item_class),
     (try_end),
     (assign, ":cur_x", ":pos_x_begin"),
     (assign, ":cur_y", ":pos_y_begin"),
     (try_for_range, ":cur_slot", multi_data_item_button_indices_begin, ":item_slots_end"),
       (troop_get_slot, ":item_no", "trp_multiplayer_data", ":cur_slot"),
       (item_get_slot, ":item_class", ":item_no", slot_item_multiplayer_item_class),
       (try_begin),
         (neq, ":item_class", ":last_item_class"),
         (val_sub, ":cur_y", 100),
         (assign, ":cur_x", ":pos_x_begin"),
         (assign, ":last_item_class", ":item_class"),
       (try_end),
       (create_image_button_overlay, ":cur_obj", "mesh_mp_inventory_choose", "mesh_mp_inventory_choose"),
       (position_set_x, pos1, 800),
       (position_set_y, pos1, 800),
       (overlay_set_size, ":cur_obj", pos1),
       (position_set_x, pos1, ":cur_x"),
       (position_set_y, pos1, ":cur_y"),
       (overlay_set_position, ":cur_obj", pos1),
       (create_mesh_overlay_with_item_id, reg0, ":item_no"),
       (store_add, ":item_x", ":cur_x", 50),
       (store_add, ":item_y", ":cur_y", 50),
       (position_set_x, pos1, ":item_x"),
       (position_set_y, pos1, ":item_y"),
       (overlay_set_position, reg0, pos1),
       (val_add, ":cur_x", ":x_adder"),
     (try_end),
     ]),

  # script_multiplayer_fill_map_game_types
  # Input: game_type
  # Output: num_maps
  ("multiplayer_fill_map_game_types",
    [
      (store_script_param, ":game_type", 1),
      (try_for_range, ":i_multi", multi_data_maps_for_game_type_begin, multi_data_maps_for_game_type_end),
        (troop_set_slot, "trp_multiplayer_data", ":i_multi", -1),
      (try_end),
      (assign, ":num_maps", 0),
      (assign, reg0, ":num_maps"),
      ]),

  
  # script_multiplayer_count_players_bots
  # Input: none
  # Output: none
  ("multiplayer_count_players_bots",
    [
      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (player_is_active, ":cur_player"),
        (player_set_slot, ":cur_player", slot_player_last_bot_count, 0),
      (try_end),

      (try_for_agents, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_get_player_id, ":agent_player", ":cur_agent"),
        (lt, ":agent_player", 0), #not a player
        (agent_get_group, ":agent_group", ":cur_agent"),
        (player_is_active, ":agent_group"),
        (player_get_slot, ":bot_count", ":agent_group", slot_player_last_bot_count),
        (val_add, ":bot_count", 1),
        (player_set_slot, ":agent_group", slot_player_last_bot_count, ":bot_count"),
      (try_end),
      ]),

  # script_multiplayer_find_player_leader_for_bot
  # Input: arg1 = team_no
  # Output: reg0 = player_no
  ("multiplayer_find_player_leader_for_bot",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (team_get_faction, ":team_faction", ":team_no"),
      (assign, ":num_ai_troops", 0),
      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
        (eq, ":ai_troop_faction", ":team_faction"),
        (val_add, ":num_ai_troops", 1),
      (try_end),

      (call_script, "script_multiplayer_count_players_bots"),

      (assign, ":team_player_count", 0),

      (get_max_players, ":num_players"),
      (try_for_range, ":cur_player", 0, ":num_players"),
        (assign, ":continue", 0),
        (player_is_active, ":cur_player"),          
        (try_begin),
          (eq, ":look_only_actives", 0),
          (assign, ":continue", 1),
        (else_try),
          (neq, ":look_only_actives", 0),
          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),
          (assign, ":continue", 1),
        (try_end),

        (eq, ":continue", 1),
      
        (player_get_team_no, ":player_team", ":cur_player"),
        (eq, ":team_no", ":player_team"),
        (val_add, ":team_player_count", 1),
      (try_end),
      (assign, ":result_leader", -1),
      (try_begin),      
        (gt, ":team_player_count", 0),
        (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_1"),
        (try_begin),
          (eq, ":team_no", 1),
          (assign, ":total_bot_count", "$g_multiplayer_num_bots_team_2"),
        (try_end),
        (store_div, ":num_bots_for_each_player", ":total_bot_count", ":team_player_count"),
        (store_mul, ":check_remainder", ":num_bots_for_each_player", ":team_player_count"),
        (try_begin),
          (lt, ":check_remainder", ":total_bot_count"),
          (val_add, ":num_bots_for_each_player", 1),
        (try_end),
      
        (assign, ":total_bot_req", 0),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),
      
          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_add, ":total_bot_req", ":num_bots_for_each_player"),
          (val_sub, ":total_bot_req", ":player_bot_count"),
        (try_end),
        (gt, ":total_bot_req", 0),
      
        (store_random_in_range, ":random_bot", 0, ":total_bot_req"),
        (try_for_range, ":cur_player", 0, ":num_players"),
          (player_is_active, ":cur_player"),

          (player_get_agent_id, ":cur_agent", ":cur_player"),
          (ge, ":cur_agent", 0),
          (agent_is_alive, ":cur_agent"),

          (player_get_team_no, ":player_team", ":cur_player"),
          (eq, ":team_no", ":player_team"),
          (assign, ":ai_wanted", 0),
          (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
          (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
            (player_slot_ge, ":cur_player", ":bot_type_wanted_slot", 1),
            (assign, ":ai_wanted", 1),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":ai_wanted", 1),
          (player_get_slot, ":player_bot_count", ":cur_player", slot_player_last_bot_count),
          (lt, ":player_bot_count", ":num_bots_for_each_player"),
          (val_sub, ":random_bot", ":num_bots_for_each_player"),
          (val_add, ":random_bot", ":player_bot_count"),
          (lt, ":random_bot", 0),
          (assign, ":result_leader", ":cur_player"),
          (assign, ":num_players", 0), #break
        (try_end),
      (try_end),
      (assign, reg0, ":result_leader"),
      ]),

  # script_multiplayer_find_bot_troop_and_group_for_spawn
  # Input: arg1 = team_no
  # Output: reg0 = troop_id, reg1 = group_id
  ("multiplayer_find_bot_troop_and_group_for_spawn",
    [
      (store_script_param, ":team_no", 1),
      (store_script_param, ":look_only_actives", 2),

      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", ":look_only_actives"),
      (assign, ":leader_player", reg0),

      (assign, ":available_troops_in_faction", 0),
      (assign, ":available_troops_to_spawn", 0),
      (team_get_faction, ":team_faction_no", ":team_no"),

      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (try_begin),
          (this_or_next|lt, ":leader_player", 0),
          (player_slot_ge, ":leader_player", ":wanted_slot", 1),
          (val_add, ":available_troops_to_spawn", 1),
        (try_end),
      (try_end),

      (assign, ":available_troops_in_faction", 0),

      (store_random_in_range, ":random_troop_index", 0, ":available_troops_to_spawn"),
      (assign, ":end_cond", multiplayer_ai_troops_end),
      (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
        (store_troop_faction, ":troop_faction", ":troop_no"),
        (eq, ":troop_faction", ":team_faction_no"),
        (store_add, ":wanted_slot", slot_player_bot_type_1_wanted, ":available_troops_in_faction"),
        (val_add, ":available_troops_in_faction", 1),
        (this_or_next|lt, ":leader_player", 0),
        (player_slot_ge, ":leader_player", ":wanted_slot", 1),
        (val_sub, ":random_troop_index", 1),
        (lt, ":random_troop_index", 0),
        (assign, ":end_cond", 0),
        (assign, ":selected_troop", ":troop_no"),
      (try_end),
      (assign, reg0, ":selected_troop"),
      (assign, reg1, ":leader_player"),
      ]),	

  # script_multiplayer_change_leader_of_bot
  # Input: arg1 = agent_no
  # Output: none
  ("multiplayer_change_leader_of_bot",
    [
      (store_script_param, ":agent_no", 1),
      (agent_get_team, ":team_no", ":agent_no"),
      (call_script, "script_multiplayer_find_player_leader_for_bot", ":team_no", 1),
      (assign, ":leader_player", reg0),
      (agent_set_group, ":agent_no", ":leader_player"),
      ]),
      
  ("multiplayer_find_spawn_point",
  [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care
     
     (set_fixed_point_multiplier, 100),
                   
     (assign, ":flags", 0),
     
     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (val_or, ":flags", spf_examine_all_spawn_points),
     (try_end),
     
     (try_begin),
       (eq, ":is_horseman", 1),
       (val_or, ":flags", spf_is_horseman),
     (try_end),

     (multiplayer_find_spawn_point, reg0, ":team_no", ":flags"),
  ]),
    
  # script_multiplayer_find_spawn_point_2
  # Input: arg1 = team_no, arg2 = examine_all_spawn_points, arg3 = is_horseman
  # Output: reg0 = entry_point_no
  ("multiplayer_find_spawn_point_2",
   [
     (store_script_param, ":team_no", 1),
     (store_script_param, ":examine_all_spawn_points", 2), #0-dm, 1-tdm, 2-cf, 3-hq, 4-sg
     (store_script_param, ":is_horseman", 3), #0:no, 1:yes, -1:do not care

     (assign, ":best_entry_point_score", -10000000),
     (assign, ":best_entry_point", 0),

     (assign, ":num_operations", 0),

     (assign, ":num_human_agents_div_3_plus_one", 0),

     (assign, ":num_human_agents_plus_one", ":num_human_agents_div_3_plus_one"),

     (try_begin), 
       (le, ":num_human_agents_plus_one", 4),
       (assign, ":random_number_upper_limit", 2), #this is not typo-mistake this should be 2 too, not 1.
     (else_try), 
       (le, ":num_human_agents_plus_one", 8),
       (assign, ":random_number_upper_limit", 2),
     (else_try), 
       (le, ":num_human_agents_plus_one", 16),
       (assign, ":random_number_upper_limit", 3),
     (else_try),
       (le, ":num_human_agents_plus_one", 24),
       (assign, ":random_number_upper_limit", 4),
     (else_try),
       (le, ":num_human_agents_plus_one", 32),
       (assign, ":random_number_upper_limit", 5),
     (else_try),
       (le, ":num_human_agents_plus_one", 40),
       (assign, ":random_number_upper_limit", 6),
     (else_try),
       (assign, ":random_number_upper_limit", 7),
     (try_end),

     (val_div, ":num_human_agents_div_3_plus_one", 3),
     (val_add, ":num_human_agents_div_3_plus_one", 1),
     (store_mul, ":negative_num_human_agents_div_3_plus_one", ":num_human_agents_div_3_plus_one", -1),

     (try_begin),
       (eq, ":examine_all_spawn_points", 1),
       (assign, ":random_number_upper_limit", 1),
     (try_end),
     
     (assign, ":first_agent", 0),
     
     (assign, ":multiplier", 0),
     
     (try_begin),
       (try_for_range, ":i_entry_point", 0, multi_num_valid_entry_points),
         (assign, ":minimum_enemy_distance", 3000), 
         (assign, ":second_minimum_enemy_distance", 3000), 
              
         (assign, ":entry_point_score", 0),
         (store_random_in_range, ":random_value", 0, ":random_number_upper_limit"), #in average it is 5
         (eq, ":random_value", 0),
         (entry_point_get_position, pos0, ":i_entry_point"), #pos0 holds current entry point position
         (try_for_agents, ":i_agent"),
           (agent_is_alive, ":i_agent"),
           (agent_is_human, ":i_agent"),
           (agent_get_team, ":agent_team", ":i_agent"),  
           (agent_get_position, pos1, ":i_agent"),
           (get_distance_between_positions_in_meters, ":distance", pos0, pos1),
           (val_add, ":num_operations", 1),
           (try_begin),
             (try_begin), #find closest enemy soldiers
               (lt, ":multiplier", 0),
               (try_begin),
                 (lt, ":distance", ":minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":minimum_enemy_distance"),
                 (assign, ":minimum_enemy_distance", ":distance"),
               (else_try),
                 (lt, ":distance", ":second_minimum_enemy_distance"),
                 (assign, ":second_minimum_enemy_distance", ":distance"),
               (try_end),
             (try_end),
     
             (lt, ":distance", 100),
             (try_begin), #do not spawn over or too near to another agent (limit is 2 meters, squared 4 meters)
               (lt, ":distance", 3),
               (try_begin),
                 (this_or_next|eq, ":examine_all_spawn_points", 0),
                 (this_or_next|lt, ":multiplier", 0), #new added 20.08.08
                 (try_begin),
                   (lt, ":distance", 1),                 
                   (assign, ":dist_point", -1000000), #never place 
                 (else_try),
                   (lt, ":distance", 2),
                   (try_begin),
                     (lt, ":multiplier", 0), 
                     (assign, ":dist_point", -20000),
                   (else_try),
                     (assign, ":dist_point", -2000), #can place, friend and distance is between 1-2 meters
                   (try_end), 
                 (else_try),
                   (try_begin),
                     (lt, ":multiplier", 0), 
                     (assign, ":dist_point", -10000), 
                   (else_try),
                     (assign, ":dist_point", -1000), #can place, friend and distance is between 2-3 meters
                   (try_end),
                 (try_end),
               (else_try),
                 #if examinining all spawn points and mod is siege only. This happens in new round start placings.
                 (try_begin),
                   (lt, ":distance", 1),                 
                   (assign, ":dist_point", -20000), #very hard to place distance is < 1 meter
                 (else_try),
                   (lt, ":distance", 2),
                   (assign, ":dist_point", -2000),
                 (else_try),       
                   (assign, ":dist_point", -1000), #can place, distance is between 2-3 meters
                 (try_end),                 
               (try_end),
     
               (val_mul, ":dist_point", ":num_human_agents_div_3_plus_one"),                 
             
             (try_end),
             (val_add, ":entry_point_score", ":dist_point"),
           (try_end),
         (try_end),


         (try_begin),

           #(assign, ":minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, ":second_minimum_enemy_dist_score", 0), #close also these with displays
           #(assign, reg2, ":minimum_enemy_distance"), #close also these with displays
           #(assign, reg3, ":second_minimum_enemy_distance"), #close also these with displays
          
           (try_begin), #if minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":minimum_enemy_distance", 3000), 
             (try_begin),
               (gt, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":minimum_enemy_dist_score", ":minimum_enemy_distance", -50),
               (val_mul, ":minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":minimum_enemy_dist_score"),
             (try_end),
           (try_end),

           (try_begin), #if second minimum enemy dist score is greater than 40(multiplayer_spawn_above_opt_enemy_dist_point) meters then give negative score
             (lt, ":second_minimum_enemy_distance", 3000), #3000 x 3000
             (try_begin),
               (gt, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (val_sub, ":second_minimum_enemy_distance", multiplayer_spawn_above_opt_enemy_dist_point),
               (store_mul, ":second_minimum_enemy_dist_score", ":second_minimum_enemy_distance", -50),
               (val_mul, ":second_minimum_enemy_dist_score", ":num_human_agents_div_3_plus_one"),
               (val_add, ":entry_point_score", ":second_minimum_enemy_dist_score"),
             (try_end),
           (try_end),
           
           #(assign, reg0, ":minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(assign, reg1, ":second_minimum_enemy_dist_score"), #close also above assignment lines with these displays
           #(display_message, "@{!}minimum enemy distance : {reg2}, score : {reg0}"), #close also above assignment lines with these displays
           #(display_message, "@{!}second minimum enemy distance : {reg3}, score : {reg1}"), #close also above assignment lines with these displays
         (try_end),
 
         (try_begin), #giving positive points for "distance of entry point position to ground" while searching for entry point for defender team
           (neq, ":is_horseman", -1), #if being horseman or rider is not (not important)

           #additional score to entry points which has distance to ground value of > 0 meters
           (position_get_distance_to_terrain, ":height_to_terrain", pos0),     
           (val_max, ":height_to_terrain", 0),
           (val_min, ":height_to_terrain", 300),
           (ge, ":height_to_terrain", 40),                      
           
           (store_mul, ":height_to_terrain_score", ":height_to_terrain", ":num_human_agents_div_3_plus_one"), #it was 8
           
           (try_begin),
             (val_mul, ":height_to_terrain_score", 4),
           (try_end),
           
           (try_begin),
             (eq, ":is_horseman", 0),
           (else_try),
             (val_mul, ":height_to_terrain_score", 5),
             (val_sub, ":entry_point_score", ":height_to_terrain_score"),
           (try_end),
         (try_end),

         (try_begin), #siege
           (eq, ":team_no", 0),
           (entry_point_get_position, pos1, multi_siege_flag_point), #our base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
           (entry_point_get_position, pos2, multi_initial_spawn_point_team_2), #enemy base is at pos2
         (else_try),
           (entry_point_get_position, pos1, multi_initial_spawn_point_team_2), #our base is at pos2
           (entry_point_get_position, pos2, multi_siege_flag_point), #enemy base is at pos1 (it was multi_initial_spawn_point_team_1 changed at v622)
         (try_end),
           
           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_our_base", pos0, pos1),
           (get_sq_distance_between_positions_in_meters, ":sq_dist_to_enemy_base", pos0, pos2),                 
           (get_distance_between_positions_in_meters, ":dist_to_enemy_base", pos0, pos2),

           #give positive points if this entry point is near to our base.
           (assign, ":dist_to_our_base_point", 0),     
           (try_begin),
             (lt, ":sq_dist_to_our_base", 10000), #in siege give entry points score until 100m distance is reached
             (try_begin),
               (eq, ":team_no", 0),
               (try_begin),
                 (lt, ":sq_dist_to_our_base", 2500), #if distance is < 50m in siege give all highest point possible
                 (assign, ":sq_dist_to_our_base", 0),
               (else_try),
                 (val_sub, ":sq_dist_to_our_base", 2500),
                 (val_mul, ":sq_dist_to_our_base", 2),
               (try_end),
             (try_end),

             (store_sub, ":dist_to_our_base_point", 10000, ":sq_dist_to_our_base"),

             #can be (10000 - (10000 - 2500) * 2) = -5000 (for only defenders) so we are adding this loss.
             (val_add, ":dist_to_our_base_point", 5000), #so score getting from being near to base changes between 0 to 15000

             (try_begin),
               (eq, ":team_no", 0), 
             (else_try), #in siege mod for attackers being near to base entry point has 45 times less importance
               (val_div, ":dist_to_our_base_point", 45),
             (try_end),
             (val_mul, ":dist_to_our_base_point", ":num_human_agents_div_3_plus_one"),
           (try_end),

           (val_add, ":entry_point_score", ":dist_to_our_base_point"),


           #give negative points if this entry point is near to enemy base.
           (assign, ":dist_to_enemy_base_point", 0),

           (val_add, ":entry_point_score", ":dist_to_enemy_base_point"),
         (try_end),

         #(assign, reg1, ":i_entry_point"),
         #(assign, reg2, ":entry_point_score"),
         #(display_message, "@{!}entry_no : {reg1} , entry_score : {reg2}"),

         (gt, ":entry_point_score", ":best_entry_point_score"),
         (assign, ":best_entry_point_score", ":entry_point_score"),
         (assign, ":best_entry_point", ":i_entry_point"),         
       (try_end),

       #(assign, reg0, ":best_entry_point"), 
       #(assign, reg1, ":best_entry_point_score"),
       #(assign, reg2, ":num_operations"),       
       #(assign, reg7, ":is_horseman"),
       #(display_message, "@{!},is horse:{reg7}, best entry:{reg0}, best entry score:{reg1}, num_operations:{reg2}"),
     (try_end),
     (assign, reg0, ":best_entry_point"), 
     ]),
  
  #script_multiplayer_buy_agent_equipment
  # Input: arg1 = player_no
  # Output: none
  ("multiplayer_buy_agent_equipment",
   [
     (store_script_param, ":player_no", 1),
     (player_get_troop_id, ":player_troop", ":player_no"),
     (player_get_gold, ":player_gold", ":player_no"),
     (player_get_slot, ":added_gold", ":player_no", slot_player_last_rounds_used_item_earnings),
     (player_set_slot, ":player_no", slot_player_last_rounds_used_item_earnings, 0),
     (val_add, ":player_gold", ":added_gold"),
     (assign, ":armor_bought", 0),
     
     #moving original values to temp slots
     (try_for_range, ":i_item", slot_player_selected_item_indices_begin, slot_player_selected_item_indices_end),
       (player_get_slot, ":selected_item_index", ":player_no", ":i_item"),
       (store_sub, ":i_cur_selected_item", ":i_item", slot_player_selected_item_indices_begin),
       (try_begin),
         (player_item_slot_is_picked_up, ":player_no", ":i_cur_selected_item"),
         (assign, ":selected_item_index", -1),
       (try_end),
       (val_add, ":i_cur_selected_item", slot_player_cur_selected_item_indices_begin),
       (player_set_slot, ":player_no", ":i_cur_selected_item", ":selected_item_index"),
     (try_end),
     (assign, ":end_cond", 1000),
     (try_for_range, ":unused", 0, ":end_cond"),
       (call_script, "script_multiplayer_calculate_cur_selected_items_cost", ":player_no", 0),
       (assign, ":total_cost", reg0),
       (try_begin),
         (gt, ":total_cost", ":player_gold"),
         #downgrade one of the selected items
         #first normalize the prices
         #then prioritize some of the weapon classes for specific troop classes
         (call_script, "script_multiplayer_get_troop_class", ":player_troop"),
         (assign, ":player_troop_class", reg0),

         (assign, ":max_cost_value", 0),
         (assign, ":max_cost_value_index", -1),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           (ge, ":item_id", 0), #might be -1 for horses etc.
           (call_script, "script_multiplayer_get_item_value_for_troop", ":item_id", ":player_troop"),
           (assign, ":item_value", reg0),
           (store_sub, ":item_type", ":i_item", slot_player_cur_selected_item_indices_begin),
           (try_begin), #items
             (this_or_next|eq, ":item_type", 0),
             (this_or_next|eq, ":item_type", 1),
             (this_or_next|eq, ":item_type", 2),
             (eq, ":item_type", 3),
             (val_mul, ":item_value", 5),
           (else_try), #head
             (eq, ":item_type", 4),
             (val_mul, ":item_value", 4),
           (else_try), #body
             (eq, ":item_type", 5),
             (val_mul, ":item_value", 2),
           (else_try), #foot
             (eq, ":item_type", 6),
             (val_mul, ":item_value", 8),
           (else_try), #gloves
             (eq, ":item_type", 7),
             (val_mul, ":item_value", 8),
           (else_try), #horse
             #base value (most expensive)
           (try_end),
           (item_get_slot, ":item_class", ":item_id", slot_item_multiplayer_item_class),
           (try_begin),
             (eq, ":player_troop_class", multi_troop_class_infantry),#############warlords_change_unfinished
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_axe),
             (this_or_next|eq, ":item_class", multi_item_class_type_blunt),
             (this_or_next|eq, ":item_class", multi_item_class_type_war_picks),
             (this_or_next|eq, ":item_class", multi_item_class_type_two_handed_sword),
             (this_or_next|eq, ":item_class", multi_item_class_type_small_shield),
             (eq, ":item_class", multi_item_class_type_two_handed_axe),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_engineer),
             (this_or_next|eq, ":item_class", multi_item_class_type_spear),
             (eq, ":item_class", multi_item_class_type_large_shield),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_cavalry),
             (this_or_next|eq, ":item_class", multi_item_class_type_lance),
             (this_or_next|eq, ":item_class", multi_item_class_type_sword),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_sailor),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (eq, ":item_class", multi_item_class_type_arrow),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_civilian),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (eq, ":item_class", multi_item_class_type_bolt),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_driver),
             (this_or_next|eq, ":item_class", multi_item_class_type_bow),
             (this_or_next|eq, ":item_class", multi_item_class_type_arrow),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (else_try),
             (eq, ":player_troop_class", multi_troop_class_supporter),
             (this_or_next|eq, ":item_class", multi_item_class_type_crossbow),
             (this_or_next|eq, ":item_class", multi_item_class_type_bolt),
             (eq, ":item_class", multi_item_class_type_horse),
             (val_div, ":item_value", 2),
           (try_end),
   
           (try_begin),
             (gt, ":item_value", ":max_cost_value"),
             (assign, ":max_cost_value", ":item_value"),
             (assign, ":max_cost_value_index", ":i_item"),
           (try_end),
         (try_end),

         #max_cost_value and max_cost_value_index will definitely be valid
         #unless no items are left (therefore some items must cost 0 gold)
         (player_get_slot, ":item_id", ":player_no", ":max_cost_value_index"),
         (call_script, "script_multiplayer_get_previous_item_for_item_and_troop", ":item_id", ":player_troop"),
         (assign, ":item_id", reg0),
         (player_set_slot, ":player_no", ":max_cost_value_index", ":item_id"),
       (else_try),
         (assign, ":end_cond", 0),
         (val_sub, ":player_gold", ":total_cost"),
         (player_set_gold, ":player_no", ":player_gold", multi_max_gold_that_can_be_stored),
         (try_for_range, ":i_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
           (player_get_slot, ":item_id", ":player_no", ":i_item"),
           #checking if different class default item replace is needed for weapons
           (try_begin),
             (ge, ":item_id", 0),
             #then do nothing
           (else_try),
             (store_sub, ":base_index_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (store_add, ":selected_item_index_slot", ":base_index_slot", slot_player_selected_item_indices_begin),
             (player_get_slot, ":selected_item_index", ":player_no", ":selected_item_index_slot"),
             (this_or_next|eq, ":selected_item_index", -1),
             (player_item_slot_is_picked_up, ":player_no", ":base_index_slot"),
             #then do nothing
           (else_try),
             #an item class without a default value is -1, then find a default weapon
             (item_get_slot, ":item_class", ":selected_item_index", slot_item_multiplayer_item_class),
             (is_between, ":item_class", multi_item_class_type_weapons_begin, multi_item_class_type_weapons_end),
             (assign, ":dc_replaced_item", -1),
             (try_for_range, ":i_dc_item_class", multi_item_class_type_melee_weapons_begin, multi_item_class_type_melee_weapons_end),
               (lt, ":dc_replaced_item", 0),
               (assign, ":dc_item_class_used", 0),
               (try_for_range, ":i_dc_item", slot_player_cur_selected_item_indices_begin, slot_player_cur_selected_item_indices_end),
                 (player_get_slot, ":dc_cur_item", ":player_no", ":i_dc_item"),
                 (ge, ":dc_cur_item", 0),
                 (item_get_slot, ":dc_item_class", ":dc_cur_item", slot_item_multiplayer_item_class),
                 (eq, ":dc_item_class", ":i_dc_item_class"),
                 (assign, ":dc_item_class_used", 1),
               (try_end),
               (eq, ":dc_item_class_used", 0),
               (assign, ":dc_end_cond", all_items_end),
               (try_for_range, ":i_dc_new_item", all_items_begin, ":dc_end_cond"),
                 (item_slot_eq, ":i_dc_new_item", slot_item_multiplayer_item_class, ":i_dc_item_class"),
                 (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_dc_new_item", ":player_troop"),
                 (assign, ":dc_end_cond", 0), #break
                 (assign, ":dc_replaced_item", ":i_dc_new_item"),
               (try_end),
             (try_end),
             (ge, ":dc_replaced_item", 0),
             (player_set_slot, ":player_no", ":i_item", ":dc_replaced_item"),
             (assign, ":item_id", ":dc_replaced_item"),
           (try_end),

           #finally, add the item to agent
           (try_begin),
             (ge, ":item_id", 0), #might be -1 for horses etc.
             (store_sub, ":item_slot", ":i_item", slot_player_cur_selected_item_indices_begin),
             (player_add_spawn_item, ":player_no", ":item_slot", ":item_id"),
             (try_begin),
               (eq, ":item_slot", ek_body), #ek_body is the slot for armor
               (assign, ":armor_bought", 1),
             (try_end),
           (try_end),
         (try_end),

         (player_set_slot, ":player_no", slot_player_total_equipment_value, ":total_cost"),     
       (try_end),
     (try_end),
     (try_begin),
       (eq, ":armor_bought", 0),
       (eq, "$g_multiplayer_force_default_armor", 1),
       (assign, ":end_cond", all_items_end),
       (try_for_range, ":i_new_item", all_items_begin, ":end_cond"),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_light_armor),
         (this_or_next|item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_medium_armor),
         (item_slot_eq, ":i_new_item", slot_item_multiplayer_item_class, multi_item_class_type_heavy_armor),
         (call_script, "script_cf_multiplayer_is_item_default_for_troop", ":i_new_item", ":player_troop"),
         (assign, ":end_cond", 0), #break
         (player_add_spawn_item, ":player_no", ek_body, ":i_new_item"), #ek_body is the slot for armor
       (try_end),
     (try_end),
     ]),


  #script_game_get_item_extra_text:
  # This script is called from the game engine when an item's properties are displayed.
  # INPUT: arg1 = item_no, arg2 = extra_text_id (this can be between 0-7 (7 included)), arg3 = item_modifier
  # OUTPUT: result_string = item extra text, trigger_result = text color (0 for default)



#  ("game_get_item_extra_text",
#    [
#      (store_script_param, ":item_no", 1),
#      (store_script_param, ":extra_text_id", 2),
#      (store_script_param, ":item_modifier", 3),
#      (try_begin),
#        (is_between, ":item_no", food_begin, food_end),
#        (try_begin),
#          (eq, ":extra_text_id", 0),
#          (assign, ":continue", 1),
#          (try_begin),
#            (this_or_next|eq, ":item_no", "itm_cattle_meat"),
#            (this_or_next|eq, ":item_no", "itm_pork"),
#				(eq, ":item_no", "itm_chicken"),
#				
#            (eq, ":item_modifier", imod_rotten),
#            (assign, ":continue", 0),
#          (try_end),
#          (eq, ":continue", 1),
#          (item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
#          (assign, reg1, ":food_bonus"),
#          (set_result_string, "@+{reg1} to party morale"),
#          (set_trigger_result, 0x4444FF),
#        (try_end),
#      (else_try),
#        (is_between, ":item_no", readable_books_begin, readable_books_end),
#        (try_begin),
#          (eq, ":extra_text_id", 0),
#          (item_get_slot, reg1, ":item_no", slot_item_intelligence_requirement),
#          (set_result_string, "@Requires {reg1} intelligence to read"),
#          (set_trigger_result, 0xFFEEDD),
#        (else_try),
#          (eq, ":extra_text_id", 1),
#          (item_get_slot, ":progress", ":item_no", slot_item_book_reading_progress),
#          (val_div, ":progress", 10),
#          (assign, reg1, ":progress"),
#          (set_result_string, "@Reading Progress: {reg1}%"),
#          (set_trigger_result, 0xFFEEDD),
#        (try_end),
#      (else_try),
#        (is_between, ":item_no", reference_books_begin, reference_books_end),
#        (try_begin),
#          (eq, ":extra_text_id", 0),
#          (try_begin),
#            (eq, ":item_no", "itm_book_wound_treatment_reference"),
#            (str_store_string, s1, "@wound treament"),
#          (else_try),
#            (eq, ":item_no", "itm_book_training_reference"),
#            (str_store_string, s1, "@trainer"),
#          (else_try),
#            (eq, ":item_no", "itm_book_surgery_reference"),
#            (str_store_string, s1, "@surgery"),
#          (try_end),
#          (set_result_string, "@+1 to {s1} while in inventory"),
#          (set_trigger_result, 0xFFEEDD),
#        (try_end),
#      (try_end),
#  ]),

  #script_calculate_flag_move_time
  # INPUT: arg1 = number_of_total_agents_around_flag, arg2 = dist_between_flag_and_its_pole
  # OUTPUT: reg0 = flag move time
  ("calculate_flag_move_time",
   [
     (store_script_param, ":number_of_total_agents_around_flag", 1),
     (store_script_param, ":dist_between_flag_and_its_target", 2),

     (try_begin), #(if no one is around flag it again moves to its current owner situation but 5 times slower than normal)
       (eq, ":number_of_total_agents_around_flag", 0),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 2500),#5.00 * 1.00 * (500 stable) = 2000 
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 1),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 500), #1.00 * (500 stable) = 500
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 2),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 300), #0.60(0.60) * (500 stable) = 300
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 3),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 195), #0.39(0.60 * 0.65) * (500 stable) = 195
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 4),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 137), #0.273(0.60 * 0.65 * 0.70) * (500 stable) = 136.5 >rounding> 137
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 5),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 102), #0.20475(0.60 * 0.65 * 0.70 * 0.75) * (500 stable) = 102.375 >rounding> 102
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 6),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 82),  #0.1638(0.60 * 0.65 * 0.70 * 0.75 * 0.80) * (500 stable) = 81.9 >rounding> 82
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 7),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 66),  #0.13104(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85) * (500 stable) = 65.52 >rounding> 66
     (else_try),
       (eq, ":number_of_total_agents_around_flag", 8),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 59),  #0.117936(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90) * (500 stable) = 58.968 >rounding> 59
     (else_try),
       (store_mul, reg0, ":dist_between_flag_and_its_target", 56),  #0.1120392(0.60 * 0.65 * 0.70 * 0.75 * 0.80 * 0.85 * 0.90 * 0.95) * (500 stable) = 56.0196 >rounding> 56
     (try_end), 

     (assign, ":number_of_players", 0),
     (get_max_players, ":num_players"),                               
     (try_for_range, ":cur_player", 0, ":num_players"),
       (player_is_active, ":cur_player"),
       (val_add, ":number_of_players", 1),
     (try_end),

     (try_begin),
       (lt, ":number_of_players", 10),
       (val_mul, reg0, 50),
     (else_try),
       (lt, ":number_of_players", 35),
       (store_sub, ":number_of_players_multipication", 35, ":number_of_players"),
       (val_mul, ":number_of_players_multipication", 2),
       (store_sub, ":number_of_players_multipication", 100, ":number_of_players_multipication"),
       (val_mul, reg0, ":number_of_players_multipication"),
     (else_try),
       (val_mul, reg0, 100),
     (try_end),

     (val_div, reg0, 10000), #100x for number of players around flag, 100x for number of players in game
     ]),

  #script_move_flag
  # INPUT: arg1 = shown_flag_id, arg2 = move time in seconds, pos0 = target position
  # OUTPUT: none
  ("move_flag",
   [
     (store_script_param, ":shown_flag_id", 1),
     (store_script_param, ":shown_flag_move_time", 2),

     (try_begin),
       (multiplayer_is_server), #added after auto-animating
     
       (try_begin),
         (eq, ":shown_flag_move_time", 0), #stop
         (prop_instance_stop_animating, ":shown_flag_id"),
       (else_try),
         (prop_instance_animate_to_position, ":shown_flag_id", pos0, ":shown_flag_move_time"),
       (try_end),
     (try_end),
   ]),
           
("player_set_score",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),
     
     (player_set_score, ":player_no", ":score"),
   ]),
           
  #script_player_set_kill_count
  # INPUT: arg1 = player_no, arg2 = score
  # OUTPUT: none
  ("player_set_kill_count",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),
     
     (player_set_kill_count, ":player_no", ":score"),
   ]),
           
           
           
  #script_player_set_death_count
  # INPUT: arg1 = player_no, arg2 = score
  # OUTPUT: none
  ("player_set_death_count",
   [
     (store_script_param, ":player_no", 1),
     (store_script_param, ":score", 2),
     
     (player_set_death_count, ":player_no", ":score"),
   ]),
# Note to modders: Uncomment these if you'd like to use the following.
  
##  #script_game_check_party_sees_party
##  # This script is called from the game engine when a party is inside the range of another party
##  # INPUT: arg1 = party_no_seer, arg2 = party_no_seen
##  # OUTPUT: trigger_result = true or false (1 = true, 0 = false)
##  ("game_check_party_sees_party",
##   [
##     (store_script_param, ":party_no_seer", 1),
##     (store_script_param, ":party_no_seen", 2),
##     (set_trigger_result, 1),
##    ]),
##
##  #script_game_get_party_speed_multiplier
##  # This script is called from the game engine when a skill's modifiers are needed
##  # INPUT: arg1 = party_no
##  # OUTPUT: trigger_result = multiplier (scaled by 100, meaning that giving 100 as the trigger result does not change the party speed)
##  ("game_get_party_speed_multiplier",
##   [
##     (store_script_param, ":party_no", 1),
##     (set_trigger_result, 100),
##    ]),



  
  
	#the following is a very simple adjustment - it measures the difference in prices between two towns
	#all goods are weighted equally except for luxuries
	#it does not take into account the prices of the goods, nor cargo capacity
	#to do that properly, a merchant would have to virtually fill his baggage, slot by slot, for each town
	#i also found that one needed to introduce demand inelasticity -- prices should vary a lot for grain,  relatively little for iron

  
  #script_shield_item_set_banner
  # INPUT: agent_no
  # OUTPUT: none
  ("shield_item_set_banner",
    [
       (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (call_script, "script_agent_troop_get_banner_mesh", ":agent_no", ":troop_no"),
       (cur_item_set_tableau_material, ":tableau_no", reg0),
     ]),

  
  #script_troop_agent_set_banner
  # INPUT: agent_no
  # OUTPUT: none
  ("troop_agent_set_banner",
    [
       (store_script_param, ":tableau_no",1),
       (store_script_param, ":agent_no", 2),
       (store_script_param, ":troop_no", 3),
       (call_script, "script_agent_troop_get_banner_mesh", ":agent_no", ":troop_no"),
       (cur_agent_set_banner_tableau_material, ":tableau_no", reg0),
     ]),

  #script_agent_troop_get_banner_mesh
  # INPUT: agent_no, troop_no
  # OUTPUT: banner_mesh
  ("agent_troop_get_banner_mesh",
    [
       (store_script_param, ":agent_no", 1),
       (store_script_param, ":troop_no", 2),
#       (assign, ":banner_troop", -1),
       (assign, ":banner_mesh", "mesh_banners_default_b"),
       (try_begin),
#         (lt, ":agent_no", 0),
#         (try_begin),
#           (ge, ":troop_no", 0),
#           (this_or_next|troop_slot_ge, ":troop_no", slot_troop_banner_scene_prop, 1),
#           (eq, ":troop_no", "trp_player"),
#           (assign, ":banner_troop", ":troop_no"),
#         (else_try),
#           (is_between, ":troop_no", companions_begin, companions_end),
#           (assign, ":banner_troop", "trp_player"),
#         (else_try),
#           (assign, ":banner_mesh", "mesh_banners_default_a"),
#         (try_end),
#       (else_try),
#         (eq, "$g_is_quick_battle", 1),
#         (agent_get_team, ":agent_team", ":agent_no"),
#         (try_begin),
#           (eq, ":agent_team", 0),
#           (assign, ":banner_mesh", "$g_quick_battle_team_0_banner"),
#         (else_try),
#           (assign, ":banner_mesh", "$g_quick_battle_team_1_banner"),
#         (try_end),
#       (else_try),
         (game_in_multiplayer_mode),
         (agent_get_group, ":agent_group", ":agent_no"),
         (try_begin),
           (neg|player_is_active, ":agent_group"),
           (agent_get_player_id, ":agent_group", ":agent_no"),
         (try_end),
         (try_begin),
           #if player banners are not allowed, use the default banner mesh
           (eq, "$g_multiplayer_allow_player_banners", 1),
           (player_is_active, ":agent_group"),
           (player_get_banner_id, ":player_banner", ":agent_group"),
           (ge, ":player_banner", 0),
           (store_add, ":banner_mesh", ":player_banner", arms_meshes_begin),
           (assign, ":already_used", 0),
           (try_for_range, ":cur_faction", multiplayer_factions_begin, multiplayer_factions_end), #wrong client data check
             (faction_slot_eq, ":cur_faction", slot_faction_banner, ":banner_mesh"),
             (assign, ":already_used", 1),
           (try_end),
           (eq, ":already_used", 0), #otherwise use the default banner mesh
         (else_try),
           (agent_get_team, ":agent_team", ":agent_no"),
           (team_get_faction, ":team_faction_no", ":agent_team"),

           (try_begin),
             (agent_is_human, ":agent_no"),
             (faction_get_slot, ":banner_mesh", ":team_faction_no", slot_faction_banner),
           (else_try),
             (agent_get_rider, ":rider_agent_no", ":agent_no"),
             #(agent_get_position, pos1, ":agent_no"),
             #(position_get_x, ":pos_x", pos1),
             #(position_get_y, ":pos_y", pos1),
             #(assign, reg0, ":pos_x"),
             #(assign, reg1, ":pos_y"),
             #(assign, reg2, ":agent_no"),
             #(display_message, "@{!}agent_no:{reg2}, pos_x:{reg0} , posy:{reg1}"),
             (try_begin),
               (ge, ":rider_agent_no", 0),
               (agent_is_active, ":rider_agent_no"),
               (agent_get_team, ":rider_agent_team", ":rider_agent_no"),
               (team_get_faction, ":rider_team_faction_no", ":rider_agent_team"),
               (faction_get_slot, ":banner_mesh", ":rider_team_faction_no", slot_faction_banner),
             (else_try),
               (assign, ":banner_mesh", "mesh_banners_default_c"),
             (try_end),                   
           (try_end),             
         (try_end),
#       (else_try),
#         (agent_get_troop_id, ":troop_id", ":agent_no"),
#         (this_or_next|troop_slot_ge,  ":troop_id", slot_troop_banner_scene_prop, 1),
#         (eq, ":troop_no", "trp_player"),
#         (assign, ":banner_troop", ":troop_id"),
#       (else_try),
#         (agent_get_party_id, ":agent_party", ":agent_no"),
#         (try_begin),
#           (lt, ":agent_party", 0),
#           (is_between, ":troop_id", companions_begin, companions_end),
#           (main_party_has_troop, ":troop_id"),
#           (assign, ":agent_party", "p_main_party"),
#         (try_end),
#         (ge, ":agent_party", 0),
#         (party_get_template_id, ":party_template", ":agent_party"),
#         (try_begin),
#           (eq, ":party_template", "pt_deserters"),
#           (assign, ":banner_mesh", "mesh_banners_default_c"),
#         (else_try),
#           (is_between, ":agent_party", centers_begin, centers_end),
#           (is_between, ":troop_id", companions_begin, companions_end),
#           (neq, "$talk_context", tc_tavern_talk),
#           #this should be a captured companion in prison
#           (assign, ":banner_troop", "trp_player"),
#         (else_try),
#           (is_between, ":agent_party", centers_begin, centers_end),
#           (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
#           (ge, ":town_lord", 0),
#           (assign, ":banner_troop", ":town_lord"),
#         (else_try),
#           (this_or_next|party_slot_eq, ":agent_party", slot_party_type, spt_kingdom_hero_party),
#           (eq, ":agent_party", "p_main_party"),
#           (party_get_num_companion_stacks, ":num_stacks", ":agent_party"),
#           (gt, ":num_stacks", 0),
#           (party_stack_get_troop_id, ":leader_troop_id", ":agent_party", 0),
#           (this_or_next|troop_slot_ge,  ":leader_troop_id", slot_troop_banner_scene_prop, 1),
#           (eq, ":leader_troop_id", "trp_player"),
#           (assign, ":banner_troop", ":leader_troop_id"),
#         (try_end),
#       (else_try), #Check if we are in a tavern
#         (eq, "$talk_context", tc_tavern_talk),
#         (neq, ":troop_no", "trp_player"),
#         (assign, ":banner_mesh", "mesh_banners_default_d"),
#       (else_try), #can't find party, this can be a town guard
#         (neq, ":troop_no", "trp_player"),
#         (is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),
#         (party_get_slot, ":town_lord", "$g_encountered_party", slot_town_lord),
#         (ge, ":town_lord", 0),
#         (assign, ":banner_troop", ":town_lord"),
       (try_end),
#       (try_begin),
#         (ge, ":banner_troop", 0),
#         (try_begin),
#           (neg|troop_slot_ge, ":banner_troop", slot_troop_banner_scene_prop, 1),
#           (assign, ":banner_mesh", "mesh_banners_default_b"),
#         (else_try), 
#           (troop_get_slot, ":banner_spr", ":banner_troop", slot_troop_banner_scene_prop),
#           (store_add, ":banner_scene_props_end", banner_scene_props_end_minus_one, 1),
#           (is_between, ":banner_spr", banner_scene_props_begin, ":banner_scene_props_end"),
#           (val_sub, ":banner_spr", banner_scene_props_begin),
#           (store_add, ":banner_mesh", ":banner_spr", arms_meshes_begin),
#         (try_end),
#       (try_end),
       (assign, reg0, ":banner_mesh"),
     ]),
           
           
  # script_draw_banner_to_region
  # Input: arg1 = troop_no, arg2 = center_pos_x, arg3 = center_pos_y, arg4 = width, arg5 = height, arg6 = stretch_width, arg7 = stretch_height, arg8 = default_scale, arg9 = max_charge_scale, arg10 = drawn_item_type
  # drawn_item_type is 0 for banners, 1 for shields, 2 for heater shield, 3 for armor
  # arguments will be used as fixed point values
  # Output: none
  ("draw_banner_to_region",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":center_pos_x", 2),
      (store_script_param, ":center_pos_y", 3),
      (store_script_param, ":width", 4),
      (store_script_param, ":height", 5),
      (store_script_param, ":stretch_width", 6),
      (store_script_param, ":stretch_height", 7),
      (store_script_param, ":default_scale", 8),
      (store_script_param, ":max_charge_scale", 9),
      (store_script_param, ":drawn_item_type", 10),

      (troop_get_slot, ":bg_type", ":troop_no", slot_troop_custom_banner_bg_type),
      (val_add, ":bg_type", custom_banner_backgrounds_begin),
      (troop_get_slot, ":bg_color_1", ":troop_no", slot_troop_custom_banner_bg_color_1),
      (troop_get_slot, ":bg_color_2", ":troop_no", slot_troop_custom_banner_bg_color_2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (troop_get_slot, ":positioning", ":troop_no", slot_troop_custom_banner_positioning),
      (call_script, "script_get_troop_custom_banner_num_positionings", ":troop_no"),
      (assign, ":num_positionings", reg0),
      (val_mod, ":positioning", ":num_positionings"),

      (init_position, pos2),
      (position_set_x, pos2, ":width"),
      (position_set_y, pos2, ":height"),
      (assign, ":default_value", 1),
      (convert_to_fixed_point, ":default_value"),
      (position_set_z, pos2, ":default_value"),

      (init_position, pos1),
      (position_set_x, pos1, ":center_pos_x"),
      (position_set_y, pos1, ":center_pos_y"),
      (position_move_z, pos1, -20),

      (init_position, pos3),
      (position_set_x, pos3, ":default_scale"),
      (position_set_y, pos3, ":default_scale"),
      (position_set_z, pos3, ":default_value"),

      (try_begin),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_bg"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg01"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg02"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg03"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg08"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg09"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg10"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg11"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg12"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg13"),
        (this_or_next|eq, ":bg_type", "mesh_custom_banner_fg16"),
        (eq, ":bg_type", "mesh_custom_banner_fg17"),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos2, 0, ":bg_color_1"),
      (else_try),
        (cur_tableau_add_mesh_with_scale_and_vertex_color, ":bg_type", pos1, pos3, 0, ":bg_color_1"),
      (try_end),
      (position_move_z, pos1, -20),
      (position_move_x, pos2, ":width"),
      (position_move_y, pos2, ":height"),
      (cur_tableau_add_mesh_with_scale_and_vertex_color, "mesh_custom_banner_bg", pos1, pos2, 0, ":bg_color_2"),
      
      (assign, ":charge_stretch", ":stretch_width"),
      (val_min, ":charge_stretch", ":stretch_height"),
      (val_min, ":charge_stretch", ":max_charge_scale"),
      (call_script, "script_get_custom_banner_charge_type_position_scale_color", "trp_player", ":positioning"),

      (try_begin),
        (this_or_next|eq, ":drawn_item_type", 2), #heater shield
        (eq, ":drawn_item_type", 3), #armor
        (assign, ":change_center_pos", 0),
        (try_begin),
          (eq, ":num_charges", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 2),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (else_try),
          (eq, ":num_charges", 3),
          (eq, ":positioning", 1),
          (assign, ":change_center_pos", 1),
        (try_end),
        (try_begin),
          (eq, ":change_center_pos", 1),
          (val_add, ":center_pos_y", 30),
        (try_end),
      (try_end),
      
      (try_begin),
        (ge, ":num_charges", 1),
        (val_mul, reg1, ":charge_stretch"),
        (val_div, reg1, 10000),
        (position_get_x, ":x", pos0),
        (position_get_y, ":y", pos0),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos0, ":x"),
        (position_set_y, pos0, ":y"),
        (assign, ":scale_value", reg1),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg0, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg0, 256), #remove orientation flags
        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg0, pos0, pos4, 0, reg2),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 2),
        (val_mul, reg4, ":charge_stretch"),
        (val_div, reg4, 10000),
        (position_get_x, ":x", pos1),
        (position_get_y, ":y", pos1),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos1, ":x"),
        (position_set_y, pos1, ":y"),

        (assign, ":scale_value", reg4),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg3, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg3, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg3, pos1, pos4, 0, reg5),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 3),
        (val_mul, reg7, ":charge_stretch"),
        (val_div, reg7, 10000),
        (position_get_x, ":x", pos2),
        (position_get_y, ":y", pos2),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos2, ":x"),
        (position_set_y, pos2, ":y"),

        (assign, ":scale_value", reg7),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg6, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg6, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg6, pos2, pos4, 0, reg8),
      (try_end),
      (try_begin),
        (ge, ":num_charges", 4),
        (val_mul, reg10, ":charge_stretch"),
        (val_div, reg10, 10000),
        (position_get_x, ":x", pos3),
        (position_get_y, ":y", pos3),
        (val_mul, ":x", ":stretch_width"),
        (val_mul, ":y", ":stretch_height"),
        (val_div, ":x", 10000),
        (val_div, ":y", 10000),
        (val_add, ":x", ":center_pos_x"),
        (val_add, ":y", ":center_pos_y"),
        (position_set_x, pos3, ":x"),
        (position_set_y, pos3, ":y"),

        (assign, ":scale_value", reg10),
        (convert_to_fixed_point, ":scale_value"),
        (store_mul, ":scale_value_inverse", ":scale_value", -1),
        (init_position, pos4),
        (position_set_x, pos4, ":scale_value"),
        (position_set_y, pos4, ":scale_value"),
        (position_set_z, pos4, ":scale_value"),
        (store_div, ":orientation", reg9, 256), #orientation flags
        (try_begin),
          (this_or_next|eq, ":orientation", 1),
          (eq, ":orientation", 3),
          (position_set_x, pos4, ":scale_value_inverse"),
        (try_end),
        (try_begin),
          (this_or_next|eq, ":orientation", 2),
          (eq, ":orientation", 3),
          (position_set_y, pos4, ":scale_value_inverse"),
        (try_end),
        (val_mod, reg9, 256), #remove orientation flags

        (cur_tableau_add_mesh_with_scale_and_vertex_color, reg9, pos3, pos4, 0, reg11),
      (try_end),
     ]),
           
  #script_add_troop_to_cur_tableau_for_profile
  # INPUT: troop_no
  # OUTPUT: none
  ("add_troop_to_cur_tableau_for_profile",
    [
       (store_script_param, ":troop_no",1),

       (set_fixed_point_multiplier, 100),

       (cur_tableau_clear_override_items),
       
       (cur_tableau_set_camera_parameters, 1, 4, 6, 10, 10000),

       (init_position, pos5),
       (assign, ":cam_height", 105),
#       (val_mod, ":camera_distance", 5),
       (assign, ":camera_distance", 380),
       (assign, ":camera_yaw", -15),
       (assign, ":camera_pitch", -18),
       (assign, ":animation", anim_stand_man),
       
       (position_set_z, pos5, ":cam_height"),

       # camera looks towards -z axis
       (position_rotate_x, pos5, -90),
       (position_rotate_z, pos5, 180),

       # now apply yaw and pitch
       (position_rotate_y, pos5, ":camera_yaw"),
       (position_rotate_x, pos5, ":camera_pitch"),
       (position_move_z, pos5, ":camera_distance", 0),
       (position_move_x, pos5, 5, 0),

       (profile_get_banner_id, ":profile_banner"),
       (try_begin),
         (ge, ":profile_banner", 0),
         (init_position, pos2),
         (val_add, ":profile_banner", banner_meshes_begin),
         (position_set_x, pos2, -175),
         (position_set_y, pos2, -300),
         (position_set_z, pos2, 180),
         (position_rotate_x, pos2, 90),
         (position_rotate_y, pos2, -15),
         (cur_tableau_add_mesh, ":profile_banner", pos2, 0, 0),
       (try_end),

       (init_position, pos2),
       (try_begin),
         (troop_is_hero, ":troop_no"),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", -1),
       (else_try),
         (store_mul, ":random_seed", ":troop_no", 126233),
         (val_mod, ":random_seed", 1000),
         (val_add, ":random_seed", 1),
         (cur_tableau_add_troop, ":troop_no", pos2, ":animation", ":random_seed"),
       (try_end),
       (cur_tableau_set_camera_position, pos5),

       (copy_position, pos8, pos5),
       (position_rotate_x, pos8, -90), #y axis aligned with camera now. z is up
       (position_rotate_z, pos8, 30), 
       (position_rotate_x, pos8, -60), 
       (cur_tableau_add_sun_light, pos8, 175,150,125),
     ]),
           
  # script_get_troop_custom_banner_num_positionings
  # Input: arg1 = troop_no
  # Output: reg0 = num_positionings
  ("get_troop_custom_banner_num_positionings",
    [
      (store_script_param, ":troop_no", 1),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (try_begin),
        (eq, ":num_charges", 1),
        (assign, ":num_positionings", 2),
      (else_try),
        (eq, ":num_charges", 2),
        (assign, ":num_positionings", 4),
      (else_try),
        (eq, ":num_charges", 3),
        (assign, ":num_positionings", 6),
      (else_try),
        (assign, ":num_positionings", 2),
      (try_end),
      (assign, reg0, ":num_positionings"),
     ]),

  # script_get_custom_banner_charge_type_position_scale_color
  # Input: arg1 = troop_no, arg2 = positioning_index
  # Output: reg0 = type_1
  #         reg1 = scale_1
  #         reg2 = color_1
  #         reg3 = type_2
  #         reg4 = scale_2
  #         reg5 = color_2
  #         reg6 = type_3
  #         reg7 = scale_3
  #         reg8 = color_3
  #         reg9 = type_4
  #         reg10 = scale_4
  #         reg11 = color_4
  ("get_custom_banner_charge_type_position_scale_color",
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":positioning", 2),
      (troop_get_slot, ":num_charges", ":troop_no", slot_troop_custom_banner_num_charges),
      (init_position, pos0),
      (init_position, pos1),
      (init_position, pos2),
      (init_position, pos3),

      (troop_get_slot, reg0, ":troop_no", slot_troop_custom_banner_charge_type_1),
      (val_add, reg0, custom_banner_charges_begin),
      (troop_get_slot, reg2, ":troop_no", slot_troop_custom_banner_charge_color_1),
      (troop_get_slot, reg3, ":troop_no", slot_troop_custom_banner_charge_type_2),
      (val_add, reg3, custom_banner_charges_begin),
      (troop_get_slot, reg5, ":troop_no", slot_troop_custom_banner_charge_color_2),
      (troop_get_slot, reg6, ":troop_no", slot_troop_custom_banner_charge_type_3),
      (val_add, reg6, custom_banner_charges_begin),
      (troop_get_slot, reg8, ":troop_no", slot_troop_custom_banner_charge_color_3),
      (troop_get_slot, reg9, ":troop_no", slot_troop_custom_banner_charge_type_4),
      (val_add, reg9, custom_banner_charges_begin),
      (troop_get_slot, reg11, ":troop_no", slot_troop_custom_banner_charge_color_4),

      (try_begin),
        (eq, ":num_charges", 1),
        (try_begin),
          (eq, ":positioning", 0),
          (assign, reg1, 100),
        (else_try),
          (assign, reg1, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 2),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -25),
          (position_set_x, pos1, 25),
          (assign, reg1, 40),
          (assign, reg4, 40),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
        (try_end),
      (else_try),
        (eq, ":num_charges", 3),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_y, pos0, 33),
          (position_set_y, pos2, -33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 1),
          (position_set_x, pos0, -33),
          (position_set_x, pos2, 33),
          (assign, reg1, 30),
          (assign, reg4, 30),
          (assign, reg7, 30),
        (else_try),
          (eq, ":positioning", 2),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, 30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 3),
          (position_set_x, pos0, -30),
          (position_set_y, pos0, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos2, 30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
        (else_try),
          (eq, ":positioning", 4),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, -25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (else_try),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_y, pos1, -25),
          (position_set_x, pos2, 25),
          (position_set_y, pos2, 25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
        (try_end),
      (else_try),
        (try_begin),
          (eq, ":positioning", 0),
          (position_set_x, pos0, -25),
          (position_set_y, pos0, 25),
          (position_set_x, pos1, 25),
          (position_set_y, pos1, 25),
          (position_set_x, pos2, -25),
          (position_set_y, pos2, -25),
          (position_set_x, pos3, 25),
          (position_set_y, pos3, -25),
          (assign, reg1, 50),
          (assign, reg4, 50),
          (assign, reg7, 50),
          (assign, reg10, 50),
        (else_try),
          (position_set_y, pos0, 30),
          (position_set_x, pos1, -30),
          (position_set_x, pos2, 30),
          (position_set_y, pos3, -30),
          (assign, reg1, 35),
          (assign, reg4, 35),
          (assign, reg7, 35),
          (assign, reg10, 35),
        (try_end),
      (try_end),
     ]),
           
  #script_check_creating_ladder_dust_effect
  # INPUT: arg1 = instance_id, arg2 = remaining_time
  # OUTPUT: none
  ("check_creating_ladder_dust_effect",
   [
      (store_trigger_param_1, ":instance_id"),
      (store_trigger_param_2, ":remaining_time"),

      (try_begin),
        (lt, ":remaining_time", 15), #less then 0.15 seconds
        (gt, ":remaining_time", 3), #more than 0.03 seconds
      
        (scene_prop_get_slot, ":smoke_effect_done", ":instance_id", scene_prop_smoke_effect_done),
        (scene_prop_get_slot, ":opened_or_closed", ":instance_id", scene_prop_open_or_close_slot),

        (try_begin),
          (eq, ":smoke_effect_done", 0),
          (eq, ":opened_or_closed", 0),
      
          (prop_instance_get_position, pos0, ":instance_id"),

          (assign, ":smallest_dist", -1),
          (try_for_range, ":entry_point_no", multi_entry_points_for_usable_items_start, multi_entry_points_for_usable_items_end),
            (entry_point_get_position, pos1, ":entry_point_no"),
            (get_sq_distance_between_positions, ":dist", pos0, pos1),
            (this_or_next|eq, ":smallest_dist", -1),
            (lt, ":dist", ":smallest_dist"),
            (assign, ":smallest_dist", ":dist"),
            (assign, ":nearest_entry_point", ":entry_point_no"),
          (try_end),

          (try_begin),
            (set_fixed_point_multiplier, 100),

            (ge, ":smallest_dist", 0),
            (lt, ":smallest_dist", 22500), #max 15m distance
      
            (entry_point_get_position, pos1, ":nearest_entry_point"),
            (position_rotate_x, pos1, -90),

            (prop_instance_get_scene_prop_kind, ":scene_prop_kind", ":instance_id"),
            (try_begin),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_6m"),              
              (init_position, pos2),
              (position_set_z, pos2, 300),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_6m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_6m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_8m"),
              (init_position, pos2),
              (position_set_z, pos2, 400),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_8m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_8m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_10m"),
              (init_position, pos2),
              (position_set_z, pos2, 500),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_10m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_10m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_12m"),
              (init_position, pos2),
              (position_set_z, pos2, 600),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_12m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_12m", pos3, 100),
            (else_try),
              (eq, ":scene_prop_kind", "spr_siege_ladder_move_14m"),
              (init_position, pos2),
              (position_set_z, pos2, 700),
              (position_transform_position_to_parent, pos3, pos1, pos2),
              (particle_system_burst, "psys_ladder_dust_14m", pos3, 100),
              (particle_system_burst, "psys_ladder_straw_14m", pos3, 100),
            (try_end),

            (scene_prop_set_slot, ":instance_id", scene_prop_smoke_effect_done, 1),
          (try_end),
        (try_end),
      (try_end),
      ]),
    
    ##delay_script_test
    #script_spawn_missile_at_point
    ("spawn_missile_at_point",[
      (store_script_param,":attacker_agent",1),
      (store_script_param,":agent_cur_weapon",2),
      (store_script_param,":cur_ammo_id",3),
      (store_script_param,":pos_x",4),
      (store_script_param,":pos_y",5),
      (store_script_param,":pos_z",6),
      (init_position,pos1),
      (position_set_x,pos1,":pos_x"),
      (position_set_y,pos1,":pos_y"),
      (position_set_z,pos1,":pos_z"),
      (agent_is_human,":attacker_agent"),
      (agent_is_alive,":attacker_agent"),
      (add_missile,":attacker_agent", pos1,0, ":agent_cur_weapon", imod_plain, ":cur_ammo_id",imod_plain),
    ]),
]

##delay script system begin
scripts.extend(generate_call_script_scripts(max_params_num_plus_1))
ex_scripts = [
  ##script_initialize_param_num_of_script
  ("initialize_param_num_of_script",set_num_of_params_in_each_script()),
  
  ##The scripts following can't be called by other custom scripts!
  ##script_add_script_after_seconds
  ("add_script_after_seconds",[
    (store_script_param_1,":script_id"),
    (store_script_param_2,":delay_seconds"),
    
    (val_max,":delay_seconds",1),#delay 1 seconds at least,or call the script directly,plz.
    (store_add,":time_slot_no","$cur_time_slot",":delay_seconds"),
    (try_begin),
      (ge,":time_slot_no",max_seconds_step),
      (val_mod,":time_slot_no",max_seconds_step),
    (try_end),
    (item_get_slot,":param_num","itm_param_num_of_script",":script_id"),
    (val_min,":param_num",max_params_num),
    (item_get_slot,":end_pointer","itm_delay_script_end_pointer_queue",":time_slot_no"),
    (val_max,":end_pointer",0),
    (store_add,":recorder_item_no",delay_script_slot_begin,":time_slot_no"),

    (item_set_slot,":recorder_item_no",":end_pointer",":script_id"),
    (val_add,":end_pointer",1),
    
    (try_for_range,":param_no",0,":param_num"),
      (item_get_slot,":param_val","itm_param_list",":param_no"),
      (item_set_slot,":recorder_item_no",":end_pointer",":param_val"),
      (val_add,":end_pointer",1),
    (try_end),
    (item_set_slot,"itm_delay_script_end_pointer_queue",":time_slot_no",":end_pointer"),
  ]),
  
  ##script_call_scripts_in_delay_script_queue
  ("call_scripts_in_delay_script_queue",[
    (store_script_param_1,":time_slot_no"),
    (store_add,":recorder_item_no",delay_script_slot_begin,":time_slot_no"),
    (item_get_slot,":end_pointer","itm_delay_script_end_pointer_queue",":time_slot_no"),
    (gt,":end_pointer",0),
    (assign,":true_slot_pointer",0),
    (try_for_range,":slot_pointer",0,":end_pointer"),
      (assign,":slot_pointer",":true_slot_pointer"),
      ##test begin
      (assign,reg0,":slot_pointer"),
      (display_message,"@begin:slot_pointer:{reg0}"),
      ##test end
      (item_get_slot,":script_no",":recorder_item_no",":slot_pointer"),
      (item_get_slot,":param_num","itm_param_num_of_script",":script_no"),
      (try_begin),
        (gt,":param_num",0),
        (val_min,":param_num",max_params_num),
        (try_for_range,":param_pointer",0,":param_num"),
          (val_add,":slot_pointer",1),
          (item_get_slot,":param_value",":recorder_item_no",":slot_pointer"),
          (item_set_slot,"itm_param_list",":param_pointer",":param_value"),##TODO
        (try_end),
        (assign,":call_script_script_no","script_call_script_0"),
        (val_add,":call_script_script_no",":param_num"),
        (call_script,":call_script_script_no",":script_no"),
        ##test begin
        (assign,reg0,":script_no"),
        (assign,reg1,":slot_pointer"),
        (assign,reg2,":end_pointer"),
        (display_message,"@script_no:{reg0} ,slot_pointer: {reg1},end_pointer: {reg2}"),
        ##test end
      (else_try),
        (eq,":param_num",0),
        (call_script,":call_script_script_no",":script_no"),
      (try_end),
      (val_add,":slot_pointer",1),
      #end decision
      (try_begin),
        (eq,":end_pointer",":slot_pointer"),
        (assign,":end_pointer",0),
      (else_try),
        (assign,":true_slot_pointer",":slot_pointer"),
      (try_end),
    (try_end),
    (item_set_slot,"itm_delay_script_end_pointer_queue",":time_slot_no",0),
  ]),
  
  ##script_clear_delay_script_data
  ("clear_delay_script_data",[
    (assign,"$cur_time_slot",0),
    (try_for_range,":time_slot_no",0,max_seconds_step),
      (store_add,":recorder_item_no",delay_script_slot_begin,":time_slot_no"),
      (item_get_slot,":end_pointer","itm_delay_script_end_pointer_queue",":time_slot_no"),
      (try_begin),
        (gt,":end_pointer",0),
        (try_for_range,":slot_pointer",0,":end_pointer"),
          (item_set_slot,":recorder_item_no",":slot_pointer",0),
        (try_end),
      (try_end),
      (item_set_slot,"itm_delay_script_end_pointer_queue",":time_slot_no",0),
    (try_end),
    (try_for_range,":param_slot_no",0,max_params_num),
      (item_set_slot,"itm_param_list",":param_slot_no",0),
    (try_end),
  ]),
]

scripts.extend(ex_scripts)

for i_script in xrange(len(scripts)):
  if scripts[i_script][0] == "game_start":
    statement_block = scripts[i_script][1]
    statement_block.append((call_script,"script_initialize_param_num_of_script"))
    break
##delay script system end