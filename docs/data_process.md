# 数据处理模块

<p style="text-indent: 2em;">数据处理模块，主要完成对Dockerfile文件中的每个阶段的识别，并且为每个阶段生成一个InstructMeta列表，一个InstructMeta列表包含很多个InstructMeta结构，例如RUN指令的InstructMeta，COPY指令的InstructMeta等等。</p>

## 概述

<p style="text-indent: 2em;">数据处理模块首先会按照FROM指令进行阶段拆分，并检查每一个阶段指令名等信息是否合法，对于不合法的Dockerfile返回其错误信息。</p>
<p style="text-indent: 2em;">数据处理借助了dockerfile库，并且实现了一套指令预处理逻辑，用于解析每一个指令行，并生成对应的指令特征结构。</p>

## InstructMeta结构

InstructMeta结构消除了指令语法的差异，提供了统一的表征形式，方便后续依赖关系判断。

```
{
    "InstructName": "",  # 指令名
    "Operand": {}, # 操作数
    "ArgList": [], # 变量列表
    "AttributeUser": "", # 所属用户
    "AttributeDir": "", # 所属目录
    "Eigenvector": "None" # 特征向量信息
}
```

### Operand概述

|             | flag  |                subcmd                 | value |       type       |
|:-----------:|:-----:|:-------------------------------------:|:-----:|:----------------:|
|     ADD     | Tuple |                 None                  | dict  |     default      |
|     ARG     | Tuple |                 None                  | dict  |     default      |
|    COPY     | Tuple |                 None                  | dict  | default or from  |
|    SHELL    | Tuple |                 None                  | Tuple | default or shell |
|     ENV     | Tuple |                 None                  | dict  |     default      |
| HEALTHCHECK | Tuple |                  str                  | Tuple |     default      |
|     RUN     | Tuple | NoneType(shell 格式) or str(default 格式) |  str  | default or shell |
|    OTHER    | Tuple |                 None                  | Tuple |     default      |

<p style="text-indent: 2em;">OTHER表示不属于以上指令的指令，例如LABEL指令。</p>

```
flag 表示指令的参数，以--开头的部分
    例如 
    COPY --chown=10:11 --from=base /app/deployer /usr/local/bin/deployer，其中--chown和--from是指令的参数
    FROM --platform=linux/amd64 adoptopenjdk:12-jre-hotspot，其中--platform是指令的参数

    注意如下情况中的--update，--no-cache不属于指令的参数，这是shell命令Flag选项
    RUN apk --update --no-cache add curl tini libcap

subcmd表示指令的子指令，仅HEALTHCHECK指令存在子指令，之前设计时考虑使用子指令的特征表示HEALTHCHECK指令的特征，但是后来发现HEALTHCHECK指令是顺序无关指令(可见dependency模块)，故subcmd字段没有实质性作用。
    例如，其中CMD是子指令
    HEALTHCHECK --interval=120s --timeout=15s --start-period=120s --retries=2 \
                CMD wget --no-check-certificate -e use_proxy=yes -e https_proxy=127.0.0.1:8118 --quiet --spider 'https://3g2upl4pq6kufc4m.onion' && echo "HealthCheck succeeded..." || exit 1

value表示指令的值
   除了指令名和指令参数外的剩余部分均保留在value字段中，不过值得注意的是，这里针对每个指令进行了预处理，消除了格式的差异。
   字典类型有两类，其中ADD和COPY指令有src_dir和dest_dir两个属性，分别表示源文件或目录和目标文件或目录，而ENV和ARG指令中键为参数名值为参数值，通常这两类需要分开考虑。
   RUN指令为字符串形式，存储的是shell命令。

type表示指令的类型
    对于SHELL指令在前，RUN指令在后的情况，如果SEHLL指令类型为shell，不管RUN指令类型是什么，两者都存在依赖关系。
    COPY指令为from时，用于多阶段构建，可用于判断不同阶段之间是否存在依赖关系。
```

### ArgList概述

<p style="text-indent: 2em;">例如RUN tar xvf "${QEMU_TARBALL}"中的${QEMU_TARBALL}就是一个使用的参数，其中QEMU_TARBALL会加入ArgList中，用于判断与ENV或ARG指令的依赖关系。ARG和ENV指令会加入ArgList中。</p>

### AttributeUser和AttributeDir概述

<p style="text-indent: 2em;">默认用户为root，默认目录为/。当使用USER和WORKDIR指令时，则所属用户和所属目录会改变。</p>

### Eigenvector概述

<p style="text-indent: 2em;">其中只有ADD，COPY，RUN指令含有特征向量信息。</p>

<p style="text-indent: 2em;">ADD和COPY指令的特征向量为输入输出目录树结构，而RUN指令的特征向量为经过ast分析和extractor模块后得到的指令特征结构(InstructFeature)。</p>

### 示例

FROM指令示例

```
{
    "Original": "FROM alpine:3.8",
    "Meta": {
        "InstructName": "FROM",
        "Operand": {
            "flags": [],
            "subcmd": "None",
            "value": [
                "alpine:3.8"
            ],
            "type": "default"
        },
        "ArgList": [],
        "AttributeUser": "root",
        "AttributeDir": "/",
        "Eigenvector": "None"
    }
}
```

COPY指令示例

```
{
    "Original": "COPY requirements.txt .",
    "Meta": {
        "InstructName": "COPY",
        "Operand": {
            "flags": [],
            "subcmd": "None",
            "value": {
                "src_dir": [
                    "requirements.txt"
                ],
                "dst_dir": "."
            },
            "type": "default"
        },
        "ArgList": [],
        "AttributeUser": "root",
        "AttributeDir": "/app",
        "Eigenvector": "{'/': {'app': {}}}"
    }
}
```

RUN指令示例

```
{
    "Original": "RUN apt install wget",
    "Meta": {
        "InstructName": "RUN",
        "Operand": {
            "flags": [],
            "subcmd": "None",
            "value": "apt install wget",
            "type": "shell"
        },
        "ArgList": [],
        "AttributeUser": "root",
        "AttributeDir": "/",
        "Eigenvector": {
            "CommandSet": [
                "apt"
            ],
            "PkgSet": [
                "wget"
            ],
            "OtherSet": [],
            "UserSet": [],
            "VarPSet": [],
            "VarCSet": [],
            "InputTree": "{'/': {'etc': {}}}",
            "OutputTree": "{'/': {'etc': {}}}"
        }
    }
}
```

## 命令行的使用

```bash
graphgen meta -f ./data/meta/Dockerfile
```
