#!/usr/bin/env python3
"""
Magic Pony Sparkle Land — Text Adventure Game
Author: ChatGPT (custom script)
"""

import random
import sys
import textwrap
import time

# ---------------------------
# ASCII ART (unicorns & title)
# ---------------------------

UNICORN_ART = r"""
             \
               \
                \\
                 \\
                  >\/7
              _.-(6'  \
             (=___._/` \
                  )  \ |
                 /   / |
                /    > /
               j    < _\
           _.-' :      ``.
           \ r=._\        `.
          <`\\_  \         .`-.
           \ r-7  `-. ._  ' .  `\
            \`,      `-.`7  7)   )
             \/         \|  \'  / `-._
                        ||    .'
                         \\  (
                         >\  >
                       ,.-' >.'
                     <.'_.''
                       <'
        MAGIC SPARKLE PONY LAND
"""

EARTH_PONY_ART = r"""
   (\_/) 
  (•_•)     Earth Pony
  / >🌾   Strong as the hills
"""

UNICORN_PONY_ART = r"""
    /\  /\ 
   //\\//\\   Unicorn
  ((  *  ))  Magic in the horn
   \\_//\\/
    `--' 
"""

PEGASUS_ART = r"""
    .-.
   (o.o)  Pegasus
  /=\ /=\  Wings of wind
  `-' `-'
"""

# ---------------------------
# Utilities
# ---------------------------

def slow_print(text, delay=0.01):
    for line in text.splitlines():
        print(line)
        time.sleep(0.01)

def wrapped(text):
    return textwrap.fill(text, width=75)

def prompt(options):
    """Prompt for input until a valid option selected from list of strings (case-insensitive)."""
    options_lower = [o.lower() for o in options]
    while True:
        choice = input("> ").strip().lower()
        if choice in options_lower:
            return choice
        # allow numeric selection if options are numbers
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options_lower[idx]
        print("Please enter one of:", ", ".join(options))

# ---------------------------
# Game data structures
# ---------------------------

class Item:
    def __init__(self, name, description="No description.", type_="misc"):
        self.name = name
        self.description = description
        self.type = type_

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.description}"

class Weapon(Item):
    def __init__(self, name, base_damage, description="", weapon_type="melee"):
        super().__init__(name, description, type_="weapon")
        self.base_damage = base_damage
        self.weapon_type = weapon_type

class Crystal(Item):
    def __init__(self, name, power, charges, description=""):
        super().__init__(name, description, type_="crystal")
        self.power = power
        self.charges = charges

    def use(self):
        if self.charges <= 0:
            return False
        self.charges -= 1
        return True

    def __str__(self):
        return f"{self.name} (Crystal, {self.power}, charges: {self.charges}) - {self.description}"

class Player:
    def __init__(self, name, pony_type, magic, strength, agility):
        self.name = name
        self.pony_type = pony_type
        self.max_health = 30 + strength * 2
        self.health = self.max_health
        self.magic = magic
        self.strength = strength
        self.agility = agility
        self.inventory = []
        self.weapon = None
        self.has_amulet = False
        self.charisma_bonus = 0  # can be raised by rose quartz
        self.location = "Dungeon Cell"

    def attack_damage(self):
        base = 2 + self.strength
        if self.weapon:
            base += self.weapon.base_damage
        return base

    def magic_power(self):
        return 1 + self.magic

    def show_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
            return
        for i, item in enumerate(self.inventory, 1):
            if isinstance(item, Weapon):
                extra = f" [Weapon dmg {item.base_damage}]"
            elif isinstance(item, Crystal):
                extra = f" [Crystal:{item.power} charges:{item.charges}]"
            else:
                extra = ""
            print(f"{i}. {item.name} - {item.description}{extra}")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Added to inventory: {item.name}")

    def find_crystal(self, power_name):
        for it in self.inventory:
            if isinstance(it, Crystal) and it.power.lower() == power_name.lower() and it.charges>0:
                return it
        return None

    def remove_item_by_index(self, idx):
        if 0 <= idx < len(self.inventory):
            return self.inventory.pop(idx)
        return None

