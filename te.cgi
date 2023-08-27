#!/usr/bin/perl

&main;                          
exit;   # There are only two exit calls in the script, here and in in &cgierr.

sub main
{
my $todaysdate = &unix_to_date(time);

$referencepath = 'references/kjv.txt';

#read bible
open (DATA, "<$referencepath") or die("Reference file $reference does not exist");
@lines = <DATA>;
close (DATA);

$templatepath = shift(@lines); #first line of text is the path to the template!

#open template file
open (DATA, "<$templatepath") or die("Template file $template does not exist");
@template = <DATA>;
close (DATA);
$template = join('' , @template);

#create field data
$line = shift(@lines);
$line =~ s/\n//g; #remove line return
@fields = split /\|/ , $line;
$count = 0;
foreach $item (@fields)
         {
         $fields{$item} = $count;  #will return the column data eg: $fields[$fields{Verse}]
         $count ++;
         }

$number_of_lines = scalar(@lines) - 1; # number of lines

#days since epoch
$today = time();
$days = int($today/60/60/24);

#days since epoch selects which line is read
srand($days); 
$todays_line = int(rand($number_of_lines));

#$line = $lines[$remainder];
$line = $lines[$todays_line];
$line =~ s/\n//g; #remove line return

@line = split(/\|/,$line);
$book = $line[$fields{Book}];
$chapter = $line[$fields{Chapter}];
$verse = $line[$fields{Verse}];
$sentence = $line[$fields{Sentence}];
$s = substr $sentence , 0 , 1;
$entence = substr $sentence , 1;

if ($remainder > 0)
    {
    $linebefore = $lines[$remainder - 1];
    $linebefore =~ s/\n//g; #remove line return

    @linebefore = split(/\|/,$linebefore);
    $bookbefore = $linebefore[$fields{Book}];
    $chapterbefore = $linebefore[$fields{Chapter}];
    $versebefore = $linebefore[$fields{Verse}];
    $sentencebefore = $linebefore[$fields{Sentence}];
    $sbefore = substr $sentencebefore , 0 , 1;
    $entencebefore = substr $sentencebefore , 1;
    }

if ($remainder < $lines)
    {
    $lineafter = $lines[$remainder + 1];
    $lineafter =~ s/\n//g; #remove line return

    @lineafter = split(/\|/,$lineafter);
    $bookafter = $lineafter[$fields{Book}];
    $chapterafter = $lineafter[$fields{Chapter}];
    $verseafter = $lineafter[$fields{Verse}];
    $sentenceafter = $lineafter[$fields{Sentence}];
    $safter = substr $sentenceafter , 0 , 1;
    $entenceafter = substr $sentenceafter , 1;
    }

#get chapter
@chapter = grep
 {eval
  {
  $line = $_;
  $line =~ s/\n//g; #remove line return
  @line = split(/\|/,$line);
  $booktemp = $line[$fields{Book}];
  $chaptertemp = $line[$fields{Chapter}];
  #$versetemp = $line[$fields{Verse}];
  #$sentencetemp = $line[$fields{Sentence}];
  if ( ($book eq $booktemp) and ($chapter == $chaptertemp) ) {return(True)}
  }
 }  @lines;

#format chapter
$wholechapter = '';
$template =~ m/\<lineformat\>([\s\S]+)\<\/lineformat\>/; #find lineformat in template
$lineformat = $1;
foreach $item (@chapter)
         {
         $lineformattemp = $lineformat;
         $item =~ s/\n//g; #remove line return
         @line = split(/\|/,$item);
         $booktemp = $line[$fields{Book}];
         $chaptertemp = $line[$fields{Chapter}];
         $versetemp = $line[$fields{Verse}];
         $sentencetemp = $line[$fields{Sentence}];
         $stemp = substr $sentencetemp , 0 , 1;
         $entencetemp = substr $sentencetemp , 1;

         $lineformattemp =~ s/<\%book\%>/$booktemp/g;
         $lineformattemp =~ s/<\%chapter\%>/$chaptertemp/g;
         $lineformattemp =~ s/<\%verse\%>/$versetemp/g;
         $lineformattemp =~ s/<\%sentence\%>/$sentencetemp/g;
         $lineformattemp =~ s/<\%s\%>/$stemp/g;
         $lineformattemp =~ s/<\%entence\%>/$entencetemp/g;
         $lineformattemp =~ s/<\%todaysdate\%>/$todaysdate/g;

         $wholechapter = "$wholechapter$lineformattemp";
         }

#replace tokens in template
$template =~ s/\<lineformat\>([\s\S]+)\<\/lineformat\>/$wholechapter/g; #first seek the lineformat tag and replace it with the formatted chapter

$template =~ s/<\%book\%>/$book/g;
$template =~ s/<\%chapter\%>/$chapter/g;
$template =~ s/<\%verse\%>/$verse/g;
$template =~ s/<\%sentence\%>/$sentence/g;
$template =~ s/<\%s\%>/$s/g;
$template =~ s/<\%entence\%>/$entence/g;
$template =~ s/<\%todaysdate\%>/$todaysdate/g;

$template =~ s/<\%bookbefore\%>/$bookbefore/g;
$template =~ s/<\%chapterbefore\%>/$chapterbefore/g;
$template =~ s/<\%versebefore\%>/$versebefore/g;
$template =~ s/<\%sentencebefore\%>/$sentencebefore/g;
$template =~ s/<\%sbefore\%>/$sbefore/g;
$template =~ s/<\%entencebefore\%>/$entencebefore/g;

$template =~ s/<\%bookafter\%>/$bookafter/g;
$template =~ s/<\%chapterafter\%>/$chapterafter/g;
$template =~ s/<\%verseafter\%>/$verseafter/g;
$template =~ s/<\%sentenceafter\%>/$sentenceafter/g;
$template =~ s/<\%safter\%>/$safter/g;
$template =~ s/<\%entenceafter\%>/$entenceafter/g;

print "Content-type:text/html\n\n";

print $template;

print "\n";
};

