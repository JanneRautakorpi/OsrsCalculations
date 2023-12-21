class NPC:
    def __init__(self, hp, defence,
                mage, range, stabD,
                slashD, crushD, mageD,
                rangeD):
        self.hp = hp
        self.defence = defence
        self.mage = mage
        self.range = range
        self.stabD = stabD
        self.slashD = slashD
        self.crushD = crushD
        self.mageD = mageD
        self.rangeD = rangeD

def main():
    bandos = NPC(255, 250, 80, 350,
                 90, 90, 90, 298, 90)
    