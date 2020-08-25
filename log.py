# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:04:20 2020

@author: juzix
"""

import os
import subprocess


#进入节点私钥所存放的目录：
os.chdir(os.path.abspath(os.path.expanduser('~')))
os.chdir('tianziliangNode') 

#登录节点：
subprocess.run('cat loginNode.sh', shell=True) 
subprocess.run('./loginNode.sh', shell=True) 

#subprocess.run(['ls','-ltr'])

#查看日志：
os.chdir('platon-node')
os.chdir('data')
subprocess.run('less platon.log', shell=True)

#subprocess.run(['ls','-ltr'])


