# extractor模块

<p style="text-indent: 2em;">extractor模块对初始指令特征结构的命令集合中的每一条命令进行特征提取得到命令特征结构(CommandFeature)。</p>

<p style="text-indent: 2em;">一条RUN指令最终会得到一个指令特征结构(InstructFeature)。其是由初始指令特征结构(InstructFeatureInit)
及其命令集合中所有命令得到的命令特征结构(CommandFeature)合并得到的。</p>

<p style="text-indent: 2em;">extractor模块主要包括两个部件，命令解析器和命令特征提取器</p>

## 命令解析器

<p style="text-indent: 2em;">针对一条普通命令，解析器解析得到CommandInvocationInitial结构，包括三个部分，分别是命令名、Flag和Option列表、操作数。</p>

### CommandInvocationInitial结构

option参数和flag参数介绍

```
Shell命令行flag参数：简称flag，由长或短选项组成，其中以一个连字符(-)开头为短选项，以两个连字符(--)开头为长选项。
例如-f为短选项形式的flag，而--force为长选项形式的flag。

Shell命令行option参数：简称option，由长或短选项及其携带的参数两部分组成。
例如-S SUFFIX为短选项形式的option，--suffix SUFFIX为长选项形式的option，其中--suffix和-S分别为长短选项，SUFFIX为所携带的参数。

flag参数和option参数的相同点在于都有以连字符开头的长或短选项，不同点在于option参数可以携带一个参数。
```

识别过程

```
通过解析命令名cmd1对应的操作手册（man page），对man page手册给出的帮助信息利用脚本进行解析，自动生成命令cmd1对应的含有flag和option信息的json格式的配置文件。

通过加载命令对应的json格式的配置文件识别命令中的flag和option参数。若不存在命令对应的json配置文件，则采用默认的识别方式进行flag和option参数。

结构如下:
{
    "cmd_name": "",
    "flag_option_list": [],
    "operand_list": []  #操作数，除了命令名和flag和option外的其余部分
}
```

示例一

```bash
tar -czvf archive.tar.gz file1.txt file2.txt directory1 directory2

解析后结果:
{
    "cmd_name": "tar",
    "flag_option_list": [
        "-c",
        "-z",
        "-v",
        [
            "-f",
            "archive.tar.gz"
        ]
    ],
    "operand_list": [
        "file1.txt",
        "file2.txt",
        "directory1",
        "directory2"
    ]
}
```

### 命令行的使用

```bash
dockdepend extractor -f ./data/extractor/shell_example.sh --only_parse
```

## 命令特征提取器

<p style="text-indent: 2em;">命令特征提取器对上述经过命令解析器得到的CommandInvocationInitial结构进行进一步处理，提取出命令特征。
命令特征提取器通过对大部分常用命令按照制定的规则对CommandInvocationInitial结构每个部分进行详细处理，提取得到命令的特征信息。
经过特征提取器后，使得shell命令能够表达出更多的语义信息，以确保更准确地描述其语义信息。</p>

<p style="text-indent: 2em;">命令特征提取器提供了一个可拓展的接口，使得用户能够快捷定义单一命令的提取规则，从而实现对更多命令的语义信息提取。</p>

使用特征提取器前后效果对比

```
current_dir = /tmp

示例:
"command": "apt install -y --allow-unauthenticated deb.torproject.org-keyring nodejs tor git tzdata",
"result": {
    "CommandSet": [
        "apt"
    ],
    "PkgSet": [
        "tzdata",
        "nodejs",
        "tor",
        "git",
        "deb.torproject.org-keyring"，
    ],
    "OtherSet": [],
    "UserSet": [],
    "VarPSet": [],
    "VarCSet": [],
    "InputTree": "{'/': {'etc': {}}}",
    "OutputTree": "{'/': {'etc': {}}}"
}
由于apt install会更改/etc下面的文件或目录，因此，在输入输出树中都包含/etc，这个特征信息通过特征提取器赋予，能够表达出超越文本的语义信息。
```

### 命令特征结构(CommandFeature)

```
包括：
CommandSet --> 命令集合
PkgSet --> 包集合
OtherSet --> 其他集合,用于存储未识别的部分
UserSet --> 用户集合,用于Dockerfile中USER指令与RUN指令依赖关系判断
InputSet,OutputSet --> 输入路径集合、输出路径集合
```

对于命令集合中的每一条命令，会得到一个命令特征结构(CommandFeature)。

## 指令特征结构(InstructFeature)

<p style="text-indent: 2em;">一条RUN指令会得到一个指令特征结构(InstructFeature)。
指令特征结构由初始指令特征结构(InstructFeatureInit)及其命令集合中所有命令得到的命令特征结构(CommandFeature)合并得到。</p>

```
{
    "CommandSet": [], # 命令集合 --> extractor阶段
    "PkgSet": [], # 包集合 --> extractor阶段
    "OtherSet": [], # 其他集合 --> 两阶段合并得到
    "UserSet": [], # 用户集合 --> extractor阶段
    "VarPSet": [], # shell变量定义集合 --> ast阶段
    "VarCSet": [], # shell变量使用集合 --> ast阶段
    "InputTree": "", # 输入目录树 --> 两阶段合并得到
    "OutputTree": "" # 输出目录树 --> 两阶段合并得到
}
}
```

示例一

