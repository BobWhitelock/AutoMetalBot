#!/usr/bin/env python3

import csv

import bot

EVALUATION_DATA_FILE = 'evaluation_data/HeadBangToThis-new-2015-03-05'


def evaluate_identify():
    with open(EVALUATION_DATA_FILE, newline = '') as dsvfile:
        rows = list(csv.reader(dsvfile,
            delimiter='|',
            quoting=csv.QUOTE_NONE,
            skipinitialspace=True,
            strict=True)
        )

    total_identified = 0
    no_correct_link_exists_identified = 0
    correct_link_exists_identified = 0

    total = len(rows)
    total_where_no_correct_link_exists = len([row for row in rows if row[2] == ""])
    total_where_correct_link_exists = total - total_where_no_correct_link_exists

    misidentified = []

    for row in rows:
        title = row[0]
        correct_link = row[2] if row[2] != '' else None
        identified_link = bot.identify(title)
        if identified_link == correct_link:
            total_identified += 1
            if correct_link is None:
                no_correct_link_exists_identified += 1
            else:
                correct_link_exists_identified += 1
        else:
            misidentified.append((identified_link, row))

    print("\nTotal correctly identified: {}/{}".format(total_identified, total))
    print("Submissions where no correct link correctly identified: {}/{}".format(no_correct_link_exists_identified, total_where_no_correct_link_exists))
    print("Submissions where correct link exists correctly identified: {}/{}".format(correct_link_exists_identified, total_where_correct_link_exists))
    print("\nMisidentified:")
    for identified_link, row in misidentified:
        title = row[0]
        correct_link = row[2] if row[2] != '' else None
        print("'{}' identified as {}. Correct link: {}".format(title, identified_link, correct_link))
    print()

if __name__ == '__main__':
    evaluate_identify()