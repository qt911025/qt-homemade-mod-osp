from header_common import *
from header_operations import *
from header_mission_templates import *
from header_animations import *
from header_sounds import *
from header_music import *
from header_items import *
from module_constants import *

####################################################################################################################
#   Each mission-template is a tuple that contains the following fields:
#  1) Mission-template id (string): used for referencing mission-templates in other files.
#     The prefix mt_ is automatically added before each mission-template id
#
#  2) Mission-template flags (int): See header_mission-templates.py for a list of available flags
#  3) Mission-type(int): Which mission types this mission template matches.
#     For mission-types to be used with the default party-meeting system,
#     this should be 'charge' or 'charge_with_ally' otherwise must be -1.
#     
#  4) Mission description text (string).
#  5) List of spawn records (list): Each spawn record is a tuple that contains the following fields:
#    5.1) entry-no: Troops spawned from this spawn record will use this entry
#    5.2) spawn flags.
#    5.3) alter flags. which equipment will be overriden
#    5.4) ai flags.
#    5.5) Number of troops to spawn.
#    5.6) list of equipment to add to troops spawned from here (maximum 8).
#  6) List of triggers (list).
#     See module_triggers.py for infomation about triggers.
#
#  Please note that mission templates is work in progress and can be changed in the future versions.
# 
####################################################################################################################

pilgrim_disguise = [itm_pilgrim_hood,itm_pilgrim_disguise,itm_practice_staff, itm_throwing_daggers]
af_castle_lord = af_override_horse | af_override_weapons| af_require_civilian


#multiplayer_server_spawn_bots = (
#  0, 0, 0, [],
#  [
#    (multiplayer_is_server),
#    (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
#    (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
#    (try_begin),
#      (gt, ":total_req", 0),
#
#      (try_begin),
#        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#        (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
#
#        (team_get_score, ":team_1_score", 0),
#        (team_get_score, ":team_2_score", 1),
#
#        (store_add, ":current_round", ":team_1_score", ":team_2_score"),
#        (eq, ":current_round", 0),
#
#        (store_mission_timer_a, ":round_time"),
#        (val_sub, ":round_time", "$g_round_start_time"),
#        (lt, ":round_time", 20),
#
#        (assign, ":rounded_game_first_round_time_limit_past", 0),
#      (else_try),
#        (assign, ":rounded_game_first_round_time_limit_past", 1),
#      (try_end),
#    
#      (eq, ":rounded_game_first_round_time_limit_past", 1),
#    
#      (store_random_in_range, ":random_req", 0, ":total_req"),
#      (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
#      (try_begin),
#        (lt, ":random_req", 0),
#        #add to team 1
#        (assign, ":selected_team", 0),
#      (else_try),
#        #add to team 2
#        (assign, ":selected_team", 1),
#      (try_end),
#
#      (try_begin),
#        (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#        (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#
#        (store_mission_timer_a, ":round_time"),
#        (val_sub, ":round_time", "$g_round_start_time"),
#
#        (try_begin),
#          (le, ":round_time", 20),
#          (assign, ":look_only_actives", 0),
#        (else_try),
#          (assign, ":look_only_actives", 1),
#        (try_end),
#      (else_try),
#        (assign, ":look_only_actives", 1),
#      (try_end),
#    
#      (call_script, "script_multiplayer_find_bot_troop_and_group_for_spawn", ":selected_team", ":look_only_actives"),
#      (assign, ":selected_troop", reg0),
#      (assign, ":selected_group", reg1),
#
#      (team_get_faction, ":team_faction", ":selected_team"),
#      (assign, ":num_ai_troops", 0),
#      (try_for_range, ":cur_ai_troop", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
#        (store_troop_faction, ":ai_troop_faction", ":cur_ai_troop"),
#        (eq, ":ai_troop_faction", ":team_faction"),
#        (val_add, ":num_ai_troops", 1),
#      (try_end),
#
#      (assign, ":number_of_active_players_wanted_bot", 0),
#
#      (get_max_players, ":num_players"),
#      (try_for_range, ":player_no", 0, ":num_players"),
#        (player_is_active, ":player_no"),
#        (player_get_team_no, ":player_team_no", ":player_no"),
#        (eq, ":selected_team", ":player_team_no"),
#
#        (assign, ":ai_wanted", 0),
#        (store_add, ":end_cond", slot_player_bot_type_1_wanted, ":num_ai_troops"),
#        (try_for_range, ":bot_type_wanted_slot", slot_player_bot_type_1_wanted, ":end_cond"),
#          (player_slot_ge, ":player_no", ":bot_type_wanted_slot", 1),
#          (assign, ":ai_wanted", 1),
#          (assign, ":end_cond", 0), 
#        (try_end),
#
#        (ge, ":ai_wanted", 1),
#
#        (val_add, ":number_of_active_players_wanted_bot", 1),
#      (try_end),
#
#      (try_begin),
#        (this_or_next|ge, ":selected_group", 0),
#        (eq, ":number_of_active_players_wanted_bot", 0),
#
#        (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
#        (try_begin),
#          (ge, ":has_item", 0),
#          (assign, ":is_horseman", 1),
#        (else_try),
#          (assign, ":is_horseman", 0),
#        (try_end),
#
#        (try_begin),
#          (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
#
#          (store_mission_timer_a, ":round_time"),
#          (val_sub, ":round_time", "$g_round_start_time"),
#
#          (try_begin),
#            (lt, ":round_time", 20), #at start of game spawn at base entry point
#            (try_begin),
#              (eq, ":selected_team", 0),
#              (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 1, ":is_horseman"), 
#            (else_try),
#              (assign, reg0, multi_initial_spawn_point_team_2),
#            (try_end),
#          (else_try),
#            (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
#          (try_end),
#        (else_try),
#          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#      
#          (try_begin),
#            (eq, ":selected_team", 0),
#            (assign, reg0, 0),
#          (else_try),
#            (assign, reg0, 32),
#          (try_end),
#        (else_try),
#          (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
#        (try_end),
#      
#        (store_current_scene, ":cur_scene"),
#        (modify_visitors_at_site, ":cur_scene"),
#        (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", ":selected_group"),
#        (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
#
#        (try_begin),
#          (eq, ":selected_team", 0),
#          (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
#        (else_try),
#          (eq, ":selected_team", 1),
#          (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
#        (try_end),
#      (try_end),
#    (try_end),    
#    ])
#
#multiplayer_server_manage_bots = (
#  3, 0, 0, [],
#  [
#    (multiplayer_is_server),
#    (try_for_agents, ":cur_agent"),
#      (agent_is_non_player, ":cur_agent"),
#      (agent_is_human, ":cur_agent"),
#      (agent_is_alive, ":cur_agent"),
#      (agent_get_group, ":agent_group", ":cur_agent"),
#      (try_begin),
#        (neg|player_is_active, ":agent_group"),
#        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
#      (else_try),
#        (player_get_team_no, ":leader_team_no", ":agent_group"),
#        (agent_get_team, ":agent_team", ":cur_agent"),
#        (neq, ":leader_team_no", ":agent_team"),
#        (call_script, "script_multiplayer_change_leader_of_bot", ":cur_agent"),
#      (try_end),
#    (try_end),
#    ])

