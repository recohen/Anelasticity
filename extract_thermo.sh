#! /bin/sh

cat $1 | sed -n "/Step/,/Loop time/p" | head -n-1 > $2
sed -i "1s/^/#/" $2
