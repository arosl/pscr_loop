#!/usr/bin/env python3
""" 
Fmix * ( Kratio * Ve * Pamb + (1 - Kratio ) * Ve * Ke) + ( Frac_loop - (Ke/Pamb) ) * ((1 - Kratio) * Ve * Pamb)
———————————————————————————————————————————————————————————————————————————————————————————————————————————————
                                                                Ve*Pamb

Fmix = Gas from cylinder in fraction of O2 (eg, 0.32, 0.36, 0.40) 
Ve = Minute Volume/RMV ex (SCR rate… 20l, 15l )
Vo2 = Volume O2L/min ex (0.8l)
Pamb = Total ambient pressure at relevant depth ex 1.6ata 
Kratio = bellow ratio fraction ex (1/10 1/6)
Ke = Ve/Vo2 ex (0.8l/20l) = 0.04 or use the static value 0.042
Frac_loop = Fraction of oxygen in RB loop (the result of this equation) FiO2


For a steady state we can do as follows: 

Qdump = Pamb * Kratio * Ke * Vo2

( Qdump + Vo2) * Fmix - Vo2
——————————————————————————— ==>
           Qdump

( Pamb * Kratio * Ke * Vo2 + Vo2) * Fmix - Vo2
—————————————————————————————————————————————— ==>
           Pamb * Kratio * Ke * Vo2

( Pamb * Kratio * Ke * 1 + 1) * Fmix - 1
———————————————————————————————————————— ==>
           Pamb * Kratio * Ke * 1

(Pamb * Kratio * Ke + 1) *Fmix -1
—————————————————————————————————
        Pamb * Kratio * Ke 
"""
import argparse
import sys
import matplotlib.pyplot as plt
from distutils.util import strtobool


# Caclulate oxygen fraction in the breathing loop
def calc_loop(frac_freshgas, mv, presure, bellow):
    frac_met_surface = (0.8/mv)  # good static value 0.042
    new_gas_fraction = 1/bellow
    old_gas_fraction = (bellow - 1)/bellow
    frac_loop = frac_freshgas
    old_loop = frac_loop + 1
    o2_drop = []

    while (old_loop - frac_loop) > 0.000000001:
        old_loop = frac_loop
        #formula from the top of the file
        frac_loop = (frac_freshgas * (new_gas_fraction * mv * presure +
        (1 - new_gas_fraction) * mv * frac_met_surface) + (frac_loop -
        (frac_met_surface/presure)) * (old_gas_fraction*mv*presure)
        )/(mv * presure)
        
        o2_drop.append(frac_loop)
    return o2_drop

# Cacluate the minumim and maximum safe area for a given oxygen fraction
def min_max_gas(frac_freshgas, mv, presure, bellow, deco):
    FiO2 = 0
    presure = float(1)
    o2_min = 0
    pp02lim = 1.3
    if deco:
        pp02lim = 1.6

    while (FiO2 * presure) <= pp02lim:
        o2drop = calc_loop(frac_freshgas, mv, presure, bellow)
        FiO2 = o2drop[-1]
        ppO2 = FiO2 * presure
        depth = (presure - 1)*10
        if ppO2 < 0.21:
            o2_min = depth
        #set o2_max 1 meter deeper than current ppO2lim
        o2_max = (presure - 0.9)*10
        presure = round((presure + 0.1), 2)

    return(o2_min, o2_max)

def run(args):
    frac_freshgas = args.fractionoxy
    mv = args.mv
    depth = args.depth
    bellow = args.bellow
    graph = args.graph
    no_min_max = args.nominmax
    noppo2 = args.nopp02
    nofio2 = args.nofi02
    deco = args.deco
    presure = (depth/10) + 1

    if frac_freshgas > 100:
        sys.exit(1)
    if frac_freshgas <= 0:
        sys.exit(1)
    if frac_freshgas > 1:
        frac_freshgas = frac_freshgas/100

    o2drop = calc_loop(frac_freshgas, mv, presure, bellow)

    if graph:
        label = """for O2 fraction %.2f at depth %.0dm
level of at FiO2 %.2f, ppO2 %.2f 
""" % (frac_freshgas, depth, o2drop[-1], (o2drop[-1]*presure))

        x = range(0, len(o2drop))
        y = o2drop
        plt.plot(x, y, label=label)
        plt.legend()
        plt.show()

    if not nofio2:
        print("FiO2 %.2f" % o2drop[-1])
    if not noppo2:
        print("ppO2 %.2f" % (o2drop[-1]*presure))
    
    if not no_min_max:
        o2_min_max = min_max_gas(frac_freshgas, mv, presure, bellow, deco)
        o2_min = o2_min_max[0]
        if (o2_min%3) != 0:
            o2_min_table = o2_min + (3 - o2_min%3)
        else:
            o2_min_table = o2_min
        o2_max = o2_min_max[1]
        o2_max_table = o2_max - (o2_max%3)
        print("Minimum depth: %.0dm \nMaximum depth: %.0dm " % 
        (o2_min_table, o2_max_table))



def main():
    parser = argparse.ArgumentParser(
        description="Calculate oxygen fraction in loop")
    parser.add_argument(
        help="Oxygen fraction of breathing gas on cylinder, " +
        "this agrument is mandatory. " +
        "It accepts both oxygen fraction (eg 0.32) and oxygen percentage " +
        "(eg 32).",
        dest="fractionoxy", type=float)
    parser.add_argument("-d", "--depth",
        help="The depth you calculate for in meters(m)",
        dest="depth", type=float, default=0, required=False)
    parser.add_argument("-v", "--minutevolume",
        help="Minute Volume, liters you breath in one minute",
        dest="mv", type=float, default=19, required=False)
    parser.add_argument("-b", "--bellowratio",
        help="Ratio of bellow replacement rate 1:6 to 1:10",
        dest="bellow", type=int, default=10, required=False)
    parser.add_argument("-g", "--graph", help="Print a graph of oxygen drop",
        dest="graph", type=lambda x: bool(strtobool(x)),
        nargs='?', const=True, default=False)
    parser.add_argument("--no-ppo2",
        help="Do not print oxygen parsial pressure",
        dest="nopp02", type=lambda x: bool(strtobool(x)),
        nargs='?', const=True, default=False)
    parser.add_argument("--no-fio2",
        help="Do not print oxygen fraction in loop",
        dest="nofi02", type=lambda x: bool(strtobool(x)),
        nargs='?', const=True, default=False)
    parser.add_argument("-m", "--no-minmax", 
        help="Do not print min and max depth(m) for gas",
        dest="nominmax", type=lambda x: bool(strtobool(x)),
        nargs='?', const=True, default=False)
    parser.add_argument("--deco",
        help="Use ppO2 limit of 1.6 instead of 1.3 in max depth",
        dest="deco", type=lambda x: bool(strtobool(x)),
        nargs='?', const=True, default=False)

    parser.set_defaults(func=run)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
