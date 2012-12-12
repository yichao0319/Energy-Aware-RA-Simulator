reset
set terminal postscript eps enhanced color 28
# monochrome




set size 0.9,0.15
set border 0
set noxtics;
set noytics;





set style data histogram
set style histogram rowstack gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
# set palette gray



set key tmargin right horizontal Right reverse spacing 1 width -2
set output "legend_ant_short.eps"
data_dir = "../analysis_data/"



plot [-10:-10.0001][-100:-100.001] \
newhistogram "mobile 1" lt 1, data_dir.'mobile_atheros_rx.trace2scheme.rx_ant.txt' using 2 t '1 ant' fs pattern 1, '' u 3 t '2 ant' fs pattern 2, '' u 4 t '3 ant' fs pattern 5, \
newhistogram "mobile 2" lt 1, data_dir.'mobile_atheros_rx.trace2scheme.rx_ant.txt' using 5 notitle fs pattern 1, '' u 6 notitle fs pattern 2, '' u 7 notitle fs pattern 5, \
newhistogram "mobile 3" lt 1, data_dir.'mobile_atheros_rx.trace2scheme.rx_ant.txt' using 8 notitle fs pattern 1, '' u 9 notitle fs pattern 2, '' u 10 notitle fs pattern 5

