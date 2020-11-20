# pscr_loop

This is a small tool to calculate o2 drop in a pSCR rebreather.

## ! Warning !
Rebreathers are inherently dangerous tools, and knowing your O2 is paramount.
Do not trust this script it most likely has bugs, and your physology is different
from the asumtions this script is making.

## Installation
To install this tool, check out the repo and install the dependencies listed in `requirements.txt` from pip.

  `pip install -r requirements.txt`

## Usage
If you run the script without arguments you get this help text:
```
./pscr_loop.py

usage: pscr_loop.py [-h] [-d DEPTH] [-v MV] [-b BELLOW] [-g [GRAPH]]
                    [--no-ppo2 [NOPP02]] [--no-fio2 [NOFI02]] [-m [NOMINMAX]]
                    [--deco [DECO]]
                    fractionoxy

Calculate oxygen fraction in loop

positional arguments:
  fractionoxy           Oxygen fraction of breathing gas on cylinder, this agrument is
                        mandatory. It accepts both oxygen fraction (eg 0.32) and oxygen
                        percentage (eg 32).

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
                        The depth you calculate for in meters(m)
  -v MV, --minutevolume MV
                        Minute Volume, liters you breath in one minute
  -b BELLOW, --bellowratio BELLOW
                        Ratio of bellow replacement rate 1:6 to 1:10
  -g, --graph
                        Print a graph of oxygen drop
  --no-ppo2             Do not print oxygen parsial pressure
  --no-fio2             Do not print oxygen fraction in loop
  -m, --no-minmax
                        Do not print min and max depth(m) for gas
  --deco                Use ppO2 limit of 1.6 instead of 1.3 in max depth
```
