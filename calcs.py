import random
import math

strengthLevel = 99
totalStrength = strengthLevel + 19
attackLevel = 99

prayerMultipliers = {
    "burst":1.05,
    "superhuman":1.10,
    "ultimate":1.15,
    "chivalry":1.18,
    "piety":1.23
}

Style = {
    "stab":False,
    "slash":False,
    "crush":False
}

class NPC:
    def __init__(self, hp, defence,
                 stabD, slashD, crushD):
        self.hp = hp
        self.defence = defence
        self.stabD = stabD
        self.slashD = slashD
        self.crushD = crushD

class Player:
    def __init__(self, attBonus, strLevel,
                 strBonus, prayer, meleeVoid,
                 effStr, attStyle, maxHit):
        self.attBonus = attBonus
        self.strLevel = strLevel
        self.strBonus = strBonus
        self.prayer = prayer
        self.meleeVoid = meleeVoid
        self.effStr = effStr
        self.attStyle = attStyle
        self.maxHit = maxHit
        Style[attStyle] = True

    def calcEffStr(self):
        prayerBonus = prayerMultipliers[self.prayer]

        tmp = math.floor(self.strLevel * prayerBonus) + 3
        tmp += 8
        if (self.meleeVoid is not None):
            tmp *= 1.1
        tmp = math.floor(tmp)
        self.effStr = tmp

    def calcMaxHit(self):
        multiplier = 1 #1 because of regular monster. Higher if undead, on-task etc..
        max = self.effStr * (self.strBonus + 64)
        max += 320
        max /= 640
        max = math.floor(max)
        max *= multiplier
        max = math.floor(max)
        self.maxHit = max

def main():
    # monster = General Graardor
    monster = NPC(255, 250, 90,
                  90, 90)
    attacker = Player(156, totalStrength, 158,
                      "piety", None, 0, "slash", 0)
    attacker.calcEffStr()
    attacker.calcMaxHit()
    print(attacker.maxHit)

if __name__ == "__main__":
    main()
