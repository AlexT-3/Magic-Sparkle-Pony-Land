# Magic-Sparkle-Pony-Land

**Magic Pony Sparkle Land** is a Python-based fantasy text adventure where you embark on a quest through a magical world filled with unicorns, dragons, and enchanted crystals.  
Your goal is to **escape the dungeon**, recover your **lost amulet**, and return it to the **Princess of the Crystal Kingdom** — if you can survive the journey.

---

## 🌈 Story Summary

While grazing for berries one night in the peaceful village of **Rainbowtopia**, you are kidnapped and trapped in a dungeon deep inside a crystal cavern.  
Your captor, a terrifying **Bulldog Cerberus**, steals your **Amethyst Star Amulet**, claiming it holds **royal crystal magic** that can control the kingdom itself.  

You must escape, reclaim your amulet, and travel through:
- 🐉 **Dragon Mountains** – Battle baby dragons.  
- 🌲 **Haunted Forest** – Deal with a malicious spirit.  
- 🌊 **Coral Sea** – Find a boat and cross dangerous waters.  
- 💎 **Crystal Empire** – Face the final choice before the princess.

Multiple endings await based on your choices:
- ✨ **Good Ending** – Return the amulet and earn your place in the empire.  
- 🚔 **Jail Ending** – Fail to convince the guards of your innocence.  
- 💥 **Explosion Ending** – Drop the amulet… with catastrophic results.  
- 💀 **Death Ending** – Perish in battle.

---

## 🧝 Character Options

When starting the game, you can choose your pony type:

| Pony Type | Magic | Strength | Agility |
|------------|--------|-----------|----------|
| **Earth Pony** | 2 | 9 | 5 |
| **Unicorn** | 8 | 3 | 6 |
| **Pegasus** | 6 | 4 | 4 |

Each has its own strengths and weaknesses that affect combat and interactions.

---

## 🔮 Crystals and Powers

During your adventure, you can collect magical crystals, each with unique powers and limited uses:

| Crystal | Power |
|----------|--------|
| 💙 **Lapis** | Telekinesis |
| 💚 **Jade** | Healing |
| ⚫ **Obsidian** | Protection Shield |
| 💛 **Citrine** | Fire Powers |
| 🤍 **Clear Quartz** | Projectile Powers |
| 💗 **Rose Quartz** | Charisma / Persuasion |

---

## ⚔️ Weapons

You may find or loot the following weapons during your journey:
- Staffs  
- Swords  
- Bows  
- Crossbows  
- Knives  
- Axes  

Your weapon and stats determine how effective attacks are during combat.

---

## 🧰 Inventory System

Use your inventory to:
- View collected weapons and crystals.  
- Use, equip, or discard items.  
- Heal or use powers during fights.

The game handles all unexpected inputs gracefully (e.g., invalid commands or empty inventory).

---

## 🕹️ Commands

During gameplay, you’ll encounter text prompts where you can enter commands such as:
* fight
* use magic
* flee
* inventory
* use [item]
* discard [item]

If you enter something invalid, the game will respond with:

That’s not a valid command.


---

## 💻 Installation & Running the Game

### Prerequisites
- Python 3.8 or newer

### How to Play
1. Download the Python file: `magic_pony_sparkle_land.py`
2. Open a terminal or command prompt.
3. Navigate to the folder containing the script.
4. Run: `unicorn.py`

## Code structure:
### Classes:
* Player() – handles stats, inventory, and combat
* Enemy() – defines battle opponents
* Item() – defines weapons and crystals
### Functions:
* battle() – combat sequence logic
* explore() – manages game events and areas
* choose_pony() – pony selection and stat assignment
* show_inventory() – view and manage items
* main() – main game loop

## 🎯 Objectives
* Escape the dungeon
* Recover your stolen amulet
* Travel through magical lands
* Defeat enemies and survive
* Return the amulet to the Princess
* Unlock one of the four possible endings

## 🧙 Credits

Created by Alex Tuell & ChatGPT (GPT-5)
© 2025 – Magic Pony Sparkle Land 🦄
A whimsical adventure written entirely in Python!

