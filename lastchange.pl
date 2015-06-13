#!/usr/bin/perl -w
#
# Print the files (recursively) modified in the
# last <age> days.
#
# Syntax: lastchange <age in days> <list of files to check>
# <age in days> can have fractional parts
#
# by guisf on 2007-10-10

$time = shift(@ARGV);
$total = 0;

if(@ARGV < 1 || $time !~ /\d+/) { 
    $msg = "Show the files modified in the last <age> days. Recursively.\n";
    $msg.= "Usage: lastchange <age in days> <list of files or directories>\n";
    die($msg); 
}

for($i = 0; $i < @ARGV; $i++) {
    $ARGV[$i] =~ s/\/$//;
}

print "Files modified in the last $time days: \n\n";
&CheckOut('.', @ARGV);
print "\nTotal files: $total\n";


sub CheckOut {
   my($DirPath,@FileList,$NewDirPath,@NewFileList);
   $DirPath = shift;
   @FileList = @_;
   foreach $filename (@FileList) { 
      if(-f $filename && ($x = -M $filename) <= $time) {
         $x = sprintf("%.5f", $x);
         print "$DirPath/$filename .......... $x days\n";
         $total++;
      } elsif(-d $filename && !-l $filename && $filename !~ /^\.+?/) {
         $filename =~ s/\/^//;
         $NewDirPath = $DirPath . '/' . $filename;
         if (opendir(DIRHANDLE,$filename)) {
            @NewFileList = readdir(DIRHANDLE);
            closedir DIRHANDLE;
            if(chdir $filename) {
               &CheckOut($NewDirPath,@NewFileList);
            } else {
               print "\t(Can not go into $NewDirPath)\n";
            }
         } else {
            print "\t(Can not open $NewDirPath)\n";
         }
      }
   }
   chdir '..';
}
