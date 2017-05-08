#!/bin/bash
function update_jekyll {
    rm -f /home/jekyll/do_update
    cd jekyll_git/jekyll/blog/
    git pull origin master
    bundle install
    jekyll build --destination /home/jekyll/thoughtvectors
    cd ../../../
}

while [ 1 ]
do
    while [ ! -f /home/jekyll/do_update ]
    do
	sleep 10;
	test $? -gt 128 && break
    done
    update_jekyll
done
ls -l /tmp/list.txt
