#!/usr/bin/env python

"""Download files from UPenn Butterflies of Costa Rica Web Site."""

import argparse
import re
import socket
import urllib.request
from urllib.error import HTTPError

import pandas as pd
from bs4 import BeautifulSoup

from src.pylib.util import DATA_DIR

# Make a few attempts to download a page
ERROR_SLEEP = 120
ERROR_RETRY = 10

# Set a timeout for requests
TIMEOUT = 30
socket.setdefaulttimeout(TIMEOUT)

# Just throw everything in here
OUT_DIR = DATA_DIR / 'costa_rica'

# URL parts for the crawl
SITE = 'http://janzen.sas.upenn.edu/caterpillars/'
FAMILY = SITE + 'checklists/{}list.htm'
GENUS = SITE + 'dblinks/cklistfd.lasso?{}herbsp={}'
SKIP = '-SkipRecords={}&'

# Used to figure out how many pages for each genus
COUNTS = re.compile(
    r'Displaying records (\d+) to (\d+) of (\d+) records',
    flags=re.IGNORECASE)


def main(args):
    """Download the data."""
    print(args.family)
    family_page = get_family_page(args)
    genera = get_genera(family_page)

    if args.reverse:
        genera.reverse()

    for genus in genera:
        print(genus)
        genus_links = get_genus_links(args, genus)
        print(genus_links[0][1].name)
        for url, path in genus_links[1:]:
            print(path.name)
            download_page(url, path)

    if args.csv_file:
        write_results(args)


def write_results(args):
    """Output the concatenated tables to a CSV file."""
    paths = [p for p in OUT_DIR.glob(f'{args.family}_*.html')]
    dfs = [pd.read_html(str(p), header=0)[0].fillna('') for p in paths]
    df = pd.concat(dfs, ignore_index=True)
    df.to_csv(args.csv_file, index=False)


def get_genus_links(args, genus):
    """Get the first page for the genus."""
    links = []

    url = GENUS.format('', genus)
    path = OUT_DIR / f'{args.family}_{genus}_1.html'
    links.append((url, path))
    download_page(url, path)

    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features='lxml')

    for font in soup.findAll('font'):
        text = font.get_text()
        if match := COUNTS.search(text):
            _, step, total = [int(g) for g in match.groups()]
            if step == 0 or total == 0:
                continue
            for page_no, skip in enumerate(range(step, total, step), 2):
                skip = SKIP.format(skip)
                url = GENUS.format(skip, genus)
                path = OUT_DIR / f'{args.family}_{genus}_{page_no}.html'
                links.append((url, path))
            break

    print(f'Count: {len(links)}')
    return links


def get_genera(family_page):
    """Get all genera for the family."""
    genera = []
    with open(family_page) as in_file:
        page = in_file.read()

    soup = BeautifulSoup(page, features='lxml')
    for tr in soup.findAll('tr'):
        tds = tr.findAll('td')
        genus = tds[0].get_text() if tds else ''
        if len(genus.split()) == 1:
            genera.append(genus)

    return genera


def get_family_page(args):
    """Download the master list of checklists."""
    url = FAMILY.format(args.family)
    path = OUT_DIR / f'{args.family}.html'
    download_page(url, path)
    return path


def download_page(url, path):
    """Download a page if it does not exist."""
    if path.exists():
        return

    for attempt in range(ERROR_RETRY):
        if attempt > 0:
            print(f'Attempt {attempt + 1}')
        try:
            urllib.request.urlretrieve(url, path)
            # time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))
            break
        except (TimeoutError, socket.timeout, HTTPError):
            pass


def parse_args():
    """Process command-line arguments."""
    description = """Download files from Butterflies of Costa Rica Web Site."""
    arg_parser = argparse.ArgumentParser(description=description)

    arg_parser.add_argument(
        '--family', '-f', default='hesperiidae',
        help="""The family (or superfamily to download.""")

    arg_parser.add_argument(
        '--reverse', '-r', action='store_true',
        help="""Go through the genus list backwards.""")

    arg_parser.add_argument(
        '--csv-file', '-C',
        help="""Output the results to this CSV file.""")

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
