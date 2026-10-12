$elapsed = time();
system "@ARGV";
$elapsed = time() - $elapsed;

print "\n$elapsed seconds\n";
