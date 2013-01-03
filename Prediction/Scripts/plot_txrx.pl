#!/bin/perl 

use strict;
use Cwd;

#####
## constant
my $DEBUG0 = 0;
my $DEBUG1 = 1;


#####
## variables
my $input_dir = "../ProcessedData";
my $output_data_dir = "./plot_dir/txrx_data";
my $output_fig_dir = "./plot_dir/txrx_figures";

my $gnuplot_tput_mother = "plot_txrx_tput";
my $gnuplot_eng_mother = "plot_txrx_eng";

my @static_traces = ("static1", "static2", "static3");
my @static_traces2 = ('static_sender2_3tx_run1', 'static_sender2_3tx_run2', 'static_sender2_3tx_run3');
my @mobile_traces = ("facespeed21", "sidespeed11", "sidespeed21");
# my @mobile_traces2 = ('sender1_lap1_seg11', 'sender1_lap1_seg21', 'sender1_lap1_seg31', 'sender1_lap1_seg41', 'sender1_lap2_seg11', 'sender1_lap2_seg21', 'sender1_lap2_seg31', 'sender1_lap2_seg41', 'sender1_lap3_seg11', 'sender1_lap3_seg21', 'sender1_lap3_seg31', 'sender1_lap3_seg41', 'sender2_lap1_seg11', 'sender2_lap1_seg21', 'sender2_lap1_seg31', 'sender2_lap1_seg41', 'sender2_lap2_seg11', 'sender2_lap2_seg21', 'sender2_lap2_seg31', 'sender2_lap2_seg41', 'sender2_lap3_seg11', 'sender2_lap3_seg21', 'sender2_lap3_seg31', 'sender2_lap3_seg41', 'sender3_lap1_seg11', 'sender3_lap1_seg21', 'sender3_lap1_seg31', 'sender3_lap1_seg41', 'sender3_lap2_seg11', 'sender3_lap2_seg21', 'sender3_lap2_seg31', 'sender3_lap2_seg41', 'sender3_lap3_seg11', 'sender3_lap3_seg21', 'sender3_lap3_seg31', 'sender3_lap3_seg41');
my @mobile_traces2 = ('sender1_lap1_seg11', 'sender1_lap3_seg31', 'sender3_lap1_seg11');
# my @mobile_traces3 = ('mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01', 'mob_recv4_run1_01');
my @mobile_traces3 = ('mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01');
my @mobile_traces4 = ('sender1_lap1_seg1_mix1', 'sender1_lap1_seg2_mix1', 'sender1_lap1_seg3_mix1');
# my @traces = (@static_traces, @mobile_traces, @mobile_traces2, @mobile_traces3, @mobile_traces4, @static_traces2);
my @traces = (@mobile_traces4, @static_traces2);

my @schemes = ("MinEng", "MaxTput", "EngTput08", "EngTput06");
my @card_types = ("atheros", "intel");
# my @constraints = ("tx", "rx", "tx_rx");
my @constraints = ("tx_rx");
my @predictions = ("True", "False");



