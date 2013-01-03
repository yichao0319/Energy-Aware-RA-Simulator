reset
set terminal postscript eps enhanced color 28


set size ratio 0.7
set xlabel "Single antenna tx time (ms)"
set ylabel "% decrease required \nin tx time"
set ytics nomirror
# set yrange [0:25]
set key right top
# set key Left under reverse nobox spacing 1
# set nokey


data_dir = "./"
fig_dir = "../motivation_figures/"
set output fig_dir."ett_motivation_plot.eps"

set style line 1 lc rgb "#FF0000" lt 1 lw 3
set style line 2 lc rgb "#0000FF" lt 4 lw 3
set style line 3 lc rgb "orange" lt 1 lw 3
set style line 4 lc rgb "green" lt 1 lw 3
set style line 5 lc rgb "yellow" lt 1 lw 3
set style line 6 lc rgb "black" lt 1 lw 3
#plot data_dir."ett_motivation.txt" using 1:3 with lines ls 2 title "3x3 Ant", \
#     data_dir."ett_motivation.txt" using 1:2 with lines ls 1 title "2x2 Ant"

plot data_dir."ett_motivation.txt" using 1:3 with linespoints lt 5 lc rgb "red" lw 3 pt 4 title "3x3 Ant", \
     data_dir."ett_motivation.txt" using 1:2 with linespoints lt 1 lc rgb "blue" lw 3 pt 2 title "2x2 Ant"

