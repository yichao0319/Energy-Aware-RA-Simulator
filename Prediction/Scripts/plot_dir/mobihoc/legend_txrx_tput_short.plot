set terminal postscript eps enhanced monochrome 28


set size 1,0.12
set border 0
set noxtics;
set noytics;



set style data histogram
set style histogram gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray



set key Left above reverse horizontal nobox spacing 0.9
set output "legend_txrx_tput_short.eps"
data_dir = "../txrx_data/"


plot [-10:-10.0001][-100:-100.001] \
data_dir.'static_intel.txrx.tput.txt' using 2:xtic(1) t '{/Helvetica=28 MaxTput}', \
data_dir.'static_intel.txrx.tput.txt' using 3:xtic(1) t '{/Helvetica=28 MinEng-TX}', \
data_dir.'static_intel.txrx.tput.txt' using 4:xtic(1) t '{/Helvetica=28 MinEng-RX}', \
data_dir.'static_intel.txrx.tput.txt' using 5:xtic(1) t '{/Helvetica=28 MinEng-BOTH}'