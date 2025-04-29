# You are my rival
import inflect, sys



from characters.wizzards import (
    AntimagicWizzard,
    WindWizzard,
    HealerWizzard,
    SpatialWizzard,
    WaterWizzard,
    FireWizzard,
)
from mechanics.logic import (
    choosePlayer,
    chooseTeam,
    rivals,
    update_history,
    previewUI,
    new_ia,
    new_UI,
    careful,
    winnersUI,
    new_chooseUI,
    playersUI,
)

order = inflect.engine()
blue_color = "\033[94m"
reset_color = "\033[00m"
green_color = "\033[92m"
red_color = "\033[91m"


Asta = AntimagicWizzard(
    "Asta",
    attack_level=15,
    mana=120,
    class_power=30,
    description="I'll be the wizzard king",
)
Yuno = WindWizzard(
    "Yuno", attack_level=20, mana=120, class_power=40, description="Im Mr. cool"
)
Finral = SpatialWizzard(
    "Finral", attack_level=14, mana=120, class_power=28, description="Im so tired"
)
Mimosa = HealerWizzard(
    "Mimosa",
    attack_level=13,
    mana=120,
    class_power=40,
    description="Kindness blooms even in battle.",
)
Noelle = WaterWizzard(
    "Noelle",
    attack_level=15,
    mana=120,
    class_power=40,
    description="Im royalty, you know?",
)
Magna = FireWizzard(
    "Magna", attack_level=10, mana=90, class_power=20, description="I am a great man"
)
Koren = FireWizzard(
    "Koren", attack_level=20, mana=120, class_power=30, description="main kit"
)


characters = [Asta, Yuno, Mimosa, Finral, Noelle, Magna, Koren]
previewUI()
number = playersUI()
two_players = False
if number == 2:
    player = choosePlayer(characters, 'team blue')
    team = chooseTeam(characters)
    rival = choosePlayer(characters, 'team blue')
    rival_team = chooseTeam(characters)
    two_players = True
if number == 1:
    player = choosePlayer(characters, 'team blue')
    team = chooseTeam(characters)
    rival_team, rival = rivals(characters)
rival_team.color = "[red]"
team.color = "[blue]"
team.reset_color = "[/blue]"
rival_team.reset_color = "[/red]"
rival.color = "[red]"
rival.reset_color = "[/red]"
player.color = "[blue]"
player.reset_color = "[/blue]"
characters = [Asta, Yuno, Mimosa, Finral, Noelle, Magna, Koren]

way = [player, rival_team, team, rival]
blue_team = [player, team]
team_blue = blue_team[:]
red_team = [rival_team, rival]
team_red = red_team[:]
record = []
round = 0

while True:
    round += 1
    for current in way[:]:
        if not team_red:
            print(f"Congratulations to the winners {[x.name for x in team_blue]}")
            winnersUI(team_blue)
            sys.exit("")
            break
        if not team_blue:
            print(f"Congratulations to the winners {[x.name for x in team_red]}")
            winnersUI(team_red)
            sys.exit("")
            break
        current.mana_regeneration()
        for h in way:
            effect_value = h.update_effects()
            if effect_value:
                record.extend(effect_value)
        new_UI(player, team, rival_team, rival, record, round)
        if current == player and player.health > 0 or two_players and current == rival and rival.health > 0:
            while True:
                new_UI(player, team, rival_team, rival, record, round)
                new_chooseUI(current)
                chose = input('')
                chose = careful(chose)
                if chose in current.new_data:
                    break
            new = chose.replace(" ", "_")
            move = getattr(current, new)
            if current.new_data[chose]["target"] == "all enemies":
                value = move(red_team)
            elif not current.new_data[chose]["target"] == "self":
                while True:
                    name = input("In who are you going to apply your move?\n")
                    name = careful(name)
                    for j in characters:
                        if name == j.name:
                            name = j
                    if not type(name) == type("s"):
                        break
                value = move(name)
            else:
                value = move()
            update_history(value, record)
        elif current.health > 0:
            if current in blue_team:
                belongs_to = blue_team
                opponents = red_team
            else:
                belongs_to = red_team
                opponents = blue_team
            input(f"Its {green_color}{current.name}{reset_color} turn")
            new_moves = current.moves[:]
            value = new_ia(current, team_blue, team_red)
            update_history(value, record)
        else:
            if current in team_blue:
                team_blue.remove(current)
            if current in team_red:
                team_red.remove(current)
