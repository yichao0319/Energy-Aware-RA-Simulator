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
set ylabel "XXX_YLABEL";
set nokey;
# set key Left above reverse horizontal nobox spacing 0.9
# set key outside right
set output fig_dir."XXX_FILE.eps"

plot \
data_dir.'XXX_FILE.txt' using 2:xtic(1) t '{/Helvetica=28 EffSnr}', \
data_dir.'XXX_FILE.txt' using 3:xtic(1) t '{/Helvetica=28 MinEng}', \
data_dir.'XXX_FILE.txt' using 4:xtic(1) t '{/Helvetica=28 MaxTput}', \
data_dir.'XXX_FILE.txt' using 5:xtic(1) t '{/Helvetica=28 SRate}', \
data_dir.'XXX_FILE.txt' using 6:xtic(1) t '{/Helvetica=28 ETput80}', \
data_dir.'XXX_FILE.txt' using 7:xtic(1) t '{/Helvetica=28 ETput60}'
