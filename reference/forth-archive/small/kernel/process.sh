#!/bin/bash
sed -e 's/\\ .*//' -e 's/( [^)]*)//g' ../kernel.4|grep -v '^\\G'|grep . >kernel-no-comments.4
#sed -e 's/\\ .*//' -e 's/( [^)]*)//g' ../cross.4|grep -v '^\\G'|grep . >cross-no-comments.4
#cat kernel-no-comments.4 cross-no-comments.4|sed -e 's/ /\n/g'|grep .|sort|uniq -c|sort -n >cross-kernel-words
cat kernel-no-comments.4|sed -e 's/ /\n/g'|grep .|sort|uniq -c|sort -n >kernel-words

