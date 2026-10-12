$max = 0;
while (<>) {
    chomp;
    $words{$_}++;
    $max = $words{$_} if $words{$_} > $max;
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