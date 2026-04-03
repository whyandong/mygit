import redis
import re,json
# 链接redis根据machineid查询仓库日志
def get_redis(device_id):
    ip = "10.0.33.45"
    password = "wlso20211116"
    r1 = redis.Redis(host=ip, password=password, port=35013, db=9)
    terminal_str = "terminal:" + device_id
    terminal_log = r1.get(terminal_str)
    terminal_log_json = json.loads(terminal_log)
    terminal_log_str = json.dumps(terminal_log_json)

    repository_all = re.search('repositoryId":.(.*?),', terminal_log_str)
    repository = int(repository_all.group(1))

    #print(repository)
    task_all = re.search('taskId":.(.*?),', terminal_log_str)

    task_id = int(task_all.group(1))
    #print(task_id)
    return repository,task_id