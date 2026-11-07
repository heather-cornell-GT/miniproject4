from math import comb, log
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
    reject_threshold = 0.01
    smoothning = 4.0
    def __init__(self, parameters):
        self.parameters = parameters
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

        #You may assume that these parameters are all that there is: if two monsters have the exact same parameters, they are guaranteed to be the same species.
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

        seen, confidence = self.agent_confidence(positives, negatives)
        #print(f'seen: {seen}, confidence: {confidence}')

        all_traits_allowed = 1.0
        for trait in self.parameters:
            value = new_monster[trait]
            all_traits_allowed *= confidence[(trait,value)]

            if all_traits_allowed < self.reject_threshold:
                return False



        is_a_member, is_not_a_member = 0.0, 0.0

        for trait, possible_value in self.parameters.items():
            value = new_monster[trait]

            allowed_count_of_values =len(seen[trait])

            for y in possible_value:
                if y not in seen[trait]:
                    allowed_count_of_values += confidence[(trait,y)]

            iterate_through_allowed_traits = confidence[(trait, value)] / allowed_count_of_values

            if iterate_through_allowed_traits <= 0.0:
                return False
            is_a_member += log(iterate_through_allowed_traits)

            negative_trait_counts = 0

            for negative in negatives:
                if negative[trait] == value:
                    negative_trait_counts += 1

            iterate_through_nonallowed_traits = ((negative_trait_counts + self.smoothning) /(len(negatives) + self.smoothning * len(possible_value)))
            is_not_a_member += log(iterate_through_nonallowed_traits)

        return is_a_member >= is_not_a_member

    def probability_of_unseen_being_valid(self, parameter_lenth, parameters_seen, position):
        still_unseen = parameter_lenth - parameters_seen
        if still_unseen <= 0: ##every possible combinatoin was already seen
            return 0.0
        if parameters_seen == 0:
            return 0.5

        weight = 0.0
        total = 0.0

        for x in range(still_unseen + 1): ##trying every combintation of parameters

            parameter_combinations = comb(parameters_seen, x)
            parameter_set_size = parameters_seen + x
            percent_of_possibility = (1.0 / parameter_set_size) ** position
            odds_of_possibility = parameter_combinations * percent_of_possibility

            fraction_of_odds = x / still_unseen

            weight += fraction_of_odds
            total += odds_of_possibility * fraction_of_odds

        return total / weight





    def agent_confidence(self, positives, negatives):
        seen_characteristics, confidence = {}, {}
        for index in self.parameters:
            #print(index)
            values_in_each_characteristic = set()
            for x in positives:
                values_in_each_characteristic.add(x[index])
            seen_characteristics[index] = values_in_each_characteristic

        #confidence maps (trait, value) to a  chance that value is possible, like confidence[("covering", "scales")] = 0.037
        for trait, possible_trait_values in self.parameters.items():
            traits_seen = seen_characteristics[trait]
            #print(f'{trait}: {traits_seen}, possible_trait_values: {possible_trait_values}, positives: {len(positives)}, negatives: {len(negatives)}')
            unseen_trait = self.probability_of_unseen_being_valid( len(possible_trait_values), len(traits_seen), len(positives))
            #print(f'unseen_trait: {unseen_trait}')

            for trait_values in possible_trait_values:
                if trait_values in traits_seen:
                    confidence[(trait, trait_values)] = 1.0
                else:
                    confidence[(trait, trait_values)] = unseen_trait

        return seen_characteristics, confidence