#!/bin/bash
function update_jekyll {
    rm -f /home/jekyll/do_update
    cd jekyll_git
    git pull origin master
    jekyll build --destination /home/jekyll/thoughtvectors
    cd ..
}

while 1
do
    while [ ! -f /home/jekyll/do_update ]
    do
	sleep 10
    done
    update_jekyll()
done
ls -l /tmp/list.txt