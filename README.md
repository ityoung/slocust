# slocust

Start [`locust`](https://github.com/locustio/locust) master and numbers of slaves(depends on numbers of CPU core) with one command.

Considering the situation of running load testing, slocust will only start as __no-web__ mode.

## Dependencies

slocust is mainly based on [`locustio`](https://github.com/locustio/locust), and you can install all dependencies through `requirements.txt`.

```bash
$ pip install -r requirements.txt --upgrade
```

## Usages

```text
$ usage: slocust [-h] [-f LOCUSTFILE] -c CLIENT_NUMBERS -r SIMULATE_RATE

Start locust master and specified number of slaves with one command.

optional arguments:
  -h, --help            show this help message and exit
  -f LOCUSTFILE, --locustfile LOCUSTFILE
                        Specify locust file to run test.
  -c CLIENT_NUMBERS     Specify numbers of client to simulate.
  -r SIMULATE_RATE      Specify simulation rate(1/sec).
```

## Examples

Start locust master and locust slaves, the slaves number is equal to the machine's cpu count.

```text
$ slocust -f examples/demo_task.py -c 10000 -r 20
[2017-02-26 10:52:04,875] Leos-MacBook-Air.local/INFO/logger: Starting Locust 0.8a2
[2017-02-26 10:52:04,897] Leos-MacBook-Air.local/INFO/logger: Starting web monitor at *:8089
[2017-02-26 01:32:15,757] Leos-MacBook-Air.local/INFO/locust.runners: Client 'Leos-MacBook-Air.local_9cfcb5acf942af4b52063c138952a999' reported as ready. Current
ly 1 clients ready to swarm.
[2017-02-26 01:32:15,757] Leos-MacBook-Air.local/INFO/locust.runners: Client 'Leos-MacBook-Air.local_0dba26cc993de413436db0f854342b9f' reported as ready. Current
ly 2 clients ready to swarm.
[2017-02-26 01:32:15,758] Leos-MacBook-Air.local/INFO/locust.runners: Client 'Leos-MacBook-Air.local_2d49585a20f6bcdca33b8c6179fa0efb' reported as ready. Current
ly 3 clients ready to swarm.
[2017-02-26 01:32:15,782] Leos-MacBook-Air.local/INFO/locust.runners: Client 'Leos-MacBook-Air.local_cc9d414341823d0e9421679b5f9dd4c4' reported as ready. Current
ly 4 clients ready to swarm.
```
