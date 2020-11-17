#!/usr/bin/env python3
""" 
Frac_freshgas * ( (1/10) * MV * P + (1 - (1/10) ) * MV * Frac_met_surface) + ( Frac_loop - (Frac_met_surface/P) ) * ((9/10) * MV)
——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
                                                              MV*P


Frac_freshgas * ( (1/10) * MV * Frac_met_surface) + ( Frac_loop - (Frac_met_surface/P) ) * ((9/10) * MV * P)
————————————————————————————————————————————————————————————————————————————————————————————————————————————
                                                      MV*P

Frac_freshgas = Gas from cylinder in fraction of O2 (eg, 0.32, 0.36, 0.40) 
MV = Minute Volume (SCR rate… 20l, 15l etc)
P = Total pressure at relevant depth ATA + Hydrostatic pressure
Frac_met_surface = Fraction of o2 metabolism on surface (ATA = 1), O2 consumption per min/MV. 
                   Eg; (0.8l/20l) = 0.04 or use the static value 0.042
Frac_loop = Fraction of oxygen in RB loop (the result of this equation) FiO2

It looks like the first formula given doesnt correct for depth so i added P to the numerator, 
and it now generate the correct FiO2 for all depths in the tables
"""

frac_freshgas = float(input("Oxygen fraction: "))
mv = float(input("Minute volume: "))
presure = float(input("Pressure at depth: "))
bellow = int(input("Bellow ratio (6-10): "))

frac_met_surface =  (0.8/mv) # good static value 0.042
new_gas_fraction = 1/bellow
old_gas_fraction = (bellow -1)/bellow
frac_loop = frac_freshgas
old_loop = frac_loop + 1

while (old_loop - frac_loop) > 0.000000001:
    old_loop = frac_loop
    frac_loop = (frac_freshgas * (new_gas_fraction * mv * presure + 
    (1 - new_gas_fraction) * mv * frac_met_surface) + (frac_loop - 
    (frac_met_surface/presure)) * (old_gas_fraction*mv*presure))/( mv * presure)

print("FiO2 %.2f" % frac_loop)
print("ppO2 %.2f" % (frac_loop*presure))