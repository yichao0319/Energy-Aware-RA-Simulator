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
my $input_dir = "../ProcessedData";
my $input_dir_static = "../Data/StaticTrace";
my $input_dir_static2 = "../Data/StaticTrace2";
my $input_dir_mobile = "../Data/MobileTrace";
my $input_dir_mobile2 = "../Data/MobileTrace2";
my $input_dir_mobile3 = "../Data/MobileTrace3";
my $output_data_dir = "./plot_dir/analysis_data";
my $output_fig_dir = "./plot_dir/analysis_figures";

my $gnuplot_trace2scheme_mother = "plot_analysis_succ";
my $gnuplot_mcs_mother = "plot_analysis_mcs";
my $gnuplot_ant_mother = "plot_analysis_ant";


my @static_traces_dir = ($input_dir_static, $input_dir_static, $input_dir_static);
my @static_traces = ("static1", "static2", "static3");
my @static_traces_dir2 = ($input_dir_static2, $input_dir_static2, $input_dir_static2);
my @static_traces2 = ('static_sender2_3tx_run1', 'static_sender2_3tx_run2', 'static_sender2_3tx_run3');
my @mobile_traces_dir = ($input_dir_mobile, $input_dir_mobile, $input_dir_mobile);
my @mobile_traces = ("facespeed2", "sidespeed1", "sidespeed2");
my @mobile_traces_dir2 = ($input_dir_mobile2, $input_dir_mobile2, $input_dir_mobile2);
my @mobile_traces2 = ('sender1_lap1_seg1', 'sender1_lap3_seg3', 'sender3_lap1_seg1');
my @mobile_traces_dir3 = ($input_dir_mobile3, $input_dir_mobile3, $input_dir_mobile3);
my @mobile_traces3 = ('mob_recv1_run1_0', 'mob_recv2_run1_0', 'mob_recv3_run1_0');
my @mobile_traces_dir4 = ($input_dir_mobile3, $input_dir_mobile3, $input_dir_mobile3);
my @mobile_traces4 = ('sender1_lap1_seg1_mix', 'sender1_lap1_seg2_mix', 'sender1_lap1_seg3_mix');
my @traces_dir = (@static_traces_dir, @static_traces_dir2, @mobile_traces_dir, @mobile_traces_dir2, @mobile_traces_dir3, @mobile_traces_dir4);
my @traces = (@static_traces, @static_traces2, @mobile_traces, @mobile_traces2, @mobile_traces3, @mobile_traces4);
my @schemes = ("EffSnr", "MinEng", "MaxTput", "SampleRate", "EngTput08", "EngTput06");
my @scheme_fig_name = ("EffSnr", "MinEng", "MaxTput", "SRate", "ETput80", "ETput60");
my @card_types = ("atheros", "intel");
my @constraints = ("tx", "rx");
# my @predictions = ("True", "False");
my @predictions = ("False");

## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
my %data = ();


