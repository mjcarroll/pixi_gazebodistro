#!/usr/bin/env python3

import os
import sys

if __name__ == "__main__":
    comment = os.environ["COMMENT_BODY"]

    args = {}
    for line in comment.splitlines():
        line = line.strip()
        if not line or line.find('=') < 0:
            continue
        k, v = line.split('=')
        args[k] = v

    if 'COLCON_ARGS' in args:
        args['COLCON_BUILD_ARGS'] = args['COLCON_ARGS']
        args['COLCON_TEST_ARGS'] = args['COLCON_ARGS']

    github_env = os.environ["GITHUB_ENV"]
    with open(github_env, 'w') as f:
        for (k, v) in args.items():
            f.write(f'{k}={v}\n')

    sys.exit(0)
