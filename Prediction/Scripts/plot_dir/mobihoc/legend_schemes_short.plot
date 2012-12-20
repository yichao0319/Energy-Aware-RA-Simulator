set terminal postscript eps enhanced monochrome 28


set size 1,0.22
set border 0
set noxtics;
set noytics;



set style data histogram
set style histogram gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray



set key Left above reverse horizontal nobox spacing 0.9
set output "legend_schemes_short.eps"
data_dir = "../data/"


plot [-10:-10.0001][-100:-100.001] \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 2 t '{/Helvetica=28 EffSnr}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 3 t '{/Helvetica=28 MinEng}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 4 t '{/Helvetica=28 OracleMinEng}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 5 t '{/Helvetica=28 MaxTput}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 6 t '{/Helvetica=28 OracleMaxTput}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 7 t '{/Helvetica=28 SRate}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 8 t '{/Helvetica=28 ETput80}', \
data_dir.'static_intel_tx.trace2scheme.tput.txt' using 9 t '{/Helvetica=28 ETput60}'
