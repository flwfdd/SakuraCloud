# API

## 概述

后端使用基于`Python`的轻量级服务模块`Flask`构建。

## 获取目录

列出文件以及文件夹或返回文件信息。

* **请求地址** `/`

* **请求类型** `GET`

* **请求数据**

```json
{
    "cmd":"list", //操作命令
    "path":"./music", //请求目录
    "lim":20, //请求数量
    "off":0, //数量偏移倍率
    "sort":"dir|file_name|time|size_up|down" //排序方式
}
```
其中例如当`off=1`，则从第`21`个文件开始返回。

`sort`中包含三个参数使用下划线隔开。分别是：文件和文件夹哪个在前；依靠什么排序；升序或降序。例如`dir_name_up`表示文件夹在前，依靠名称升序排序。

* **返回数据**

如果是目录
```json
{
    "type":"list", //返回类型
    "path":"music", //当前目录
    "dir_num":233, //目录下文件夹总数
    "file_num":233, //目录下文件总数
    "data":[
        {
            "type":"file|dir", //类型
            "path":"music/horizon.mp3", //路径
            "name":"horizon.mp3", //名称
            "size":233, //大小
            "time":1591197832 //修改时间
        }
    ]
}
```

如果是文件
```json
{
    "type":"file", //返回类型
    "path":"music", //当前目录
    "data":[
        {
            "type":"file", //类型
            "path":"music/horizon.mp3", //路径
            "name":"horizon.mp3", //名称
            "size":233, //大小
            "time":1591197832 //修改时间
        }
    ]
}
```

## 上传文件

文件上传接口。

* **请求地址** `/upload/`

* **请求类型** `POST`

* **请求数据**

使用`form`进行上传。

```json
{
    "path":"music", //上传目录
    "files":[
        //一个或多个文件
    ]
}
```

注意，实际上是以`FormData`为媒介传输的，上面只是直观展示。文件全部以`files`命名，这里的命名是指`form`中的`name`，程序会全部读取出来，并用`filename`即上传文件的实际名称保存到`form`中`path`参数所指示的文件夹中。
