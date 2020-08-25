# 区块链日志小工具的使用手册

## 基本功能

该工具根据区块链日志的内容获取并显示当前Platon链上的各类信息， 信息包括：      

1. epoch   
2. round  
3. view   
4. block，包括finished，locked，prepare（以块高的形式呈现）   
5. 当前25个验证节点（以nodeID的形式呈现）     

******

## 运行方法

1. 修改工具py文件中的相关目录的代码（共4处，2处为节点日志所在目录，2处为该小工具py文件所在目录）   
2. 在linux环境下（例如ubuntu）进入该工具文件所在路径（例如输入命令cd /mnt/d/python)之后，输入命令python3 dynamic.py即可运行

******

## 使用说明

1. 需要在linux环境下启动图形化界面，因此需要安装并运行插件Xming    
   Xming下载地址: https://sourceforge.net/projects/xming/     
   安装时一定要勾选No Access Control的选项！         
2. 运行该工具前务必保证已经成功连接您的节点

******

## 界面介绍

![image-20200804170217905](C:\Users\juzix\AppData\Roaming\Typora\typora-user-images\image-20200804170217905.png)

* 第一行显示当前epoch数据（为1~10750之间的数值）  
* 第二行显示当前round数据（为1~250之间的数值）       
* 第三行显示当前view数据（为0~24之间的数值）      
* 第四至六行显示当前的block数据，从上往下依次为finished，locked，prepare     
* 之后的25行显示当前的25个验证节点的nodeID，并按照index的顺序排序     

******

## 常见问题说明   

1. 无法显示图形化界面    
   A：检查是否启动了插件Xming，启动后重启ubuntu即可开启界面    
2. 界面中的数值不会变化    
   A：检查是否成功启动了节点，查看节点日志是否能正常读取    

******

