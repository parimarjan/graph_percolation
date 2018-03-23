import subprocess as sp
import time
import argparse
from collections import defaultdict
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
NUM_TRIES = 1
import math

parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, required=True, default=100)
args = parser.parse_args()

import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


def run_hamiltonian(p):
    template = 'python main.py -n {n} -p {p} -ham 1'
    cmd = template.format(n = args.n, p = p)
    cmd = cmd.split()
    success = 0.0
    for i in range(NUM_TRIES):
        process = sp.Popen(cmd, stdout=sp.PIPE)
        # process.wait()
        stdout = process.communicate()[0]
        stdout = stdout.split('\n')
        if stdout[0] == "True":
            success += 1

        # if NUM_TRIES == 20 and success == 0.00:
            # break
    
    print "Ham: {}: {}".format(p, success / float(NUM_TRIES))
    return (success / float(NUM_TRIES))

def run_connected(p):
    template = 'python main.py -n {n} -p {p} -connected 1'
    cmd = template.format(n = args.n, p = p)
    # print(cmd)
    cmd = cmd.split()
    success = 0.0
    for i in range(NUM_TRIES):
        process = sp.Popen(cmd, stdout=sp.PIPE)
        # process.wait()
        stdout = process.communicate()[0]
        stdout = stdout.split('\n')
        if stdout[0] == "True":
            success += 1

        if NUM_TRIES == 20 and success == 0.00:
            break
    
    print "Connected: {}: {}".format(p, success / float(NUM_TRIES))
    return (success / float(NUM_TRIES))

def prob_connected(n, p):
    summation = 0.00
    for i in range(1,n+1,1):
        summation += nCr(n, i) * (1-p)**(i*(n-1))
        # summation += nCr(n, i) * (1-p)**((n-1))
    
    return 1 - summation

for n in range(10, 101, 10):
    print("n = ", n)
    args.n = n
    critical = float(math.e) / args.n
    print("critical: ", critical)
    print("critical 2: ", critical*2)

    # start_val = critical / 2
    start_val = critical 
    hamiltonians = []
    connecteds = []

    for i in range(0, 10, 1):
        p = start_val * i 
        print("prob connected: ", prob_connected(n, p))
        # h = run_hamiltonian(p)
        c = run_connected(p)

        # if (c > 0.00): 
            # connecteds.append(c)

        # if (h > 0.0 and c > 0.0): 
            # break

