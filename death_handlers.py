import tcod as libtcod

from game_states import GameStates


def kill_player(player):
    player.char = "%"
    player.color = libtcod.dark_red

    return "You Died!", GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = f"{monster.name.capitalize()} is dead!"

    monster.char = "%"
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = f"remains of {monster.name}" 

    return death_message
