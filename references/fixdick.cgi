#!/usr/bin/perl

#read bible
open (DATA, "<dick.txt") or die("Word file $bible_file does not exist");
@lines = <DATA>;
close (DATA);

$text = join('' , @lines);
$text =~ s/\n/ /g; #replace line returns with spaces
$text =~ s/\"/ /g; #replace " with spaces
$text =~ s/\s{2,}/ /g; #remove double spaces

@lines = split /\./g , $text;

open (DATA, ">moby.txt");
foreach $item (@lines)
         {
         print DATA "$item.\n";
         }
close (DATA);

