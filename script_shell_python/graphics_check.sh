#! /bin/bash


list=(520 430 230M HD8550M 540X)


check_drive_KP(){
graphics_id=`lspci -nnn | grep Audio | awk '{print $20}' | awk -F ':' '{print $2}'` 
graphics_name=`lspci -nnn | grep VGA | awk '{print $17}'`
driver=`lshw -c video | grep driver | awk '{print $2}' | awk -F '=' '{print $2}'`
echo 当前显卡版本: ${graphics_name%%/*}
echo 显卡ID: ${graphics_id%?}
sleep 1 

        for data in ${list[@]}
            do
                #echo $data
                if [[ ${graphics_name%%/*} == $data ]] ; then
                        #echo graphics not in write list
                        #exit 2
                        if [ $driver == "amdgpu"  ] ; then
                                echo driver:amdgpu : CASE PASS
                        else
                                echo  please check $data config : CASE FAIL
                        fi
                fi
        done
}

check_drive_FT(){
graphics_id=`lspci -nnn | grep Audio | awk '{print $18}' | awk -F ':' '{print $2}'` 
graphics_name=`lspci -nnn | grep VGA | awk '{print $24}'`
driver=`lshw -c video | grep driver | awk '{print $2}' | awk -F '=' '{print $2}'`
echo 当前显卡版本: $graphics_name 
echo 显卡ID: ${graphics_id%?}
sleep 1 

	for data in ${list[@]}
            do
		#echo $data
		if [[ $graphics_name == $data ]] ; then
			#echo graphics not in write list
			#exit 2
			if [ $driver == "amdgpu"  ] ; then
				echo driver:amdgpu : CASE PASS
			else
				echo  please check $data config : CASE FAIL
			fi
		fi
	done	
}

check_result(){
	if [ $? != 0 ] ; then
		echo "canot find Model size"
		echo "just for ARM "
		exit 2	
	fi
}

model_size=`lscpu | grep "Model name:" | awk '{print $3}' | awk -F '-' '{print $1}'`
check_result

model_size1=`lscpu | grep "Model name:" | awk '{print $3}'`
check_result
if [ $model_size == "FT"  ] ; then
	 check_drive_FT
fi

if [[ $model_size1 == "HUAWEI" ]] ; then 
	 check_drive_KP
else
echo just for ARM 
fi
