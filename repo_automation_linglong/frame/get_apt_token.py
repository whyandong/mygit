import random
def get_apt_token(version,machine_id):

    v = "20." + str(version) + ".11018.101;"

    token = "a=UnionTech OS Desktop;b=Desktop;c=Professional;" +  "v=" + v + "i=" + machine_id + ";" + "m=Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz;ac=amd64;cu=0;sn="

    return token

