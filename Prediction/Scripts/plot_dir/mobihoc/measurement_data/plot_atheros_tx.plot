reset
set terminal postscript eps enhanced color 28


set size ratio 0.7
set xlabel "Transmission Time (S)"
set ylabel "Energy (J)"
set ytics nomirror
# set yrange [0:25]
set key right bottom
# set key Left under reverse nobox spacing 1
# set nokey


data_dir = "./"
fig_dir = "../measurement_figures/"
set output fig_dir."atheros-tx-ettvs-energy.eps"

set style line 1 lc rgb "#FF0000" lt 1 lw 3 pt 3 
set style line 2 lc rgb "#0000FF" lt 2 lw 3 pt 3 
set style line 3 lc rgb "orange" lt 1 lw 3 pt 3 
set style line 4 lc rgb "green" lt 3 lw 3 pt 3 
set style line 5 lc rgb "yellow" lt 1 lw 3 pt 3 
set style line 6 lc rgb "black" lt 1 lw 3 pt 3

set pointsize 1.5

plot data_dir."txatherosdata.dat.out" using 21:22 with linespoints lt 1 lc rgb "green" lw 3 pt 3 title "3 Ant", \
     data_dir."txatherosdata.dat.out" using 23:24 with linespoints lt 1 lc rgb "green" lw 3 pt 3 notitle, \
     data_dir."txatherosdata.dat.out" using 25:26 with linespoints lt 1 lc rgb "green" lw 3 pt 3 notitle, \
     data_dir."txatherosdata.dat.out" using 27:28 with linespoints lt 1 lc rgb "green" lw 3 pt 3 notitle, \
     data_dir."txatherosdata.dat.out" using 29:30 with linespoints lt 1 lc rgb "green" lw 3 pt 3 notitle, \
     data_dir."txatherosdata.dat.out" using 11:12 with linespoints lt 2 lc rgb "blue" lw 3 pt 2 title "2 Ant", \
     data_dir."txatherosdata.dat.out" using 13:14 with linespoints lt 2 lc rgb "blue" lw 3 pt 2 notitle, \
     data_dir."txatherosdata.dat.out" using 15:16 with linespoints lt 2 lc rgb "blue" lw 3 pt 2 notitle, \
     data_dir."txatherosdata.dat.out" using 17:18 with linespoints lt 2 lc rgb "blue" lw 3 pt 2 notitle, \
     data_dir."txatherosdata.dat.out" using 19:20 with linespoints lt 2 lc rgb "blue" lw 3 pt 2 notitle, \
     data_dir."txatherosdata.dat.out" using 1:2   with linespoints lt 3 lc rgb "#FF0000" lw 3 pt 4 title "1 Ant", \
     data_dir."txatherosdata.dat.out" using 3:4   with linespoints lt 3 lc rgb "#FF0000" lw 3 pt 4 notitle, \
     data_dir."txatherosdata.dat.out" using 5:6   with linespoints lt 3 lc rgb "#FF0000" lw 3 pt 4 notitle, \
     data_dir."txatherosdata.dat.out" using 7:8   with linespoints lt 3 lc rgb "#FF0000" lw 3 pt 4 notitle, \
     data_dir."txatherosdata.dat.out" using 9:10  with linespoints lt 3 lc rgb "#FF0000" lw 3 pt 4 notitle
     
     
