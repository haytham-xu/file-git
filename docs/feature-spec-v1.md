# File-Git V1.0

## requreiment
#### 0-0 碎碎念
需要一个状态机确定middle_path的转换？或者直接写一个转换函数
但其实好像转换只会发生在基础地方，
    1.密文下载后，在move前需要解密+解码路径    
    2。密文上传，在move到buffer前，需要加密+编码路径
也就这两种情况
在这两种情况期间，middle——path在local.json和remote.json的值重要吗？
分析一下
主要也就是那几个acion，download，upload，local delete， remote delete
对于local delete，无论什么情况都是明文的，直接拼接root path，trash path， middle path就完事了
对于remote delete，无论明文密文，直接拼接remote root path，trash path，middle path，就完事了
对于Download，明文无所谓
对于Download，密文的情况下，分两步操作 下载到buffer(remote.json是密文，下载， 全程用密文) -> buffer移动到本地(需要解密+解码)
对于upload，明文无所谓
对于upload，密文的情况下，分两步操作，移动到buffer(加密+编码)，上传到remote(全程密文)

#### 1-1 需求杂记(最后应该是空的)
* config_instance 在每次执行前怎么操作？
* 应该支持命令verify（甚至verify是不是也应该封装成一个函数）
* 每个命令执行前买应该有一个检查fgit文件夹的hook


#### 1-2 需求梳理(最后应该是满的)()
* r01: 大面积文件操作, 这会花费大量的时间、可能一次无法完成, 对于一个文件, 可能上传成功, 也可能上传失败, 失败可能就是单纯的失败, 也可能是文件名称不对等问题, 或者文件过大超时
* r01: 操作有可能中断, 需要在中断后继续完成操作
* r01: 对比后获得操作队列, 并加锁, 以单个文件作为操作最小单元, 只要操作队列还在就不允许其他操作, 只允许继续擦操作
* r02: 加密方式测试
* r03: 文件变化的标志定什么？不同操作系统/网盘, 文件的hash/md5/last_modifyed
* r03: last modify在不用操作系统的修改标志, 或者直接filegit文件上传到远端？ -> 不可行，即便没有修改save了就会变化
* r03: md5：不可行，计算效率低，且百度网盘提供的虚拟md5
* r03: size：可行
* r04: 测试需要确保失败后, 删除所有临时文件
* r05: 需要支持clone
* r06: 对于clone的repo, 需要有repo的mate信息
* r07: 操作最好可以选择文件夹, 不然一起操作全部文件太多了
* r08: 所有命令执行前, 都应该有一个hook, 之前内容, 比如: 删除超过一定天数的删除文件
* r09: 操作的基本单位（字段）: code, 文件名, 路径, 上传时间？, 最后更改时间？, 文件标识？
* r10: 对于大面积的文件操作, 查看数据库表过长可能很不友好 -> 不用数据库
* r11: 需要支持备份到远端
* r12: 需要支持下载到本地
* r13: 对于加密方式, 文件名需要进行base64转换
* r14: 对queue.json的操作应该写一个单独的函数，简版的数据库系统
* r15: 应该有友好且清晰的日志
* r16: UT - 应该有足够的测试用例
* r17: 删除文件, 挪到临时文件夹, 别删除, 稍后手动删除、
* r18: 对于失败的处理: 需要记录日志, 可能会需要手动操作, 但是后续怎么办？
* r19: 需要支持把一个本地的文件夹, 编程支持该工具的状态
* r20: 开发完之后，应该封装一个别名在shell里，而不是一直用python3
* r21: 需要一个中间路径作为中专，以适应加密文件的下载和上传
* r22: 多个端的时候，一个端酸辛token另外一个会失效啊，所以好像还是需要将一个配置文件上传到云端？

#### 2-1 方案-已找到(最后应该是满的, 且id和1-2意义对应)
* r01: 引入queue机制
* r02: done, 找到了一个高效的方式
* r03: 使用文件size作为标志
* r04: UT after all， delete
* r05: command-clone
* r08: class hook
* r09: class File
* r10: class Queue，查看queue比较友好
* r11: command-push
* r12: command-pull
* r13: base64
* r14: class Queue
* r15: class Logger
* r16: UT
* r17: .fgit/trash
* r18: ./fgit/action/xxxx/log/error.log
* r19: command-init
* r20: alias
* r21: ./fgit/action/xxxx/buffer/
* r22: token不允许自动刷新，需要

