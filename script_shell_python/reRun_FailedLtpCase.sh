#! /bin/bash
#获取fail项的case进行 重新测试覆盖
cat $1 | grep FAIL  > ./failed.log 
#遍历failed的case项,并获取其case名 
for fail in `cat ./failed.log | awk '{print $1}'` 
    do 
        #echo $fail
        #遍历进行case执行
        for data in ${fail[@]}
            do
            #echo ${data}  >  ./retest.log
            caseName=`ls -al /opt/ltp/testcases/bin/ | grep ${data} | awk '{print $9}'`
            caseSize=`file /opt/ltp/testcases/bin/$caseName | awk '{print $2}'`   
            echo $b
            #判断case路径下case是否存在
            if [ ! -f /opt/ltp/testcases/bin/${data} ]; then                    
                echo "${data} case not found !!!! " >>  ./retest.log
                   else         
                    if [ "$caseSize" == "ELF" ];then
                        echo $caseName
                        echo $caseSize        
                       /opt/ltp/testcases/bin/$caseName >>  ./retest.log                   
                        else                  
                      ./opt/ltp/testcases/bin/$caseName >>  ./retest.log
                    fi
            fi 
        done
               # rm -rf ./failed.log
done 
