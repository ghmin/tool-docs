##  前言
配置文件 tinode.conf 包含了关于服务器配置的详细说明。

## 从二进制包安装
1、访问发布页面，选择最新或最适合的版本。从二进制文件列表中下载适用于你的数据库和平台的版本。下载完成后，将其解压到你选择的目录，并 cd 到该目录。

2、确保你的数据库正在运行。确保数据库配置为接受来自 localhost 的连接。对于 MySQL，Tinode 将尝试以无密码的 root 用户连接。对于 PostgreSQL，Tinode 将尝试使用密码 postgres 以 postgres 用户连接。关于如何配置 Tinode 使用不同的用户或密码，请参阅下面的说明（从源代码构建，第 4 节）。需要 MySQL 5.7 或更高版本（使用 InnoDB 存储引擎，不要使用 MyISAM）。MySQL 5.6 或更低版本无法工作，使用 MyISAM 会导致问题。需要 PostgreSQL 13 或更高版本。PostgreSQL 12 或更低版本无法工作。

3、运行数据库初始化程序 init-db（在 Windows 上是 init-db.exe）：

```shell

./init-db -data=data.json
运行 tinode（在 Windows 上是 tinode.exe）服务器。它可以在没有任何参数的情况下工作。

补充说明，如果你不想用 init-db,那么可以使用 以下提供的数据库脚本【仅仅针对pgsql以及版本0.25.0】：

```

```shell

./tinode
```

通过在浏览器中访问 http://localhost:6060/ 来测试你的安装。

## 从源代码构建

1. 安装 Go 环境。以下安装说明适用于 Go 1.18 及更新版本。

2. 仅当你打算修改代码时才需要：安装 protobuf 和 gRPC，包括 Go 的代码生成器。

3. 确保以下数据库之一已安装并正在运行：

MySQL 5.7 或更高版本，配置为使用 InnoDB 引擎（首选 8.x）。MySQL 5.6 或更低版本无法工作。

PostgreSQL 13 或更高版本。PostgreSQL 12 或更低版本无法工作。

MongoDB 4.4 或更高版本（首选 8.x）。MongoDB 4.2 及更低版本无法工作。

RethinkDB（已弃用，除非 RethinkDB 团队恢复开发，否则支持将在 2027 年终止）。

4. 获取并构建 Tinode 服务器和 tinode-db 数据库初始化程序：

### MYSQL
```shell
go install -tags mysql github.com/tinode/chat/server@latest
go install -tags mysql github.com/tinode/chat/tinode-db@latest
```

### pgsql
```shell
go install -tags postgres github.com/tinode/chat/server@latest
go install -tags postgres github.com/tinode/chat/tinode-db@latest
```

### MongoDb

```shell
go install -tags mongodb github.com/tinode/chat/server@latest
go install -tags mongodb github.com/tinode/chat/tinode-db@latest
```

上述步骤将 Tinode 二进制文件安装在 $GOPATH/bin/ 中，源代码和支持文件位于 $GOPATH/pkg/mod/github.com/tinode/chat@vX.XX.X/，其中 X.XX.X 是你安装的版本，例如 0.19.1。

注意必需的构建选项 -tags rethinkdb、-tags mysql、-tags mongodb 或 -tags postgres。

你还可以选择为服务器定义 main.buildstamp，通过添加构建选项，例如，加上时间戳：

```shell
go install -tags mysql -ldflags "-X main.buildstamp=`date -u '+%Y%m%dT%H:%M:%SZ'`" github.com/tinode/chat/server@latest
```
buildstamp 的值将由服务器发送给客户端。

使用 Go 1.17 或更低版本构建会失败！

打开 tinode.conf（位于 $GOPATH/pkg/mod/github.com/tinode/chat@vX.XX.X/server/）。
检查数据库连接参数是否适合你的数据库。如果你使用 MySQL，请确保 "mysql" 部分中的 DSN 适合你的 MySQL 安装。
选项 parseTime=true 是必需的。
```shell
"mysql": {
    "dsn": "root@tcp(localhost)/tinode?parseTime=true",
    "database": "tinode"
},
```
确保你在 tinode.conf 中指定了适配器名称。例如，你想使用 MySQL 运行 Tinode：
```shell
"store_config": {
    ...
    "use_adapter": "mysql",
    ...
},
```

