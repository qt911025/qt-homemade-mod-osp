from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################

game_menus = [
(
    "reserved0",mnf_disable_all_keys,
    "You approach a field where the locals are training with weapons. You can practice here to improve your combat skills.",
    "none",
    [],
    []
  ),
(
    "reserved1",mnf_disable_all_keys,
    "You approach a field where the locals are training with weapons. You can practice here to improve your combat skills.",
    "none",
    [],
    []
  ),
(
    "reserved2",mnf_disable_all_keys,
    "You approach a field where the locals are training with weapons. You can practice here to improve your combat skills.",
    "none",
    [],
    []
  ),


  (
    "tutorial",mnf_disable_all_keys,
    "You approach a field where the locals are training with weapons. You can practice here to improve your combat skills.",
    "none",
    [
      (try_begin),
        (eq, "$g_tutorial_entered", 1),
        (change_screen_quit),
      (else_try),
        (set_passage_menu, "mnu_tutorial"),
        (assign, "$g_tutorial_entered", 1),
      (try_end),
    ],
    [
      ("scene_1",[],"Automatic Test Scene",[
        (modify_visitors_at_site,"scn_random_scene"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
        (troop_set_type,"trp_player",1),
        
        (troop_clear_inventory, "trp_player"),
        (troop_add_item, "trp_player","itm_ha_cartridges",0),
        (troop_add_item, "trp_player","itm_test_rifle",0),
        (troop_equip_items, "trp_player"),
        
        (set_visitor, 0, "trp_player"),
        (set_jump_entry,0),
        (set_jump_mission,"mt_test_scene_1"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),
      ("scene_2",[],"Delay Script Scene",[
        (modify_visitors_at_site,"scn_random_scene"),
        (reset_visitors, 0),
        (set_player_troop, "trp_player"),
        (troop_set_type,"trp_player",1),
        
        (troop_clear_inventory, "trp_player"),
        (troop_add_item, "trp_player","itm_test_magic_swords",0),
        (troop_equip_items, "trp_player"),
        
        (set_visitor, 0, "trp_player"),
        (set_jump_entry,0),
        (set_jump_mission,"mt_test_scene_2"),
        (jump_to_scene, "scn_random_scene"),
        (change_screen_mission),
      ]),

      ("go_back_dot",
      [],
      "Go back.",
       [
         (change_screen_quit),
       ]),
    ]
  ),
]