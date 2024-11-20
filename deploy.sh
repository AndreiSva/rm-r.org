#!/bin/sh

python3 build.py
rsync -av --delete ./build/ andrei@rm-r.org:/var/www/rm-r.org/
