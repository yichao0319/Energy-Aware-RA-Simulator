#!/bin/perl 

use strict;


#####
## constant
my $DEBUG0 = 1;
my $DEBUG1 = 1;


#####
## global variables
my $input_dir = "./";
my $output_dir = "./";
my @files = ("txinteldata.dat", "txatherosdata.dat", "rxinteldata.dat", "rxatherosdata.dat", "phone_data.dat");


#####
## main
foreach my $file (@files) {
    print $file."\n" if($DEBUG1);
    open FH, "<$input_dir/$file";


    ## $set{1 | 2 | ... | 6}{@data}
    my %groups = ();
    # foreach my $grp_i (1 .. 6) {
    #     my @values = ();
    #     $groups{$grp_i} = @values;
    # }


    my $set_cnt = 0;
    my $point_cnt = 0;
    my ($last1, $last2);
    while(<FH>) {
        if($_ =~ /(\d+\.*\d*)\s(\d+\.*\d*)/) {
            $set_cnt ++ if($point_cnt == 0);
            $point_cnt ++;
            die "wrong number of points" if($point_cnt > 6);

            push(@{$groups{$point_cnt}}, $1);
            push(@{$groups{$point_cnt}}, $2);
            ($last1, $last2) = ($1, $2);
        }
        else {
            while($point_cnt != 0 && $point_cnt < 6) {
                $point_cnt ++;

                push(@{$groups{$point_cnt}}, $last1);
                push(@{$groups{$point_cnt}}, $last2);
            }
            print "$_ set $set_cnt has $point_cnt points\n" if($DEBUG0);
            $point_cnt = 0;
        }
    }
    close(FH);


    #####
    ## print out
    open FH_OUT, ">$output_dir/$file.out" or die $!;
    foreach my $grp_i (1 .. 6) {
        print FH_OUT join(", ", @{$groups{$grp_i}})."\n";
    }
    close FH_OUT;


    print $set_cnt."\n";
}