#!/bin/sh
#set -x

if [ "$4" == "" ]
then
	tmux send-keys -t $1:$2 "$3" C-m
else
	tmux send-keys -t $1:$2 "$3"  " " "$4" C-m
fi
