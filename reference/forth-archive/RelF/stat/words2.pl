$max = 0;
$prev = <>;
chomp $prev;
while (<>) {
    chomp;
    $pair = "$prev $_";
    $prev = $_;
    $words{$pair}++;
    $max = $words{$pair} if $words{$pair} > $max;
}

while ($max > 0) {
    $nextmax = 0;
    for (keys(%words)) {
        $count = $words{$_};
        if ($count > $nextmax and $count < $max) {
            $nextmax = $count;
        }
        if ($count == $max) {
            print "$count $_\n";
        }
    }
    $max = $nextmax;
}