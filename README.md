# ECMulator
Copyright (c) 2017 Po Huit

There is a lot of confusion about how to calculate jam
probabilities for EVE Online ECM modules. This program
caculates single-cycle jam probabilities for any combination
of ECM modules and drones.

## Usage

Run `python3 ecmulator.py` with appropriate arguments.

* The `--jam` (`-j`) argument specifies a jam module or
  drone, including a repeat count for convenience.  Multiple
  `--jam` arguments may be given. All jams are applied to a
  single target.

  The module or drone is specified in the format

  > *&lt;base-type&gt;&lt;variant&gt;[*`x`*&lt;count&gt;]*

  The *count* defaults to 1 if omitted.

  The *base types* are as follows:

  * D: A drone. The *variant* must be one of:

      * 3: EC-300
      * 6: EC-600
      * 9: EC-900

  * M: A multispectral jammer. The *variant* must be one of:

      * 1: T1
      * M: Meta 1
      * 2: T2
      * L: Legion
      * G: Dread Guristas
      * K: Kaikka's
      * T: Thon's
      * V: Vaipas' *[sic]*
      * E: Estamel's

  * R or X: a "matched" or "mismatched" racial jammer,
    respectively. The "matched" case (R) applies the jammer
    to a hull whose sensor type matches the jammer's; the
    "mismatched" case (X) applies the jammer to a hull of
    some other sensor type. The *variant* must be one of:

      * 1: T1
      * M: Meta 1
      * 2: T2
      * S: Storyline [named]
      * L: Legion

  * B: A Burst Jammer. These have a 30 second cycle time
    instead of 20, which is not taken into account here in
    any way. The *variant* must be one of:

      * 1: T1
      * M: Meta
      * 2: T2
      * G: 'Ghost'
      * S: Sentient
      * D: Unit D-34343's Modified
      * F: Unit F-435454's Modified
      * P: Unit P-343554's Modified
      * W: Unit W-634's Modified

  For example, if you have 1 matched racial meta jammer and 4
  mismatched racial meta jammers fitted, say

      --j RM --j XMx4

* The `--resist` (`-r`) argument specifies the sensor
  strength of the target hull. The default of 20 represents
  an "average" T1 Cruiser hull.

* The `--skill` (`-s`) argument specifies the Signal
  Dispersion skill level of the pilot. Jammer effectiveness
  increases by 5% per level. The default of 5 is what a good
  pilot should have.

* The `--hull` (`-H` — don't ask about the uppercase)
  argument specifies the hull bonus percentage (for example,
  `30` for 30%) for jammers. The default of 0 reflects an
  unbonused ship. Hull bonuses must be calculated manually:
  there's too many cases to be specified to make a
  programmatic calculation useful.

* The `--fitting` (`-f`) argument specifies a rig or module
  that gives an ECM strength bonus. See the description of
  `--jam` for general syntax. Stacking penalties are
  applied.

  The *base types* are as follows:

  * S: A Signal Distortion Amplifier module. The *variant*
    must be one of:

      * 1: T1
      * i: Initiated
      * I: Induced *[sigh]*
      * C: Compulsive
      * H: 'Hypnos'
      * 2: T2

  * P: A Particle Dispersion Augmentor rig. The *variant*
    must be one of:

      * 1: T1
      * 2: T2

## Frequently Asked Questions

* Q: *Why doesn't this tool also deal with ECM ranges?*

  A: Your fitting tool does this fine.

* Q: *Why not just copy jam strengths from my fitting tool?*

  A: What a pain.

* Q: *What about implants?*

  A: As far as I know, there are not any that specifically
     affect ECM strength.

* Q: *Why is the syntax for specifying jams and fittings so
     gross?*

  A: It was designed for brevity and scripting rather than
     for readability. Patches welcome.

* Q: *Can you do pretty graphs?*

  A: Not yet. You can script something with a plotting tool
     if you want to make your own.

## Thanks

Props to [PyFA](http://github.com/pyfa-org/Pyfa) and the EVE
University [wiki](http://wiki.eveuniversity.org) for making
development and checking of this tool much, much easier.

## License

This program is licensed under the "MIT License". Please see
the file `COPYING` in the source distribution of this software
for license terms.
