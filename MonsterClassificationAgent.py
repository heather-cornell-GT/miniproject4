class MonsterClassificationAgent:
    parameters = {
        "size": ["tiny", "small", "medium", "large", "huge"],
        "color": ["black", "white", "brown", "gray", "red", "yellow", "blue", "green", "orange", "purple"],
        "covering": ["fur", "feathers", "scales", "skin"],
        "foot-type": ["paw", "hoof", "talon", "foot", "none"],
        "leg-count": list(range(9)),
        "arm-count": list(range(9)),
        "eye-count": list(range(9)),
        "horn-count": [0, 1, 2],
        "lays-eggs": [True, False],
        "has-wings": [True, False],
        "has-gills": [True, False],
        "has-tail": [True, False],
    }
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, samples, new_monster):
        #Add your code here!
        #
        #The first parameter to this method will be a labeled list of samples in the form of
        #a list of 2-tuples. The first item in each 2-tuple will be a dictionary representing
        #the parameters of a particular monster. The second item in each 2-tuple will be a
        #boolean indicating whether this is an example of this species or not.
        #
        #The second parameter will be a dictionary representing a newly observed monster.
        #
        #Your function should return True or False as a guess as to whether or not this new
        #monster is an instance of the same species as that represented by the list.
        for monster, label in samples:
            if monster == new_monster:
                return label

        positives = []
        negatives = []
        for monster, label in samples:
            if label:
                positives.append(monster)
            else:
                negatives.append(monster)

        if not positives:
            return False
        pass

    def probability_of_unseen_being_valid(parameter_lenth, parameters_seen, position):
        still_unseen = parameter_lenth - parameters_seen
        if still_unseen <= 0:
            return 0.0
        

    def agent_confidence(self, positives, negatives):
        seen_characteristics = {}
        for index in self.parameters:
            print(index)
            values_in_each_characteristic = set()
            for x in positives:
                values_in_each_characteristic.add(x[index])
            seen_characteristics[index] = values_in_each_characteristic