multiplayer_server_check_polls = (
  1, 5, 0,
  [
    (multiplayer_is_server),
    (eq, "$g_multiplayer_poll_running", 1),
    (eq, "$g_multiplayer_poll_ended", 0),
    (store_mission_timer_a, ":mission_timer"),
    (store_add, ":total_votes", "$g_multiplayer_poll_no_count", "$g_multiplayer_poll_yes_count"),
    (this_or_next|eq, ":total_votes", "$g_multiplayer_poll_num_sent"),
    (gt, ":mission_timer", "$g_multiplayer_poll_end_time"),
    (call_script, "script_cf_multiplayer_evaluate_poll"),
    ],
  [
    (assign, "$g_multiplayer_poll_running", 0),
    (try_begin),
      (this_or_next|eq, "$g_multiplayer_poll_to_show", 0), #change map
      (eq, "$g_multiplayer_poll_to_show", 3), #change map with factions
      (call_script, "script_game_multiplayer_get_game_type_mission_template"),
      (start_multiplayer_mission, reg0, "$g_multiplayer_poll_value_to_show", 1),
      (call_script, "script_game_set_multiplayer_mission_end"),
    (try_end),
    ])
    
#multiplayer_server_check_end_map = ( 
#  1, 0, 0, [],
#  [
#    (multiplayer_is_server),
#    #checking for restarting the map
#    (assign, ":end_map", 0),
#    (try_begin),
#      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#      (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#      (eq, "$g_multiplayer_game_type", multiplayer_game_type_siege),
#    
#      (try_begin),
#        (eq, "$g_round_ended", 1),
#
#        (store_mission_timer_a, ":seconds_past_till_round_ended"),
#        (val_sub, ":seconds_past_till_round_ended", "$g_round_finish_time"),
#        (store_sub, ":multiplayer_respawn_period_minus_one", "$g_multiplayer_respawn_period", 1),
#        (ge, ":seconds_past_till_round_ended", ":multiplayer_respawn_period_minus_one"),
#  
#        (store_mission_timer_a, ":mission_timer"),    
#        (try_begin),
#          (this_or_next|eq, "$g_multiplayer_game_type", multiplayer_game_type_battle),
#          (eq, "$g_multiplayer_game_type", multiplayer_game_type_destroy),
#          (assign, ":reduce_amount", 90),
#        (else_try),
#          (assign, ":reduce_amount", 120),
#        (try_end),
#    
#        (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
#        (store_sub, ":game_max_seconds_min_n_seconds", ":game_max_seconds", ":reduce_amount"), #when round ends if there are 60 seconds to map change time then change map without completing exact map time.
#        (gt, ":mission_timer", ":game_max_seconds_min_n_seconds"),
#        (assign, ":end_map", 1),
#      (try_end),
#      
#      (eq, ":end_map", 1),
#    (else_try),
#      (neq, "$g_multiplayer_game_type", multiplayer_game_type_battle), #battle mod has different end map condition by time
#      (neq, "$g_multiplayer_game_type", multiplayer_game_type_destroy), #fight and destroy mod has different end map condition by time
#      (neq, "$g_multiplayer_game_type", multiplayer_game_type_siege), #siege mod has different end map condition by time
#      (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #in headquarters mod game cannot limited by time, only can be limited by score.
#      (store_mission_timer_a, ":mission_timer"),
#      (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
#      (gt, ":mission_timer", ":game_max_seconds"),
#      (assign, ":end_map", 1),
#    (else_try),
#      #assuming only 2 teams in scene
#      (team_get_score, ":team_1_score", 0),
#      (team_get_score, ":team_2_score", 1),
#      (try_begin),
#        (neq, "$g_multiplayer_game_type", multiplayer_game_type_headquarters), #for not-headquarters mods
#        (try_begin),
#          (this_or_next|ge, ":team_1_score", "$g_multiplayer_game_max_points"),
#          (ge, ":team_2_score", "$g_multiplayer_game_max_points"),
#          (assign, ":end_map", 1),
#        (try_end),
#      (else_try),
#        (assign, ":at_least_one_player_is_at_game", 0),
#        (get_max_players, ":num_players"),
#        (try_for_range, ":player_no", 0, ":num_players"),
#          (player_is_active, ":player_no"),
#          (player_get_agent_id, ":agent_id", ":player_no"),
#          (ge, ":agent_id", 0),
#          (neg|agent_is_non_player, ":agent_id"),
#          (assign, ":at_least_one_player_is_at_game", 1),
#          (assign, ":num_players", 0),
#        (try_end),
#    
#        (eq, ":at_least_one_player_is_at_game", 1),
#
#        (this_or_next|le, ":team_1_score", 0), #in headquarters game ends only if one team has 0 score.
#        (le, ":team_2_score", 0),
#        (assign, ":end_map", 1),
#      (try_end),
#    (try_end),
#    (try_begin),
#      (eq, ":end_map", 1),
#      (call_script, "script_game_multiplayer_get_game_type_mission_template"),
#      (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
#      (call_script, "script_game_set_multiplayer_mission_end"),           
#    (try_end),
#    ])

