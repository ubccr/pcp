#!/bin/csh

@ numt = 4
@ numrun = 0

foreach dir (`/bin/ls -d c560*`)
    echo $dir
    foreach file (`/bin/ls $dir`)
        #echo $dir/$file
        set cmd = "../taccstats2pcp.py -d $dir $dir/$file"
        echo $cmd
        $cmd &
        set numrun = (`pgrep -P $$`)
        while ($#numrun >= $numt )
            sleep 1
            set numrun = (`pgrep -P $$`)
        end
    end
end

wait