运行独立服务器
如果你按照上一节的说明操作，那么 Tinode 二进制文件安装在 $GOPATH/bin/ 中，源代码和支持文件位于 $GOPATH/pkg/mod/github.com/tinode/chat@vX.XX.X/，其中 X.XX.X 是你安装的版本，例如 0.19.1。

切换到源代码目录（将 X.XX.X 替换为你的实际版本，例如 0.19.1）：

```shell
cd $GOPATH/pkg/mod/github.com/tinode/chat@vX.XX.X
```

2. 运行数据库初始化程序

```shell
$GOPATH/bin/tinode-db -config=./tinode-db/tinode.conf
```
如果你想加载示例数据，添加 -data=./tinode-db/data.json 标志：

```shell
$GOPATH/bin/tinode-db -config=./tinode-db/tinode.conf -data=./tinode-db/data.json
```
数据库初始化程序每个安装只需运行一次。更多选项请参见说明。

将 JS 客户端解压到一个目录，例如 $HOME/tinode/webapp/，
将 https://github.com/tinode/webapp/archive/master.zip 
和 https://github.com/tinode/tinode-js/archive/master.zip 解压到同一目录。

将模板目录 ./server/templ 复制或符号链接到 $GOPATH/bin/templ

```shell
ln -s ./server/templ $GOPATH/bin
```
运行服务器

```shell
$GOPATH/bin/server -config=./server/tinode.conf -static_data=$HOME/tinode/webapp/
```
通过在浏览器中访问 http://localhost:6060/ 来测试你的安装。-static_data 路径下的静态文件在 web 根目录 / 下提供服务。
你可以通过编辑配置文件中的 static_mount 行来更改此设置。

重要！ 如果你将 Tinode 与其他 Web 服务器（如 Apache 或 nginx）一起运行，请记住你需要通过 Tinode 提供的 URL 来启动 web 应用。
否则它将无法工作。

### 运行集群
按照上一节所述安装并运行数据库，运行数据库初始化程序，解压 JS 文件，并链接或复制模板目录。MySQL 和 RethinkDB 都支持集群模式。为了增加弹性，你可以考虑使用集群模式。

集群至少需要两个节点。建议至少三个节点。

以下部分配置集群。

```shell
"cluster_config": {
    // 当前节点的名称。
    "self": "",
    // 所有集群节点的列表，包括当前节点。
    "nodes": [
        {"name": "one", "addr":"localhost:12001"},
        {"name": "two", "addr":"localhost:12002"},
        {"name": "three", "addr":"localhost:12003"}
    ],
    // 故障转移功能的配置。不要更改。
    "failover": {
        "enabled": true,
        "heartbeat": 100,
        "vote_after": 8,
        "node_fail_after": 16
    }
}
```

1. self 是当前节点的名称。通常，使用命令行选项 cluster_self 指定当前节点的名称更方便。命令行值会覆盖配置文件值。如果既没有在配置文件中提供，也没有通过命令行提供该值，则集群功能被禁用。

nodes 定义各个集群节点。示例定义了三个节点，分别名为 one、two 和 three，在本地主机上运行，使用指定的集群通信端口。集群地址不需要暴露给外部世界。

2. failover 是一个实验性功能，用于从故障集群节点迁移主题，使其保持可访问：

enabled 打开故障转移模式；故障转移模式要求集群中至少有三个节点。

heartbeat 是领导者节点向跟随者节点发送心跳以确认它们可访问的间隔时间（毫秒）。

vote_after 是在选举新的领导者节点之前，心跳失败的次数。

node_fail_after 是跟随者节点在被认为宕机之前错过的心跳次数。

3. 如果你在同一主机上运行所有节点来测试集群，你还必须覆盖 listen 和 grpc_listen 端口。以下是从同一主机使用同一配置文件启动两个集群节点的示例：


