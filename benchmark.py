import subprocess as sp
import time
import argparse
from collections import defaultdict
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
NUM_TRIES = 50
import math

parser = argparse.ArgumentParser()
parser.add_argument("-n", "-n", type=int, required=False,
                    default=11, help="number of vertices")

args = parser.parse_args()

def get_time_from_string(string):
    '''
    '''
    # matches scientific notation and stuff.
    numbers = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
            string)
    # all the things we are printing so far has just 1 num.
    if len(numbers) >= 1:
        return float(numbers[0])
    else:
        return None

def run_hamiltonian(p):
    template = 'python main.py -n 100 -p {p}'
    cmd = template.format(p = p)
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
    
    print "{}: {}".format(p, success / float(NUM_TRIES))

def run_chromatic(p):
    template = 'python main.py -n {N} -p {p} -chrom 1'
    cmd = template.format(N = args.n, p = p)
    cmd = cmd.split()
    chrom_num = []
    for i in range(NUM_TRIES):
        process = sp.Popen(cmd, stdout=sp.PIPE)
        # process.wait()
        stdout = process.communicate()[0]
        stdout = stdout.split('\n')
        for s in stdout:
            chrom = get_time_from_string(s)
            chrom_num.append(chrom)
            break
    
    print("{}: {} ".format(p, sum(chrom_num) / len(chrom_num)))

# for i in range(0, 20, 1):
    # p = 0.01 * i/2
    # exp = math.pow(p, 100) * math.factorial(100-1)
    # print("exp: ", exp)
    # run_hamiltonian(p)

for i in range(1, 10, 1):
    p = 0.05 * i
    run_chromatic(p)