#####
## main
foreach my $card_type (@card_types) {
    foreach my $constraint (@constraints) {


        foreach my $trace_i (0 .. scalar(@traces)-1) {
            my $trace = $traces[$trace_i];
            my $trace_dir = $traces_dir[$trace_i];

            foreach my $scheme_tmp (@schemes) {
                my $scheme = $scheme_tmp;
                my $threshold = 0;
                if($scheme_tmp =~ /(EngTput)(\d)(\d)/) {
                    $scheme = $1;
                    $threshold = $2 + 0 + 0.1 * $3;
                }

                ## prediction 1 (previous pkt)
                ## prediction 2 (Holt-Winters)
                foreach my $prediction (@predictions) {
                    my $this_file = "$trace_dir/".$scheme."_".$trace."_".$card_type."_".$constraint."_pred".$prediction."_inc1.dat";
                    if($scheme_tmp =~ /EngTput/) {
                        $this_file = "$trace_dir/".$scheme."_".$trace."_".$card_type."_".$constraint."_pred".$prediction."th".$threshold."_inc1.dat";
                    }
                    my ($cnt, $succ, $ref_mcs, $ref_tx_antenna, $ref_rx_antenna) = get_statistics_from_file($this_file);
                    $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{count} = $cnt;
                    $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{succ} = $succ / $cnt;
                    $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_mcs} = $ref_mcs;
                    $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_tx_antenna} = $ref_tx_antenna;
                    $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_rx_antenna} = $ref_rx_antenna;


                    #####
                    ## print results
                    print $trace.", ".$scheme_tmp.", ".$card_type.", ".$constraint.", ".$prediction.", ".$cnt.", ".($succ/$cnt).", ";
                    foreach my $mcs_i (0 .. scalar(@$ref_mcs)-1) {
                        print "".(($ref_mcs->[$mcs_i])/$cnt).", ";

                        $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_mcs}->[$mcs_i] /= $cnt;
                    }
                    foreach my $antenna_i (0 .. scalar(@$ref_tx_antenna)-1) {
                        print "".(($ref_tx_antenna->[$antenna_i])/$cnt).", ";

                        $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_tx_antenna}->[$antenna_i] /= $cnt;
                    }
                    foreach my $antenna_i (0 .. scalar(@$ref_rx_antenna)-1) {
                        print "".(($ref_rx_antenna->[$antenna_i])/$cnt).", ";

                        $data{$trace}{$scheme_tmp}{$card_type}{$constraint}{$prediction}{ref_rx_antenna}->[$antenna_i] /= $cnt;
                    }
                    print "\n";

                }
            }
        }   ## end of all traces

        #####
        ## output data
        ##  i) static traces
        ##      a) success rate
        ##          1) generate data file
        my $out_filename = "static_".$card_type."_".$constraint.".trace2scheme.succ";
        my $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_succ($this_file, \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint);
        ##          2) generate gnuplot script
        my $cmd = "sed 's/XXX_YLABEL/Success rate/; s/XXX_FILE/$out_filename/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.static.succ.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        my $cur_dir = cwd;
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.static.succ.plot");
        chdir $cur_dir or die $!;
        
        ##      b) MCS
        ##          1) generate data file
        $out_filename = "static_".$card_type."_".$constraint.".trace2scheme.mcs";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_mcs($this_file, \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, \@scheme_fig_name);
        write_to_file_mcs_excell($this_file.".xlsx", \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/static/g' $gnuplot_mcs_mother.mother.plot > $output_data_dir/$gnuplot_mcs_mother.$card_type.$constraint.static.mcs.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_mcs_mother.$card_type.$constraint.static.mcs.plot");
        chdir $cur_dir or die $!;

        ##      c) TX antenna
        ##          1) generate data file
        $out_filename = "static_".$card_type."_".$constraint.".trace2scheme.tx_ant";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_ant($this_file, \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, "ref_tx_antenna", \@scheme_fig_name);
        write_to_file_ant_excell($this_file.".xlsx", \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, "ref_tx_antenna", \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/static/g' $gnuplot_ant_mother.mother.plot > $output_data_dir/$gnuplot_ant_mother.$card_type.$constraint.static.txant.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_ant_mother.$card_type.$constraint.static.txant.plot");
        chdir $cur_dir or die $!;

        ##      d) RX antenna
        ##          1) generate data file
        $out_filename = "static_".$card_type."_".$constraint.".trace2scheme.rx_ant";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_ant($this_file, \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, "ref_rx_antenna", \@scheme_fig_name);
        write_to_file_ant_excell($this_file.".xlsx", \%data, 'static', \@static_traces, \@schemes, $card_type, $constraint, "ref_rx_antenna", \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/static/g' $gnuplot_ant_mother.mother.plot > $output_data_dir/$gnuplot_ant_mother.$card_type.$constraint.static.rxant.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_ant_mother.$card_type.$constraint.static.rxant.plot");
        chdir $cur_dir or die $!;


        ##  ii) mobile traces
        my @this_mobile_traces = @mobile_traces4;
        ##      a) success rate
        ##          1) generate data file
        my $out_filename = "mobile_".$card_type."_".$constraint.".trace2scheme.succ";
        my $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_succ($this_file, \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint);
        ##          2) generate gnuplot script
        my $cmd = "sed 's/XXX_YLABEL/Success rate/; s/XXX_FILE/$out_filename/g;' $gnuplot_trace2scheme_mother.mother.plot > $output_data_dir/$gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.succ.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_trace2scheme_mother.$card_type.$constraint.mobile.succ.plot");
        chdir $cur_dir or die $!;

        ##      b) MCS
        ##          1) generate data file
        $out_filename = "mobile_".$card_type."_".$constraint.".trace2scheme.mcs";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_mcs($this_file, \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, \@scheme_fig_name);
        write_to_file_mcs_excell($this_file.".xlsx", \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/mobile/g' $gnuplot_mcs_mother.mother.plot > $output_data_dir/$gnuplot_mcs_mother.$card_type.$constraint.mobile.mcs.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_mcs_mother.$card_type.$constraint.mobile.mcs.plot");
        chdir $cur_dir or die $!;

        ##      c) TX antenna
        ##          1) generate data file
        $out_filename = "mobile_".$card_type."_".$constraint.".trace2scheme.tx_ant";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_ant($this_file, \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, "ref_tx_antenna", \@scheme_fig_name);
        write_to_file_ant_excell($this_file.".xlsx", \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, "ref_tx_antenna", \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/mobile/g' $gnuplot_ant_mother.mother.plot > $output_data_dir/$gnuplot_ant_mother.$card_type.$constraint.mobile.txant.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_ant_mother.$card_type.$constraint.mobile.txant.plot");
        chdir $cur_dir or die $!;

        ##      d) RX antenna
        ##          1) generate data file
        $out_filename = "mobile_".$card_type."_".$constraint.".trace2scheme.rx_ant";
        $this_file = "$output_data_dir/$out_filename.txt";
        write_to_file_ant($this_file, \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, "ref_rx_antenna", \@scheme_fig_name);
        write_to_file_ant_excell($this_file.".xlsx", \%data, 'mobile', \@this_mobile_traces, \@schemes, $card_type, $constraint, "ref_rx_antenna", \@scheme_fig_name);
        ##          2) generate gnuplot script
        $cmd = "sed 's/XXX_YLABEL/ratio/; s/XXX_FILE/$out_filename/g; s/XXX_TYPE/mobile/g' $gnuplot_ant_mother.mother.plot > $output_data_dir/$gnuplot_ant_mother.$card_type.$constraint.mobile.rxant.plot";
        print $cmd if($DEBUG0);
        system($cmd);
        ##          3) plot
        chdir $output_data_dir or die $!;
        system("gnuplot $gnuplot_ant_mother.$card_type.$constraint.mobile.rxant.plot");
        chdir $cur_dir or die $!;


    }
}



1;


#####
## functions

sub get_statistics_from_file {
    my ($filename) = @_;
    print "get $filename\n" if($DEBUG0);
    
    my $cnt = 0;
    my $succ = 0;
    my @mcs = (0, 0, 0, 0, 0, 0, 0);
    my @tx_antenna = (0, 0, 0);
    my @rx_antenna = (0, 0, 0);


    if(!(-e $filename)) {
        print $filename." does not exist\n";
        return ($tput, $energy);
    }

    open FH, "<$filename" or die "$!\n$filename\n";
    while(<FH>) {
        print $_ if($DEBUG0);

        if($_ =~ /{'succ': (\d+), 'mcs': (\d+), 'mode': .*(\d+)by(\d+).*'}/) {
            $cnt ++;
            $succ += ($1 + 0);
            
            my $mcs_ind = $2 - 1;
            $mcs[$mcs_ind] ++;

            my $num_tx_antenna = $3;
            my $num_rx_antenna = $4;
            
            $tx_antenna[$num_tx_antenna-1] ++;
            $rx_antenna[$num_rx_antenna-1] ++;
        }
        else {
            print $filename."\n".$_."\n";
            die "wrong file format\n";
        }

    }
    close(FH);

    return ($cnt, $succ, \@mcs, \@tx_antenna, \@rx_antenna);
}



sub write_to_file_succ {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes, $card_type, $constraint) = @_;
    
    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        my $trace = $ref_traces->[$trace_i-1];
        print $trace.", " if($DEBUG1);
        print FH "\"$type $trace_i\", ";
        
        foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
            my $scheme = $ref_schemes->[$scheme_i-1];
            print $scheme.", " if($DEBUG1);

            ## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
            print FH $ref_data->{$trace}{$scheme}{$card_type}{$constraint}{$pred}{succ}.", ";
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}


sub write_to_file_mcs {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes, $card_type, $constraint, $ref_scheme_name) = @_;
    

    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
        my $scheme = $ref_schemes->[$scheme_i-1];
        print $scheme.", " if($DEBUG1);
        print FH "\"".($ref_scheme_name->[$scheme_i-1])."\", ";
        
        foreach my $trace_i (1 .. scalar(@$ref_traces)) {
            my $trace = $ref_traces->[$trace_i-1];
            print $trace.", " if($DEBUG1);
            
            foreach my $mcs_i (0 .. 6) {
                ## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
                print FH "".($ref_data->{$trace}{$scheme}{$card_type}{$constraint}{$pred}{ref_mcs}->[$mcs_i]).", ";
            }
            
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}


sub write_to_file_mcs_excell {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes, $card_type, $constraint, $ref_scheme_name) = @_;
    

    my $pred = 'False';

    open FH, ">$filename" or die $!;

    print FH ", ";
    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
            my $scheme = $ref_schemes->[$scheme_i-1];

            print FH "".($ref_scheme_name->[$scheme_i-1]).", ";
        }
    }
    print FH "\n";

    foreach my $mcs_i (0 .. 6) {
        print FH "\"MCS ".($mcs_i + 1)."\", ";
            
        foreach my $trace_i (1 .. scalar(@$ref_traces)) {
            my $trace = $ref_traces->[$trace_i-1];
            print $trace.", " if($DEBUG1);

            foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
                my $scheme = $ref_schemes->[$scheme_i-1];
                print $scheme.", " if($DEBUG1);
            
                ## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
                print FH "".($ref_data->{$trace}{$scheme}{$card_type}{$constraint}{$pred}{ref_mcs}->[$mcs_i]).", ";
            }
            
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}



