set terminal postscript eps enhanced monochrome 28

set size 1,0.8

set style data histogram
set style histogram gap 1
set style fill solid border -1
set boxwidth 0.9

set style fill pattern 
set palette gray

data_dir = "./"
fig_dir = "../txrx_figures/"

set yrange [0:]

# set xlabel "traces";
set ylabel "Energy (nJ/bit)";
set nokey;
# set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."XXX_FILE.eps"


plot \
data_dir.'XXX_FILE.txt' using 2:xtic(1) t '{/Helvetica=28 MaxTput,tx}', \
data_dir.'XXX_FILE.txt' using 3:xtic(1) t '{/Helvetica=28 MaxTput,rx}', \
data_dir.'XXX_FILE.txt' using 4:xtic(1) t '{/Helvetica=28 MaxTput,sum}', \
data_dir.'XXX_FILE.txt' using 5:xtic(1) t '{/Helvetica=28 MinEng-TX,tx}', \
data_dir.'XXX_FILE.txt' using 6:xtic(1) t '{/Helvetica=28 MinEng-TX,rx}', \
data_dir.'XXX_FILE.txt' using 7:xtic(1) t '{/Helvetica=28 MinEng-TX,sum}', \
data_dir.'XXX_FILE.txt' using 8:xtic(1) t '{/Helvetica=28 MinEng-RX,tx}', \
data_dir.'XXX_FILE.txt' using 9:xtic(1) t '{/Helvetica=28 MinEng-RX,rx}', \
data_dir.'XXX_FILE.txt' using 10:xtic(1) t '{/Helvetica=28 MinEng-RX,sum}', \
data_dir.'XXX_FILE.txt' using 11:xtic(1) t '{/Helvetica=28 MinEng-BOTH,tx}', \
data_dir.'XXX_FILE.txt' using 12:xtic(1) t '{/Helvetica=28 MinEng-BOTH,rx}', \
data_dir.'XXX_FILE.txt' using 13:xtic(1) t '{/Helvetica=28 MinEng-BOTH,sum}'


