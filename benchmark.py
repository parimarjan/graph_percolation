import subprocess as sp
import time
import argparse
from collections import defaultdict
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import json
NUM_TRIES = 10
import math

parser = argparse.ArgumentParser()
template = 'python main.py -n 100 -p {p}'

def run_hamiltonian(p):
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


for i in range(0, 20, 1):
    p = 0.01 * i/2
    exp = math.pow(p, 100) * math.factorial(100-1)
    print("exp: ", exp)
    run_hamiltonian(p)

