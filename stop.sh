ps -ef | grep "c soulbook" | grep -v grep | awk '{print $2}' | xargs kill -9