# Date Routines
# --------------------------------------------------------
# Your date format can be whatever you like, as long as the following
# two functions are defined &date_to_unix and &unix_to_date:
# The default is dd-mmm-yyyy.

sub date_to_unix {
# --------------------------------------------------------
# This routine must take your date format and return the time a la UNIX time().
# Some things to be careful about..
#     timelocal does not like to be in array context, don't do my($time) = timelocal (..)
#     int your values just in case to remove spaces, etc.
#     catch the fatal error timelocal will generate if you have a bad date..
#     don't forget that the month is indexed from 0!
#
    my $date = shift; my $i;
    my %months = map { $_ => $i++ } qw!Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec!;
    my ($day, $mon, $year) = split(/-/, $date);

    exists $months{$mon} or return undef;

    $day = int($day);

    #$year = $year - 1900; #fix less than 1960 bug

    require Time::Local;
    my $time = 0;
    eval {
        $time = &Time::Local::timelocal(0,0,0, $day, $months{$mon}, $year);
    };
    #if ($@) { die "invalid date format: $date - parsed as (day: $day, month: $months{$mon}, year: $year). Reason: $@";  }
    if ($@) { die "Dates from 1902 to 2038 please.";  }
    return $time;
}

sub unix_to_date {
# --------------------------------------------------------
# This routine must take a unix time and return your date format
# A much simpler routine, just make sure your format isn't so complex that
# you can't get it back into unix time.
#
    my $time   = shift;
    my ($sec, $min, $hour, $day, $mon, $year, $dweek, $dyear, $tz) = localtime $time;
    my @months = qw!Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec!;
    $year      = $year + 1900;
    return "$day-$months[$mon]-$year";
}

sub long_date {
# --------------------------------------------------------
# This routine is for printing a nicer date format on the what's new page. It should
# take in a date in your current format and return a new one.
    my $time   = shift;
    $time      = &date_to_unix($time);
    my ($sec, $min, $hour, $day, $mon, $year, $dweek, $dyear, $tz) = localtime $time;
    my @months = qw!January February March April May June July August September October November December!;
    my @days   = qw!Sunday Monday Tuesday Wednesday Thursday Friday Saturday!;
    $year      = $year + 1900;
    return "$days[$dweek], $months[$mon] $day $year";
}
