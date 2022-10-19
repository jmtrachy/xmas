__author__ = 'jamest'

import argparse
import json
import random
from typing import Optional


class Hat:
    participants = [
        'Janet', 'Bill', 'Jennifer', 'Nathan', 'Julia', 'Sam', 'James', 'Teri'
    ]

    def __init__(self):
        self.receivers = Hat.participants.copy()
        self.pickers = Hat.participants.copy()

        # Spouses don't get each other
        self.spouse_combos = {
            'James': 'Teri',
            'Teri': 'James',
            'Janet': 'Bill',
            'Bill': 'Janet',
            'Julia': 'Sam',
            'Sam': 'Julia',
            'Nathan': 'Jennifer',
            'Jennifer': 'Nathan'
        }

        # Last year's picks
        self.last_year_combos = {
            'Janet': 'Nathan',
            'Bill': 'James',
            'Jennifer': 'Julia',
            'Nathan': 'Sam',
            'Julia': 'Teri',
            'Sam': 'Janet',
            'James': 'Bill',
            'Teri': 'Jennifer'
        }

        # Shuffle the pickers
        random.shuffle(self.pickers)
        self.matches = {}

    def make_pick(self, picker: str) -> Optional[str]:
        valid_pick = False
        pick = None
        position = 0
        attempts = 0

        while not valid_pick and attempts < 50:
            position: int = random.randint(0, len(self.receivers) - 1)
            pick: str = self.receivers[position]
            if pick != picker:
                if self.spouse_combos.get(picker) != pick and self.last_year_combos.get(picker) != pick:
                    self.receivers.remove(pick)
                    valid_pick = True
            attempts += 1

        if valid_pick:
            return pick
        else:
            return None

    def make_picks(self):
        for picker in self.pickers:
            receiver = self.make_pick(picker)
            if receiver is None:
                #print('We seem to have reached an impossible to resolve situation where {} has no valid '
                #      'choices in the hat'.format(picker))
                return None

            self.matches[picker] = receiver

        #for p, r in self.matches.items():
        #    print(p + ' will be buying a gift for ' + r)

        return self.matches


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Gathering arguments')
    parser.add_argument('-n', required=True, dest='num_iterations', action='store',
                        help='The number of iterations to run')
    args = parser.parse_args()

    combos = {}
    none_picks = 0

    for j in range(0, int(args.num_iterations)):
        hat = Hat()
        picks = hat.make_picks()

        if picks is not None:
            result = str(picks)
            if result in combos:
                num_matches = combos[result]
            else:
                num_matches = 0
            num_matches += 1
            combos[result] = num_matches
        else:
            none_picks += 1

    top_fit = 0
    final = None
    for k, v in combos.items():
        if v > top_fit:
            top_fit = v
            final = k

    #print(result)
    #result = result.replace('\'', '"')
    final_results = json.loads(final.replace('\'', '"'), strict=True)

    print('total none picks = {}'.format(none_picks))
    for k, v in final_results.items():
        print(k + ' will be buying for ' + v)
    print('This decision was based on ' + str(args.num_iterations) + ' attempts at drawing names out of a hat.  The result displayed occurred ' + str(top_fit) + ' times.')
