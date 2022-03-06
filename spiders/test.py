#-*- coding = utf-8 -*-
#@Time : 2022/2/28 15:15
#@Author : BAYERN
#@File : test.py
#@software: PyCharm

import json
import os


def main():
    with open('./settings/formSetting.json','r',encoding='utf-8') as f:
        d = json.loads(f.read())
    print(os.getcwd())

if __name__ == '__main__':
    main()