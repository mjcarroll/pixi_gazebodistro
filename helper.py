#!/usr/bin/env python3

# Copyright 2023 Michael Carroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This is a very simple helper script to get around some of the limitations of the pixi task command.

Mostly this holds a common default configuration in ros.toml.
"""

import argparse
import os
import shutil
import sys
import urllib.request

WORKSPACE_NAME = 'gazebosim_ws'
COLCON_DEFAULTS_FILE = '.github/ci/colcon_defaults.yaml'
DEFAULT_COLLECTION = 'collection-ionic.yaml'

def sync(args, rem_args):
    from vcstool.commands.vcs import main as vcs_main

    uri = f'https://raw.githubusercontent.com/gazebo-tooling/gazebodistro/master/{args.collection}'
    if args.repos_uri:
        uri = args.repos_uri

    if not os.path.exists(f'{args.workspace_name}/src'):
        os.makedirs(os.path.join(args.curdir, f'{args.workspace_name}/src'))

    repos_file = f'{args.workspace_name}/workspace.repos'
    print(f'Fetching: {uri}')
    urllib.request.urlretrieve(uri, repos_file)

    argv = ['import', '--input', repos_file, *rem_args, f'{args.workspace_name}/src']
    return vcs_main(argv)


def colcon(args, rem_args):
    from colcon_core.command import main as colcon_main
    os.environ["COLCON_DEFAULTS_FILE"] = os.path.join(args.curdir, args.colcon_defaults)
    os.chdir(os.path.join(args.curdir, f'{args.workspace_name}'))
    return colcon_main(argv=rem_args)


def clean(args, rem_args):
    for subdir in ['build', 'install', 'log']:
        try:
            shutil.rmtree(os.path.join(os.curdir, f'{args.workspace_name}/{subdir}'))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Pixi Task Helper',
                    description='Help with common pixi tasks')

    parser.add_argument('--workspace-name', type=str, default=WORKSPACE_NAME)
    parser.add_argument('--colcon-defaults', type=str, default=COLCON_DEFAULTS_FILE)

    subparsers = parser.add_subparsers()
    sync_parser = subparsers.add_parser('sync')
    sync_parser.add_argument('--collection', type=str, default=DEFAULT_COLLECTION)
    sync_parser.add_argument('--repos-uri', type=str)
    sync_parser.set_defaults(func=sync)

    colcon_parser = subparsers.add_parser('colcon')
    colcon_parser.set_defaults(func=colcon)

    clean_parser = subparsers.add_parser('clean')
    clean_parser.set_defaults(func=clean)

    args, rem_args = parser.parse_known_args()

    args.curdir = os.path.abspath(os.path.curdir)
    sys.exit(args.func(args, rem_args))
