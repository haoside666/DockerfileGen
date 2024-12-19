The pre-processed formatting standard for all commands is as follows:

|             | flag  |                subcmd                 | value |       type       |
|:-----------:|:-----:|:-------------------------------------:|:-----:|:----------------:|
|     ADD     | Tuple |                 None                  | dict  |     default      |
|     ARG     | Tuple |                 None                  | dict  |     default      |
|    COPY     | Tuple |                 None                  | dict  | default or from  |
| ENTRYPOINT  | Tuple |                 None                  | Tuple | default or shell |
|     ENV     | Tuple |                 None                  | dict  |     default      |
| HEALTHCHECK | Tuple |                  str                  | Tuple |     default      |
|     RUN     | Tuple | NoneType(shell 格式) or str(default 格式) |  str  | default or shell |
|    OTHER    | Tuple |                 None                  | Tuple |     default      |
