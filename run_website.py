#!/usr/bin/env python
"""
run a simple nmp_broker server.

Set environment variable MODE to use different config files or use -m/--mode argument to set on command line.

MODE:
    production: use conf ./conf/production.config.yaml
    develop: use conf ./conf/develop.config.yaml

"""
import argparse
import os
import sys

if 'NWPC_MONITOR_PLATFORM_BASE' in os.environ:
    sys.path.append(os.environ['NWPC_MONITOR_PLATFORM_BASE'])


def runserver():

    mode = "production"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
DESCRIPTION
    Run nwpc monitor website.""")

    parser.add_argument(
        "-m", "--mode",
        help="run mode, [production, develop]. "
             "If not set, use mode set in environment variable MODE. "
             "If there is no such env variable, use default value: production."
    )

    args = parser.parse_args()
    if args.mode:
        os.environ['MODE'] = args.mode
    elif 'MODE' not in os.environ:
        os.environ['MODE'] = mode

    from nmp_web import app

    app.run(
        host=app.config['NWPC_MONITOR_WEB_CONFIG']['host']['ip'],
        port=app.config['NWPC_MONITOR_WEB_CONFIG']['host']['port']
    )


if __name__ == '__main__':
    runserver()