multiplayer_once_at_the_first_frame = (
  0, 0, ti_once, [], [
    (start_presentation, "prsnt_multiplayer_welcome_message"),
    ])

multiplayer_battle_window_opened = (
  ti_battle_window_opened, 0, 0, [], [
    (start_presentation, "prsnt_multiplayer_team_score_display"),
    ])

common_battle_init_banner = (
  ti_on_agent_spawn, 0, 0, [],
  [
    (store_trigger_param_1, ":agent_no"),
    (agent_get_troop_id, ":troop_no", ":agent_no"),
    (call_script, "script_troop_agent_set_banner", "tableau_game_troop_label_banner", ":agent_no", ":troop_no"),
  ])

##New automatic begin
common_automatic = (
	0.1,0,0,[],[
		(try_for_agents,":attacker_agent"),
			(agent_is_human,":attacker_agent"),
			(agent_is_alive,":attacker_agent"),
			(agent_get_wielded_item,":agent_cur_weapon",":attacker_agent"),
			(gt,":agent_cur_weapon",0),
			(agent_get_attack_action, ":action_state", ":attacker_agent"),
			(try_begin),
				(eq,":action_state",1),
        (item_get_type, ":item_type", ":agent_cur_weapon"),
        (eq,":item_type",itp_type_musket),
                
				#ticker trigger
				(agent_get_slot,":ticker_time",":attacker_agent",slot_agent_shoot_time_ticker),
				(try_begin),
					(le,":ticker_time",0),
					#ticker trigger
					(item_get_slot,":ticker_time",":agent_cur_weapon",slot_item_speed_rtng),
          (val_max,":ticker_time",1),
					(store_div,":ticker_time",200,":ticker_time"),
					(agent_set_slot,":attacker_agent",slot_agent_shoot_time_ticker,":ticker_time"),
          (agent_get_item_cur_ammo, ":cur_ammo", ":attacker_agent"),
					(gt,":cur_ammo",0),
                    
          #match the right ammmo type
          (assign,":cur_ammo_id",-1),
          (assign,":item_slot_num",4),
          (try_for_range,":cur_item_slot",0,":item_slot_num"),
            (agent_get_item_slot, ":item_no", ":attacker_agent", ":cur_item_slot"),
            (ge,":cur_ammo_id",0),
            (item_get_type, ":item_type", ":item_no"),
            (eq,":item_type",itp_type_bullets),
            (assign,":cur_ammo_id",":item_no"),
            (assign,":item_slot_num",0),#break
          (try_end),
          (try_begin),
            (lt,":cur_ammo_id",0),
            (assign,":cur_ammo_id","itm_ha_cartridges"),#as default
          (try_end),

					#get original position of weapon
					(agent_get_look_position,pos24,":attacker_agent"),
					(item_get_slot,":length",":agent_cur_weapon",slot_item_length),
					(position_move_y, pos24,":length"),
					(agent_get_horse,":attacker_agent_horse",":attacker_agent"),
          (agent_get_animation, ":attacker_animation", ":attacker_agent", 0),
					(try_begin),
            (this_or_next|eq,":attacker_animation","anim_walk_forward_crouch"),
            (eq,":attacker_animation","anim_stand_to_crouch"),
            (position_move_z,pos24,115,1),
          (else_try),
						(lt,":attacker_agent_horse",0),
						(position_move_z,pos24,170,1),
					(else_try),
						(position_move_z,pos24,270,1),
					(try_end),

					##get weapon position after calculating accuracy
					(copy_position,pos25,pos24),
					(item_get_slot,":accuracy",":agent_cur_weapon",slot_item_accuracy),
          (val_max,":accuracy",1),
					(store_div,":randomize_value",500,":accuracy"),
					(store_random_in_range,":z",0,":randomize_value"),
					(store_random_in_range,":x",0,":randomize_value"),
					(position_rotate_z,pos25,":z"),
					(position_rotate_x,pos25,":x"),

					#create particle,animation and sound effect of weapon
					(agent_set_animation, ":attacker_agent", "anim_release_musket", 1),
					(item_get_slot,":shoot_sound",":agent_cur_weapon",slot_item_shot_sound),
                    
					(play_sound_at_position, ":shoot_sound", pos24),
					(particle_system_burst, "psys_rifle_smoke", pos24, 10),
					(particle_system_burst, "psys_gun_fire", pos24, 20),
                    
          (item_get_slot,":shoot_speed",":agent_cur_weapon",slot_item_shoot_speed),
          (set_fixed_point_multiplier,1),
          (add_missile, ":attacker_agent", pos25, ":shoot_speed", ":agent_cur_weapon", imod_plain, ":cur_ammo_id",imod_plain),

					#reduce ammo
					(val_sub,":cur_ammo",1),
					(agent_set_ammo,":attacker_agent",":agent_cur_weapon",":cur_ammo"),
				(else_try),
					(val_sub,":ticker_time",1),
					(agent_set_slot,":attacker_agent",slot_agent_shoot_time_ticker,":ticker_time"),
				(try_end),
			(else_try),
				(agent_get_defend_action, ":defend_action_state", ":attacker_agent"),
				(this_or_next|gt,":defend_action_state",0),
				(gt,":action_state",1),
        (item_get_slot,":ticker_time",":agent_cur_weapon",slot_item_speed_rtng),
        (val_max,":ticker_time",1),
				(store_div,":ticker_time",800,":ticker_time"),
				(agent_set_slot,":attacker_agent",slot_agent_shoot_time_ticker,":ticker_time"),
			(try_end),
		(try_end),
	]
)
#New automatics end
#delay script system begin
common_init_delay_script = (ti_before_mission_start, 0, 0, [],
 [
  (call_script,"script_initialize_param_num_of_script"),#this statement is just for this mod only,because this mod has not sp mode.
  (call_script,"script_clear_delay_script_data"),
 ]
)
common_delay_script = (delay_script_call_interval, 0, 0, [],
 [
  (val_add,"$cur_time_slot",1),
  (try_begin),
    (ge,"$cur_time_slot",max_seconds_step),
    (val_mod,"$cur_time_slot",max_seconds_step),
  (try_end),
  (call_script,"script_call_scripts_in_delay_script_queue","$cur_time_slot"),
 ]
)
#delay script system end

