sub index2name {
    s/^10/vmover 10/;
    s/^11/vmcfetch 11/;
    s/^12/vmfetch 12/;
    s/^13/vmcstore 13/;
    s/^14/vmstore 14/;
    s/^15/vmand 15/;
    s/^16/vmor 16/;
    s/^17/vmxor 17/;
    s/^18/vmfromr 18/;
    s/^19/vmtor 19/;
    s/^20/vmrfetch 20/;
    s/^21/vmeq 21/;
    s/^22/vmugt 22/;
    s/^23/vmgt 23/;
    s/^24/vmplus 24/;
    s/^25/vmnegate 25/;
    s/^26/vmlshift 26/;
    s/^27/vmrshift 27/;
    s/^28/vmummult 28/;
    s/^29/vmumdiv 29/;
    s/^30/vmdplus 30/;
    s/^31/vmemit 31/;
    s/^32/vmkey 32/;
    s/^33/vmbye 33/;
    s/^34/vmspfetch 34/;
    s/^35/vmspstore 35/;
    s/^36/vmrpfetch 36/;
    s/^37/vmrpstore 37/;
    s/^38/vmopenfile 38/;
    s/^39/vmclosefile 39/;
    s/^40/vmreadline 40/;
    s/^41/vmwriteline 41/;
    s/^42/vmreadfile 42/;
    s/^43/vmwritefile 43/;
    s/^44/vmsystem 44/;
    s/^45/vmreposfile 45/;
    s/^46/vmfilepos 46/;
    s/^47/vmdelfile 47/;
    s/^48/vmfilesize 48/;
    s/^0/vmdolist 0/;
    s/^1/vmnoop 1/;
    s/^2/vmexit 2/;
    s/^3/vmlit 3/;
    s/^4/vmbranch 4/;
    s/^5/vm0branch 5/;
    s/^6/vmdrop 6/;
    s/^7/vmdup 7/;
    s/^8/vmswap 8/;
    s/^9/vmrot 9/;
    return $_;
}

sub sortstat {
    for $i (1..$entries) {
        if ($stat[$i] > $stat[$i - 1]) {
            $t = $stat[$i];
            $stat[$i] = $stat[$i - 1];
            $stat[$i - 1] = $t;
            return 1;
        }
    }
    return 0;
}

$entries = 0;
$total = 0;

while (<>) {
    chomp;
    index2name();
    ($name = $_) =~ s/^(\S+)(\s+)(\S+)(\s+)(\S+)/$1/;
    $index = $3;
    $value = $5;
    $names[$index] = $name;
    $stat[$index] = $value;
    $stat2{$value} = $index;
    $entries++;
    $total += $value;
}

#print "entries $entries\n";

#for $key (sort(keys(%stat2))) {
#    print "$key\n";
#}

while (sortstat()) {}

$sum = 0;

for $i (@stat) {
    $perc = $i / $total;
    $sum += $perc;
    $name = $names[$stat2{$i}];
    printf("%10s %7d %f %f\n", $name, $i, $perc, $sum);
}