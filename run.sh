#!/bin/sh

suffix=`date +%Y%m%d%H%M%S`

cfg="./rebang.conf"
res="./result/"
workdir="$res/workdir/"


python spider_by_rule.py $cfg $res/rebang.data $workdir 1>/dev/null 2>/dev/null

