import random

CRITIC_CHANCE = 0.10
red_color = "[red]"
green_color = "[green]"
blue_color = "[blue]"
purple_color = "[purple]"
reset_red_color = "[/red]"
reset_green_color = "[/green]"
reset_blue_color = "[/blue]"
reset_purple_color = "[/purple]"


# Decorator that looks if you have enought mana
def count_mana(mana):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            new_mana = mana
            for i in self.effects:
                if i["super effect"] == "mana cost" and i["type"] == "good":
                    new_mana = mana * (1 - i["amount"])

            if self.mana < new_mana:
                value = [f"{self.name} dont have enought mana to do {func.__name__}"]
                return value
            self.mana -= new_mana
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def get_all(mana):
    def decorator(func):
        def wrapper(self, enemies, *args, **kwargs):
            new_mana = mana
            result = func(self, enemies, *args, **kwargs)
            if len(result) == 3:
                damage, text_template, variable = result
            elif len(result) == 2:
                (
                    damage,
                    text_template,
                ) = result
                variable = {}
            for x in self.effects:
                if x["super effect"] == "mana cost" and x["type"] == "good":
                    new_mana = mana * (1 - i["amount"])
            if self.mana < new_mana:
                value = [f"{self.name} dont have enought mana to do {func.__name__}"]
                return value
            self.mana -= new_mana
            for r in self.effects:
                if r["super effect"] == "nerf precision":
                    if random.random() < r["amount"]:
                        value = [f"{self.name} have fail to do {func.__name__}"]
                        return value
            for i in self.effects:
                if i["super effect"] == "attack buff":
                    damage = damage + i["amount"]
                if i["super effect"] == "attack nerf":
                    damage = damage - i["amount"]

            if isinstance(enemies, list):
                for t in enemies:
                    for s in t.effects:
                        if s["super effect"] == 'increase damage':
                            times = int(s['amount'])
                            damage *= (1 + times)
                        if s["super effect"] == "shield":
                            amount = int(s["amount"])
                            damage = damage * (1 - amount)
                    t.receive_damage(damage)
            else:
                enemy = enemies
                for y in enemy.effects:
                        if y["super effect"] == 'increase damage':
                            times = int(y['amount'])
                            damage *= (1 + times)
                            raise EOFError(damage)
                        if y["super effect"] == "shield":
                            amount = int(y["amount"])
                            damage = damage * (1 - amount)
                enemy.receive_damage(damage)
            value = text_template[0].format(
                color=self.color,
                reset_color=self.reset_color,
                name=self.name,
                damage=damage,
                red_color=red_color,
                enemy_name=enemy.name,
                reset_red_color=reset_red_color,
                attack_level=self.attack_level,
                class_power=self.class_power,
                enemy_reset_color=enemy.reset_color,
                enemy_color=enemy.color,
                **variable,
            )
            return [value]

        return wrapper

    return decorator


