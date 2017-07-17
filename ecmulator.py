#!/usr/bin/python3
# Copyright (c) 2017 Po Huit
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Jam probabilities for an EVE Online ECM ship setup.

from math import exp
from sys import exit, stderr
import argparse
import re

def usage(message, *args):
    print(message, file=stderr)
    exit(1)

# Strengths of jam sources.
jammer_strengths = {
    # Drones
    "D3": 1,
    "D6": 1.5,
    "D9": 2,
    # Multispectral
    "M1": 2.2,  # T1
    "MM": 2.2,  # Meta
    "M2": 2.4,  # T2
    "ML": 2.5,  # Legion
    "MG": 2.6,  # Dread Guristas
    "MK": 2.8,  # Kaikka's
    "MT": 2.9,  # Thon's
    "MV": 3.1,  # Vaipas' [sic]
    "ME": 3.2,  # Estamel's
    # Racial
    "R1": 3.0,  # T1
    "RM": 3.3,  # Meta
    "R2": 3.6,  # T2
    "RS": 3.45, # Storyline
    "RL": 3.7,  # Legion [breaks pattern]
    # Mismatched Racial
    "X1": 1.0,  # T1
    "XM": 1.1,  # Meta
    "X2": 1.2,  # T2
    "XS": 1.15, # Storyline
    "XL": 1.2,  # Legion
    # Burst
    "B1": 6.0,  # T1
    "BM": 6.6,  # Meta
    "B2": 7.2,  # T2
    "BG": 7.0,  # 'Ghost'
    "BS": 8.0,  # Sentient
    "BD": 9.0,  # Unit D-34343's Modified
    "BF": 9.5,  # Unit F-435454's Modified
    "BP": 12.7, # Unit P-343554's Modified
    "BW": 10.5, # Unit W-634's Modified
}
jam_pattern = "|".join(jammer_strengths.keys())
jam_regex = re.compile("(%s)(x[1-9])?" % jam_pattern)

class Jam:
    """Description of a jam source."""
    def __init__(self, desc):
        # Parse description.
        stats = re.fullmatch(jam_regex, desc)
        if not stats:
            usage("unknown jammer: %s" % (desc,))
        jam, count = stats.groups()

        # Record type.
        self.desc = jam
        self.jam = jam[0]

        # Record count.
        self.count = 1
        if count:
            count_digit = re.fullmatch("x([1-9])", count)
            self.count = int(count_digit.group(1))

        # Record jammer stats.
        self.strength = jammer_strengths[jam]

    def __str__(self):
        return "%sx%d:strength=%g" % \
            (self.desc, self.count, self.strength)

# XXX: This next bit is gross copy-paste.
# Should restructure.

# Bonuses of fittings.
fitting_bonuses = {
    # Signal Distortion Amplifier (module)
    "S1": 0.10, # T1
    "Si": 0.07, # Initiated
    "SI": 0.08, # Induced [sigh]
    "SC": 0.09, # Compulsive
    "SH": 0.10, # 'Hypnos'
    "S2": 0.10, # T2
    # Particle Dispersion Amplifier (rig)
    "P1": 0.10, # T1
    "P2": 0.15, # T2
}
fitting_pattern = "|".join(fitting_bonuses.keys())
fitting_regex = re.compile("(%s)(x[1-9])?" % fitting_pattern)

class Fitting:
    """Description of an ECM fitting."""
    def __init__(self, desc):
        # Parse description.
        stats = re.fullmatch(fitting_regex, desc)
        if not stats:
            usage("unknown fitting: %s" % (desc,))
        fitting, count = stats.groups()

        # Record type.
        self.desc = fitting
        self.fitting = fitting[0]

        # Record count.
        self.count = 1
        if count:
            count_digit = re.fullmatch("x([1-9])", count)
            self.count = int(count_digit.group(1))

        # Record jammer stats.
        self.bonus = fitting_bonuses[fitting]

    def __str__(self):
        return "%sx%d:bonus=%g" % \
            (self.desc, self.count, self.bonus)

# Parse arguments.
parser = argparse.ArgumentParser(description="ECM jam probabilities.")
parser.add_argument("-j", "--jam", action="append",
                    help="Add a jam to the fit.",
                    dest="jams")
parser.add_argument("-r", "--resist", type=float,
                    help="Sensor strength of target ship (default 20).",
                    default=20,
                    dest="resist")
parser.add_argument("-s", "--skill", type=int,
                    help="Pilot Signal Dispersion skill level (default 5).",
                    default=5,
                    dest="skill")
parser.add_argument("-H", "--hull", type=float,
                    help="Hull bonus percent (default 0).",
                    default=0.0,
                    dest="hull")
parser.add_argument("-f", "--fitting", action="append",
                    help="Add a fitting to the fit.",
                    dest="fittings")
args = parser.parse_args()
if not args.jams:
    usage("no jammers specified")
if not args.fittings:
    args.fittings = []

# Process arguments.
jams = [Jam(desc) for desc in args.jams]
fittings = [Fitting(desc) for desc in args.fittings]
resist = args.resist
if resist <= 0:
    usage("non-positive resist: %d" % (resist,))
skill = args.skill
if skill < 1 or skill > 5:
    usage("skill must be between 1 and 5: %d" % (skill,))
hull = args.hull / 100.0

# https://wiki.eveuniversity.org/Stacking_penalties
def stacking(n):
    """Compute the stacking penalty for the n-th bonus
    counting from zero."""
    return exp(-(n / 2.67)**2)

# Collect the fitting bonuses and compute an overall bonus
# including stacking.
bonuses = list()
for f in fittings:
    bonuses += [f.bonus] * f.count
bonuses = sorted(bonuses, reverse=True)
fitting_bonus = 1.0
for b in range(len(bonuses)):
    fitting_bonus *= 1.0 + bonuses[b] * stacking(b)

# Collect the bonused jam strengths.
base_bonus = (1.0 + 0.05 * skill) * (1.0 + hull)
strengths = list()
for j in jams:
    strength = j.strength
    if j.jam != "D":
        strength *= base_bonus * fitting_bonus
    strengths += [strength] * j.count
    print("jam strength:", j.desc, round(strength, 2))

# Do the math and print the result.
cp = 1.0
for s in strengths:
    cp *= (resist - s)/resist
print("jam probability:", str(round((1.0 - cp) * 100)) + "%")
