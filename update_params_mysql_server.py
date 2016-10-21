''' Check and update parameters for MySQL server

    Author: Artem Rybin
    Usage: update_params_mysql_server.py -f <inputfile> -p <period(sec)>
'''

import getopt, sys, os
import time 
import subprocess

user = 'root'
password = '775ft'

def main():
    print('Start')
    while True:
        # parsing args
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'f:p:', ['file=','period='])
        except getopt.GetoptError as err:
            print(err)
            sys.exit(2)

        filename = None
        period = None

        for option, arg in opts:
            if option in ('-f', '--file'):
                filename = arg
            elif option in ('-p', '--period'):
                period = float(arg)
            else:
                assert False, 'No option'

        # get parameters from inputfile
        params = get_params_from_file(filename)

        # get current parameters from mysql
        cur_params = get_current_params(params.keys());

        # set new params
        set_params(params)

        # check new params
        cur_params = get_current_params(params.keys());

        time.sleep(period)

def get_params_from_file(fname):
    file = open(fname)
    data = file.read()
    lines = data.splitlines()
    file.close()
    
    parameters = {}
    for line in lines:
        key, value = line.split('|', 1 )
        parameters[key] = value

    print(parameters)
    return parameters

def get_current_params(keys):
    cur_params = {}
    for key in keys:
        select_str = 'SELECT @@%s'%key + ';'
        cmd = ['mysql', '-u', user, '-p%s'%password, '-Bse', select_str]
        proc = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        value = proc.communicate()[0]
        cur_params[key] = value.rstrip('\n')
    print(cur_params)
    return cur_params

def set_params(params):
    keys = params.keys()
    for key in keys:
        set_str = 'SET GLOBAL %s=%s'%(key, params[key])  + ';'
        cmd = ['mysql', '-u', user, '-p%s'%password, '-Bse', set_str]
        proc = subprocess.Popen(cmd, stdout = subprocess.PIPE)

if __name__ == '__main__':
    main()