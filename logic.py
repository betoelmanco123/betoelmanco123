import random, inflect, os, re, time, copy
from pyfiglet import Figlet
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

order = inflect.engine()
figlet = Figlet()
console = Console()

class_color_rich = {
    "AntimagicWizzard": "dark_orange",  # o "orange3"
    "WaterWizzard": "bright_blue",  # vibrante y mágico
    "WindWizzard": "sea_green3",  # verde claro
    "HealerWizzard": "green3",  # saludable y natural
    "SpatialWizzard": "bright_black",  # como un gris elegante
    "FireWizzard": "bright_red",  # intenso y claro
}


def chooseTeam(caracters):
    while True:
        team = input(f"Chose a caracter to team with:\n")
        team = careful(team)
        for k in caracters:
            if k.name == team:
                team = k
                caracters.remove(k)
                return team

def careful(name):
    value = name.strip()
    player = value.capitalize()
    return player
def choosePlayer(caracters, team):
    show_two_cards(caracters)
    while True:
        name = input(f"Chose a caracter to play with: {team}\n")
        player = careful(name)
        for i in caracters:
            if i.name == player:
                player = i
                caracters.remove(i)
                return player


def rivals(caracters):
    rival0 = random.choice(caracters)
    caracters.remove(rival0)
    rival = random.choice(caracters)
    caracters.remove(rival)
    return rival0, rival


def clean_screen():
    os.system("clear")


def new_ia(current, team_blue, team_red):
    if current in team_blue:
        enemy_team = team_red
        belongs_to = team_blue
    if current in team_red:
        enemy_team = team_blue
        belongs_to = team_red
    target = False
    action = False
    avaiable_moves = copy.deepcopy(current.new_data)
    # Delete all moves that cost more mana than avaiable
    avaiable_moves = {
        k: v for k, v in avaiable_moves.items() if v["mana cost"] < current.mana
    }
    # Return rest if current mana is less or equal 9
    if current.mana <= 9:
        action = "Rest"
    # Delete reset if current mana is equal to de maximun mana
    if current.mana == current.maximun_mana and not action:
        avaiable_moves.pop("Rest", None)
    # Delete all self healing spells if current have all health
    if current.health == current.maximun_life and not action:
        avaiable_moves = {
            k: v
            for k, v in avaiable_moves.items()
            if not (v["target"] == "self" and v.get("effect") == "healing")
        }
    # If self have less than 40 points of health will try to use a self healing spell
    if current.health <= 40 and not action:
        avaiable_heal_moves = {
            k: v
            for k, v in avaiable_moves.items()
            if v["target"] == "self" and v.get("effect") == "healing"
        }
        if avaiable_heal_moves:
            avaiable_moves = avaiable_heal_moves
    # if current can kill a rival he'll do it
    if not action:
        for k, v in avaiable_moves.items():
            if v.get("target") == "enemy" and v.get("effect") == "damage":
                for i in enemy_team:
                    if v['amount'] >= i.health:
                        target = i

    if not action:
        action = random.choice(list(avaiable_moves.keys()))
    new_action = action
    if " " in new_action:
        new_action = new_action.replace(" ", "_")
    move = getattr(current, new_action)
    if avaiable_moves[action]["target"] == "self":
        value = move()
        return value
    if not target:
        if avaiable_moves[action]["target"] == "enemy":
            choices = enemy_team
        if avaiable_moves[action]["target"] == "ally":
            choices = belongs_to
        if avaiable_moves[action]["target"] == "all enemies":
            target = enemy_team
            value = move(target)
            return value
        target = random.choice(choices)
    value = move(target)
    return value


def ansi_ljust(s, width):
    padding = width - visible_length(s)
    return s + " " * max(padding, 0)


