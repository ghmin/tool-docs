## SSL证书签名以及部署-nginx篇


## 一、HTTP-01挑战原理

**HTTP-01验证要求在你的网站根目录创建特定文件：**
> http://你的域名/.well-known/acme-challenge/{token}


>文件内容必须是ACME服务器提供的特定字符串。

## nginx服务器配置示例

#### 情况A：静态网站（无现有应用）

```nginx
# /etc/nginx/sites-available/your-site

server {
    listen 80;
    server_name example.com www.example.com;
    
    # 网站根目录
    root /var/www/html;
    index index.html;
    
    # 自动包含ACME挑战目录
    # 不需要特殊配置，Nginx会自动服务文件
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

#### 情况B：已有动态应用（如PHP/Node.js）

```
server {
    listen 80;
    server_name example.com www.example.com;
    
    # 主应用配置
    root /var/www/example-app;
    index index.php;
    
    # 重要：为ACME挑战创建独立location
    location ^~ /.well-known/acme-challenge/ {
        # 指定挑战文件的独立目录
        root /var/www/acme-challenges;
        
        # 禁用所有重写规则
        try_files $uri =404;
        
        # 确保允许访问
        allow all;
    }
    
    # 主应用路由
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    }
}
```


#### 情况C：代理到后端服务（API网关）

```
server {
    listen 80;
    server_name api.example.com;
    
    # ACME挑战文件目录
    location ^~ /.well-known/acme-challenge/ {
        root /var/www/acme-challenges;
        try_files $uri =404;
    }
    
    # 其他所有请求代理到后端
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

```


## 三、验证步骤

1. 创建挑战目录

```shell

# 测试Nginx配置
nginx -t

# 创建测试文件
echo "test123" > /var/www/acme-challenges/.well-known/acme-challenge/test.txt

# 测试访问
curl http://example.com/.well-known/acme-challenge/test.txt
```
2. 测试配置

```shell

# 测试Nginx配置
nginx -t

# 创建测试文件
echo "test123" > /var/www/acme-challenges/.well-known/acme-challenge/test.txt

# 测试访问
curl http://example.com/.well-known/acme-challenge/test.txt
```

## 引用证书配置HTTPS

# HTTPS部署及HTTP/HTTPS共存配置指南

## 一、证书文件准备

### 1. 获取证书文件
申请成功后你会得到以下文件：
- `fullchain.pem` - 完整证书链（推荐使用）
- `private.key` - 私钥文件
- `server.crt` - 服务器证书（可选）
- `chain.pem` - 中间证书链（可选）

### 2. 文件存放建议
```bash
# 创建SSL证书目录
mkdir -p /etc/ssl/example.com

# 复制证书文件
cp fullchain.pem /etc/ssl/example.com/
cp private.key /etc/ssl/example.com/

# 设置权限
chmod 600 /etc/ssl/example.com/private.key
chmod 644 /etc/ssl/example.com/fullchain.pem

```

#### 基本HTTPS配置
```
# /etc/nginx/sites-available/example.com

server {
    # HTTPS监听端口
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # 证书路径
    ssl_certificate /etc/ssl/example.com/fullchain.pem;
    ssl_certificate_key /etc/ssl/example.com/private.key;
    
    # SSL协议配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # SSL会话缓存
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # 启用OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # 网站根目录
    root /var/www/html;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
}
```

#### HTTP重定向到HTTPS

```
server {
    listen 80;
    server_name example.com www.example.com;
    
    # 301永久重定向到HTTPS
    return 301 https://$server_name$request_uri;
}
```

**额外补充，如果你要启用 gzip ，那么 可以参考如下：**

```
    
#开启gzip
gzip  on;  
##低于1kb的资源不压缩 
gzip_min_length 1k;
##压缩级别【1-9】，越大压缩率越高，同时消耗cpu资源也越多，建议设置在4左右。 
gzip_comp_level 3; 
##需要压缩哪些响应类型的资源，多个空格隔开。不建议压缩图片，下面会讲为什么。
gzip_types  application/javascript application/x-javascript text/javascript  text/css;  
##配置禁用gzip条件，支持正则。此处表示ie6及以下不启用gzip（因为ie低版本不支持）
gzip_disable "MSIE [1-6]\.";  
##是否添加“Vary: Accept-Encoding”响应头
gzip_vary on;

```