sub write_to_file_ant {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes, $card_type, $constraint, $ant_type, $ref_scheme_name) = @_;
    

    my $pred = 'False';

    open FH, ">$filename" or die $!;


    foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
        my $scheme = $ref_schemes->[$scheme_i-1];
        print $scheme.", " if($DEBUG1);
        print FH "\"".($ref_scheme_name->[$scheme_i-1])."\", ";
        
        foreach my $trace_i (1 .. scalar(@$ref_traces)) {
            my $trace = $ref_traces->[$trace_i-1];
            print $trace.", " if($DEBUG1);
            
            foreach my $ant_i (0 .. 2) {
                ## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
                print FH "".($ref_data->{$trace}{$scheme}{$card_type}{$constraint}{$pred}{$ant_type}->[$ant_i]).", ";
            }
            
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}


sub write_to_file_ant_excell {
    my ($filename, $ref_data, $type, $ref_traces, $ref_schemes, $card_type, $constraint, $ant_type, $ref_scheme_name) = @_;
    

    my $pred = 'False';

    open FH, ">$filename" or die $!;

    print FH ", ";
    foreach my $trace_i (1 .. scalar(@$ref_traces)) {
        foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
            my $scheme = $ref_schemes->[$scheme_i-1];

            print FH "".($ref_scheme_name->[$scheme_i-1]).", ";
        }
    }
    print FH "\n";

    foreach my $ant_i (0 .. 6) {
        print FH "\"".($ant_i + 1)." antenna\", ";
            
        foreach my $trace_i (1 .. scalar(@$ref_traces)) {
            my $trace = $ref_traces->[$trace_i-1];
            print $trace.", " if($DEBUG1);

            foreach my $scheme_i (1 .. scalar(@$ref_schemes)) {
                my $scheme = $ref_schemes->[$scheme_i-1];
                print $scheme.", " if($DEBUG1);
            
                ## data{trace}{scheme}{card_type}{constraint}{prediction}{tx_antenna | rx_antenna | succ | count | mcs}
                print FH "".($ref_data->{$trace}{$scheme}{$card_type}{$constraint}{$pred}{$ant_type}->[$ant_i]).", ";
            }
            
        }
        print "\n" if($DEBUG1);
        print FH "\n";
    }

    close(FH);
}



