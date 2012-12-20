set terminal postscript eps enhanced monochrome 28

set style data histogram
set style histogram gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray

data_dir = "./"
fig_dir = "../analysis_figures/"

set yrange [0:]

# set xlabel "traces";
set ylabel "Success rate";
set nokey;
# set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."mobile_atheros_rx.trace2scheme.succ.eps"

plot \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 2:xtic(1) t '{/Helvetica=28 EffSnr}', \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 3:xtic(1) t '{/Helvetica=28 MinEng}', \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 4:xtic(1) t '{/Helvetica=28 MaxTput}', \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 5:xtic(1) t '{/Helvetica=28 SRate}', \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 6:xtic(1) t '{/Helvetica=28 ETput80}', \
data_dir.'mobile_atheros_rx.trace2scheme.succ.txt' using 7:xtic(1) t '{/Helvetica=28 ETput60}'
