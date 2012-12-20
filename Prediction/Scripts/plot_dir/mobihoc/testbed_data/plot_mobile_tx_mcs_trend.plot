reset
set terminal postscript eps enhanced color 28


set size ratio 0.7
set xlabel "packet"
set ylabel "MCS index"
set ytics nomirror
set yrange [0:25]
set key right top
# set key Left under reverse nobox spacing 1
# set nokey


data_dir = "./"
fig_dir = "../testbed_figures/"
set output fig_dir."testbed_mobile_tx_mcs_trend.eps"

set style line 1 lc rgb "#FF0000" lt 1 lw 3
set style line 2 lc rgb "#0000FF" lt 2 lw 3
set style line 3 lc rgb "orange" lt 1 lw 3
set style line 4 lc rgb "green" lt 1 lw 3
set style line 5 lc rgb "yellow" lt 1 lw 3
set style line 6 lc rgb "black" lt 1 lw 3
plot data_dir."mobile_tx_mcs_trend.txt" using 1 with lines ls 1 title "MaxTput", \
     "" using 3 with lines ls 2 title "MinEng"

