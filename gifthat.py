__author__ = 'jamest'

import argparse
import json
import random


class Hat():

    __participants = [
        'Janet', 'Bill', 'Jennifer', 'Nathan', 'Julia', 'Sam', 'James', 'Teri'
    ]

    __invalid_combos = {
        'James': 'Teri',
        'Teri': 'James',
        'Janet': 'Bill',
        'Bill': 'Janet',
        'Julia': 'Sam',
        'Sam': 'Julia',
        'Nathan': 'Jennifer',
        'Jennifer': 'Nathan'
    }

    def __init__(self):
        self.receivers = Hat.__participants.copy()
        self.pickers = Hat.__participants.copy()
        self.matches = {}

    def make_pick(self, picker):
        valid_pick = False
        pick = None
        position = 0
        attempts = 0

        while not valid_pick and attempts < 50:
            position = random.randint(0, len(self.receivers) - 1)
            pick = self.receivers[position]
            if pick != picker:
                if Hat.__invalid_combos[picker] != pick:
                    self.receivers.remove(pick)
                    valid_pick = True
            attempts += 1

        return pick

    def make_picks(self):
        for picker in self.pickers:
            receiver = self.make_pick(picker)
            if receiver is None:
                print('We seem to have reached an impossible to resolve situation where ' + picker + ' has no valid choices in the hat')

            self.matches[picker] = receiver

        #for p, r in self.matches.items():
        #    print(p + ' will be buying a gift for ' + r)

        return self.matches


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gathering arguments')
    parser.add_argument('-n', required=True, dest='num_iterations', action='store', help='The number of iterations to run')
    args = parser.parse_args()

    combos = {}

    for j in range(0, int(args.num_iterations)):
        hat = Hat()
        result = str(hat.make_picks())

        if result in combos:
            num_matches = combos[result]
        else:
            num_matches = 0

        num_matches += 1
        combos[result] = num_matches

    top_fit = 0
    final = None
    for k, v in combos.items():
        if v > top_fit:
            top_fit = v
            final = k

    print(result)
    result = result.replace('\'', '"')
    final_results = json.loads(result, strict=True)

    for k, v in final_results.items():
        print(k + ' will be buying for ' + v)
    print('This decision was based on ' + str(args.num_iterations) + ' attempts at drawing names out of a hat.  The result displayed occurred ' + str(top_fit) + ' times.')