#### 2-2 不会处理的需求(不实现)
* r06: repo meta 信息
* r07: 文件夹颗粒度

-----------------------

#### 3-1 需求整理(最后应该为空，应该都在4-1)

#### 4-1落实好细节的需求
* command-init
* command-clone
* command-set
* command-refresh-token

* command-queue
* command-push
* command-pull

* alias

-------------------------------------------------------------------------------

## UT
* 测试需要创建临时文件，测试后需要删除文件

#### test infrastructure
* test bdwp_support

#### test happy flow
* integration test - original
    * init
    * 创建文件
    * push
    * 修改本地文件
    * push
    * hack的方式修改远端
    * pull
    * hack在queue中添加至
    * queue
* integration test - encrypted
    * init
    * 创建文件
    * push
    * 修改本地文件
    * push
    * hack的方式修改远端
    * pull
    * hack在queue中添加至
    * queue

#### error case
* 其他情况很难测试，就这样吧，比如
    * 未知的上传错误
    * log

-------------------------------------------------------------------------------


## spec
#### folder structure
```shell
/.fgit
|__trash    # 垃圾桶buffer
    |__20241009
        |__xxxx
        |__xxxx
    |__20241010
|__action   # 每一次操作的action
    |__20241009_pull
        |__index
            |__local.json: scan all local file
            |__remote.json: get all info from API
        |__buffer
            |__xxxx.txt
        |__log    
            |__error.json
            |__success.json
|__config.json
|__queue.json
```

#### config_instance.json
```json
{
    "mode": "original/encrypted",
    "password": "xxxxxx",
    "access_token": "xxxxx",
    "refresh_token": "xxxx",
    "Xxxx": "xxxxx",
    "token_timestamp": "1939495",
    "local_path": "/User/…./photo",
    "remote_path": "/sync-assistant/photo"
}
```

#### queue.json
```json
{
    "lock": true,
    "queue": [
        {
            "local_middle_path": "x",
            "remote_middle_path": "x",
            "action": "UPDATE/DELTE",
            "status": "TODO/IN_PROGRESS/ERROR"
        },
        {}
    ]
}
```

#### local.json
```json
{
    "middle_path_HASH": {
        "middle_path": "yyyy/…/test_1.txt",
        "size": "133854"
    },
    "HASH_2": {},
}
```

#### remote.json
```json
{
    "middle_path_HASH": {
        "middle_path": "xxx/…/test_1.txt",
        "size": "133854"
    },
    "HASH_2": {},
}
```

-------------------------------------------------------------------------------
## Command
#### refresh-token
* refresh token后更新本地的

#### init
* 创建.fgit结构

#### clone
* 执行init
* 执行pull

#### set
fgit set KEY=VALUE
* KEY必须是存在的

#### push
* 检查和执行hook: delete_trash, delete_action
* 检查lock: queue_lock
    * lock存在, 异常退出
* 执行push逻辑: original/encrypted-push

#### pull
* 检查和执行hook: delete_trash, delete_action
* 检查lock: queue_lock
    * lock存在, 异常退出
* 执行pull逻辑: original/encrypted-pull

#### queue
* 检查和执行hook: delete_trash, delete_action
* 检查lock: queue_lock
    * lock不存在, 则正常退出
* 继续执行original/encrypted-queue

## Scenraio
#### init
* 创建文件夹trash，action，config_instance.json, queue.json
* 在config.json中
    * 接收参数：mode/password/local_path/remote_path
    * 接收参数：app_id/secret_key/app_key/sign_code
    * 接收参数：expires_in/refresh_token/access_token

#### original/encrypted-pull
* 在./fgit/action中创建文件夹
* 调用build_remote_json()，得到remote.json
* 调用build_local_json()， 得到local.json
* 将remote.json和local.json交给pull-diff, 得到queue
* 将queue放入queu.json
* 触发original-queue

#### original/encrypted-push
* 在./fgit/action中创建文件夹
* 调用build_remote_json()，得到remote.json
* 调用build_local_json()， 得到local.json
* 将remote.json和local.json交给push-diff, 得到queue
* 将queue放入queu.json
* 触发original-queue

