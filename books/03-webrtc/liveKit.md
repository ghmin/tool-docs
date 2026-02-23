## ubuntu20环境下配置liveKit


## liveKit是什么
是webrtc的一个sfu

## 如何运行
如果你使用的是 源代码编译，那么 执行命令是：
```shell
# 开发模式：
cd cmd/server
go run main.go commands.go --dev --bind 0.0.0.0
# 生成模式--自行配置config：并且下载官方发布的版本：
#!/bin/sh
touch log.log
nohup ./livekit-server --config config-pro.yaml  >> log.log 2>&1 &
tail -f log.log
```

## 配置文件说明
下面是一份 配置文件sample：
```shell
port: 7880 # http 端口
bind_addresses:                # 监听地址列表
  - "0.0.0.0"
keys:
  YOUR_CUSTOM_API_KEY: YOUR_CUSTOM_API_SECRET

# WebRTC configuration
rtc:
  # UDP ports to use for client traffic.
  # this port range should be open for inbound traffic on the firewall
  port_range_start: 50000
  port_range_end: 60000


  tcp_port: 7881 # tcp端口

  node_ip: 103.133.8.8 # 服务器的公网ip--如果是内网机器，填写内网ip--例如 192.168.8.8
  use_external_ip: false # 不要使用 turn server 辅助获取 公网ip，直接指定。

webhook:
  # The API key to use in order to sign the message
  # This must match one of the keys LiveKit is configured with
  api_key: 'YOUR_CUSTOM_API_KEY'
  urls:
    - 'http://localhost:8080/api/webhook'

## 记得要把 http port，tcp port port range 范围的端口，无论是 tcp还是udp协议的，都在防火墙放开。
## webhook是liveKit调用业务机器的网址，如果你没有业务机器网站，也不会开发，那么就删除webhook配置。
```