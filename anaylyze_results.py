import json
from typing import Dict


def load_results() -> Dict:
    with open('xmas_results.json', 'r') as json_data:
        results = json.load(json_data)
    return results


if __name__ == '__main__':
    raw_results = load_results()
    results_to_person_map = {}

    # loop through each person and figure out their frequency
    for year in raw_results.keys():
        hat_picks = raw_results.get(year)
        for picker in hat_picks.keys():
            receiver = hat_picks.get(picker)
            picker_total = results_to_person_map.get(picker)
            if picker_total is None:
                picker_total = {}

            picker_receiver_total = picker_total.get(receiver)
            if picker_receiver_total is None:
                picker_receiver_total = 0
            picker_receiver_total += 1

            picker_total[receiver] = picker_receiver_total
            results_to_person_map[picker] = picker_total

    print('results = {}'.format(json.dumps(results_to_person_map)))

    with open('xmas_results_by_person.json', 'w') as file:
        file.write(json.dumps(results_to_person_map, indent=4, sort_keys=True))