class Wizzard:
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        maximun_life=120,
        health=120,
        maximun_mana=120,
        dodge_attack=0.01,
        shield=0,
    ):
        self.name = name
        self.health = health
        self.attack_level = attack_level
        self.mana = mana
        self.maximun_life = maximun_life
        self.maximun_mana = maximun_mana
        self.dodge_attack = dodge_attack
        self.class_power = class_power
        self.shield = shield
        self.effects = []
        self.moves = ["Attack", "Rest"]
        self.dic = [
            "⚔️ Basic attack to enemy",
            "🛌 Rest the round and recover mana and heal",
        ]
        self.color = 0
        self.description = description
        self.inventory = []
        self.new_data = {
            "Attack": {
                "description": "⚔️ Basic attack to enemy",
                "effect" : 'damage',
                "target": "enemy",
                "mana cost": 0,
                "amount" : self.attack_level
            },
            "Rest": {
                "description": "🛌 Rest the round and recover mana and heal",
                "effect" : 'resting',
                "target": "self",
                "mana cost": 0,
                "amount" : 5,
            },
        }

    def show_state(self):
        lines = [""]
        if isinstance(self, AntimagicWizzard):
            color_type = "\033[38;5;208m"
        elif isinstance(self, WaterWizzard):
            color_type = "\033[38;5;81m"
        elif isinstance(self, WindWizzard):
            color_type = "\033[38;2;80;200;120m"
        elif isinstance(self, HealerWizzard):
            color_type = "\033[38;5;34m"
        elif isinstance(self, SpatialWizzard):
            color_type = "\033[38;5;250m"
        elif isinstance(self, FireWizzard):
            color_type = "\033[38;5;196m"
        lines.append(
            f"{self.name} | {color_type}{self.__class__.__name__}{self.reset_color}"
        )
        lines.append(self.bar("health"))
        if isinstance(self, AntimagicWizzard):
            lines.append(self.bar("energy"))
        else:
            lines.append(self.bar("mana"))
        return lines

    def bar(self, types, lenght=20):
        if types == "health":
            percentile = round(self.health) / self.maximun_life
        if types == "mana" or types == "energy":
            percentile = round(self.mana) / self.maximun_mana
        filed = int(lenght * percentile)
        empty = int(lenght - filed)
        if percentile > 0.66:
            color = "[green]"
            reset = "[/green]"
        elif percentile > 0.33:
            color = "[yellow]"
            reset = "[/yellow]"
        else:
            color = "[red]"
            reset = "[/red]"

        if types == "mana":
            color = "[purple]"
            reset = "[/purple]"
        if types == "energy":
            color = "[blue]"
            reset = "[/blue]"
        bar = color + "█" * filed + "-" * empty + reset
        if types == "health":
            stats = f"Hp[{bar}]{round(self.health)}/{self.maximun_life}"
        if types == "mana":
            stats = f"Mn[{bar}]{round(self.mana)}/{self.maximun_mana}"
        if types == "energy":
            stats = f"Eg[{bar}]{round(self.mana)}/{self.maximun_mana}"
        return stats

    @get_all(0)
    def Attack(self, enemy):
        if random.random() < enemy.dodge_attack:
            value = [
                "{color}{name}{reset_color} is attacking {enemy_name}",
                "{enemy_name} has dodge {name} attack",
            ]
            enemy.dodge_attack = 0.01
            return 0, value
        else:
            if random.random() < CRITIC_CHANCE:
                value = [
                    "{red_color}{name} has made a critical strike to {enemy_name}{reset_red_color}"
                ]
                damage = self.attack_level * 2
                enemy.receive_damage(damage)
            else:
                value = [
                    "{color}{name}{reset_color} is attacking {enemy_name} with {red_color}{attack_level}{reset_red_color} points of damage"
                ]
                damage = self.attack_level
        return damage, value

    def Rest(self):
        self.mana += 20
        self.health += 5
        value = [
            f"{self.color}{self.name}{self.reset_color} has rested the round and have received {purple_color}20 points of mana{reset_purple_color} and {green_color}10 points of health{reset_green_color}"
        ]
        self.show_state()
        return value

    def receive_damage(self, damage):
        if self.health > 0:
            if damage * (1 - self.shield) >= self.health:
                self.health = 0
                self.die()
            else:
                self.health -= damage * (1 - self.shield)
            self.show_state()
        else:
            self.die()

    def confusion(self, level):
        if self.attack_level <= 0:
            self.attack_level = 0
            return f"{self.name} is inmune to confusion"
        self.attack_level -= 1 * level
        self.receive_damage(0.5 * level)
        return f"{self.color}{self.name}{self.reset_color} is confused, attack power reduce"

    def update_effects(self):
        effect = []
        for i in self.effects:
            i["duration"] -= 1
            try:
                value = i["effect"](self)
            except KeyError:
                continue
            if i["duration"] == 0:
                self.effects.remove(i)
            if value:
                effect.extend(value)
            if effect:
                return effect

    def rest(self):
        self.effects.append(
            {
                "name": "🧘 Serenity",
                "duration": 4,
                "effect": rest,
                "type": "good",
                "amount": 4,
                "super effect": "rest",
            }
        )
        return f"{self.name} is resting +5 "

    def die(self):
        self.mana = 0
        self.health = 0

    def resurrect(self, ally, mana, health):
        self.mana = mana
        self.health = health
        print(f"{self.name} has been resurected by {ally.name}")

    def mana_regeneration(self):
        self.effects.append(
            {
                "name": "🔵 Mana Flow",
                "duration": 1,
                "effect": rest,
                "type": "default",
                "super effect": "default",
                'amount' : 5
            }
        )

    def show_moves(self):
        return f"{self.name}'s moves: {', '.join(self.moves)}"


class HealerWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        maximun_life=120,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            maximun_life=120,
            health=120,
            shield=0,
        )
        self.new_data.update(
            {
                "Heal": {
                    "description": "🧪 Heal an ally",
                    "target": "ally",
                    "effect": "healing",
                    "mana cost": 20,
                    "amount" : self.class_power/2,
                },
                "Heal myself": {
                    "description": "💖 Heal yourself",
                    "target": "self",
                    "effect": "healing",
                    "mana cost": 20,
                    "amount" : self.class_power,
                },
                "Clean spirit": {
                    "description": "🧹 Remove bad effects from an ally",
                    "target": "ally",
                    "effect": "support",
                    "mana cost": 10,
                    "amount" : 0,
                },
                "Energize": {
                    "description": "🧹 Power up the attack of an ally",
                    "target": "ally",
                    "effect": "buff",
                    "mana cost": 20,
                    "amount" : 20,
                },
                "Floral thorns": {
                    "description": "🌸 Trap the enemy with magic thorns, dealing damage and weakening their attacks.",
                    "target": "enemy",
                    "effect": "debuff",
                    "mana cost": 30,
                    "amount" : 10,
                },
            }
        )

    @count_mana(20)
    def Heal(self, ally):
        healing = self.class_power / 2
        ally.health += healing
        if ally.health > ally.maximun_life:
            ally.health = ally.maximun_life
        value = [
            f"{self.color}{ally.name}{self.reset_color} have received {green_color}{self.class_power * 0.5}{reset_green_color} point of health"
        ]
        ally.show_state()
        return value

    @count_mana(20)
    def Heal_myself(self):
        healing = self.class_power
        self.health += healing
        if self.health > self.maximun_life:
            self.health = self.maximun_life
        value = [
            f"{self.color}{self.name}{self.reset_color} have received {green_color}{self.class_power}{reset_green_color} points of health"
        ]
        self.show_state()
        return value

    @count_mana(10)
    def Clean_spirit(self, ally):
        removes = []
        for i in ally.effects[:]:
            if i["type"] == "bad":
                removes.append(i["name"])
                ally.effects.remove(i)
        value = [
            f"{self.color}{self.name}{self.reset_color} have deleted all dangerous effects on {ally.name} ({removes})"
        ]
        return value

    @count_mana(20)
    def Energize(self, ally):
        ally.effects.append(
            {
                "name": "🌟 Energy Surge",
                "duration": 8,
                "effect": attack_buff,
                "type": "good",
                "amount": 20,
                "super effect": "attack buff",
            }
        )
        value = [
            f"{self.color}{self.name}{self.reset_color} have used Aenergize on {ally.name} powering up the attack on {blue_color}20 points{reset_blue_color}"
        ]
        return value

    @get_all(30)
    def Floral_thorns(self, enemy):
        enemy.effects.append(
            {
                "name": "🌵 Thorns",
                "effect": attack_nerf,
                "duration": 8,
                "type": "good",
                "amount": 10,
                "super effect": "attack nerf",
            }
        )
        damage = self.class_power
        value = [
            "{color}{name}{reset_color} have used floral thorns unleashing the effect thorns on {enemy_name} and dealing {damage} "
        ]
        return damage, value


class SpatialWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            health=120,
            shield=0,
        )
        self.new_data.update(
            {
                "Teleport": {
                    "description": "🌀 Teleport and deal damage",
                    "target": "enemy",
                    "effect": "damage",
                    "mana cost": 25,
                    "amount" : self.class_power,
                },
                "Make portal": {
                    "description": "🚪 Create a portal for strategic advantage",
                    "target": "ally",
                    "effect": "support",
                    "mana cost": 15,
                    "amount" : 0,
                },
                "Space shield": {
                    "description": "🛡️ Create a space shield to block attacks",
                    "target": "self",
                    "effect": "shield",
                    "mana cost": 20,
                    "amount" : .20,
                },
                "Space cut": {
                    "description": "✂️ Slash through space to deal damage",
                    "target": "enemy",
                    "effect": "damage",
                    "mana cost": 20,
                    "amount" : self.class_power,
                },
                "Dimensional rift": {
                    "description": "🌀 Tear open space to damage an enemy and distort their movements.",
                    "target": "enemy",
                    "effect": "debuff",
                    "mana cost": 35,
                    "amount" : .50,
                },
            }
        )

    @count_mana(20)
    def Teleport(self, object):
        conf = object.confusion(self.class_power)
        value = [
            f"{self.color}{self.name}{self.reset_color} has been teleported behind {object.name}",
            conf,
        ]

        return value

    @count_mana(40)
    def Make_portal(self, ally):
        ally.dodge_attack = 1
        value = [
            f"{self.color}{ally.name}{self.reset_color} will dodge the next direct attack"
        ]
        return value

    @count_mana(20)
    def Space_shield(self):
        value = [
            f"{self.color}{self.name}{self.reset_color} has applied an space shield on hiself"
        ]
        self.effects.append(
            {
                "name": "🛡️ Space Shield",
                "duration": 4,
                "effect": shield,
                "type": "good",
                "amount": "+20% 🛡️ ",
                "super effect": "shield",
            }
        )
        return value

    @get_all(20)
    def Space_cut(self, enemy):
        value = [
            "{color}{name}{reset_color} has cut the space close to {enemy_name} dealing {red_color}{class_power}{reset_red_color} points of damage"
        ]
        damage = self.class_power
        return damage, value

    @get_all(30)
    def Dimensional_rift(self, enemy):
        enemy.effects.append(
            {
                "name": "🔮 Spatial Disruption",
                "duration": 4,
                "effect": attack_buff,
                "type": "bad",
                "amount": 0.50,
                "super effect": "nerf precision",
                "pretty amount": " - .50 🎯",
            }
        )
        value = [
            "{color}{name}{reset_color} has made a dimensional, activating the effect spatial disruption on {enemy_name} and dealing {red_color}{damage}{reset_red_color} points of damage "
        ]
        damage = self.class_power
        return damage, value


class WindWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            health=120,
            shield=0,
        )
        self.new_data.update(
            {
                "Tornado": {
                    "description": "🌪️ Create a powerful tornado to deal damage and control the battlefield",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 30,
                },
                "Gale white bow": {
                    "description": "🏹 Summon the white bow to deal a precise and strong shot",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power * 2,
                    "mana cost": 20,
                },
                "Eye of the storm": {
                    "description": "🌩️ Unleash the eye of the storm, a massive force that disrupts enemies",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power + (self.mana * 0.3),
                    "mana cost": 40,
                },
                "Falling air": {
                    "description": "💨 Create a gust of falling air to knock back and damage enemies",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power * 1.2,
                    "mana cost": 25,
                },
                "Wind embrace": {
                    "description": "🍃 Channel the wind around an ally, reducing their mana cost for the next 3 rounds.",
                    "target": "ally",
                    "effect": "buff",
                    "mana cost": 20,
                    "amount" : .33,
                },
            }
        )

    @get_all(20)
    def Tornado(self, enemy):
        value = [
            "{color}{name}{reset_color} has made a tornado affecting {enemy_name} dealing {red_color}{damage}{reset_red_color} points of damage"
        ]
        damage = self.class_power
        return damage, value

    @get_all(40)
    def Gale_white_bow(self, enemy):
        arrows = 0
        for _ in range(4):
            if random.random() < 0.33:
                arrows += 1
        damage = self.class_power * 0.5 * arrows
        value = [
            "{color}{name}{reset_color} has used gale white bow in {enemy_name}",
            "arrows arrows have reach {enemy_name} dealing {red_color}{damage}{reset_red_color} points of damage",
        ]

        return damage, value

    @get_all(0)
    def Eye_of_the_storm(self, enemy):
        self.new_data.pop("Eye_of_the_storm", None)
        damage = self.class_power + (self.mana * 0.3)
        self.mana = 0
        value = [
            "{enemy_color}{enemy_name}{enemy_reset_color} is in the eye of the tornado of {color}{name}{reset_color} receiving {damage} points of damage"
        ]

        return damage, value

    @get_all(40)
    def Falling_air(self, enemy):
        if random.random() < 0.33:
            damage = self.class_power * 1.7
        elif random.random() < 0.33:
            damage = self.class_power * 1.4
        elif random.random() < 0.33:
            damage = self.class_power * 0.8
        elif random.random() < 0.33:
            damage = self.class_power * 0.3
        else:
            damage = self.class_power * 0.1

        value = [
            "{color}{name}{reset_color} has throw air to {enemy_name} dealing {damage} point of damage"
        ]

        return damage, value

    @count_mana(20)
    def Wind_embrace(self, ally):
        value = [
            f"{self.color}{self.name}{self.reset_color} just made air pass trought {ally.name} decreasing the mana cost for 3 rounds"
        ]
        ally.effects.append(
            {
                "name": "💨 Ether Surge ",
                "duration": 8,
                "effect": attack_buff,
                "type": "good",
                "amount": 0.33,
                "super effect": "mana cost",
            }
        )
        return value


class AntimagicWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            health=120,
            shield=0,
        )

        self.new_data.update(
            {
                "Break spell": {
                    "description": "🛡️ Avoid next attack",
                    "target": "self",
                    "effect": "dodge",
                    "mana cost": 15,
                    "amount" : 0,
                },
                "Demon slasher": {
                    "description": "⚡ Attack and shock enemy",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power + 15,
                    "mana cost": 25,
                },
                "Super bicep": {
                    "description": "👊 Throw a bunch of punches which can deal damage",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 20,
                },
                "Arcane boost": {
                    "description": "✨ Buffs ally's next two attacks",
                    "target": "ally",
                    "effect": "buff",
                    "mana cost": 20,
                    "amount" : 2,
                },
                "Antimagic shockwave": {
                "description": "🌀 Release a powerful antimagic shockwave that damages all enemies at once.",
                "target": "all enemies",
                "effect": "area_attack",
                "mana cost": 40,
                "amount" : self.class_power * 0.9,
                },

            }
        )

    @count_mana(30)
    def Break_spell(self):
        self.dodge_attack = 0.80
        value = [
            f"{self.color}{self.name}{self.reset_color} its likely to dodge the next direct attack"
        ]
        return value

    @get_all(30)
    def Demon_slasher(self, enemy):
        value = ["{color}{name}{reset_color} has used demon slasher {enemy_name}"]
        enemy.effects.append(
            {
                "name": "⚡ Shock",
                "duration": 3,
                "effect": shock,
                "type": "bad",
                "amount": "-5 ❤️",
                "super effect": "shock",
            }
        )
        damage = self.class_power
        return damage, value

    @count_mana(20)
    def Arcane_boost(self, ally):
        value = [
            f"{self.color}{self.name}{self.reset_color} will buff the next 2 class attacks of {ally.name}"
        ]
        ally.effects.append(
            {
                "name": "🔮 Arcane Boost",
                "duration": 8,
                "effect": attack_buff,
                "type": "good",
                "amount": 2,
                "super effect": "attack buff",
            }
        )
        return value

    @get_all(30)
    def Super_bicep(self, enemy):
        hits = 0
        for _ in range(10):
            if random.random() < 0.20:
                hits += 1
        damage = hits * (self.class_power * 0.70)
        value = [
            "{color}{name}{reset_color} has hit {enemy_name} {hits}  times, dealling {red_color}{damage}{reset_red_color} points of damage"
        ]
        variable = {"hits": hits}
        return damage, value, variable

    @get_all(40)
    def Antimagic_shockwave(self, enemies):
        damage = self.class_power *.9
        value = [
                "{color}{name}{reset_color} has made a antimagic shockwave dealing {damage} points of damage to all enemies"
            ]
        return damage, value
class WaterWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            health=120,
            shield=0,
        )
        self.new_data.update(
            {
                "Sea dragons roar": {
                    "description": "🐉 Unleash the dragon's roar to deal massive damage and intimidate enemies",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 30,
                },
                "Water sphere": {
                    "description": "💧 Create a water sphere to control the battlefield and protect allies",
                    "target": "ally",
                    "effect": "shield",
                    "amount": .20,
                    "mana cost": 20,
                },
                "Valkyre armor": {
                    "description": "🛡️ Summon a mystical armor of water to shield yourself",
                    "target": "self",
                    "effect": "shield",
                    "mana cost": 15,
                    "amount": .20,
                },
                "Water ball": {
                    "description": "🌊 Launch a pressurized water ball to damage an enemy",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power * 2,
                    "mana cost": 45,
                },
                "Tide siphon": {
                "description": "🌊 Create a magical whirlpool that damages an enemy and drains their mana over time.",
                "target": "enemy",
                "effect": "attack",
                "mana cost": 35,
                "amount": self.class_power ,
                }
            }
        )

    # Defensive
    @count_mana(20)
    def Water_sphere(self, ally):
        value = [
            f"{self.color}{self.name}{self.reset_color} has used water sphere in {ally.name} giving a shield of {blue_color}20%{reset_blue_color}"
        ]
        ally.effects.append(
            {
                "name": "🛡️ Magic Shield",
                "duration": 3,
                "effect": shield,
                "type": "good",
                "amount": "20% 🛡️",
                "super effect": "shield",
            }
        )
        return value

    # Ofensive
    @get_all(20)
    def Sea_dragons_roar(self, enemy):
        value = [
            "{color}{name}{reset_color} has made dragon roar dealing {red_color}{class_power}{reset_red_color} points of damage on {enemy_name}"
        ]
        damage = self.class_power
        return damage, value

    @get_all(45)
    def Water_ball(self, enemy):
        damage = self.class_power * 2
        value = [
            "{color}{name}{reset_color} has made a big water ball dealing {red_color}{damage}{reset_red_color} points of damage on {enemy_name}"
        ]
        return damage, value

    @count_mana(60)
    def Valkyre_armor(self):
        value = [
            f"{self.color}{self.name}{self.reset_color} is wearing valkyre armor buffing attack and shield, also healing herself"
        ]
        self.effects.extend(
            [
                {
                    "name": "🛡️ Magic Shield",
                    "duration": 8,
                    "effect": shield,
                    "type": "good",
                    "amount": "20% 🛡️",
                    "super effect": "shield",
                },
                {
                    "name": "🌟 Energy Surge",
                    "duration": 8,
                    "effect": attack_buff,
                    "type": "good",
                    "super effect": "attack buff",
                    "amount": 2,
                },
                {
                    "name": "🌿 Healing Touch",
                    "duration": 8,
                    "effect": self_healing,
                    "type": "good",
                    "amount": "+10 ❤️",
                    "super effect": "healing",
                },
            ]
        )

        return value
    @get_all(35)
    def Tide_siphon(self,enemy):
        value = [
            "{color}{name}{reset_color} has made tide shipon on {red_color}{class_power}{reset_red_color} draning 20 points of mana and dealing {damage} points of damage"
        ]
        damage = self.class_power
        return damage, value

