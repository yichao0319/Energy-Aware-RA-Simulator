#!/bin/perl 

use strict;
use Cwd;


#####
## constant
my $DEBUG0 = 0;
my $DEBUG1 = 1;


#####
## variables
my $oracle_dir = "../oracle_results";
my $input_dir = "../PPrProcessedData";
my $output_data_dir = "./plot_dir/ppr_data";
my $output_fig_dir = "./plot_dir/ppr_figures";

my $gnuplot_trace2scheme_mother = "plot_ppr_trace2scheme";

# my @traces = ("facespeed11", "facespeed21", "facespeed31", "sidespeed11", "sidespeed21", "static1", "static2", "static3");
my @static_traces = ("static1", "static2", "static3");
my @mobile_traces = ("facespeed21", "sidespeed11", "sidespeed21");
# my @mobile_traces2 = ('sender1_lap1_seg11', 'sender1_lap1_seg21', 'sender1_lap1_seg31', 'sender1_lap1_seg41', 'sender1_lap2_seg11', 'sender1_lap2_seg21', 'sender1_lap2_seg31', 'sender1_lap2_seg41', 'sender1_lap3_seg11', 'sender1_lap3_seg21', 'sender1_lap3_seg31', 'sender1_lap3_seg41', 'sender2_lap1_seg11', 'sender2_lap1_seg21', 'sender2_lap1_seg31', 'sender2_lap1_seg41', 'sender2_lap2_seg11', 'sender2_lap2_seg21', 'sender2_lap2_seg31', 'sender2_lap2_seg41', 'sender2_lap3_seg11', 'sender2_lap3_seg21', 'sender2_lap3_seg31', 'sender2_lap3_seg41', 'sender3_lap1_seg11', 'sender3_lap1_seg21', 'sender3_lap1_seg31', 'sender3_lap1_seg41', 'sender3_lap2_seg11', 'sender3_lap2_seg21', 'sender3_lap2_seg31', 'sender3_lap2_seg41', 'sender3_lap3_seg11', 'sender3_lap3_seg21', 'sender3_lap3_seg31', 'sender3_lap3_seg41');
my @mobile_traces2 = ('sender1_lap1_seg11', 'sender1_lap3_seg31', 'sender3_lap1_seg11');
# my @mobile_traces3 = ('mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01', 'mob_recv4_run1_01');
my @mobile_traces3 = ('mob_recv1_run1_01', 'mob_recv2_run1_01', 'mob_recv3_run1_01');
my @mobile_traces4 = ('sender1_lap1_seg1_mix1', 'sender1_lap1_seg2_mix1', 'sender1_lap1_seg3_mix1');
my @static_traces2 = ('static_sender2_3tx_run1', 'static_sender2_3tx_run2', 'static_sender2_3tx_run3');
my @traces = (@static_traces, @mobile_traces, @mobile_traces2, @mobile_traces3, @mobile_traces4, @static_traces2);
# my @traces = ("static1", "static2", "static3");
# my @schemes = ("PPrMinEng", "PPrMaxTput", "PPrEngTput08", "PPrEngTput06", "PPrEngTput04", "PPrEngTput02");
my @schemes = ("PPrMinEng", "PPrMaxTput", "PPrEngTput08", "PPrEngTput06");
# my @schemes = ("PPrMinEng", "OraclePPrMinEng", "PPrMaxTput", "OraclePPrMaxTput", "PPrEngTput08", "PPrEngTput06");
my @card_types = ("atheros", "intel");
my @constraints = ("tx", "rx");
my @predictions = ("True", "False");