```shell
$GOPATH/bin/tinode -config=./server/tinode.conf -static_data=./server/webapp/ -listen=:6060 -grpc_listen=:6080 -cluster_self=one &
$GOPATH/bin/tinode -config=./server/tinode.conf -static_data=./server/webapp/ -listen=:6061 -grpc_listen=:6081 -cluster_self=two &
```

Bash 脚本 run-cluster.sh 可能会有所帮助。

```shell
#!/bin/bash

# Start/stop test cluster on localhost. This is NOT a production script. Use it for reference only.

# Names of cluster nodes
ALL_NODE_NAMES=( one two three )
# Port where the first node will listen for client connections over http
HTTP_BASE_PORT=6060
# Port where the first node will listen for gRPC intra-cluster connections.
GRPC_BASE_PORT=16060

USAGE="Usage: $0 [ --config <path_to_tinode.conf> ] {start|stop}"

# Your server binary may have a different name and location.
SERVER='./server'

if [ "$#" -lt "1" ]; then
  echo $USAGE
  exit 1
fi

while [[ $# -gt 0 ]]; do
  key="$1"
  shift
  echo "$key"
  case "$key" in
    -c|--config)
      config=$1
      shift # value
      ;;
    -s|--static_data)
      static_data=$1
      shift # value
      ;;
    start)
      if [ ! -z "$config" ] ; then
        TINODE_CONF=$config
      else
        TINODE_CONF="tinode.conf"
      fi
      if [ ! -z "${static_data+x}" ] ; then
        STATIC_DATA_DIR=$static_data
      else
        STATIC_DATA_DIR="static"
      fi

      echo "HTTP ports 6060-6062, gRPC ports 16060-16062, config ${config}"

      HTTP_PORT=$HTTP_BASE_PORT
      GRPC_PORT=$GRPC_BASE_PORT
      for NODE_NAME in "${ALL_NODE_NAMES[@]}"
      do
        # Start the node
        $SERVER -config=${TINODE_CONF} -cluster_self=${NODE_NAME} -listen=:${HTTP_PORT} -grpc_listen=:${GRPC_PORT} -static_data=${STATIC_DATA_DIR} -log_flags=stdFlags,shortfile &
        # Save PID of the node to a temp file.
        # /var/tmp/ does not requre root access.
        echo $!> "/var/tmp/tinode-${NODE_NAME}.pid"
        # Increment ports for the next node.
        HTTP_PORT=$((HTTP_PORT+1))
        GRPC_PORT=$((GRPC_PORT+1))
      done
      exit 0
      ;;
    stop)
      echo 'Stopping cluster'

      for NODE_NAME in "${ALL_NODE_NAMES[@]}"
      do
        # Read PIDs of running nodes from temp files and kill them.
        kill `cat /var/tmp/tinode-${NODE_NAME}.pid`
        # Clean up: delete temp files.
        rm "/var/tmp/tinode-${NODE_NAME}.pid"
      done
      exit 0
      ;;
    *)
      echo $USAGE
      exit 1
  esac
done
```

### 启用视频通话
视频通话使用 WebRTC。WebRTC 是一种点对点协议：一旦通话建立，客户端应用程序直接交换数据。直接数据交换效率很高，但当通话双方无法从互联网访问时就会产生问题。WebRTC 通过 ICE 服务器解决此问题，这些服务器实现 TURN(S) 和 STUN 协议作为后备。

Tinode 不直接提供 ICE 服务器。你必须安装并配置（或购买）你自己的服务器，否则视频和语音通话将不可用。

一旦你从服务提供商处获得 ICE TURN/STUN 配置，将其添加到 tinode.conf 的 "webrtc" - "ice_servers"（或 "ice_servers_file"）部分。同时将 "webrtc" - "enabled" 更改为 true。tinode.conf 中提供的示例配置仅用于说明。它无法工作，因为它使用的是虚拟值而不是实际的服务器地址。

你可能会发现此信息对选择服务器有用：https://gist.github.com/yetithefoot/7592580