class FireWizzard(Wizzard):
    def __init__(
        self,
        name,
        attack_level,
        mana,
        class_power,
        description,
        reset_color=0,
        health=120,
        shield=0,
    ):
        super().__init__(
            name,
            attack_level,
            mana,
            class_power,
            description,
            reset_color=0,
            health=120,
            shield=0,
        )
        self.new_data.update(
            {
                "Fire ball": {
                    "description": "🔥 Launch a fiery ball to deal explosive damage to enemies",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 10,
                },
                "Soul chain": {
                    "description": "💫 Summon the soul chain to bind enemies and drain their energy",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 15,
                },
                "Fire bat storm": {
                    "description": "🦇 Summon a swarm of flaming bats to overwhelm enemies",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 25,
                },
                "Volcanic surge": {
                    "description": "🌋 Unleash a volcanic eruption to deal massive fire damage",
                    "target": "enemy",
                    "effect": "damage",
                    "amount": self.class_power,
                    "mana cost": 30,
                },
                "Scorching chains": {
                "description": "🔥 Enchain an enemy in flames, dealing damage and making them take 25% more damage for a few turns.",
                "target": "enemy",
                "effect": "attack",
                "mana cost": 40,
                "amount": self.class_power,
                }
            }
        )

    # Ofensive
    @get_all(20)
    def Fire_ball(self, enemy):
        value = [
            "{color}{name}{reset_color} has thrown a fire ball to {enemy_name} dealing {red_color}{class_power}{reset_red_color} points of damage"
        ]
        damage = self.class_power
        return damage, value

    # Special ofensive
    @count_mana(60)
    def Soul_chain(self, enemy):
        new = (self.class_power + enemy.class_power) / 2
        self.class_power = new
        enemy.class_power = new
        self.new_data.pop("Esoul_chain", None)
        value = [
            f"{self.color}{self.name}{self.reset_color} and {enemy.name} now have the same power attack ({new} points of atack)"
        ]
        return value

    @get_all(30)
    def Fire_bat_storm(self, enemy):
        hits = 0
        for _ in range(5):
            if random.random() > 0.25:
                hits += 1
        damage = self.class_power * hits * 0.8
        value = [
            "{color}{name}{reset_color} hit {hits} times {enemy_name} whit his fire bat storm, dealing {red_color}{damage}{reset_red_color} points of damage"
        ]
        variable = {"hits": hits}
        return damage, value, variable

    @get_all(30)
    def Volcanic_surge(self, enemy):
        if enemy.health <= 50:
            damage = self.class_power * 2
        else:
            damage = self.class_power / 2
        value = [
            "{color}{name}{reset_color} has made a volcan just below {enemy_name} dealing {red_color}{damage}{reset_red_color} points of damage"
        ]

        return damage, value

    @get_all(40)
    def Scorching_chains(self, enemy):
        damage = self.class_power
        value = [
            "{color}{name}{reset_color} is enchainig {enemy_name} dealing {damage} increasing the damage received in 25% for 2 rounds"
        ]
        enemy.effects.append(
            {
                "name": "scorching chain",
                "duration": 8,
                "effect": attack_nerf,
                "type": "bad",
                "amount": .25,
                "super effect": "increase damage",
            }
        )
        return damage, value


# Spells that last along the rounds
def shock(target):
    target.receive_damage(5)
    value = [
        f"{target.color}{target.name}{target.reset_color} is shocked, will lose {red_color} 5 points of damage{reset_red_color}"
    ]
    return value


def self_healing(target):
    target.health += 10
    value = [
        f"{target.color}{target.name}{target.reset_color} is healing, will gain {green_color} 10 points of health{reset_green_color}"
    ]
    return value


def shield(target):
    return


def rest(target):
    target.mana += 3
    if target.mana > 120:
        target.mana = 120


def attack_buff(target):

    return


def attack_nerf(target):
    return
