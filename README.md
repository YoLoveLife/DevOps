## devEops
devEops通过封装Ansible api来处理实际业务运行可能遇到的安装部署运维工作

## Getting started
devEops是一个django项目，依赖于

* gradle
* Python2.7+
* Ansible2.2+
* HTTP文件服务器环境
* 基础YUM源

## Log
### 2017-3-28
#### Info
  完成了除了Nginx之外的所有应用批量部署的功能。针对重新采用的动态主机列表，将底端的封装api重新修改，去除所有的server字段。
#### For
* 重新思考页面的业务解决方式(目前倾向于部署只部署应用 通过初始化来配置以及启动关闭)
* 在页面尝试配置修改并且批量推送的功能
* 数据库添加历史记录表 规划dashboard的组织方法