#####
## main
foreach my $card_type (@card_types) {
    foreach my $constraint (@constraints) {

        ## data{throughput | energy}{trace}{oracle | prediction1 | prediction2}{EffSnr | MaxTput | MinEng}
        my %data = ();
        foreach my $trace (@traces) {            
            foreach my $scheme (@schemes) {
                ## prediction 1 (previous pkt)
                ## prediction 2 (Holt-Winters)
                foreach my $prediction (@predictions) {
                    next if $prediction eq 'True' && $scheme =~ /Oracle/;
                    my $this_file = "$input_dir/$trace/$card_type/$constraint/$scheme$prediction.dat";
                    my ($tput, $energy) = get_tput_eng_from_file($this_file);
                    $data{throughput}{$trace}{$prediction}{$scheme} = $tput;
                    $data{energy}{$trace}{$prediction}{$scheme} = $energy;
                }
            }
        }   ## end for each trace


        #####
        ## i) static traces * scheme
        ##    - generate data file to plot
        my $out_filename_tput = "static_".$card_type."_".$constraint.".ppr.trace2scheme.tput";
        my $this_file = "$output_data_dir/$out_filename_tput.txt";
        write_to_file_trace2scheme($this_file, \%{$data{throughput}}, 'static', \@static_traces2, \@schemes);
        my $out_filename_eng = "static_".$card_type."_".$constraint.".ppr.trace2scheme.eng";
        $this_file = "$output_data_dir/$out_filename_eng.txt";
        write_to_file_trace2scheme($this_file, \%{$data{energy}}, 'static', \@static_traces2, \@schemes);

        
        ##    - generate gnuplot script
        my $cmd = "sed 's/XXX_YLABEL/Throughput (Mbps)/; s/XXX_FILE/$out_filename_tput/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.static.tput.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        
        my $cur_dir = cwd;
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.static.tput.plot");
        chdir $cur_dir or die $!;

        $cmd = "sed 's/XXX_YLABEL/Energy (nJ\\\/bit)/; s/XXX_FILE/$out_filename_eng/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.static.eng.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.static.eng.plot");
        chdir $cur_dir or die $!;


        #####
        ## ii) mobile traces * scheme
        ##     - generate data file to plot
        $out_filename_tput = "mobile_".$card_type."_".$constraint.".ppr.trace2scheme.tput";
        $this_file = "$output_data_dir/$out_filename_tput.txt";
        write_to_file_trace2scheme($this_file, \%{$data{throughput}}, 'mobile', \@mobile_traces4, \@schemes);
        $out_filename_eng = "mobile_".$card_type."_".$constraint.".ppr.trace2scheme.eng";
        $this_file = "$output_data_dir/$out_filename_eng.txt";
        write_to_file_trace2scheme($this_file, \%{$data{energy}}, 'mobile', \@mobile_traces4, \@schemes);

        
        ##     - generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/Throughput (Mbps)/; s/XXX_FILE/$out_filename_tput/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.tput.plot";
        print $cmd if($DEBUG0);
        system($cmd);

        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.tput.plot");
        chdir $cur_dir or die $!;

        $cmd = "sed 's/XXX_YLABEL/Energy (nJ\\\/bit)/; s/XXX_FILE/$out_filename_eng/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.eng.plot";
        print $cmd if($DEBUG0);
        system($cmd);

        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.eng.plot");
        chdir $cur_dir or die $!;
    }
}




#####
## functions

sub get_tput_eng_from_file {
    my ($filename) = @_;
    print "get $filename\n" if($DEBUG0);
    my $tput = 0;
    my $energy = 0;

    if(!(-e $filename)) {
        print $filename." does not exist\n";
        # die $!;
        return ($tput, $energy);
    }

    open FH, "<$filename" or die "$!\n$filename\n";
    while(<FH>) {
        print $_ if($DEBUG1);
        if($_ =~ /{'tput': (\d+\.*\d*), 'eng': (\d+\.*\d*e*-*\d*)}/) {
            $tput = ($1 + 0) / 1000000; ## Mbps
            $energy = ($2 + 0) / 1e-6;
        }
        else {
            print $filename."\n".$_."\n";
            die "wrong file format\n";
        }
        print "-> ".join(", ", ($tput, $energy))."\n" if($DEBUG1);
    }
    close(FH);

    return ($tput, $energy);
}


## traces * schemes
sub write_to_file_trace2scheme {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes) = @_;

    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        my $trace = $ref_traces->[$trace_i-1];
        print $trace.", " if($DEBUG1);
        print FH "\"$type $trace_i\", ";
        
        foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
            my $scheme = $ref_schemes->[$scheme_i-1];
            print $scheme.", " if($DEBUG1);
            print FH $ref_data->{$trace}{$pred}{$scheme}.", ";
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}


