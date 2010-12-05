#!/bin/ksh
#
# This will serve tictactroll endlessly for development purpose.
#

BASE=virtualenv
PASTER=$BASE/bin/paster

. $BASE/bin/activate

while :; do
	paster serve --reload development.ini $*;
	# --log-file test.log;
	# python -m cProfile $PASTER serve --reload development.ini;
	echo -n "--- Server has died, press enter to restart ---"
	if ! read X; then
		exit
	fi
done
