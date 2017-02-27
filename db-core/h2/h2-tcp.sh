#!/bin/sh
dir=$(dirname "$0")
java -Dh2.bindAddress=127.0.0.1 -cp "$dir/h2-1.4.192.jar:$H2DRIVERS:$CLASSPATH" org.h2.tools.Server -baseDir $dir/db -tcp -web -webAllowOthers -tcpAllowOthers -tcpPort 64000