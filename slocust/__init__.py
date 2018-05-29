import sys
import argparse
from slocust.logger import logger
from slocust.locust import LocustStarter

# from locust.main import find_locustfile
# Todo:

def main():
    """ parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='Wrappers for making load test with locust more convienient.')

    parser.add_argument(
        '-f', '--locustfile',
        default='locustfile.py',
        help="Python module file to import, e.g. '../other.py'. Default: locustfile.py")
    # parser.add_argument(
    #     '--web', help="Specify locust to run test with web page.")

    # Number of clients
    parser.add_argument(
        '-c', '--clients',
        action='store',
        type=int,
        dest='num_clients',
        default=1,
        help="Number of concurrent Locust users. Only used together with --no-web")

    # Client hatch rate
    parser.add_argument(
        '-r', '--hatch-rate',
        action='store',
        type=float,
        dest='hatch_rate',
        default=1,
        help="The rate per second in which clients are spawned. \
        Only used together with --no-web"
    )

    # Time limit of the test run
    parser.add_argument(
        '-t', '--run-time',
        action='store',
        # type='str',
        dest='run_time',
        default=None,
        help="Stop after the specified amount of time, \
        e.g. (300s, 20m, 3h, 1h30m, etc.). Only used together with --no-web"
    )

    # Host to test
    parser.add_argument(
        '-H', '--host',
        help="Host to load test in the following format: http://10.0.3.50")

    # Port of web page
    parser.add_argument(
        '-P', '--port', '--web-port',
        default=8089,
        type=int,
        help="Port on which to run web host, default is 8089.")

    parser.add_argument(
        '--slave-only',
        action='store_true',
        help="Only start locust slaves.")

    parser.add_argument(
        '--master-host',
        default='127.0.0.1',
        help="Host or IP address of locust master for distributed load testing.")

    parser.add_argument(
        '--slaves-num',
        type=int,
        help="Specify number of locust slaves, default to machine's cpu count.")
    parser.set_defaults(func=main_locust)

    args = parser.parse_args()
    args.func(args)


def main_locust(args):
    locustfile = args.locustfile
    if not locustfile:
        logger.error("locustfile must be specified! use the -f option.")
        sys.exit(0)

    LocustStarter(
        args.host, args.master_host, args.port, args.num_clients,
        args.hatch_rate, args.slave_only
    ).start(
        args.locustfile,
        args.slaves_num
    )
