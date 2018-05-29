import gevent.monkey

gevent.monkey.patch_all()
import sys
import time
import multiprocessing
import socket
# import gevent
from locust import runners
# from locust import events, web
from locust import events
from locust.main import version, load_locustfile
from locust.stats import print_percentile_stats, print_error_report, print_stats
from slocust.base import master_options, slave_options
from slocust.logger import logger


def parse_locustfile(locustfile):
    docstring, locusts = load_locustfile(locustfile)
    locust_classes = list(locusts.values())
    return locust_classes


def start_master(locust_classes, slaves_num):
    # web
    # logger.info("Starting web monitor at {}:{}".format(
    #     master_options.web_host or "*", master_options.port))
    # master_greenlet = gevent.spawn(web.start, locust_classes, master_options)
    # no_web
    # todo: run time
    runners.locust_runner = runners.MasterLocustRunner(locust_classes, master_options)
    while len(runners.locust_runner.clients.ready) < slaves_num:
        logger.info("Waiting for slaves to be ready, %s of %s connected",
                    len(runners.locust_runner.clients.ready), slaves_num)
        time.sleep(1)
    logger.info("%s slave connected, start hatching",
                len(runners.locust_runner.clients.ready))
    runners.locust_runner.start_hatching(master_options.num_clients, master_options.hatch_rate)
    master_greenlet = runners.locust_runner.greenlet
    try:
        master_greenlet.join()
    except KeyboardInterrupt:
        events.quitting.fire()
        print_stats(runners.locust_runner.request_stats)
        print_percentile_stats(runners.locust_runner.request_stats)
        print_error_report()
        sys.exit(0)


def start_slave(locust_classes):
    runners.locust_runner = runners.SlaveLocustRunner(locust_classes, slave_options)
    slave_greenlet = runners.locust_runner.greenlet
    try:
        slave_greenlet.join()
    except socket.error as ex:
        logger.error("Failed to connect to the Locust master: %s", ex)
        sys.exit(-1)
    except KeyboardInterrupt:
        events.quitting.fire()
        sys.exit(0)


class LocustStarter(object):
    def __init__(self, api_host, master_host, port, num_clients, hatch_rate,
                 slave_only=False):
        logger.info("Starting Locust %s" % version)
        master_options.host = api_host
        master_options.port = port
        master_options.num_clients = num_clients
        master_options.hatch_rate = hatch_rate
        slave_options.master_host = master_host
        self.slave_only = slave_only

    def start(self, locustfile, slaves_num):
        locust_classes = parse_locustfile(locustfile)
        slaves_num = slaves_num or multiprocessing.cpu_count()

        logger.info("Starting %s slaves" % slaves_num)
        processes = []
        for _ in range(slaves_num):
            p_slave = multiprocessing.Process(target=start_slave, args=(locust_classes,))
            p_slave.daemon = True
            p_slave.start()
            processes.append(p_slave)

        try:
            if self.slave_only:
                [process.join() for process in processes]
            else:
                start_master(locust_classes, slaves_num)
        except KeyboardInterrupt:
            sys.exit(0)
