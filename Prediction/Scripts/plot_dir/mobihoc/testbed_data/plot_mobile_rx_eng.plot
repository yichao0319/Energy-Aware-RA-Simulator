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
set ylabel "Energy (nJ/bit)";
# set nokey;
set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."testbed_mobile_rx_eng.eps"

set xtics rotate by -25

plot \
data_dir.'mobile_rx_eng.txt' using 2:3:xtic(1) t '{/Helvetica=28 Measurement}' fs pattern 1, \
data_dir.'mobile_rx_eng.txt' using 4:5:xtic(1) t '{/Helvetica=28 Model}' fs pattern 4
