import math

strengthLevel = 99
totalStrength = strengthLevel + 19
attackLevel = 99
totalAttack = attackLevel + 19

AttDefRolls = {
    "AttRoll":0,
    "DefRoll":0
}

prayerStr = {
    "burst":1.05,
    "superhuman":1.10,
    "ultimate":1.15,
    "chivalry":1.18,
    "piety":1.23
}

prayerAtt = {
    "clarity":1.05,
    "improved":1.10,
    "incredible":1.15,
    "chivalry":1.15,
    "piety":1.20
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

    def calcDefRoll(self):
        if (Style["stab"] == True):
            defStyle = self.stabD
        elif (Style["slash"] == True):
            defStyle = self.slashD
        else:
            defStyle = self.crushD
        
        defRoll = (self.defence + 9) * (defStyle + 64)
        AttDefRolls["DefRoll"] = defRoll

class Player:
    def __init__(self, attBonus, strLevel,
                 strBonus, prayer, meleeVoid,
                 effStr, attStyle, maxHit,
                 effAtt):
        self.attBonus = attBonus
        self.strLevel = strLevel
        self.strBonus = strBonus
        self.prayer = prayer
        self.meleeVoid = meleeVoid
        self.effStr = effStr
        self.attStyle = attStyle
        self.maxHit = maxHit,
        self.effAtt = effAtt
        Style[attStyle] = True

    def calcEffStr(self):
        prayerBonus = prayerStr[self.prayer]

        tmp = math.floor(self.strLevel * prayerBonus) + 3
        tmp += 8
        if (self.meleeVoid is not None):
            tmp *= 1.1
        tmp = math.floor(tmp)
        self.effStr = tmp

    def calcEffAtt(self):
        prayerBonus = prayerAtt[self.prayer]

        att = math.floor(totalAttack * prayerBonus)
        att += 8
        if (self.meleeVoid is not None):
            att *= 1.1
        self.effAtt = math.floor(att)

    def calcMaxHit(self):
        multiplier = 1 #1 because of regular monster. Higher if undead, on-task etc..
        max = self.effStr * (self.strBonus + 64)
        max += 320
        max /= 640
        max = math.floor(max)
        max *= multiplier
        max = math.floor(max)
        self.maxHit = max

    def calcAttRoll(self):
        attackMult = 1 #1 because regular monster
        tmpAtt = self.effAtt * (self.attBonus + 64)
        tmpAtt *= attackMult
        AttDefRolls["AttRoll"] = math.floor(tmpAtt)

def calcDps(speed, attRoll, defRoll, maxHit):
    if (attRoll > defRoll):
        hitChance = 1 - ((defRoll + 2) / (2*(attRoll + 1)))
    else:
        hitChance = (attRoll) / (2 * (defRoll + 1))
    
    avgDamage = 0.5 * maxHit * hitChance 
    avgDps = avgDamage / speed
    return avgDps

def calcAvgDuration(health, dps):
    return health / dps

def main():
    weaponSpeed = 4 # in ticks (tick = 0.6 seconds)
    attacker = Player(156, totalStrength, 158,
                      "piety", None, 0, "slash", 0,
                      0)
    attacker.calcEffStr()
    attacker.calcMaxHit()
    attacker.calcEffAtt()
    attacker.calcAttRoll()

    # monster = General Graardor
    monster = NPC(255, 250, 90,
                  90, 90)
    monster.calcDefRoll()
    
    dps = calcDps(weaponSpeed,
                  AttDefRolls["AttRoll"],
                  AttDefRolls["DefRoll"],
                  attacker.maxHit)

    duration = calcAvgDuration(monster.hp, dps)
    print(f'On average the fight will last for  {duration:.0f} seconds')

if __name__ == "__main__":
    main()