```
set -ex && \
apk add --no-cache --virtual .build-deps \
                            autoconf \
                            build-base \
                            curl \
                            libev-dev \
                            linux-headers \
                            libsodium-dev \
                            mbedtls-dev \
                            pcre-dev \
                            tar \
                            tzdata \
                            c-ares-dev \
                            git \
                            gcc \
                            make \
                            libtool \
                            zlib-dev \
                            automake \
                            openssl \
                            asciidoc \
                            xmlto \
                            wget \
                            libpcre32 \
                            g++ && \
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
cd /tmp && \
curl -sSL $KCP_URL | tar xz server_linux_amd64 && \
mv server_linux_amd64 /usr/bin/ && \
mkdir ss && \
cd ss && \
curl -sSL $SS_URL | tar xz --strip 1 && \
./configure --prefix=/usr --disable-documentation && \
make install && \
cd /tmp && \
runDeps="$( \
    scanelf --needed --nobanner /usr/bin/ss-* \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | xargs -r apk info --installed \
        | sort -u \
)" && \
apk add --no-cache --virtual .run-deps $runDeps && \
apk del .build-deps && \
rm -rf /tmp/*

特征提取后结果:
{
    "CommandSet": [
        "./configure",
        "mv",
        "awk",
        "cd",
        "make",
        "scanelf",
        "curl",
        "apk",
        "sort",
        "tar",
        "cp",
        "rm",
        "set",
        "mkdir"
    ],
    "PkgSet": [
        "${runDeps}",
        "tar",
        "git",
        "wget",
        "asciidoc",
        "tzdata",
        "libsodium-dev",
        ".build-deps",
        "g++",
        "automake",
        "libev-dev",
        "zlib-dev",
        "mbedtls-dev",
        "openssl",
        "build-base",
        "--installed",
        "make",
        "unknown_scanelf",
        "linux-headers",
        "pcre-dev",
        "curl",
        "xmlto",
        "unknown_./configure",
        "libpcre32",
        "c-ares-dev",
        "autoconf",
        "libtool",
        "gcc"
    ],
    "OtherSet": [
        "--installed"
    ],
    "UserSet": [],
    "VarPSet": [
        "runDeps"
    ],
    "VarCSet": [
        "KCP_URL",
        "runDeps",
        "SS_URL"
    ],
    "InputTree": "{'/': {'etc': {}, 'usr': {'share': {'zoneinfo': {'Asia': {'Shanghai': {}}}}, 'bin': {'ss-*': {}}}, 'tmp': {'server_linux_amd64': {}, 'ss': {'configure': {}, 'Makefile': {}}, '*': {}}}}",
    "OutputTree": "{'/': {'etc': {'localtime': {}}, 'tmp': {'${KCP_URL}': {}, 'server_linux_amd64': {}, 'ss': {'${SS_URL}': {}}, '*': {}}, 'usr': {'bin': {'ss-*': {}}}}}"
}
```

使用

```bash
dockdepend extractor -f ./data/extractor/shell_example.sh
```

对于多行命令，想单独得到每个命令的命令特征结构，可以使用--detach选项:

```
mutil_command.sh内容如下(包含三条命令):
wget -qO client.zip https://static2.askmrrobot.com/wowsite/client/AskMrRobotClient-any-1201.zip
tar -czvf archive.tar.gz file1.txt file2.txt directory1 directory2
apt install -y --allow-unauthenticated deb.torproject.org-keyring nodejs tor git tzdata

使用--detach选项分别得到wget和tar命令以及apt的命令特征结构:
dockdepend extroctor -f ./data/ast/mutil_command.sh --detach
```

## shell命令依赖

关于shell命令之间的依赖关系，可分为四种:

+ pkg-command依赖

```
即前一个shell命令的pkg集合与后一个shell命令的command集合有交集

before command:
    apt install wget

after command:
    wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz

这里后一个命令的wget依赖于前一个命令的pkg集合
```

+ VarPSet-VarCSet依赖

```
before command:
    runDeps="$( \
        scanelf --needed --nobanner /usr/bin/ss-* \
            | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
            | xargs -r apk info --installed \
            | sort -u \
    )"

after command:
    apk add --no-cache --virtual .run-deps $runDeps
```

+ 目录依赖

```
示例一:
before command:
    wget -q -nc --no-check-certificate -P /var/tmp https://cmake.org/files/v3.11/cmake-3.11.1-Linux-x86_64.sh
    
after command:
    /var/tmp/cmake-3.11.1-Linux-x86_64.sh --prefix=/usr/local --skip-license


/var/tmp/cmake-3.11.1-Linux-x86_64.sh 来自于wget下载的文件

示例二:
before command:
    mkdir -p /var/tmp && touch 1.txt
    
after command:
    cd /var/tmp
    
/var/tmp依赖于mkdir的创建

```

+ other-other依赖

```
借鉴与文本依赖，如果前后两个命令之间存在相同的文本，则认为这两个命令之间存在依赖关系

before command:
    groupadd -g 1000 laradock && useradd -l -u 1000 -g laradock -m laradock -G docker_env && usermod -p "*" laradock -s /bin/bash

after command:
    chown laradock:laradock /home/laradock/aliases.sh
    
其中groupadd会创建laradock用户组,且laradock会添加到other集合中
而chown指定了/home/laradock/aliases.sh的拥有者和所在组,解析后会将laradock会添加到other集合中
由于other集合存在交集即认为这两个命令之间存在依赖关系

```