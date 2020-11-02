#!/usr/bin/env python

"""Download files from UPenn Butterflies of Costa Rica Web Site."""

import argparse
import random
import re
import socket
import time
import urllib.request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

from src.pylib.util import DATA_DIR

# Don't hit the site too hard
SLEEP_MID = 4
SLEEP_RADIUS = 3
SLEEP_RANGE = (SLEEP_MID - SLEEP_RADIUS, SLEEP_MID + SLEEP_RADIUS)

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

    for genus in genera:
        print(genus)
        genus_links = get_genus_links(args, genus)
        for url, path in genus_links[1:]:
            print(path.name)
            download_page(url, path)


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
            for page_no, skip in enumerate(range(step, total, step), 2):
                skip = SKIP.format(skip)
                url = GENUS.format(skip, genus)
                path = OUT_DIR / f'{args.family}_{genus}_{page_no}.html'
                links.append((url, path))
            break

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
            time.sleep(random.randint(SLEEP_RANGE[0], SLEEP_RANGE[1]))
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

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
