## 工具简介
SSL证书申请工具是一款基于Java Swing开发的图形界面应用程序，它通过ACME协议（如Let's Encrypt）自动申请和管理SSL/TLS证书。工具支持通配符证书、多域名证书，并提供DNS和HTTP两种验证方式。


## 🚀 快速开始
### 系统要求
+ 有效的域名（用于申请证书）
+ 根据验证方式，需要DNS管理权限或网站文件管理权限
+ 
##  🖥️ 界面操作指南
**1. 主界面布局**

应用程序界面分为三个主要区域：

左侧表单区：填写申请参数

右侧日志区：显示操作日志和进度

底部按钮区：执行流程控制

**2. 填写申请参数**

**基本参数**

   |参数	|说明	|示例|
   | :--- | :--- | :--- |
   | 邮箱地址 | ``接收证书通知的邮箱`` | admin@example.com |
   | 主域名 | ``申请证书的主要域名`` | example.com |
   | CA机构 | ``证书颁发机构（测试/生产）`` | Let's Encrypt（测试） |
   | 加密方案 | ``密钥算法`` | RSA-2048 |

**警告：邮箱 使用 xxx@example.com，主域名 使用 example.com 都是非法的，服务端不作响应**


**域名列表配置**

+ 通配符证书：输入*，工具会自动生成*.example.com

+ 多域名证书：每行输入一个子域名前缀，例如：
  >www
  > 
  >mail
  > 
  >api
  > 
  >blog
  > 

**验证方式选择**

工具提供两种验证方式，根据你的需求选择：

|验证方式	|适用场景	| 准备工作                          |
   | :--- | :--- |:------------------------------|
| DNS TXT记录验证 | ``通配符证书、无Web服务器`` | DNS管理控制台访问权限                  |
| HTTP文件验证 | ``有Web服务器、可公开访问的网站`` | Web服务器文件写入权限(注意 通配符证书不可使用此方案) |



### 🔐 验证方式详解
#### 方式一：DNS TXT记录验证
+ 工作原理

在域名DNS解析中添加指定的TXT记录，CA服务器通过查询该记录验证域名所有权。

+ 操作步骤
1. 生成挑战信息：点击"生成验证信息"按钮，工具会显示类似如下的信息：


>域名: example.com
> 
>DNS记录名: _acme-challenge.example.com
> 
>TXT值: LHDjB6T7G9k8hYH5gF4rD3eW2qQ1aZ0x

2. 添加DNS记录：

登录你的DNS服务商控制台（如阿里云、腾讯云、Cloudflare等）：

+ 记录类型：选择 TXT

+ 主机记录：填写 _acme-challenge（或完整记录名）

+ 记录值：粘贴工具显示的TXT值

+ TTL：建议设置300秒（5分钟）

**常见DNS服务商操作路径：**

+ 阿里云：控制台 → 域名与网站 → 域名 → 解析设置 → 添加记录

+ 腾讯云：控制台 → 域名管理 → 解析 → 添加记录

+ Cloudflare：Dashboard → 选择域名 → DNS → Records → Add Record

3. 等待DNS生效：添加记录后需要等待1-5分钟让DNS全球生效。

4. 执行验证：返回工具点击"开始验证"按钮，工具会自动检查DNS记录。

**注意事项**
+ ⏱️ DNS传播时间：全球DNS生效可能需要几分钟，请耐心等待

+ 🔍 验证工具：可使用nslookup或dig命令检查记录是否生效：

```
nslookup -type=TXT _acme-challenge.example.com 
dig TXT _acme-challenge.example.com
```

+ **🛡️ 通配符证书：通配符证书必须使用DNS验证方式**


#### 方式二：HTTP文件验证
**工作原理**

在你的网站根目录创建特定文件，CA服务器通过HTTP访问该文件验证域名所有权。

**操作步骤**

1. 生成挑战信息：点击"生成验证信息"按钮，工具会显示：

```
域名: example.com

文件路径: /.well-known/acme-challenge/kjH6G5f4D3s2a1Qw9
 
文件内容: kjH6G5f4D3s2a1Qw9.8yT7R6E5W4Q3a2Z1x0

```

2. 创建验证文件：在你的Web服务器上创建指定文件：

+ 完整路径：网站根目录/.well-known/acme-challenge/kjH6G5f4D3s2a1Qw9

+ 文件内容：粘贴工具显示的内容

3. 配置Web服务器：确保可通过HTTP访问验证文件：

**Nginx配置示例：**

```
server {
    listen 80;
    server_name example.com;
    
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/html;
        try_files $uri =404;
    }
    
    # 其他配置...
}
```



**Apache配置示例：**

```
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html
    
    <Directory "/var/www/html/.well-known/acme-challenge">
        Options None
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```


与现有应用共存：如果网站已有应用运行，需要确保验证路径不被重写规则拦截。

4. 测试访问：在浏览器中访问验证URL，确认可看到正确内容：

```
http://example.com/.well-known/acme-challenge/kjH6G5f4D3s2a1Qw9

```

5. 执行验证：返回工具点击"开始验证"按钮。

注意事项
+ 🔒 仅限HTTP：验证必须通过HTTP（端口80），HTTPS无法用于此验证

+ 📁 目录权限：确保Web服务器对.well-known/acme-challenge目录有读取权限





### 💾 证书保存与管理
**证书文件说明**

申请成功后，工具会生成以下文件：

+ fullchain.pem：完整证书链（服务器证书+中间证书）

+ private.key：私钥文件（务必安全保管！）

+ server.crt：服务器证书

+ chain.pem：中间证书链

**文件保存**
1. 选择保存目录：点击"保存证书"按钮选择目录

2. 查看保存结果：保存完成后，日志区会显示证书文件路径

3. 安全建议：

+ 私钥文件权限设置为600：chmod 600 private.key

+ 备份证书和私钥到安全位置

+ 不要将私钥提交到版本控制系统