import random

def roll_dice(text):
    dice_roll = text.split("d")
    results = []
    for dice in range(int(dice_roll[0])):
        roll = random.randint(1,int(dice_roll[1]))
        results.append(roll)
    return results