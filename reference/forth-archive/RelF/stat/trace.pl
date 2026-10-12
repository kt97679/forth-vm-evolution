$max = 0;
while (<>) {
    chomp;
    ($count = $_) =~ s/^\s*(S+).*/$1/;
    $code{$count} = $_;
    $max = $count if $count > $max;
}

while ($max > 0) {
    $nextmax = 0;
    for $count (keys(%code)) {
        if ($count > $nextmax and $count < $max) {
            $nextmax = $count;
        }
        if ($count == $max) {
            print "$code{$count}\n";
        }
    }
    $max = $nextmax;
}