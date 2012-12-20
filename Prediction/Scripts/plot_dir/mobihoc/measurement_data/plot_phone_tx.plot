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
set output fig_dir."phone-tx-ettvs-energy.eps"


set xrange [0.004:0.016]
set yrange [0:0.009]
set xtics 0.003
set ytics 0.002


set pointsize 1.5

plot data_dir."phone_data.dat.out" using 1:2 with linespoints lt 1 lc rgb "red" lw 3 pt 4 title "1 Ant", \
     data_dir."phone_data.dat.out" using 3:4 with linespoints lt 1 lc rgb "red" lw 3 pt 4 notitle, \
     data_dir."phone_data.dat.out" using 5:6 with linespoints lt 1 lc rgb "red" lw 3 pt 4 notitle, \
     data_dir."phone_data.dat.out" using 7:8 with linespoints lt 1 lc rgb "red" lw 3 pt 4 notitle
     
     
