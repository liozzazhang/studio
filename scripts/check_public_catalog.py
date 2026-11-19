#!/usr/bin/env python3
"""Validate disclosure rules and verify public repository visibility before publication."""
import argparse
import json
import os
import re
import subprocess
import time
from collections import Counter
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from build_catalog import load_content
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--gh', metavar='GH_EXECUTABLE', help='Use an existing GitHub CLI login for local checks')
    args = parser.parse_args()
    _, _, _, modules = load_content()
    projects = [item for item in modules if item['visibility'] == 'public']
    private_count = sum(item['visibility'] == 'private' for item in modules)
    # Private modules are intentionally published summaries, never fetched or copied here.
    token = os.environ.get('STUDIO_GITHUB_TOKEN')

    def verify(item):
        slug = item['slug']
        if item.get('visibility') != 'public' or not re.fullmatch(r'[A-Za-z0-9_.-]+', slug):
            return (False, 'invalid-catalog-entry')
        endpoint = 'repos/liozzazhang/' + slug
        failure = 'unavailable'
        for attempt in range(3):
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
                public = metadata.get('visibility') == 'public' and metadata.get('full_name', '').casefold() == ('liozzazhang/' + slug).casefold()
                return (public, 'not-public' if not public else '')
            except HTTPError as error:
                failure = 'HTTP-' + str(error.code)
            except Exception as error:
                failure = type(error).__name__
            if attempt < 2:
                time.sleep(attempt + 1)
        return (False, failure)

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(verify, projects))
    failures = Counter(reason for passed, reason in results if not passed)
    failed = sum(failures.values())
    if failed:
        details = ", ".join(f"{reason}: {count}" for reason, count in sorted(failures.items()))
        raise SystemExit(f'Public visibility check failed for {failed} catalog entries ({details}). Review the public snapshot before deployment.')
    print(f'Confirmed {len(projects)} public repositories; validated {private_count} explicitly disclosed private summaries.')


if __name__ == '__main__':
    main()
