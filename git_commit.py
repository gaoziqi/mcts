'''
Created on 2016年12月16日

@author: gzq
'''
import os
import time
import getopt
import sys

# tdq$abc123

if __name__ == '__main__':
    commit = 1
    # 获取输入参数 -c commit
    opts, args = getopt.getopt(sys.argv[1:], "hp", ['help', 'pull'])
    for op, value in opts:
        if op in ("-p", "--pull"):
            commit = 0
        elif op in ("-h", "--help"):
            print('-h     : print this help message and exit (also --help)')
            print('-p     : git pull  (also --pull)')
            sys.exit()
    if commit:
        os.system('git add *')
        os.system('git commit -m \'%s\'' % time.strftime('%Y-%m-%d %X',
                                                         time.localtime()))
        os.system('git push origin master')
        print('提交完成')
    else:
        os.system('git fetch origin master')
        os.system('git merge origin/master')
        print('更新完成')
