 #-*- coding:utf-8 -*-

import time
import os
STOR_PATH = "/home/backups/"
WEB_PATH = '/home/wwwroot/'
CONF_PATH = '/usr/local/nginx/conf/'
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PWD = ''
DB_NAME = 'wordpress'
DATETIME = time.strftime('%Y-%m-%d%H_%M_%S')
TMP_BKP_PATH = STOR_PATH + DATETIME

def init():
    global TMP_BKP_PATH
    if not os.path.exists(STOR_PATH):
        print('备份目录:'+STOR_PATH+' 不存在，建立中...')
        os.mkdir(STOR_PATH)
    if not os.path.exists(TMP_BKP_PATH):
        print('备份目录:'+TMP_BKP_PATH+' 不存在，建立中...')
        os.mkdir(TMP_BKP_PATH)
    print('初始化完成，备份文件会被存储到目录: '+TMP_BKP_PATH+'中。')

def mysql():
    global DB_NAME,TMP_BKP_PATH,SQL_USER,SQL_PWD
    print('开始从MySQL/MariaDB中备份数据库...')
    DB = DB_NAME
    dump_command = "mysqldump -u " + SQL_USER + ' -p' + SQL_PWD + ' ' + DB + '>' + TMP_BKP_PATH + '/' + DB +'.sql'
    os.system(dump_command)
    print('数据库 '+DB+' 备份完成')

def site():
    global CONF_PATH,TMP_BKP_PATH,WEB_PATH
    print('开始备份nginx配置和站点文件...')
    cd_cmd = "cd" + TMP_BKP_PATH
    os.system(cd_cmd)
    website_cmd = "zip -r " + TMP_BKP_PATH + '/nginx-www.zip ' + WEB_PATH
    os.system(website_cmd)
    conf_cmd = "zip -r " + TMP_BKP_PATH + '/nginx-conf.zip ' + CONF_PATH
    os.system(conf_cmd)
    print('站点根目录与nginx配置文件备份完成。')

def comupload():
    global TMP_BKP_PATH,DATETIME,STOR_PATH
    compress_cmd = 'zip -r ' + STOR_PATH + DATETIME + '.zip ' + TMP_BKP_PATH
    os.system(compress_cmd)
    print('打包完成，开始上传至百度网盘...')
    upload_cmd = 'bypy -v upload '+ STOR_PATH + DATETIME + '.zip ' + '/站点备份/'
    os.system(upload_cmd)
    print('备份完成，程序将会自动退出...')
if __name__ == '__main__':
    init()
    mysql()
    site()
    comupload()