def visible_length(s):

    return len(re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", s))




def update_history(value, history):
    if value is None:
        print("El problema esta aqui")
        return
    if isinstance(value, str):
        history.append(value)
    else:
        history.extend(value)


def new_chooseUI(current):
    new_moves1 = current.new_data
    new_moves = dict(sorted(new_moves1.items(), key=lambda item: item[1]['mana cost']))
    choose = Table.grid(padding=(0,3))
    choose.add_column()
    choose.add_column()
    choose.add_column()
    choose.add_row(spells_UI(new_moves), description_UI(new_moves),mana_UI(new_moves))

    console.print(choose)


def spells_UI(new_moves):
    choose = Table.grid()
    choose.add_column()
    for i in new_moves:
        choose.add_row(i)
    value = Panel(
        choose,
        title='Spells',
        border_style='bright_yellow',
        box=box.ROUNDED,
    )

    return value

def mana_UI(new_moves):
    choose = Table.grid()
    choose.add_column(justify='center')
    for i in new_moves:
        choose.add_row(str(new_moves[i]['mana cost']))
    mana = Panel(
        choose,
        title='Mana',
        border_style='bright_yellow',
        box=box.ROUNDED,
    )

    return mana

def description_UI(new_moves):
    choose = Table.grid()
    choose.add_column()
    for i in new_moves:
        choose.add_row(new_moves[i]['description'])
    description = Panel(
        choose,
        title='Description',
        border_style='bright_yellow',
        box=box.ROUNDED,
    )

    return description
def previewUI():
    clean_screen()
    print(figlet.renderText("Black Clover"))
    print(f"\n" * 20)
    print(f"Welcome to Black Clover duel game")
    input(f"Press any button to start the game")
    clean_screen()

def mini_tables(player, team, title, color):
    teams_stats = Table.grid(padding=1)
    teams_stats.add_column()
    teams_stats.add_row(f'{player.name} | {player.__class__.__name__}')
    teams_stats.add_row(player.bar("health"))
    teams_stats.add_row(player.bar('mana'))
    if player.effects:
        for w in player.effects:
            if not w['type'] == 'default':
                teams_stats.add_row(f'{w["name"]} : {w["amount"]}')
    teams_stats.add_row(f'{team.name} | {team.__class__.__name__}')
    teams_stats.add_row(team.bar('health'))
    teams_stats.add_row(team.bar('mana'))
    if team.effects:
        for w in team.effects:
            if not w['type'] == 'default':
                teams_stats.add_row(f'{w["name"]} : {w["amount"]}')
    supernew = Panel(
        teams_stats,
        title=title,
        border_style=color,
        box=box.ROUNDED,
        width=40,
    )
    return supernew

def new_UI(player, team, rival0, rival, record, round):
    while len(record) >= 25:
        record.pop(0)
    clean_screen()
    supernew = mini_tables(player, team, 'Blue Team', 'bright_blue')
    enemy = mini_tables(rival0, rival, 'Red Team', 'bright_red')
    stats = Table.grid(expand=True)
    stats.add_column()
    stats.add_row(supernew)
    stats.add_row(enemy)
    # Create the table for the history
    history =  Table.grid()
    history.add_column()
    subtitle = f'Round {round}'
    for p in record:
        history.add_row(p)
    complete = Panel(
        history,
        title='record',
        subtitle=subtitle,
        border_style="steel_blue",
        box=box.ROUNDED,
    )

    background = Table.grid(expand=True)
    background.add_column(ratio=2)
    background.add_column(ratio=6)
    background.add_row(stats, complete)
    console.print(background)

def show_character_card(target):
    table = Table.grid(padding=1)
    table.add_column(justify="right", style="cyan", no_wrap=True)
    table.add_column(justify="left", style="bold white")

    table.add_row("Class", target.__class__.__name__)
    table.add_row("HP", str(target.health))
    table.add_row("Mana", str(target.mana))
    table.add_row("Power", str(target.class_power))
    table.add_row("Special", target.description)

    subtitle = Text(str(target.description), style="dim")
    try:
        color = class_color_rich[target.__class__.__name__]
    except KeyError:
        color = "bright_magenta"
    title = f"🧙 {target.name}"
    full_card = Panel(
        table,
        title=title,
        subtitle=subtitle,
        border_style=color,
        box=box.ROUNDED,
        width=40,
    )

    return full_card


def show_two_cards(characters):
    two = False
    one = False
    characters = characters[:]  # Crear copia para no modificar la original
    while len(characters) % 3 != 0:
        one = characters.pop()
        if len(characters) % 3 != 0:
            two = characters.pop()


    while characters:
        layout = Table.grid(expand=True)
        layout.add_column()
        layout.add_column()
        layout.add_column()

        a = characters.pop(0)
        b = characters.pop(0)
        c = characters.pop(0)
        layout.add_row(
            show_character_card(a), show_character_card(b), show_character_card(c)
        )
        console.print(layout)
    if one and two:
        for2 = Table.grid(padding=(0,12))
        for2.add_column()
        for2.add_column()
        for2.add_column()
        for2.add_row(
            show_character_card(one), show_character_card(two),'')
        console.print(for2)
    if one and not two:
        console.print(show_character_card(one))  # Lo imprime solo al final

def winnersUI(winners):
    clean_screen()
    print(figlet.renderText("Congratulations"))
    for i in winners:
        console.print(show_character_card(i))
def playersUI():
    elements = [1,2]
    clean_screen()
    print(f"Welcome to Black Clover duel game\n")
    while True:
        try:
            number = int(input(f"How many players are going to play\n"))
            break
        except ValueError:
            continue
    return number
