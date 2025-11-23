from enum import Enum
import random
from typing import Dict, List, Optional, Set


class Person(Enum):
    XAVIER = 'Xavier'
    JANET = 'Janet'
    BILL = 'Bill'
    SAM = 'Sam'
    JULIA = 'Julia'
    JENNIFER = 'Jennifer'
    NATHAN = 'Nathan'
    TERI = 'Teri'
    JAMES = 'James'


relationships: Dict[Person, Set[Person]] = {
    Person.XAVIER: {Person.JENNIFER, Person.NATHAN},
    Person.JANET: {Person.BILL},
    Person.BILL: {Person.JANET},
    Person.SAM: {Person.JULIA},
    Person.JULIA: {Person.SAM},
    Person.JENNIFER: {Person.XAVIER, Person.NATHAN},
    Person.NATHAN: {Person.XAVIER, Person.NATHAN},
    Person.TERI: {Person.JAMES},
    Person.JAMES: {Person.TERI},
}

last_year: Dict[Person, Person] = {
    Person.JANET: Person.XAVIER,
    Person.BILL: Person.TERI,
    Person.JENNIFER: Person.SAM,
    Person.JAMES: Person.BILL,
    Person.NATHAN: Person.JAMES,
    Person.JULIA: Person.NATHAN,
    Person.SAM: Person.JANET,
    Person.XAVIER: Person.JULIA,
    Person.TERI: Person.JENNIFER,
}


def determine_legit_pairings(picker: Person) -> Set[Person]:
    return {
        recipient
        for recipient in Person
        if recipient not in (relationships[picker] | {last_year[picker]} | {picker})
    }


valid_combos: Dict[Person, Set[Person]] = {
    p: determine_legit_pairings(p) for p in Person
}


class GiftHat:
    def __init__(self):
        self.all_recipients: Set[Person] = set()
        self.combos: Dict[Person, Person] = {}

    def pick(self, picker: Person) -> Person:
        valid_remaining_combos: List[Person] = list(valid_combos[picker] - self.all_recipients)
        if not valid_remaining_combos:
            print(f'attempted to pick for {picker.value} but only {",".join([p.value for p in Person if p not in self.all_recipients])} remains')
            raise RuntimeError('no valid choices')

        the_pick = random.choice(valid_remaining_combos)
        self.all_recipients.add(the_pick)

        return the_pick

    def everybody_pick(self) -> Dict[Person, Person]:
        count = 0
        while not self.combos and count < 100:
            count += 1
            try:
                self.combos = {
                    p: self.pick(p) for p in Person
                }
            except RuntimeError:
                self.combos = {}
                self.all_recipients = set()

        return self.combos


if __name__ == '__main__':
    gh = GiftHat()

    picks = gh.everybody_pick()
    for pick, recipient in picks.items():
        print(f'{pick.value} will be buying for {recipient.value}')
