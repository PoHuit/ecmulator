#!/usr/bin/python3
# Copyright (c) 2017 Po Huit
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.


# Jam probabilities for an EVE Online ECM ship setup.

from sys import exit
import argparse
import re

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
}
jam_pattern = "|".join(jammer_strengths.keys())
jam_regex = re.compile("(%s)(x[1-9])?" % jam_pattern)

# Description of a jam source.
class Jam:
    def __init__(self, desc):
        # Parse description.
        stats = re.fullmatch(jam_regex, desc)
        if not stats:
            print("unknown jammer: %s" % (desc,))
            exit(1)
        jam, count = stats.groups()

        # Record type.
        self.jam = jam[0]

        # Record count.
        self.count = 1
        if count:
            count_digit = re.fullmatch("x([1-9])", count)
            self.count = int(count_digit.group(1))

        # Record jammer stats.
        self.strength = jammer_strengths[jam]

    def __str__(self):
        return "jam=%s str=%g count=%d" % (self.jam, self.strength, self.count)

# Parse arguments.
parser = argparse.ArgumentParser(description="ECM jam probabilities.")
parser.add_argument("-j", "--jam", action="append",
                    help="Add a jam to the fit.",
                    dest="jams")
parser.add_argument("-r", "--resist", type=int,
                    help="Sensor strength of target ship (default 20).",
                    default=20,
                    dest="resist")
parser.add_argument("-s", "--skill", type=int,
                    help="Pilot Signal Dispersion skill level (default 5).",
                    default=5,
                    dest="skill")
args = parser.parse_args()
if not args.jams:
    print("no jammers specified")
    exit(1)

# Process arguments.
jams = [Jam(desc) for desc in args.jams]
resist = args.resist
if resist <= 0:
    print("non-positive resist:", resist)
    exit(1)
skill = args.skill
if skill < 1 or skill > 5:
    print("skill must be between 1 and 5:", skill)
    exit(1)

# Collect the strengths.
strengths = list()
for j in jams:
    strength = j.strength
    if j.jam != "D":
        strength *= 1.0 + 0.05 * skill
    strengths += [strength] * j.count

# Do the math and print the result.
cp = 1.0
for s in strengths:
    cp *= (resist - s)/resist
print("jam probability:", 1.0 - cp)
