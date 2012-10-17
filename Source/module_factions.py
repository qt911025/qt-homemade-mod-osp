from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################

factions = [
  ("commoners","Commoners"     ,0, 0,[],[],0xffffff),
  ("outlaws"  ,"Outlaws"       ,0, 0,[],[],0x775500),
  ("bandits"  ,"Bandits"       ,0, 0,[],[],0xff0000),
# Factions before this point are hardwired into the game end their order should not be changed.
  ("1"        ,"Purple_faction",0, 0,[],[],0x800080),
  ("2"        ,"Red_faction"   ,0, 0,[],[],0xdd0000),
  ("3"        ,"Yellow_faction",0, 0,[],[],0xdaa520),
  ("4"        ,"Black_faction" ,0, 0,[],[],0x000000),
  ("5"        ,"Green_faction" ,0, 0,[],[],0x228b22),
  ("6"        ,"Blue_faction"  ,0, 0,[],[],0x000080),
  ("factions_end","End"  ,0, 0,[],[]),
]
