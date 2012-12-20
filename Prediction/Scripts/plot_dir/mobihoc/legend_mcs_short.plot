reset
set terminal postscript eps enhanced color 28
# monochrome



set size 0.9,0.18
set border 0
set noxtics;
set noytics;




set style data histogram
set style histogram rowstack gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
# set palette gray



set key Left above reverse horizontal nobox spacing 0.9
set output "legend_mcs_short.eps"
data_dir = "../analysis_data/"


plot [-10:-10.0001][-100:-100.001] \
newhistogram "static 1" lt 1, data_dir.'static_atheros_tx.trace2scheme.mcs.txt' using 2 t 'MCS 1' fs pattern 5, '' u 3 t 'MCS 2' fs pattern 6, '' u 4 t 'MCS 3' fs pattern 7, '' u 5 t 'MCS 4' fs pattern 4, '' u 6 t 'MCS 5' fs pattern 3, '' u 7 t 'MCS 6' fs pattern 2, '' u 8 t 'MCS 7' fs pattern 1, \
newhistogram "static 2" lt 1, data_dir.'static_atheros_tx.trace2scheme.mcs.txt' using 9 notitle fs pattern 5, '' u 10 notitle fs pattern 6, '' u 11 notitle fs pattern 7, '' u 12 notitle fs pattern 4, '' u 13 notitle fs pattern 3, '' u 14 notitle fs pattern 2, '' u 15 notitle fs pattern 1, \
newhistogram "static 3" lt 1, data_dir.'static_atheros_tx.trace2scheme.mcs.txt' using 16 notitle fs pattern 5, '' u 17 notitle fs pattern 6, '' u 18 notitle fs pattern 7, '' u 19 notitle fs pattern 4, '' u 20 notitle fs pattern 3, '' u 21 notitle fs pattern 2, '' u 22 notitle fs pattern 1
