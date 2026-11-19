#!/usr/bin/env python3
"""Verify that every reviewed catalog entry is still a public GitHub repository."""
import argparse
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gh', metavar='GH_EXECUTABLE', help='Use an existing GitHub CLI login for local checks')
    args = parser.parse_args()
    projects = json.loads((ROOT / 'data/projects.json').read_text())['projects']
    token = os.environ.get('STUDIO_GITHUB_TOKEN')

    def verify(item):
        slug = item['slug']
        if item.get('visibility') != 'public' or not re.fullmatch(r'[A-Za-z0-9_.-]+', slug):
            return False
        endpoint = 'repos/liozzazhang/' + slug
        try:
            if args.gh:
                env = os.environ.copy()
                env.pop('GITHUB_TOKEN', None)
                env.pop('GH_TOKEN', None)
                result = subprocess.run([args.gh, 'api', endpoint], env=env, capture_output=True, text=True, timeout=30, check=True)
                metadata = json.loads(result.stdout)
            else:
                headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Studio-Public-Catalog-Check'}
                if token:
                    headers['Authorization'] = 'Bearer ' + token
                # The only authenticated destination is the fixed GitHub API origin.
                with urlopen(Request('https://api.github.com/' + endpoint, headers=headers), timeout=30) as response:
                    metadata = json.load(response)
            return metadata.get('visibility') == 'public' and metadata.get('full_name', '').casefold() == ('liozzazhang/' + slug).casefold()
        except Exception:
            return False

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(verify, projects))
    failed = len(results) - sum(results)
    if failed:
        raise SystemExit(f'Public visibility check failed for {failed} catalog entries. Review the public snapshot before deployment.')
    print(f'Confirmed {len(projects)} catalog repositories are currently public.')


if __name__ == '__main__':
    main()
