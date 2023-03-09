from source import Weapon, Dice


colt45 = Weapon(
    "Colt .45",
    cost=6_70,
    desc="A military-issue Colt .45, strong enough to penetrate light armor at close range",
    attack=Dice(mod=1),
    damage=Dice(mod=2, dice=6),
    ammo=6,
)
