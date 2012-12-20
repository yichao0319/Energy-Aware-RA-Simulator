reset
set terminal postscript eps enhanced monochrome 28

set size 1,0.8

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
set output fig_dir."testbed_static_combine_tput.eps"

# set xtics rotate by -25

plot \
data_dir.'static_combine.tput.txt' using 2:3:xtic(1) t '{/Helvetica=28 MinEng}', \
data_dir.'static_combine.tput.txt' using 4:5:xtic(1) t '{/Helvetica=28 MaxTput}', \
data_dir.'static_combine.tput.txt' using 6:7:xtic(1) t '{/Helvetica=28 ETput80}', \
data_dir.'static_combine.tput.txt' using 8:9:xtic(1) t '{/Helvetica=28 ETput70}', \
data_dir.'static_combine.tput.txt' using 10:11:xtic(1) t '{/Helvetica=28 ETput60}'