#####
## main
foreach my $card_type (@card_types) {

    ## data{tx | rx | tx_rx}{trace}{oracle | prediction}{MaxTput | MinEng}{throughput | eng_tx | eng_rx | eng_txrx}
    my %data = ();
        
    foreach my $constraint (@constraints) {
        foreach my $trace (@traces) {            
            foreach my $scheme (@schemes) {
                ## prediction 1 (previous pkt)
                ## prediction 2 (Holt-Winters)
                foreach my $prediction (@predictions) {
                    my $this_file = "$input_dir/$trace/$card_type/$constraint/$scheme$prediction.dat";
                    my ($tput, $energy, $energy_tx, $energy_rx) = get_tput_eng_from_file($this_file);
                    $data{$constraint}{$trace}{$prediction}{$scheme}{throughput} = $tput;
                    $data{$constraint}{$trace}{$prediction}{$scheme}{energy_tx_rx} = $energy;
                    $data{$constraint}{$trace}{$prediction}{$scheme}{energy_tx} = $energy_tx;
                    $data{$constraint}{$trace}{$prediction}{$scheme}{energy_rx} = $energy_rx;
                }
            }
        }   ## end for each trace
    }


    #####
    ##  i) static traces * scheme
    ##    - generate data file to plot
    my $out_filename_tput = "static_".$card_type.".txrx.tput";
    my $this_file = "$output_data_dir/$out_filename_tput.txt";
    write_to_file_throughput($this_file, \%data, 'static', \@static_traces2);

    my $out_filename_eng = "static_".$card_type.".txrx.eng";
    $this_file = "$output_data_dir/$out_filename_eng.txt";
    write_to_file_energy($this_file, \%data, 'static', \@static_traces2);

    
    ##    - generate gnuplot script
    my $cmd = "sed 's/XXX_FILE/$out_filename_tput/g;' $gnuplot_tput_mother.mother.plot > $output_data_dir/$gnuplot_tput_mother.$card_type.static.tput.plot";
    print $cmd if($DEBUG0);
    system($cmd);
    
    my $cur_dir = cwd;
    chdir $output_data_dir or die $!;
    system("gnuplot $gnuplot_tput_mother.$card_type.static.tput.plot");
    chdir $cur_dir or die $!;
    
    $cmd = "sed 's/XXX_FILE/$out_filename_eng/g;' $gnuplot_eng_mother.mother.plot > $output_data_dir/$gnuplot_eng_mother.$card_type.static.eng.plot";
    print $cmd if($DEBUG0);
    system($cmd);
    
    chdir $output_data_dir or die $!;
    system("gnuplot $gnuplot_eng_mother.$card_type.static.eng.plot");
    chdir $cur_dir or die $!;


    #####
    ##  ii) mobile traces * scheme
    ##      - generate data file to plot
    $out_filename_tput = "mobile_".$card_type.".txrx.tput";
    $this_file = "$output_data_dir/$out_filename_tput.txt";
    write_to_file_throughput($this_file, \%data, 'mobile', \@mobile_traces4);
    $out_filename_eng = "mobile_".$card_type.".txrx.eng";
    $this_file = "$output_data_dir/$out_filename_eng.txt";
    write_to_file_energy($this_file, \%data, 'mobile', \@mobile_traces4);

    
    ##      - generate gnuplot script
    $cmd = "sed 's/XXX_FILE/$out_filename_tput/g;' $gnuplot_tput_mother.mother.plot > $output_data_dir/$gnuplot_tput_mother.$card_type.mobile.tput.plot";
    print $cmd if($DEBUG0);
    system($cmd);
    
    chdir $output_data_dir or die $!;
    system("gnuplot $gnuplot_tput_mother.$card_type.mobile.tput.plot");
    chdir $cur_dir or die $!;
    
    $cmd = "sed 's/XXX_YLABEL/Energy (nJ\\\/bit)/; s/XXX_FILE/$out_filename_eng/g;' $gnuplot_eng_mother.mother.plot > $output_data_dir/$gnuplot_eng_mother.$card_type.mobile.eng.plot";
    print $cmd if($DEBUG0);
    system($cmd);
    
    chdir $output_data_dir or die $!;
    system("gnuplot $gnuplot_eng_mother.$card_type.mobile.eng.plot");
    chdir $cur_dir or die $!;
    
}




#####
## functions

sub get_tput_eng_from_file {
    my ($filename) = @_;
    print "get $filename\n" if($DEBUG0);
    my $tput = 0;
    my $energy = 0;
    my $energy_tx = 0;
    my $energy_rx = 0;

    if(!(-e $filename)) {
        print $filename." does not exist\n";
        return ($tput, $energy);
    }

    open FH, "<$filename" or die "$!\n$filename\n";
    while(<FH>) {
        print $_ if($DEBUG1);
        # if($_ =~ /{'tput': (\d+\.*\d*), 'eng': (\d+\.*\d*e*-*\d*)}/) {
        if($_ =~ /{'eng_tx': (\d+\.*\d*e*-*\d*), 'tput': (\d+\.*\d*e*-*\d*), 'eng_rx': (\d+\.*\d*e*-*\d*), 'eng': (\d+\.*\d*e*-*\d*)}/) {
            $tput = ($2 + 0) / 1000000; ## Mbps
            $energy_tx = ($1 + 0) / 1e-6;
            $energy_rx = ($3 + 0) / 1e-6;
            $energy = ($4 + 0) / 1e-6;
        }
        else {
            print $filename."\n".$_."\n";
            die "wrong file format\n";
        }
        print "-> ".join(", ", ($tput, $energy))."\n" if($DEBUG1);
    }
    close(FH);

    return ($tput, $energy, $energy_tx, $energy_rx);
}


##   traces * schemes
sub write_to_file_throughput {
    my ($filename, $ref_data, $type, $ref_traces) = @_;

    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        my $trace = $ref_traces->[$trace_i-1];
        print $trace.", " if($DEBUG1);
        print FH "\"$type $trace_i\", ";

        ## MinEng
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'MinEng'}{throughput}.", ";

        ## MaxTput
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'MaxTput'}{throughput}.", ";
        
        ## ETput80
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'EngTput08'}{throughput}.", ";

        ## ETput60
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'EngTput06'}{throughput}."\n";
    }
    print "\n" if($DEBUG1);

    close(FH);
}


sub write_to_file_energy {
    my ($filename, $ref_data, $type, $ref_traces) = @_;

    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        my $trace = $ref_traces->[$trace_i-1];
        print $trace.", " if($DEBUG1);
        print FH "\"$type $trace_i\", ";

        ## MinEng
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'MinEng'}{energy_tx_rx}.", ";

        ## MaxTput
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'MaxTput'}{energy_tx_rx}.", ";
        
        ## ETput80
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'EngTput08'}{energy_tx_rx}.", ";

        ## ETput60
        print FH $ref_data->{'tx_rx'}{$trace}{$pred}{'EngTput06'}{energy_tx_rx}."\n";

    }
    print "\n" if($DEBUG1);

    close(FH);
}


