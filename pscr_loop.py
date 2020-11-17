#!/usr/bin/env python3
""" 
Frac_freshgas * ( (1/10) * MV * P + (1 - (1/10) ) * MV * Frac_met_surface) + ( Frac_loop - (Frac_met_surface/P) ) * ((9/10) * MV * P)
—————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
                                                                MV*P

Frac_freshgas = Gas from cylinder in fraction of O2 (eg, 0.32, 0.36, 0.40) 
MV = Minute Volume (SCR rate… 20l, 15l etc)
P = Total pressure at relevant depth ATA + Hydrostatic pressure
Frac_met_surface = Fraction of o2 metabolism on surface (ATA = 1), O2 consumption per min/MV. 
                   Eg; (0.8l/20l) = 0.04 or use the static value 0.042
Frac_loop = Fraction of oxygen in RB loop (the result of this equation) FiO2
"""
import argparse

def calc_loop(frac_freshgas, mv, presure, bellow):
    frac_met_surface =  (0.8/mv) # good static value 0.042
    new_gas_fraction = 1/bellow
    old_gas_fraction = (bellow -1)/bellow
    frac_loop = frac_freshgas
    old_loop = frac_loop + 1

    while (old_loop - frac_loop) > 0.000000001:
        old_loop = frac_loop
        frac_loop = (frac_freshgas * (new_gas_fraction * mv * presure + 
        (1 - new_gas_fraction) * mv * frac_met_surface) + (frac_loop - 
        (frac_met_surface/presure)) * (old_gas_fraction*mv*presure)
        )/( mv * presure)
    return frac_loop

def run(args):
    frac_freshgas = args.o2fraction
    mv = args.mv
    depth = args.depth
    bellow = args.bellow
    presure = (depth/10) + 1

    loop = calc_loop(frac_freshgas, mv, presure, bellow)

    print("FiO2 %.2f" % loop)
    print("ppO2 %.2f" % (loop*presure))

def main():
    parser=argparse.ArgumentParser(description="Calculate oxygen fraction in loop")
    parser.add_argument("-f","--o2fraction",help="Oxygen fraction of breathing gas on cylinder" ,dest="o2fraction", type=float, required=True)
    parser.add_argument("-d","--depth",help="Depth you calculate for in meters" ,dest="depth", type=float, default=0 , required=False)
    parser.add_argument("-v","--minutevolume",help="Minute Volume, liters you breath in one minute" ,dest="mv", type=float, default=19 , required=False)
    parser.add_argument("-b","--bellowratio",help="Ratio of bellow replacement rate 1:6 to 1:10" ,dest="bellow", type=int, default=10 , required=False)
    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()