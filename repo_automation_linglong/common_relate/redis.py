import redis
r=redis.Redis(host='redis-master.sndu.cn',port=6739)
n=r.lrange('keys',start=0,end=1)
print(n)
