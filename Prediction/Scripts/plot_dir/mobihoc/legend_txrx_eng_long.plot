set terminal postscript eps enhanced monochrome 28


set size 2,0.22
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
set output "legend_txrx_eng_long.eps"
data_dir = "../txrx_data/"


plot [-10:-10.0001][-100:-100.001] \
data_dir.'static_intel.txrx.eng.txt' using 2:xtic(1) t '{/Helvetica=28 MaxTput,tx}', \
data_dir.'static_intel.txrx.eng.txt' using 3:xtic(1) t '{/Helvetica=28 MaxTput,rx}', \
data_dir.'static_intel.txrx.eng.txt' using 4:xtic(1) t '{/Helvetica=28 MaxTput,sum}', \
data_dir.'static_intel.txrx.eng.txt' using 5:xtic(1) t '{/Helvetica=28 MinEng-TX,tx}', \
data_dir.'static_intel.txrx.eng.txt' using 6:xtic(1) t '{/Helvetica=28 MinEng-TX,rx}', \
data_dir.'static_intel.txrx.eng.txt' using 7:xtic(1) t '{/Helvetica=28 MinEng-TX,sum}', \
data_dir.'static_intel.txrx.eng.txt' using 8:xtic(1) t '{/Helvetica=28 MinEng-RX,tx}', \
data_dir.'static_intel.txrx.eng.txt' using 9:xtic(1) t '{/Helvetica=28 MinEng-RX,rx}', \
data_dir.'static_intel.txrx.eng.txt' using 10:xtic(1) t '{/Helvetica=28 MinEng-RX,sum}', \
data_dir.'static_intel.txrx.eng.txt' using 11:xtic(1) t '{/Helvetica=28 MinEng-BOTH,tx}', \
data_dir.'static_intel.txrx.eng.txt' using 12:xtic(1) t '{/Helvetica=28 MinEng-BOTH,rx}', \
data_dir.'static_intel.txrx.eng.txt' using 13:xtic(1) t '{/Helvetica=28 MinEng-BOTH,sum}'


