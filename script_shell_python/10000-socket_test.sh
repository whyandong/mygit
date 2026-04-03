#! /bin/bash
# can^t update hostname , if you do that , will be err from running  the  server 

#chear history PRO
kill -9 `ps -ef | grep "server.py" | awk '{print $2}'`
kill -9 `ps -ef | grep "client.py" | awk '{print $2}'`
#ERR CATH
check_err(){
	if [ $? != 0 ]
        then
  		echo  option Fail ...
		kill -9 `ps -ef | grep "python3" | awk '{print $2}'`
	      	exit 2	
        else
               echo check option Pass ...
        fi
}
#INSTALL
tar -zxvf ./10000-socket.tar.gz
sleep 1
#RUNING
cd ./10000-socket && ./server.py &
check_err
sleep 2
cd ./10000-socket && python3 ./client.py 127.0.1.1  2>&1 &
check_err
sleep 600
echo  socket_creat loading ..... please waiting for 10 min
# FOR CHECK 10000 PRO
cli=`netstat -anpten | grep 3000 | wc -l` 
if [[ $cli == "2001" ]] ; then
				echo  : conction $cli  CASE PASS
			else
				echo   conction err  CASE Fail 
			fi  

# restore 			
echo restore env  loading ...
kill -9 `ps -ef | grep "python3" | awk '{print $2}'`

echo done !
