import math
import random

strengthLevel = 99
totalStrength = strengthLevel + 19
attackLevel = 99
totalAttack = attackLevel + 19

AttDefRolls = {
    "AttRoll":0,
    "DefRoll":0
}

# Strength multipliers when prayer is activated
prayerStr = {
    "burst":1.05,
    "superhuman":1.10,
    "ultimate":1.15,
    "chivalry":1.18,
    "piety":1.23
}

# Attack multipliers when prayer is activated
prayerAtt = {
    "clarity":1.05,
    "improved":1.10,
    "incredible":1.15,
    "chivalry":1.15,
    "piety":1.20
}

# To determine which style is being used
Style = {
    "stab":False,
    "slash":False,
    "crush":False
}

class NPC:
    '''
    Class is for NPCs (non-player characters).

    Args and attributes (identical in this case):
        hp (int): amount of health NPC has
        defence (int): defence level
        stabD (int): defence bonus for stab style
        slashD (int): defence bonus for slash style
        crushD (int): defence bonus for crush style
    '''
    def __init__(self, hp, defence,
                 stabD, slashD, crushD):
        self.hp = hp
        self.defence = defence
        self.stabD = stabD
        self.slashD = slashD
        self.crushD = crushD

    def getHp(self):
        return self.hp
    
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
    '''
    Class is to hold player object's properties. They are used
    to simulate fights with fight-specific values.

    Args:
        attBonus (int): player's total attack bonus (gear dependant)
        strLevel (int): player's total strength level (base level + boost)
        strBonus (int): strength bonus (gear dependant)
        prayer (str): key to get corresponding multiplier from global dictionary
        meleeVoid (bool): If the player has void melee. None as default
        attStyle (str): chosen attack style
        
    Attributes:
        All arguments and next three:
        maxHit (int): describes player's maximal damage hitsplat. 0 as default, calculated later
        effAtt (int): effective attack level
        effStr (int): effective strength level. Used to calculate max hits
    '''

    def __init__(self, attBonus, strLevel,
                 strBonus, prayer, meleeVoid,
                 attStyle):
        self.attBonus = attBonus
        self.strLevel = strLevel
        self.strBonus = strBonus
        self.prayer = prayer
        self.meleeVoid = meleeVoid
        self.effStr = 0
        self.attStyle = attStyle
        self.maxHit = 0,
        self.effAtt = 0
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
    '''
    Calculates the very average damage-per-second.

    Parameters:
        speed (int): attack speed of given weapon in seconds
        attRoll (int): rolled attack
        defRoll (int): rolled attack
        maxHit (int): maximum value of damage

    Return:
        avgDps (float): Damage-per-second
    '''
    roll = hitChance(attRoll, defRoll)

    avgDamage = 0.5 * maxHit * roll 
    avgDps = avgDamage / speed
    return avgDps

def calcAvgDuration(health, dps):
    '''
    Calculates the average time the fight takes.

    Parameters:
        health (int): how much health does the enemy (NPC) have
        dps (int): average damage-per-second

    Return:
        average fight duration in seconds
    '''
    return health / dps

def hitChance(attRoll, defRoll):
    '''
    Calculates the chance of successful hit

    Paramters:
        attRoll (int): attack roll
        defRoll (int): defense roll

    Return:
        hitChance (int): Probability of rolling successful hit [0, 1].
    '''

    if (attRoll > defRoll):
        hitChance = 1 - ((defRoll + 2) / (2 * (attRoll + 1)))
    else:
        hitChance = (attRoll) / (2 * (defRoll + 1))

    return hitChance

def simulation(npc, player, speed, count):
    '''
    Simulates fight 'count' times. 

    Parameters:
        npc (NPC): enemy of the fight
        player (Player): attacker
        speed (int): attack speed of the weapon, given in seconds. Converted to ticks later on
        count (int): how many times simulation is ran

    Return:
        average time (in ticks) of simulated fights
    '''
    ticks = 0
    totalTicks = 0
    health = getattr(npc, "hp")
    maxhit = getattr(player, "maxHit")
    chance = hitChance(AttDefRolls["AttRoll"], AttDefRolls["DefRoll"])
    speed /= 0.6 # conversion to ticks

    for _ in range(count):
        while (health > 0):
            rolledAccuracy = random.random()
            rolledDamage = random.randint(0, maxhit)

            if (rolledAccuracy > chance):
                #print(f"health: {health} - dmg: {rolledDamage}")
                health -= rolledDamage
            ticks += speed

        # reset values back to normal.
        health = getattr(npc, "hp")
        totalTicks += ticks
        ticks = 0
    
    averageTicks = (totalTicks) / (count)
    return averageTicks

def main():
    weaponSpeed = 4 * 0.6 # in seconds. (ticks * 0.6s)
    simulationCount = 2

    attacker = Player(156, totalStrength, 158,
                      "piety", None, "slash")
    attacker.calcEffStr()
    attacker.calcMaxHit()
    attacker.calcEffAtt()
    attacker.calcAttRoll()

    # monster = General Graardor
    monster = NPC(255, 250, 90,
                  90, 90)
    monster.calcDefRoll()
    
    print(simulation(monster, attacker, weaponSpeed, simulationCount))
    
    """dps = calcDps(weaponSpeed,
                  AttDefRolls["AttRoll"],
                  AttDefRolls["DefRoll"],
                  attacker.maxHit)
    
    duration = calcAvgDuration(monster.hp, dps)
    print(f'On average the fight will last for  {duration:.0f} seconds')
    """
if __name__ == "__main__":
    main()
