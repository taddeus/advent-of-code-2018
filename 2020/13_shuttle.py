#!/usr/bin/env python3
import sys
from functools import reduce
from math import gcd

def parse(f):
    yield int(next(f))
    yield list(map(int, next(f).replace('x', '0').split(',')))

def earliest_bus(arrival, buses):
    wait, bus = min(((bus - arrival % bus) % bus, bus) for bus in buses if bus)
    return wait * bus

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def sync(buses):
    period, maxi = max((bus, i) for i, bus in enumerate(buses))
    diffs = [(i - maxi, bus) for i, bus in enumerate(buses) if bus]
    mindiff = diffs[0][0]
    t = 0
    while diffs:
        t += period
        synced = [bus for diff, bus in diffs if (t + diff) % bus == 0]
        if synced:
            period = reduce(lcm, [period] + synced)
            diffs = [(diff, bus) for diff, bus in diffs if bus not in synced]
    return t + mindiff

def sync_chinese_remainder(buses):
    indices = [i for i, bus in enumerate(buses) if bus]
    diff = indices[-1] - indices[0]
    prod = reduce(lambda a, b: a * b, filter(None, buses))
    return sum((diff - i) * pow(prod // n, n - 2, n) * prod // n
               for i, n in enumerate(buses) if n) % prod - diff

arrival, buses = parse(sys.stdin)
print(earliest_bus(arrival, buses))
print(sync(buses))