# ---------------------------
# Enemies & NPCs
# ---------------------------

class Enemy:
    def __init__(self, name, health, strength, agility, magic, description=""):
        self.name = name
        self.health = health
        self.strength = strength
        self.agility = agility
        self.magic = magic
        self.description = description

    def attack_damage(self):
        return 1 + self.strength

# ---------------------------
# Game Mechanics
# ---------------------------

def roll(chance):
    return random.random() < chance

def fight(player, enemy):
    print(f"\nA battle begins: {player.name} vs {enemy.name}!")
    print(enemy.description)
    # loop
    while player.health > 0 and enemy.health > 0:
        print("\nYour HP: {}/{}".format(player.health, player.max_health))
        print(f"{enemy.name} HP: {enemy.health}")
        print("Options: [fight] [magic] [use item] [flee] [inv]")
        choice = input("> ").strip().lower()
        if choice == "inv" or choice == "inventory":
            player.show_inventory()
            continue
        if choice == "use item":
            use_item_in_fight(player, enemy)
            if enemy.health <= 0:
                break
        elif choice == "fight":
            # player's attack
            hit_chance = 0.6 + (player.agility - enemy.agility) * 0.03
            hit_chance = max(0.2, min(0.95, hit_chance))
            if roll(hit_chance):
                dmg = player.attack_damage()
                enemy.health -= dmg
                print(f"You strike {enemy.name} for {dmg} damage!")
            else:
                print("You miss!")
        elif choice == "magic":
            # use innate magic or crystals
            if player.magic <= 0:
                print("You have no magic power.")
            else:
                # Simple magic blast damage scaled by magic stat
                dmg = player.magic_power() + random.randint(0, player.magic)
                enemy.health -= dmg
                print(f"You unleash magical power for {dmg} damage!")
        elif choice == "flee":
            flee_chance = 0.25 + (player.agility - enemy.agility) * 0.05
            if roll(flee_chance):
                print("You flee successfully!")
                return "fled"
            else:
                print("You fail to escape!")
        else:
            print("Unknown choice — pick fight, magic, use item, flee, or inv.")
            continue

        # Enemy turn if still alive
        if enemy.health > 0:
            hit_chance = 0.5 + (enemy.agility - player.agility) * 0.03
            hit_chance = max(0.2, min(0.9, hit_chance))
            if roll(hit_chance):
                dmg = enemy.attack_damage()
                player.health -= dmg
                print(f"{enemy.name} hits you for {dmg} damage!")
            else:
                print(f"{enemy.name} misses!")
    if player.health <= 0:
        print("\nYou have been defeated...")
        return "dead"
    else:
        print(f"\nYou defeated {enemy.name}!")
        return "victory"