tournament_triggers = []

mission_templates = [
    (
    "conquest",mtf_battle_mode,-1, #Warlords mode
    "Make your life!",
    [
      (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (8,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (9,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (10,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (11,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (12,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (13,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (14,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (15,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (16,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (17,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (18,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (19,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (20,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (21,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (22,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (23,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (24,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (25,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (26,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (27,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (28,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (29,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (30,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
      (31,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

      (32,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (33,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (34,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (35,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (36,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (37,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (38,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (39,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (40,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (41,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (42,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (43,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (44,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (45,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (46,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (47,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (48,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (49,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (50,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (51,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (52,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (53,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (54,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (55,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

      (56,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (57,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (58,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (59,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (60,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (61,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (62,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
      (63,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
     ],
    [
      #multiplayer_server_check_belfry_movement,      
     
      multiplayer_server_check_polls,

      (ti_on_agent_spawn, 0, 0, [],
       [
         (store_trigger_param_1, ":agent_no"),
         (call_script, "script_multiplayer_server_on_agent_spawn_common", ":agent_no"),
         ]),

      (ti_server_player_joined, 0, 0, [],
       [
         (store_trigger_param_1, ":player_no"),
         (call_script, "script_multiplayer_server_player_joined_common", ":player_no"),
         ]),

      (ti_before_mission_start, 0, 0, [],
       [
         (assign, "$g_multiplayer_game_type", multiplayer_game_type_conquest),
         (call_script, "script_multiplayer_server_before_mission_start_common"),
         
         (multiplayer_make_everyone_enemy),

         (call_script, "script_multiplayer_init_mission_variables"),
         (call_script, "script_multiplayer_remove_destroy_mod_targets"),
#         (call_script, "script_multiplayer_remove_headquarters_flags"), # close this line and open map in deathmatch mod and use all ladders firstly 
         ]),                                                            # to be able to edit maps without damaging any headquarters flags ext. 

      (ti_after_mission_start, 0, 0, [], 
       [
         (set_spawn_effector_scene_prop_kind, 0, -1), #during this mission, agents of "team 0" will try to spawn around scene props with kind equal to -1(no effector for this mod)
         (set_spawn_effector_scene_prop_kind, 1, -1), #during this mission, agents of "team 1" will try to spawn around scene props with kind equal to -1(no effector for this mod)

         (call_script, "script_initialize_all_scene_prop_slots"),
         
         (call_script, "script_multiplayer_move_moveable_objects_initial_positions"),

         (assign, "$g_multiplayer_ready_for_spawning_agent", 1),
         ]),

      (ti_on_multiplayer_mission_end, 0, 0, [],
       [
         #ELITE_WARRIOR achievement
         (try_begin),
           (multiplayer_get_my_player, ":my_player_no"),
           (is_between, ":my_player_no", 0, multiplayer_max_possible_player_id),
           (player_get_team_no, ":my_player_team", ":my_player_no"),
           (lt, ":my_player_team", multi_team_spectator),
           (player_get_kill_count, ":kill_count", ":my_player_no"),
           (player_get_death_count, ":death_count", ":my_player_no"),
           (store_mul, ":my_score_plus_death", ":kill_count", 1000),
           (val_sub, ":my_score_plus_death", ":death_count"),
           (assign, ":continue", 1),
           (get_max_players, ":num_players"),
           (assign, ":end_cond", ":num_players"),
           (try_for_range, ":player_no", 0, ":end_cond"),
             (player_is_active, ":player_no"),
             (player_get_team_no, ":player_team", ":player_no"),
             (this_or_next|eq, ":player_team", 0),
             (eq, ":player_team", 1),
             (player_get_kill_count, ":kill_count", ":player_no"),
             (player_get_death_count, ":death_count", ":player_no"), #get_death_count
             (store_mul, ":player_score_plus_death", ":kill_count", 1000),
             (val_sub, ":player_score_plus_death", ":death_count"),
             (gt, ":player_score_plus_death", ":my_score_plus_death"),
             (assign, ":continue", 0),
             (assign, ":end_cond", 0), #break
           (try_end),
           (eq, ":continue", 1),
           (unlock_achievement, ACHIEVEMENT_ELITE_WARRIOR),
         (try_end),
         #ELITE_WARRIOR achievement end

         (call_script, "script_multiplayer_event_mission_end"),

#         (assign, "$g_multiplayer_stats_chart_opened_manually", 0),
#         (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
         ]),

      (ti_on_agent_killed_or_wounded, 0, 0, [],
       [
         (store_trigger_param_1, ":dead_agent_no"), 
         (store_trigger_param_2, ":killer_agent_no"),
         (call_script, "script_multiplayer_server_on_agent_killed_or_wounded_common", ":dead_agent_no", ":killer_agent_no"),
         ]),
      
      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         (get_max_players, ":num_players"),
         (try_for_range, ":player_no", 0, ":num_players"),
           (player_is_active, ":player_no"),
           (neg|player_is_busy_with_menus, ":player_no"),

           (player_get_team_no, ":player_team", ":player_no"), #if player is currently spectator do not spawn his agent
           (lt, ":player_team", multi_team_spectator),

           (player_get_troop_id, ":player_troop", ":player_no"), #if troop is not selected do not spawn his agent
           (ge, ":player_troop", 0),

           (player_get_agent_id, ":player_agent", ":player_no"),
           (assign, ":spawn_new", 0),
           (try_begin),
             (player_get_slot, ":player_first_spawn", ":player_no", slot_player_first_spawn),
             (eq, ":player_first_spawn", 1),
             (assign, ":spawn_new", 1),
             (player_set_slot, ":player_no", slot_player_first_spawn, 0),
           (else_try),
             (try_begin),
               (lt, ":player_agent", 0),
               (assign, ":spawn_new", 1),
             (else_try),
               (neg|agent_is_alive, ":player_agent"),
               (agent_get_time_elapsed_since_removed, ":elapsed_time", ":player_agent"),
               (gt, ":elapsed_time", "$g_multiplayer_respawn_period"),
               (assign, ":spawn_new", 1),
             (try_end),             
           (try_end),
           (eq, ":spawn_new", 1),
           (call_script, "script_multiplayer_buy_agent_equipment", ":player_no"),

           (troop_get_inventory_slot, ":has_item", ":player_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),
         
           (call_script, "script_multiplayer_find_spawn_point", ":player_team", 0, ":is_horseman"), 
           (player_spawn_new_agent, ":player_no", reg0),
         (try_end),
         ]),

      (1, 0, 0, [], #do this in every new frame, but not at the same time
       [
         (multiplayer_is_server),
         (store_mission_timer_a, ":mission_timer"),
         (ge, ":mission_timer", 2),
         (assign, ":team_1_count", 0),
         (assign, ":team_2_count", 0),
         (try_for_agents, ":cur_agent"),
           (agent_is_non_player, ":cur_agent"),
           (agent_is_human, ":cur_agent"),
           (assign, ":will_be_counted", 0),
           (try_begin),
             (agent_is_alive, ":cur_agent"),
             (assign, ":will_be_counted", 1), #alive so will be counted
           (else_try),
             (agent_get_time_elapsed_since_removed, ":elapsed_time", ":cur_agent"),
             (le, ":elapsed_time", "$g_multiplayer_respawn_period"),
             (assign, ":will_be_counted", 1), 
           (try_end),
           (eq, ":will_be_counted", 1),
           (agent_get_team, ":cur_team", ":cur_agent"),
           (try_begin),
             (eq, ":cur_team", 0),
             (val_add, ":team_1_count", 1),
           (else_try),
             (eq, ":cur_team", 1),
             (val_add, ":team_2_count", 1),
           (try_end),
         (try_end),
         (store_sub, "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_team_1", ":team_1_count"),
         (store_sub, "$g_multiplayer_num_bots_required_team_2", "$g_multiplayer_num_bots_team_2", ":team_2_count"),
         (val_max, "$g_multiplayer_num_bots_required_team_1", 0),
         (val_max, "$g_multiplayer_num_bots_required_team_2", 0),
         ]),

      (0, 0, 0, [],
       [
         (multiplayer_is_server),
         (eq, "$g_multiplayer_ready_for_spawning_agent", 1),
         (store_add, ":total_req", "$g_multiplayer_num_bots_required_team_1", "$g_multiplayer_num_bots_required_team_2"),
         (try_begin),
           (gt, ":total_req", 0),
           (store_random_in_range, ":random_req", 0, ":total_req"),
           (val_sub, ":random_req", "$g_multiplayer_num_bots_required_team_1"),
           (try_begin),
             (lt, ":random_req", 0),
             #add to team 1
             (assign, ":selected_team", 0),
             (val_sub, "$g_multiplayer_num_bots_required_team_1", 1),
           (else_try),
             #add to team 2
             (assign, ":selected_team", 1),
             (val_sub, "$g_multiplayer_num_bots_required_team_2", 1),
           (try_end),

           (team_get_faction, ":team_faction_no", ":selected_team"),
           (assign, ":available_troops_in_faction", 0),

           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, multiplayer_ai_troops_end),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_add, ":available_troops_in_faction", 1),
           (try_end),

           (store_random_in_range, ":random_troop_index", 0, ":available_troops_in_faction"),
           (assign, ":end_cond", multiplayer_ai_troops_end),
           (try_for_range, ":troop_no", multiplayer_ai_troops_begin, ":end_cond"),
             (store_troop_faction, ":troop_faction", ":troop_no"),
             (eq, ":troop_faction", ":team_faction_no"),
             (val_sub, ":random_troop_index", 1),
             (lt, ":random_troop_index", 0),
             (assign, ":end_cond", 0),
             (assign, ":selected_troop", ":troop_no"),
           (try_end),
         
           (troop_get_inventory_slot, ":has_item", ":selected_troop", ek_horse),
           (try_begin),
             (ge, ":has_item", 0),
             (assign, ":is_horseman", 1),
           (else_try),
             (assign, ":is_horseman", 0),
           (try_end),

           (call_script, "script_multiplayer_find_spawn_point", ":selected_team", 0, ":is_horseman"), 
           (store_current_scene, ":cur_scene"),
           (modify_visitors_at_site, ":cur_scene"),
           (add_visitors_to_current_scene, reg0, ":selected_troop", 1, ":selected_team", -1),
           (assign, "$g_multiplayer_ready_for_spawning_agent", 0),
         (try_end),
         ]),

      (1, 0, 0, [],
       [
         (multiplayer_is_server),
         #checking for restarting the map
         (assign, ":end_map", 0),
         (try_begin),
           (store_mission_timer_a, ":mission_timer"),
           (store_mul, ":game_max_seconds", "$g_multiplayer_game_max_minutes", 60),
           (gt, ":mission_timer", ":game_max_seconds"),
           (assign, ":end_map", 1),
         (try_end),
         (try_begin),
           (eq, ":end_map", 1),
           (call_script, "script_game_multiplayer_get_game_type_mission_template"),
           (start_multiplayer_mission, reg0, "$g_multiplayer_selected_map", 0),
           (call_script, "script_game_set_multiplayer_mission_end"),
         (try_end),
         ]),
        
#      (ti_tab_pressed, 0, 0, [],
#       [
#         (try_begin),
#           (eq, "$g_multiplayer_mission_end_screen", 0),
#           (assign, "$g_multiplayer_stats_chart_opened_manually", 1),
#           (start_presentation, "prsnt_multiplayer_stats_chart_deathmatch"),
#         (try_end),
#         ]),

      multiplayer_once_at_the_first_frame,
      
      (ti_escape_pressed, 0, 0, [],
       [
         (neg|is_presentation_active, "prsnt_multiplayer_escape_menu"),
#         (neg|is_presentation_active, "prsnt_multiplayer_stats_chart_deathmatch"),
         (eq, "$g_waiting_for_confirmation_to_terminate", 0),
         (start_presentation, "prsnt_multiplayer_escape_menu"),
         ]),
      ],
  ),


 (
   "test_scene_1",mtf_battle_mode|mtf_synch_inventory,-1,
   "test scene 1",
   [
 (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[itm_test_rifle,itm_ha_cartridges]),
 (1,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[itm_test_rifle,itm_ha_cartridges]),
],
[
#	(0,0,0,[(key_clicked,key_b)],
#	[
#		(get_player_agent_no, ":player_agent"),
#		(agent_get_position, pos0, ":player_agent"),
#		(set_spawn_position, pos0),
#		(spawn_scene_prop, "spr_catapult_destructible"),
#	],
#	),
	
#	(0,0,0,[(key_clicked,key_n)],
#	[
#		(display_log_message,"@Printing agents information:"),
#		(try_for_agents,":agent_no"),
#			(str_clear,s0),
#			(assign,reg0,":agent_no"),
#			(str_store_string,s0,"@ ID: {reg0} Agent name: "),
#			(display_log_message,s0),
#			(str_store_agent_name,s0,":agent_no"),
#			(display_log_message,s0),
#			(try_begin),
#				(neg|agent_is_non_player,":agent_no"),
#				(str_store_string,s0,"@ Agent is player"),
#				(display_log_message,s0),
#			(try_end),
#			(try_begin),
#				(agent_is_ally,":agent_no"),
#				(str_store_string,s0,"@ Agent is ally"),
#				(display_log_message,s0),
#			(try_end),
#		(try_end),
#	],
#	),
	(0,0,0,[(key_clicked,key_j)],
	[
		(add_visitors_to_current_scene,0,"trp_test_troop",50, mtef_team_0, 0),
	],
	),
    (0,0,0,[(key_clicked,key_k)],
    [
    	(add_visitors_to_current_scene,1,"trp_test_troop",50, mtef_team_1, 0),
    ],
    ),    
	##tab pressed
  	(ti_tab_pressed, 0, 0, [],
  	 [
		(finish_mission,0),
		],
	),
#	automatic_player,
    common_automatic,
    ],
 ),
 (
   "test_scene_2",mtf_battle_mode|mtf_synch_inventory,-1,
   "test scene 2",
   [
 (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[itm_test_rifle,itm_ha_cartridges]),
 (1,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[itm_test_rifle,itm_ha_cartridges]),
],
[
#	(0,0,0,[(key_clicked,key_b)],
#	[
#		(get_player_agent_no, ":player_agent"),
#		(agent_get_position, pos0, ":player_agent"),
#		(set_spawn_position, pos0),
#		(spawn_scene_prop, "spr_catapult_destructible"),
#	],
#	),
	
#	(0,0,0,[(key_clicked,key_n)],
#	[
#		(display_log_message,"@Printing agents information:"),
#		(try_for_agents,":agent_no"),
#			(str_clear,s0),
#			(assign,reg0,":agent_no"),
#			(str_store_string,s0,"@ ID: {reg0} Agent name: "),
#			(display_log_message,s0),
#			(str_store_agent_name,s0,":agent_no"),
#			(display_log_message,s0),
#			(try_begin),
#				(neg|agent_is_non_player,":agent_no"),
#				(str_store_string,s0,"@ Agent is player"),
#				(display_log_message,s0),
#			(try_end),
#			(try_begin),
#				(agent_is_ally,":agent_no"),
#				(str_store_string,s0,"@ Agent is ally"),
#				(display_log_message,s0),
#			(try_end),
#		(try_end),
#	],
#	),
	(0,0,0,[(key_clicked,key_j)],
	[
		(add_visitors_to_current_scene,0,"trp_test_troop",50, mtef_team_0, 0),
	],
	),
    (0,0,0,[(key_clicked,key_k)],
    [
    	(add_visitors_to_current_scene,1,"trp_test_troop",50, mtef_team_1, 0),
    ],
    ),    
    (0,0,0,[(key_clicked,key_b)],
    [
    	(get_player_agent_no, ":player_agent"),
      (agent_get_position, pos0, ":player_agent"),
      (init_position,pos1),
      (position_copy_origin,pos1,pos0),
      (position_get_x,":pos_x",pos1),
      (position_get_y,":pos_y",pos1),
      (position_get_z,":pos_z",pos1),
      (val_add,":pos_z",200),
      (call_script,"script_spawn_missile_at_point",":player_agent","itm_test_magic_swords_sub","itm_test_magic_swords_sub",":pos_x",":pos_y",":pos_z"),
    ],
    ),  
	##tab pressed
  	(ti_tab_pressed, 0, 0, [],
  	 [
		(finish_mission,0),
		],
	),
#	automatic_player,
    common_automatic,
    common_init_delay_script,
    common_delay_script
    ],
 ),
]
