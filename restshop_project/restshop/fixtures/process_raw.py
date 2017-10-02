from json import load, dump
from argparse import ArgumentParser

from fixture_creator import FixtureCreator


def get_args():
    parser = ArgumentParser(description='Process raw data after scraping')

    parser.add_argument('-i',
                        metavar='INPUT',
                        dest='infile',
                        required=True,
                        help='JSON file with scraped data')
    parser.add_argument('-o',
                        metavar='OUTPUT',
                        dest='outfile',
                        required=True,
                        help='target JSON')

    return parser.parse_args()


def main():
    args = get_args()

    with open(args.infile) as infile:
        data = load(infile)

    fm = FixtureCreator(data)
    fixtures = fm.get_fixtures()

    with open(args.outfile, 'w') as outfile:
        dump(fixtures, outfile, indent=4)


if __name__ == '__main__':
    main()
