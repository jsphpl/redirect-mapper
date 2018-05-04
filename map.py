#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generates a redirect map from two sitemaps for website migration.

By default, all matches are dumped on the standard output. If an item
from list1 is exactly contained in list2, it will be assigned right
away, without calculating distance or checking for ambiguity.

Issues & Documentation: https://github.com/jsphpl/redirect-mapper
"""

import csv
import argparse
import Levenshtein

def main(args):
    # Read files into memory and remove trailing newlines
    list1 = [line[:-1] for line in args.list1]
    list2 = [line[:-1] for line in args.list2]

    # Inform the user what's happening
    print('%i lines in list1' % len(list1))
    print('%i lines in list2' % len(list2))
    print('Threshold is %f' % args.threshold)

    # Do the hard work
    iterator = levenshteinMatch(list1, list2, args.threshold, args.drop_exact)

    # Ouput results
    if (args.csv):
        print('Writing CSV output to "%s"' % args.csv)
        with open(args.csv, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(('Item (list1)', 'Match (list2)', 'Score', 'Ambiguous', 'Exact', 'Alternatives'))
            writer.writerows(iterator)
    else:
        print('\nResults:')
        print('--------------------------------------------------------------------------------')
        for item in iterator:
            print(item)
        print('--------------------------------------------------------------------------------')
        print('Note: Use the --csv flag to save results into a file')

def levenshteinMatch(list1, list2, threshold, drop_exact):
    """Find matches based on the levenshtein distance.

    Arguments:
        list1 {List} -- List of target items for which to find matches
        list2 {List} -- List of search items on which to search for matches
        threshold {float} -- Range within which two scores are considered equal
        drop_exact {bool} -- Omit exact matches
    """
    for key in list1:
        if key in list2:
            # Can skip all the Levenshtein in this case
            if not drop_exact:
                yield((key, key, 1.0, False, True, []))

        else:
            # Calculate all scores
            scores = [round(Levenshtein.ratio(key, value), 2) for value in list2]

            # Find all matches within `threshold` of the highest score
            max_score = max(scores)
            winners = [i for i, score in enumerate(scores) if max_score - score <= threshold]
            winners.sort(reverse=True)

            # Prepare result values for current pass
            is_ambiguous = len(winners) > 1
            winner_index = None
            winner = None
            winner_score = None
            alternatives = []

            winner_index = winners[0]

            if winner_index is not None:
                winner = list2[winner_index]
                winner_score = scores[winner_index]

            if is_ambiguous:
                winners.remove(winner_index)
                alternatives = [list2[index] for index in winners]

            yield (key, winner, winner_score, is_ambiguous, False, alternatives)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('list1', type=argparse.FileType('r'),
                        help='List of target items for which to find matches. (1 item per line)')
    parser.add_argument('list2', type=argparse.FileType('r'),
                        help='List of search items on which to search for matches. (1 item per line)')
    parser.add_argument('-t', '--threshold', type=float, default=0.05, metavar='VALUE',
                        help='Range within which two scores are considered equal. (default: 0.05)')
    parser.add_argument('-c', '--csv', type=str, metavar='PATH',
                        help='If specified, the output will be formatted as CSV and written to PATH')
    parser.add_argument('-d', '--drop-exact', action='store_true',
                        help='If specified, exact matches will be ommited from the output')

    main(parser.parse_args())
