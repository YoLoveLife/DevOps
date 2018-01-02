## 项目结构

说明如下：

```
.
├── config-example.py                    // 配置文件样例
├── docs                                 // 所有doc文件放到该目录
│   └── README.md                        // 文档目录
├── LICENSE
├── README.md
├── logs                                 // 编码日程日志
├── apps                                 // 模块目录
│   └── application                      // 应用管理模块目录
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── api.py                       // api请求
│   │   ├── models.py                    // 应用模型 存储所有应用的资产信息
│   │   ├── templates                    // app下模板目录
│   │   │   ├── application              // 资源引用区分
│   │   │   │   └── db
│   │   │   │       └── detail_db.html   // 数据库细节模板
│   │   │   └── batch                    // 批量操作模板
│   │   ├── tests.py                     // 模块及API请求测试
│   │   ├── urls                         // URL请求
│   │   │   ├── api_urls.py              // API请求URL
│   │   │   └── views_urls.py            // 视图请求URL
│   │   ├── utils
│   │   │   ├── constant.py              // Bash代码格式维护
│   │   │   └── utils.py                 // Bash数据库到文本转化
│   │   ├── views                        // 视图请求区分
│   │   │   └── db.py                    // 关于数据库的视图请求
{#│   ├── common#}
{#│   │   ├── templatetags                 // 通用template tag#}
{#│   │   ├── utils.py                     // 通用的函数方法#}
{#│   │   └── views.py#}
{#│   ├── fixtures                         // 初始化数据目录#}
{#│   │   ├── init.json                    // 初始化项目数据库#}
{#│   │   └── fake.json                    // 生成大量测试数据#}
{#│   ├── jumpserver                       // 项目设置目录#}
{#│   │    ├── __init__.py#}
{#│   │    ├── settings.py                 // 项目设置文件#}
{#│   │    ├── urls.py                     // 项目入口urlconf#}
{#│   │    └── wsgi.py#}
{#│   ├── manage.py#}
{#│   ├── static                           // 项目静态资源目录#}
{#│   ├── static                           // 项目多语言目录#}
{#│   └── templates                        // 项目模板目录#}
```