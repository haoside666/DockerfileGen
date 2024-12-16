# DockDepend安装

## pip安装

```
# 下载代码
git clone https://github.com/haoside666/DockerDepend.git
cd DockerDepend
# 安装
pip install .
# 测试
dockdepend dependency -f ./dockdepend/test/data/dependency/Dockerfile1
```

## docker安装

```
# 下载代码
git clone https://github.com/haoside666/DockerDepend.git
cd DockerDepend

# 构建镜像
docker build -f ./Dockerfile . -t dockdepend

# 使用
# 显示帮助信息  
docker run --rm dockdepend 

# -v 使用挂载卷，挂载本地文件夹
docker run --rm -v /home/user/data:/data dockdepend dependency -f /data/Dockerfile

```

# DockDepend命令行使用

```
有四个子模块 
1.dependency  ---> 得到依赖结果
2.meta  ---> 得到meta结构信息
3.ast	---> 得到ast分析后的结果
4.extractor ---> 得到特征结构信息
```

## dependency

```bash
# -f 指定脚本文件，默认输出到标准输出，默认含有原指令信息对，依赖指令行号对，依赖类型，依赖原因
dockdepend dependency -f ./data/dependency/Dockerfile
# -o 指定输出文件，默认输出到标准输出
dockdepend dependency -f ./data/dependency/Dockerfile -o dependency_result.json
如果Dckerfile含有多个阶段,则输出文件名会加上阶段名
例如Dockerfile1 含有两个阶段,则会得到如下两个文件
    dependency_result_1.json
    dependency_result_2.json
# -d 指定输出文件,使用-d选项时-o选项也必须是目录
dockdepend dependency -d ./data/dependency -o ./data/output 
# --simple-mode 简单模式，只输出依赖指令行号对
dockdepend dependency -f ./data/dependency/Dockerfile --simple-mode
# --no-instruct-mode 不输出指令模式，不输出原指令信息对
dockdepend dependency -f ./data/dependency/Dockerfile --no-instruct-mode
# --ignore-side-effect 不显示副作用影响依赖
dockdepend dependency -f ./data/dependency/Dockerfile --ignore-side-effect
# --ignore-unknown-command 不显示未识别命令依赖
dockdepend dependency -f ./data/dependency/Dockerfile --ignore-unknown-command
## 可以同时使用--ignore-side-effect 和 --ignore-unknown-command
dockdepend dependency -f ./data/dependency/Dockerfile --ignore-side-effect --ignore-unknown-command
# --show-consistency-dependency 显示一致性依赖
dockdepend dependency -f ./data/dependency/Dockerfile --show-consistency-dependency
# --build-info 获取构建时间，依赖数量，指令数等信息,显示所有依赖，不支持--ignore-side-effect等选项
dockdepend dependency -f ./data/dependency/Dockerfile --build-info
```

## meta

```bash
# -f 指定脚本文件，默认输出到标准输出，输出格式为meta元信息结构
dockdepend meta -f ./data/meta/Dockerfile
# -o 指定输出文件，默认输出到标准输出
dockdepend meta -f ./data/meta/Dockerfile -o meta_result.json
如果Dckerfile含有多个阶段,则输出文件名会加上阶段名
例如Dockerfile1 含有两个阶段,则会得到如下两个文件
    meta_result_1.json
    meta_result_2.json
# -d 指定输出文件,使用-d选项时-o选项也必须是目录
dockdepend meta -d ./data/mate -o ./data/output
```

## ast

```bash
# -f 指定脚本文件，默认输出到标准输出，，默认情况会合并所有命令仅输出一个初始指令特征结构(InstructFeatureInit)
dockdepend ast -f ./data/ast/shell_example.sh 
# --raw 指定输出格式为libdash原始解析结构
dockdepend ast -f ./data/ast/shell_example.sh --raw
# -o 指定输出文件
dockdepend ast -f ./data/ast/shell_example.sh -o ast_result.json
# -d 指定输出文件,使用-d选项时-o选项也必须是目录
dockdepend ast -d ./data/ast -o ./data/output
dockdepend ast -d ./data/ast -o ./data/output --raw
# --detach 分离命令，以最小命令为基元，一个基元生成一个初始指令特征结构
dockdepend ast -f ./data/ast/mutil_shell_command.sh --detach
```

## extractor

```bash
# -f 指定脚本文件，默认输出到标准输出，输出格式为指令特征结构(InstructFeature)
dockdepend extractor -f ./data/extractor/shell_example.sh 
# -o 指定输出文件
dockdepend extractor -f ./data/extractor/shell_example.sh -o feature_result.json
# -d 指定输出文件,使用-d选项时-o选项也必须是目录
dockdepend extractor -d ./data/extractor -o ./data/output
# --current_user 指定当前用户，默认用户为root
dockdepend extractor -f ./data/extractor/shell_example.sh --current_user root
# --current_dir 指定当前脚本目录，默认用户为/tmp,会影响cd,wget等命令的指令特征结果
dockdepend extractor -f ./data/extractor/shell_example.sh --current_dir /tmp
# --only_parse 只对命令特征结构中的命令列表进行命令解析操作，不进行特征提取
dockdepend extractor -f ./data/extractor/shell_example.sh --only_parse
# --detach 分离命令，以最小命令为基元，一个基元生成一个指令特征结构(InstructFeature)
dockdepend extractor -f ./data/extractor/mutil_shell_command.sh --detach
```

# DockDepend介绍

DockDepend是一个依赖关系抽取工具，能够准确、高效地判断Dockerfile指令行间的依赖关系。
DockDepend为不同指令类型提供了统一的表示方式(meta)，有效地将指令行的语义信息编码为可计算的数据结构，从而提升了依赖关系判断的准确率和效率。

## 概述

DockDepend包含四个子模块，分别为：shell parse、extractor、data process、dependency judgment。

其中shell parse和extractor模块仅针对shell命令或者说RUN指令，而data process模块和dependency模块针对Dockerfile文件。

shell parse模块将shell脚本解析为AST结构，并最终得到初始指令特征结构(InstructFeatureInit)。
extractor模块对初始指令特征结构的命令集合中的每一条命令进行特征提取得到命令特征结构，合并两阶段信息得到最终的指令特征结构(
InstructFeature)。

data process模块按照FROM指令将Dockerfile分割为每一个阶段，并且为每个阶段生成一个meta结构信息。
对于meta结构中的指令特征结合dependency judgment模块的自定义依赖表格和规则进行依赖关系判断。

正常情况下，对于RUN指令特征的提取，data process模块会自动调用shell
parse模块和extractor模块进行处理，如果你只关注shell命令，可以查看[shell parse](./shell_parse.md)
模块和[extractor](./extractor.md)模块。

# 子模块介绍

- [shell parse](./shell_parse.md)
- [extractor](./extractor.md)
- [data process](./data_process.md)
- [dependency judgment](./dependency.md)