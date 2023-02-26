# py_textrpglib

## About project

What is py_textrpglib?

: It is an in-development text-based role-playing game library for Python developers.

Who is developing py_textrpglib?

: My name is Daniel. I'm a beginner Python programmer, starting in Nov 2022. 

What will py_textrpglib "look" like when finished?

: It will be a simple but flexible library that allows developers to create games with branching paths and user-directed movement in-world (through text, of course). The ruleset is broadly based on the d20 System.

: Another goal is to create template worlds for developers with items and NPCs from specific settings. Developers would also be free to make their own for added customization. 

What is the design ethos for py_textrpglib?

: Classes that model real-world items such as people, weapons, etc., can only perform operations on themselves. Additional classes that store gameplay segments, such as multiple choice menus, etc., can act as bridges between real-world classes, and take user input to do so. 

: Players will be free to explore worlds as they like, and speaking to certain NPCs or main characters will give an opportunity for a side quest, or to continue a main quest plotline. Similar to tabletop RPGs and dungeon crawls, the library will be designed to support these segments being more focussed on story and less exploratory for players.

## Sample deployment code

````python
import source as rp


# Money is given is US cent amounts
# Weight is given in gram amounts

# WEAPONS #
colt_45 = rp.Weapon(
    "Colt .45",
    cost=9_90,
    desc="Six-shooter manufactured by Colt. Good at close quarters.",
    attack=rp.Dice(2),
    damage=rp.Dice(2, 6),
)

# ITEMS #
rations = rp.Item("rations", cost=2_70, desc="3 days' rations.")
water = rp.Item("water", cost=15, desc="A waterskin holding half a day's water.")

# ARMOR #
light_leath_armor = rp.Armor(
    "light leather armor",
    cost=13_00,
    desc="Lightly padded leather armor. Good enough to stop a bullet at long range.",
    mod=1,
)

# SPELLS #
cure_light_wounds = rp.Spell(
    "spell of cure light wounds",
    cost=2_30,
    desc="Cures light wounds, such as cuts and braises.",
    effects=(rp.ProxyCallable(rp.Player.instance.hp.heal, rp.Dice(1, 4)),),
)


# ASSIGNING PLAYER ATTRIBUTES
player = rp.Player(name=input("\t> What is your character's name? "))

(
    player.scores.assign(
        strength=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
        dexterity=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
        intelligence=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
        wisdom=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
        charisma=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
        constitution=sum(sorted([rp.Dice(0, 6)() for i in range(4)])[1:]),
    )
    .money.receive(rp.Dice(1, 4)() * 10)
    .inventory.add(
        rations.copy().set_count(2), water.copy().set_count(2), light_leath_armor.copy()
    )
    .weapons.add(colt_45)
    .spells.add(cure_light_wounds.copy())
)

# CHAINED AND NESTED BRANCHING
rp.AbilityCheck(
    on_pass=[
        rp.ProxyCallable(
            print,
            f"{player.name} leaps over the gorge and across to the other side for safety!",
        ),
    ],
    on_fail=[
        rp.MultipleChoice(
            f"{player.name} takes a mighty run, but before she can reach the edge, she slips and"
            "begins to fall. She tumbles down the steep cliff side and, some well-placed branches"
            "slowing her descent, falls in a heap on the ground.",
            options=[
                "Try to find a way back up the cliff face",
                "See if there's another way around",
            ],
            outcomes=[
                [rp.MultipleChoice("...", options=[...], outcome=[...])],
                [locations.Cliffvale],
            ],
        ),
    ],
)
````
