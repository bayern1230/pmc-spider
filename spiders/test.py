#-*- coding = utf-8 -*-
#@Time : 2022/2/28 15:15
#@Author : BAYERN
#@File : test.py
#@software: PyCharm

import json
import os
import pymysql


def main():
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123456',
                         port=3306,
                         db='Spider'
                         )

    cursor = db.cursor()

    table = 'TextInfoTable'

    # 查询数据
    cursor.execute('''select title from {table}'''.format(table=table))
    results = cursor.fetchall()
    for i in range(len(results)):
        print("%s:%s"%(i+1,results[i][0]))
    db.close()



if __name__ == '__main__':
    main()