# shell_parse模块

<p style="text-indent: 2em;">借用了libdash库和shasta库，其中libdash库将shell脚本解析为AST结构，shasta库对AST结构中的所有字符类型和命令结点进行了封装，并且对于所有AST节点都提供了pretty方法，用于提取shell脚本。</p>

<p style="text-indent: 2em;">DockDepend在shasta基础上，对所有命令结点都实现feature方法，用于得到初始指令特征结构(InstructFeatureInit)
，利用libdash和feature方法可以去除shell语法的影响，得到统一的命令集合，便于后续命令特征的提取。</p>

## libdash介绍

<p style="text-indent: 2em;">libdash是 Linux 内核 shell 的一个分支dash，它构建了一个具有额外公开接口的可链接库。libdash 的主要用途是解析 shell 脚本。</p>

示例一 普通命令

```bash
score=0

AST后结果:
['Command', [3, [('score', [['C', 48]])], [], []]]
```

示例二 if语句

```bash
if [ -d output ]; then
    echo "output directory already exists, aborting"
    exit 1
fi

AST后结果:
['If', [['Command', [6, [], [[['C', 91]], [['C', 45], ['C', 100]], [['C', 111], ['C', 117], ['C', 116], ['C', 112], ['C', 117], ['C', 116]], [['C', 93]]], []]], ['Semi', [['Command', [7, [], [[['C', 101], ['C', 99], ['C', 104], ['C', 111]], [['Q', [['C', 111], ['C', 117], ['C', 116], ['C', 112], ['C', 117], ['C', 116], ['C', 32], ['C', 100], ['C', 105], ['C', 114], ['C', 101], ['C', 99], ['C', 116], ['C', 111], ['C', 114], ['C', 121], ['C', 32], ['C', 97], ['C', 108], ['C', 114], ['C', 101], ['C', 97], ['C', 100], ['C', 121], ['C', 32], ['C', 101], ['C', 120], ['C', 105], ['C', 115], ['C', 116], ['C', 115], ['C', 44], ['C', 32], ['C', 97], ['C', 98], ['C', 111], ['C', 114], ['C', 116], ['C', 105], ['C', 110], ['C', 103]]]]], []]], ['Command', [8, [], [[['C', 101], ['C', 120], ['C', 105], ['C', 116]], [['C', 49]]], []]]]], ['Command', [-1, [], [], []]]]]
```

更多请详见[libdash](https://github.com/mgree/libdash)

### 命令行使用

```bash
dockdepend ast -f ./data/ast/shell_example.sh --raw
```

## shasta介绍

<p style="text-indent: 2em;">shasta 是一个带有libdash AST的 shell AST 定义的 Python 库。它可用于开发 shell AST 分析和转换。
所有 AST 节点都支持pretty()将它们提取为 shell 脚本的方法，并且该库提供了一个json_to_ast模块，可以从 JSON 对象创建 AST 对象。</p>

字符类型

```
C--> 普通字符
A-->(()) 算术扩展运算符
B-->``或$()
E-->转义字符
Q-->引号
T-->~ 用户默认家目录
V-->变量 $var或者${var}形式
```

结点类型

```
CommandNode
PipeNode
SubshellNode
AndNode
OrNode
SemiNode
NotNode
RedirNode
BackgroundNode
DefunNode
ForNode
WhileNode
IfNode
CaseNode
AssignNode
RedirectionNode
FileRedirNode
DupRedirNode
HeredocRedirNode
```

更多请详见[shasta](https://github.com/binpash/shasta)

## 初始指令特征结构(InstructFeatureInit)

<p style="text-indent: 2em;">初始指令特征结构借助AST结构提取了shell命令的部分特征，包括shell变量定义集合以及shell变量使用集合，命令特征信息详见<a href="./extractor.md">命令特征提取器</a>。
此外，针对重定向符，提取了重定向的输入和输出信息，以便最终得到输入输出目录树特征，命令集合去除了shell语法的影响，得到了干净的命令形式，可用于extractor模块。</p>

```
{
    "VarPSet": [],
    "VarCSet": [],
    "CommandSet": [],
    "RedirectInputSet": [],
    "RedirectOutputSet": [],
    "OtherSet": []
}
包括VarPSet,VarCSet,CommandSet,RedirectInputSet,RedirectOutputSet,OtherSet字段

VarPSet,VarCSet字段分别是shell变量定义集合(形如var1=xxx)以及shell变量使用集合(形如 $var1)

CommandSet字段是shell命令集合 ---> 包括两类命令,分别是普通命令以及管道命令
===> shell命令集合字段会用于后续的特征提取阶段,充分提取出命令特征以便于RUN指令间的依赖判断

RedirectInputSet,RedirectOutputSet字段分别是shell命令的输入重定向集合,shell命令的输出重定向集合

OtherSet字段用于存储命令结点中未解析的部分 ---> 如ForNode中for循环条件等
```

示例一

```bash
apk add --no-cache gcc make musl-dev && wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz && tar -xJvf gawk-5.1.0.tar.xz && rm gawk-5.1.0.tar.xz

解析后结果:
{
    "VarPSet": [],
    "VarCSet": [],
    "CommandSet": [
        "apk add --no-cache gcc make musl-dev",
        "wget http://ftp.gnu.org/gnu/gawk/gawk-5.1.0.tar.xz",
        "tar -xJvf gawk-5.1.0.tar.xz",
        "rm gawk-5.1.0.tar.xz"
    ],
    "RedirectInputSet": [],
    "RedirectOutputSet": [],
    "OtherSet": []
}
```

示例二

```bash
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

解析后结果:
{
    "VarPSet": [
        "runDeps"
    ],
    "VarCSet": [
        "KCP_URL",
        "runDeps",
        "SS_URL"
    ],
    "CommandSet": [
        "set -ex",
        "apk add --no-cache --virtual .build-deps autoconf build-base curl libev-dev linux-headers libsodium-dev mbedtls-dev pcre-dev tar tzdata c-ares-dev git gcc make libtool zlib-dev automake openssl asciidoc xmlto wget libpcre32 g++",
        "cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime",
        "cd /tmp",
        [
            "curl -sSL ${KCP_URL}",
            "tar xz server_linux_amd64"
        ],
        "mv server_linux_amd64 /usr/bin/",
        "mkdir ss",
        "cd ss",
        [
            "curl -sSL ${SS_URL}",
            "tar xz --strip 1"
        ],
        "./configure --prefix=/usr --disable-documentation",
        "make install",
        "cd /tmp",
        "apk add --no-cache --virtual .run-deps ${runDeps}",
        "apk del .build-deps",
        "rm -rf /tmp/*",
        [
            "scanelf --needed --nobanner /usr/bin/ss-*",
            "awk \"{ gsub(/,/, \\\"\\nso:\\\", $2); print \\\"so:\\\" $2 }\"",
            "xargs -r apk info --installed",
            "sort -u"
        ]
    ],
    "RedirectInputSet": [],
    "RedirectOutputSet": [],
    "OtherSet": []
}
```

### 命令行使用

```bash
dockdepend ast -f ./data/ast/shell_example.sh
```

对于多行命令，想单独得到每个命令的命令特征结构，可以使用--detach选项:

```
mutil_command.sh内容如下(包含两条命令):
mkdir output
echo "LEXER/PARSER AUTOGRADER RESULTS"

使用--detach选项分别得到mkdir和echo命令的命令特征结构:
dockdepend ast -f ./data/ast/mutil_command.sh --detach
```