def use_item_in_fight(player, enemy):
    print("Choose item to use (number), or 'back':")
    player.show_inventory()
    choice = input("> ").strip().lower()
    if choice == "back":
        return
    if not choice.isdigit():
        print("That's not a number.")
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(player.inventory):
        print("Invalid selection.")
        return
    item = player.inventory[idx]
    if isinstance(item, Crystal):
        # apply crystal effects
        if item.charges <= 0:
            print(f"{item.name} has no charges left.")
            return
        item.use()
        if item.power.lower() == "telekinesis" or item.power.lower()=="lapis":
            dmg = player.magic_power() + 3
            enemy.health -= dmg
            print(f"You use {item.name} (Telekinesis) to slam the enemy for {dmg} damage!")
        elif item.power.lower() in ("healing", "jade"):
            heal = 8 + player.magic
            player.health = min(player.max_health, player.health + heal)
            print(f"Jade heals you for {heal} HP!")
        elif item.power.lower() in ("protection shield","obsidian"):
            # blocks next hit completely: implement as a temporary buff using a flag
            player.shielded = True
            print("A shimmering shield surrounds you, ready to block one attack.")
        elif item.power.lower() in ("fire powers","citrine","citrine - fire powers","citrine"):
            dmg = 6 + player.magic
            enemy.health -= dmg
            print(f"Flames burst from the crystal, dealing {dmg} fire damage!")
        elif item.power.lower() in ("projectile powers","clear quartz", "clear quartz - projectile powers", "clear quarts"):
            dmg = 4 + player.magic
            enemy.health -= dmg
            print(f"Projectiles from the crystal hit for {dmg} damage!")
        elif item.power.lower() in ("charisma","rose quartz"):
            # increases chance to avoid fighting, maybe charm enemy to skip next turn
            enemy_agility_backup = enemy.agility
            enemy.agility = max(0, enemy.agility - 3)
            print("Rose quartz glows — the enemy's aggression lowers.")
        else:
            print("You used the crystal, but nothing obvious happened.")
        # remove crystals with zero charges optionally
        if item.charges <= 0:
            print(f"{item.name} shatters after use.")
            player.inventory.pop(idx)
    elif isinstance(item, Weapon):
        print("You equip the weapon for this fight.")
        player.weapon = item
    else:
        print(f"You use {item.name} but nothing major happens.")

# ---------------------------
# Scene handlers
# ---------------------------

def dungeon_intro(player):
    print(UNICORN_ART)
    print(wrapped(
        "While grazing for berries late at night in the peaceful village of Rainbowtopia, "
        "you are suddenly seized and find yourself trapped in a dungeon deep inside a crystal cavern."
    ))
    time.sleep(1.0)
    print(wrapped(
        "You notice your amethyst, star-shaped amulet—given by your great-grandmother—is missing. "
        "A terrifying bulldog-cerberus creature snarls: the amulet contains royal magic that harnesses crystal power. "
        "With it he will take over the Crystal Kingdom. Escape and retrieve your amulet!"
    ))
    time.sleep(0.8)
    print("\nYou search your cell...")
    # give starting item
    kit = Item("Bread", "A small piece of bread to keep you going.")
    player.add_item(kit)
    # find a rusty knife
    knife = Weapon("Rusty Knife", base_damage=2, description="A dull but still useful knife.", weapon_type="melee")
    player.add_item(knife)

def find_in_corridor(player):
    print("\nYou slip into the corridor and find a small wooden staff leaning against the wall.")
    staff = Weapon("Wooden Staff", base_damage=3, description="Simple staff. Good for channeling magic.")
    player.add_item(staff)
    # maybe also find a crystal
    lapis = Crystal("Lapis", power="Telekinesis", charges=2, description="Grainy blue crystal. Lifts things with thought.")
    player.add_item(lapis)

def dragon_mountains(player):
    print("\n--- Dragon Mountains ---")
    print(wrapped("The path climbs into ash-scented air. Baby dragons glare with ember eyes."))
    # group of baby dragons
    dragons = Enemy("Baby Dragon Pack", health=18, strength=4, agility=3, magic=2,
                    description="A group of small dragons, quick but not very clever.")
    result = fight(player, dragons)
    if result == "dead":
        return "dead"
    # loot
    sword = Weapon("Short Sword", base_damage=4, description="A short, balanced sword.")
    player.add_item(sword)
    citrine = Crystal("Citrine", power="Fire Powers", charges=2, description="Warm, golden crystal of flame.")
    player.add_item(citrine)
    return "ok"

