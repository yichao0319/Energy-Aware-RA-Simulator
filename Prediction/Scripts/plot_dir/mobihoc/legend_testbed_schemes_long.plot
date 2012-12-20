set terminal postscript eps enhanced monochrome 28


set size 2,0.07
set border 0
set noxtics;
set noytics;



set style data histogram
set style histogram errorbars gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray



set key Left above reverse horizontal nobox spacing 0.9
set output "legend_testbed_schemes_long.eps"
data_dir = "./testbed_data/"


plot [-10:-10.0001][-100:-100.001] \
data_dir.'mobile_combine.tput.txt' using 2:3:xtic(1) t '{/Helvetica=28 MinEng}', \
data_dir.'mobile_combine.tput.txt' using 4:5:xtic(1) t '{/Helvetica=28 MaxTput}', \
data_dir.'mobile_combine.tput.txt' using 6:7:xtic(1) t '{/Helvetica=28 ETput80}', \
data_dir.'mobile_combine.tput.txt' using 8:9:xtic(1) t '{/Helvetica=28 ETput70}', \
data_dir.'mobile_combine.tput.txt' using 10:11:xtic(1) t '{/Helvetica=28 ETput60}'
