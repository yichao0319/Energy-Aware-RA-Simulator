reset
set terminal postscript eps enhanced color 28
# monochrome

set size 1,0.8

set style data histogram
set style histogram rowstack gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
# set palette gray

data_dir = "./"
fig_dir = "../analysis_figures/"

set yrange [0:1]

# set xlabel "traces";
set ylabel "ratio";
set nokey;
# set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."mobile_atheros_tx.trace2scheme.rx_ant.eps"


set xtics rotate by 90

plot \
newhistogram "mobile 1" lt 1, data_dir.'mobile_atheros_tx.trace2scheme.rx_ant.txt' using 2:xtic(1) t '1 ant' fs pattern 1, '' u 3 t '2 ant' fs pattern 2, '' u 4 t '3 ant' fs pattern 5, \
newhistogram "mobile 2" lt 1, data_dir.'mobile_atheros_tx.trace2scheme.rx_ant.txt' using 5:xtic(1) notitle fs pattern 1, '' u 6 notitle fs pattern 2, '' u 7 notitle fs pattern 5, \
newhistogram "mobile 3" lt 1, data_dir.'mobile_atheros_tx.trace2scheme.rx_ant.txt' using 8:xtic(1) notitle fs pattern 1, '' u 9 notitle fs pattern 2, '' u 10 notitle fs pattern 5

