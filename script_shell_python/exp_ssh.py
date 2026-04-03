#！/usr/bin/python3 
# -*- coding: utf-8 -*-

import subprocess,sys,os

root_cmd="""cat /boot/config-* | egrep 'CONFIG_ZSWAP|CONFIG_FRONTSWAP'"""

def su_root(root_pwd,rcmd):
    cmd="su -s"
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write(root_pwd.encode('utf-8'))
    p.stdin.write("\n".encode('utf-8'))
    # p.stdin.write(rcmd.encode('utf-8'))
    out,err=p.communicate(rcmd.encode('utf-8'))
    # p.stdin.flush()
    if err == None:
       print(str(out),encoding='utf-8' )
    else:
       print(type(err))

def main():
    if len(sys.argv) != 2:
        print("eg:  python "+os.path.basename(sys.argv[0])+" root_pwd")
        exit(0)
    else:
        rpwd = sys.argv[1]
    su_root(rpwd,root_cmd)

if __name__ == '__main__':
    main()