#### original/encrypted-queue
* queue加锁
* 针对queue中的所有文件，对于每一个文件
    * 触发action
        * -> DOWNLOAD: <!-- download 时需要使用原始的路径，即便是密文的 -->
            * 下载，直接获取文件原始中间路径，分离文件名和路径，调用API搜索文件，获取dlink， 通过API获取下载文件，放在buffer路径下
            * 调用move_to_local（）移动，
            * 处理buffer(删除buffer)
        * -> UPLOAD:
            * 调用move_to_buffer（）移动
            * 上传，bd上传API
            * 处理buffer
        * -> LOCAL_DELETE:
            * 检查和在trash下面创建日期文件
            * 本地挪到临时删除文档
        * -> REMOTE_DELETE:
            * * 检查和在trash下面创建日期文件
            * 远端文件挪到临时删除路径
    * 如果action成功
        * 该文件从queue中删除, 
        * log进success.log格式如下：success 2024-10-10 14:00 DOWNLOAD local_path remote_path
    * 如果action失败
        * 将该文件保留在queue, 更新queue状态
        * log错误日志, log格式如下：error 2024-10-10 14:00 DOWNLOAD local_path remote_path error_track
        * 跳过该文件, 继续其他操作
* 检查queue内是否为空
    * 若为空则释放lock
    * 否则什么也不做

## function
#### function
* pull_diff(local_dict, remote_dict)
    * only_in_A(local_dict, remote_dict)得到only_local_dict
        * 将only_local_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为LOCAL_DELETE 
    * only_in_B(local_dict, remote_dict)得到only_remote_dict
        * 将only_remote_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为DOWNLOAD
    * in_both_AB_but_diff(local_dict, remote_dict)得到difference_dict
        * 将difference_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为DOWNLOAD
* push_diff(local_dict, remote_dict)
    * only_in_A(local_dict, remote_dict)得到only_local_dict
        * 将only_local_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为UPLOAD
    * only_in_B(local_dict, remote_dict)得到only_remote_dict
        * 将only_remote_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为REMOTE_DELETE
    * in_both_AB_but_diff(local_dict, remote_dict)得到difference_dict
        * 将difference_dict中的元素添加到queue_dict, 对于每一个元素
        * 构造{"local_middle_path": "x", "remote_middle_path": "x", "action": ""}
        * action为UPLOAD
* build_local_json()
    * 递归的扫描路径下的所有文件，对于每一个文件
        * 根据中间路径计算hash，
        * 根据本地文件元信息构建json体，包含：middle_path, size
        * 将构造好的信息以字典格式存入local_dict
    * 将local_dict存入local.json
* build_remote_json()
    * 递归的获取路径下的所有文件，对于每一个文件
        * 使用get_decode_middle_path获取decrypted_middle_path中间路径
        * 根据中间路径计算hash，
        * 根据远端文件元信息构建json体，包含：middle_path(密文), size
        * 将构造好的信息以字典格式存入remote_dict
    * 将remote_dict存入remote.json


#### utils function
* move_to_local（middle_path）
    * -> ORIGINAL: 拷贝
    * -> ENCRYPTED: output_path需要解码中间路径, 然后拼接出明文的路径，直接解码出文件
* move_to_buffer()
    * -> ORIGINAL: 拷贝
    * -> ENCRYPTED: output_path需要编码成中间路径，将加密文件放在buffer
* only_in_A(A_dict, B_dict)
    * 直接调用库函数
* only_in_B(A_dict, B_dict)
    * 直接调用库函数
* in_both_AB_but_diff(A_dict, B_dict)
    * 调用库函数取得交集
    * 以A的key开始便利，得到所有size不一样的，放入result
    * 返回result


#### class
class File
    self.middle_path
    self.size

    def get_source_middle_path(root_path, file_path)
        -> 返回middle path
    def get_decode_middle_path(root_path, file_path)
        -> ORIGINAL: 直接返回
        -> ENCRYPTED: 编码后返回
    def get_encode_middle_path(root_path, file_path)
        -> ORIGINAL: 直接返回
        -> ENCRYPTED: 编码后返回

class Queue
    def get_a_objet(cls)
        * pop
        * set IN_PROGRESS
    def set_status(cls, token, STATUS)
        * DONE -> delete
        * ERROR -> update

class Logger
    success_path
    error_path 

    success_template
    error_template

    def log_success(cls)
    def log_error(cls)

class Hook
    hook_queue
    xxxx

enum STATUS
    TODO
    IN_PROGRESS
    ERROR
    DONE

enum MODE
    ORIGINAL
    ENCRYPTED

enum ACTION
    DOWNLOAD
    UPLOAD
    LOCAL_DELETE
    REMOTE_DELETE