def haunted_forest(player):
    print("\n--- Haunted Forest ---")
    print(wrapped("A malicious spirit winds through the trees, whispering doubts and fears."))
    spirit = Enemy("Malicious Spirit", health=25, strength=3, agility=6, magic=6,
                   description="Shifting form that feeds on fear.")
    # You can try to talk (charisma), use rose quartz, fight, or flee
    while True:
        print("\nOptions: [talk] [fight] [magic] [use item] [flee] [inv]")
        choice = input("> ").strip().lower()
        if choice in ("inv", "inventory"):
            player.show_inventory()
            continue
        if choice == "use item":
            print("Pick an item to use on the spirit:")
            player.show_inventory()
            idx = input("> ").strip()
            if not idx.isdigit():
                print("Back.")
                continue
            idx = int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory[idx]
            if isinstance(item, Crystal) and item.power.lower() in ("charisma","rose quartz"):
                # charm the spirit
                if item.use():
                    print("Rose quartz glows warmly and the spirit calms, retreating into the trees.")
                    if item.charges <= 0:
                        print(f"{item.name} crumbles.")
                        player.inventory.pop(idx)
                    return "ok"
            else:
                print("That doesn't affect the spirit.")
            continue
        if choice == "talk":
            # charisma check: base + luck from rose quartz / player charismabonus
            charisma = player.charisma_bonus + (player.magic // 2)
            chance = 0.3 + charisma * 0.1
            if roll(chance):
                print("You speak with calm and kindness; the spirit ceases its torment and fades.")
                return "ok"
            else:
                print("The spirit is not convinced; it lashes out.")
                res = fight(player, spirit)
                return res
        if choice == "fight":
            res = fight(player, spirit)
            return res
        if choice == "magic":
            # magic approach: attempt to dispel
            if player.magic >= 5:
                print("Your strong magic pushes the spirit away.")
                return "ok"
            else:
                print("Your magic is insufficient; the spirit attacks.")
                res = fight(player, spirit)
                return res
        if choice == "flee":
            if roll(0.4 + player.agility * 0.02):
                print("You escape deeper into the wood and find a safer path.")
                return "ok"
            else:
                print("You cannot escape!")
                res = fight(player, spirit)
                return res
        print("Unknown choice.")

def port_and_coral_sea(player):
    print("\n--- Port of Shimmering Tides ---")
    print(wrapped("A worn dock and a merchant stands near a small boat. You need to get a boat across the Coral Sea."))
    print("Options: [pay] [persuade] [sneak] [look inv]")
    while True:
        choice = input("> ").strip().lower()
        if choice == "look inv" or choice == "inv" or choice == "inventory":
            player.show_inventory()
            continue
        if choice == "pay":
            # if player has coins? we didn't implement coins; fail gracefully
            print("You have no coins... the merchant frowns.")
            continue
        if choice == "persuade":
            # persuasion based on charisma and rose quartz
            charisma = player.charisma_bonus + (player.magic // 2)
            chance = 0.3 + 0.12 * charisma
            if roll(chance):
                print("The merchant smiles and lets you aboard for free.")
                return "ok"
            else:
                print("The merchant refuses. He demands a reason.")
                # maybe use rose quartz automatically
                rq = player.find_crystal("Charisma") or player.find_crystal("Rose Quartz")
                if rq:
                    rq.use()
                    print("Your Rose Quartz glows and the merchant becomes sympathetic; he lets you aboard.")
                    if rq.charges<=0:
                        print(f"{rq.name} crumbles after use.")
                        player.inventory.remove(rq)
                    return "ok"
                continue
        if choice == "sneak":
            if roll(0.4 + player.agility*0.02):
                print("You slip onto a small fishing boat unnoticed and cross the sea.")
                return "ok"
            else:
                print("You are caught and the port guards make you pay a fine you don't have. The merchant refuses service.")
                continue
        print("Choose pay / persuade / sneak / look inv")

def crystal_empire_guards(player):
    print("\n--- Gates of the Crystal Empire ---")
    print(wrapped("Massive faceted gates stand watch. The royal guards glance at you as you approach with an amulet in hand."))
    # guards check: if player has amulet, they may suspect you
    if not player.has_amulet:
        print("You approach without the amulet. The guards let you through after a brief inspection.")
        return "ok"
    # if has amulet:
    print("A stern guard asks: 'Where did you get that amulet?'")
    # options: tell truth, lie, hand over
    while True:
        print("Options: [explain] [lie] [hand over] [use item] [inv]")
        choice = input("> ").strip().lower()
        if choice in ("inv", "inventory"):
            player.show_inventory()
            continue
        if choice == "use item":
            print("Try using a crystal to charm or persuade:")
            player.show_inventory()
            idx = input("> ").strip()
            if not idx.isdigit():
                print("Back.")
                continue
            idx = int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory[idx]
            if isinstance(item, Crystal) and item.power.lower() in ("charisma","rose quartz"):
                if item.use():
                    print("Your Rose Quartz glows. The guard relaxes and decides not to arrest you.")
                    if item.charges<=0:
                        player.inventory.pop(idx)
                    return "ok"
            else:
                print("That doesn't sway the guard.")
            continue
        if choice == "explain":
            # charisma / magic checks
            base = 0.2 + (player.charisma_bonus * 0.1) + (player.magic * 0.03)
            if roll(base + 0.2):
                print("Your explanation sounds honest—guards decide not to arrest you.")
                return "ok"
            else:
                print("They are suspicious and call for arrest.")
                return "jail"
        if choice == "lie":
            chance = 0.15 + player.charisma_bonus*0.08 + (player.agility*0.02)
            if roll(chance):
                print("Your lie is convincing; they wave you through.")
                return "ok"
            else:
                print("They see through your lie and move to detain you.")
                return "jail"
        if choice == "hand over":
            # handing to guard — slight chance to go bad => explosion ending
            print("You step forward to hand the amulet to the guard...")
            # risk depends on agility — lower agility increases chance to fumble
            fumble_chance = 0.1 + max(0, 5 - player.agility)*0.05
            if roll(fumble_chance):
                print("You fumble the amulet! It slips from your hooves...")
                print("The amulet detonates in terrible crystal energy.")
                return "explosion"
            else:
                print("You hand the amulet over carefully; the guard inspects it and nods.")
                return "ok"
        print("Choose a valid option.")

def final_princess_scene(player):
    print("\n--- Throne Room, Crystal Palace ---")
    print(wrapped("You approach the princess of the Crystal Kingdom, amulet in hand. Will you return it?"))
    print("Options: [give] [explain] [use item] [inv]")
    while True:
        choice = input("> ").strip().lower()
        if choice in ("inv", "inventory"):
            player.show_inventory()
            continue
        if choice == "use item":
            print("You can use items before giving the amulet (for safety or persuasion).")
            player.show_inventory()
            idx = input("> ").strip()
            if not idx.isdigit():
                print("Back.")
                continue
            idx = int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory[idx]
            if isinstance(item, Crystal) and item.power.lower() in ("protection shield","obsidian"):
                if item.use():
                    player.shielded = True
                    print("Obsidian forms a protective shell around the amulet, dampening its volatile power.")
                    if item.charges<=0:
                        player.inventory.pop(idx)
            elif isinstance(item, Crystal) and item.power.lower() in ("charisma","rose quartz"):
                if item.use():
                    player.charisma_bonus += 1
                    print("Rose quartz increases your persuasive aura.")
                    if item.charges<=0:
                        player.inventory.pop(idx)
            else:
                print("That won't help here.")
            continue
        if choice == "explain":
            # persuasion to hand over to princess gracefully
            chance = 0.3 + player.charisma_bonus*0.1 + player.magic*0.03
            if roll(chance):
                print("You explain the amulet's history and the princess gratefully accepts it.")
                return "good"
            else:
                print("The princess is suspicious; she orders guards to take you.")
                return "jail"
        if choice == "give":
            print("You step forward and place the amulet in the princess's hands...")
            # if shielded, safe
            if getattr(player, "shielded", False):
                print("Thanks to the Obsidian protection, nothing explodes.")
                return "good"
            # otherwise chance of explosion depending on agility/handling
            fumble_chance = 0.05 + max(0, 5 - player.agility) * 0.06
            if roll(fumble_chance):
                print("A tragic slip! The amulet sparks and releases raw crystal energy...")
                return "explosion"
            # otherwise maybe princess accepts but guards still suspicious
            # final persuasion by charisma
            if roll(0.7 + player.charisma_bonus*0.05):
                print("The princess accepts the amulet and recognizes your bravery.")
                return "good"
            else:
                print("Even as you hand it over, someone cries theft and the guards step forward.")
                return "jail"
        print("Choose give / explain / use item / inv")

# ---------------------------
# Game Flow
# ---------------------------

def choose_pony():
    print("Choose your pony:")
    print("1) Earth pony: Magic 2, Strength 9, Agility 5")
    print("2) Unicorn: Magic 8, Strength 3, Agility 6")
    print("3) Pegasus: Magic 6, Strength 4, Agility 4")
    while True:
        c = input("> ").strip()
        if c in ("1","2","3"):
            if c=="1":
                print(EARTH_PONY_ART)
                return ("Earth Pony", 2, 9, 5)
            elif c=="2":
                print(UNICORN_PONY_ART)
                return ("Unicorn", 8, 3, 6)
            else:
                print(PEGASUS_ART)
                return ("Pegasus", 6, 4, 4)
        else:
            print("Enter 1, 2, or 3.")

def manage_inventory(player):
    while True:
        print("\nInventory Menu: [view] [use] [discard] [equip] [back]")
        choice = input("> ").strip().lower()
        if choice == "view":
            player.show_inventory()
        elif choice == "use":
            player.show_inventory()
            print("Enter number to use or 'back'")
            idx = input("> ").strip()
            if idx=="back":
                continue
            if not idx.isdigit():
                print("Invalid.")
                continue
            idx=int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory[idx]
            if isinstance(item, Crystal):
                if item.use():
                    print(f"You use {item.name} ({item.power}). Charges left: {item.charges}")
                    # immediate effects (healing only)
                    if item.power.lower() in ("healing","jade"):
                        heal = 8 + player.magic
                        player.health = min(player.max_health, player.health + heal)
                        print(f"You heal {heal} HP.")
                    if item.charges<=0:
                        print(f"{item.name} shatters.")
                        player.inventory.pop(idx)
                else:
                    print("No charges left.")
            elif isinstance(item, Weapon):
                player.weapon = item
                print(f"You equip {item.name}.")
            else:
                print(f"You use {item.name}. Nothing dramatic happened.")
        elif choice == "discard":
            player.show_inventory()
            print("Enter number to discard or 'back'")
            idx = input("> ").strip()
            if idx=="back":
                continue
            if not idx.isdigit():
                print("Invalid.")
                continue
            idx=int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory.pop(idx)
            print(f"You discard {item.name}.")
        elif choice=="equip":
            player.show_inventory()
            print("Enter weapon number to equip:")
            idx = input("> ").strip()
            if not idx.isdigit():
                print("Invalid.")
                continue
            idx=int(idx)-1
            if idx<0 or idx>=len(player.inventory):
                print("Invalid.")
                continue
            item = player.inventory[idx]
            if isinstance(item, Weapon):
                player.weapon = item
                print(f"You equip {item.name}.")
            else:
                print("Not a weapon.")
        elif choice == "back":
            return
        else:
            print("Unknown choice.")

def game_over(ending):
    print("\n--- GAME OVER ---")
    if ending == "good":
        print(wrapped("Good Ending: You return the amulet and the princess rewards you with your own place in the empire."))
    elif ending == "jail":
        print(wrapped("Jail Ending: Guards arrest you for possessing the amulet. You are held in a crystal cell."))
    elif ending == "explosion":
        print(wrapped("Explosion Ending: The amulet's energy explodes. A tragic end."))
    elif ending == "dead":
        print(wrapped("You died in battle. Your story ends here."))
    else:
        print("Unknown ending.")
    print("Thank you for playing Magic Pony Sparkle Land.")
    sys.exit(0)

def main():
    print(UNICORN_ART)
    print("#" * 60)
    print("WELCOME TO MAGIC PONY SPARKLE LAND")
    print("#" * 60)
    name = input("Your name, brave pony: ").strip() or "Player"
    pony, mag, strg, agi = choose_pony()
    player = Player(name, pony, magic=mag, strength=strg, agility=agi)
    print(f"Welcome, {player.name} the {player.pony_type}!")
    print("\n(Commands during exploration: inventory, manage inv, status, help)\n")
    dungeon_intro(player)

    # Simple linear progression with choices and small branching
    find_in_corridor(player)

    # First fight: miniboss - guard dog
    bulldog = Enemy("Bulldog Cerberus", health=22, strength=6, agility=3, magic=2,
                    description="The dreadful captor who stole your amulet roams the cavern.")
    print("\nAs you proceed, you confront a snarling guard — perhaps involved in your kidnapping.")
    res = fight(player, bulldog)
    if res == "dead":
        game_over("dead")
    # chance to find an amulet? Not yet — captor may have hidden it.
    # give a healing crystal
    jade = Crystal("Jade", power="Healing", charges=1, description="Green healing crystal.")
    player.add_item(jade)

    print("\nYou trek onward from the cavern, into the Dragon Mountains...")
    res = dragon_mountains(player)
    if res == "dead":
        game_over("dead")

    print("\nNext, you arrive at a haunted forest.")
    res = haunted_forest(player)
    if res == "dead":
        game_over("dead")

    print("\nAt the forest's edge, you find a clue: a glimmering shard — a Rose Quartz.")
    rose = Crystal("Rose Quartz", power="Charisma", charges=1, description="Soft pink crystal that warms hearts.")
    player.add_item(rose)

    print("\nYou reach the Port and must get across the Coral Sea.")
    res = port_and_coral_sea(player)
    if res == "dead":
        game_over("dead")

    # After sea, chance to meet a trader who returns the amulet to you in exchange for a favor
    print("\nOn the far shore, a cloaked figure beckons. He offers you a deal: help steal back a guard's keys and he will reveal the amulet's location.")
    print("Do you accept? [yes/no]")
    if input("> ").strip().lower() in ("yes","y"):
        print("You retrieve a simple keychain and the cloaked figure keeps his promise.")
        # Receive amulet
        print("You recover an amethyst star-shaped amulet hidden inside a secret box!")
        player.has_amulet = True
        amulet = Item("Amethyst Amulet", "Star-shaped amulet — your family's heirloom.", type_="amulet")
        player.add_item(amulet)
    else:
        print("You decline. You keep moving, but the amulet remains lost for now.")
        # maybe find it later — for simplicity, we give it later via chance
        if roll(0.4):
            print("By chance you find the amulet in a cave. You pick it up.")
            player.has_amulet = True
            amulet = Item("Amethyst Amulet", "Star-shaped amulet — your family's heirloom.", type_="amulet")
            player.add_item(amulet)

    print("\nYou approach the glittering gates of the Crystal Empire.")
    res = crystal_empire_guards(player)
    if res == "dead":
        game_over("dead")
    if res == "jail":
        game_over("jail")
    if res == "explosion":
        game_over("explosion")

    # If allowed through, head to princess
    print("\nYou are escorted into the palace and find the princess awaiting.")
    ending = final_princess_scene(player)
    if ending == "good":
        game_over("good")
    elif ending == "jail":
        game_over("jail")
    elif ending == "explosion":
        game_over("explosion")
    else:
        game_over("dead")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye.")
        sys.exit(0)
