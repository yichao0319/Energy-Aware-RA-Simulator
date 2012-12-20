reset
set terminal postscript eps enhanced monochrome 28

set style data histogram
set style histogram errorbars gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray

data_dir = "./"
fig_dir = "../testbed_figures/"

set yrange [0:]

# set xlabel "traces";
set ylabel "Throughput (Mbps)";
set nokey;
# set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."testbed_static_tx_tput.eps"

set xtics rotate by -25

plot \
data_dir.'static_tx_tput.txt' using 2:3:xtic(1) fs pattern 1