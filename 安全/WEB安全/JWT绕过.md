# JWT 绕过

## JWT 是什么 
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。 

## 为什么要用 JWT

进行身份认证。

基于token的鉴权机制类似于http协议也是无状态的，它不需要在服务端去保留用户的认证信息或者会话信息。这就意味着基于token认证机制的应用不需要去考虑用户在哪一台服务器登录了，这就为应用的扩展提供了便利。

## JWT 怎么生成

jwt便是一种基于token的认证方法，一个jwt字符串包括以下三个部分:头部(header)，载荷(payload)，签名(signature)

1. 头部(header) 用于描述JWT的最基本的信息，其所用的签名与算法类似这样
```json
{
"typ": "JWT",
"alg": "HS256"
}
```

2. 载荷(payload) 也是json形式的，官方定义的有如下六个部分

```json
{
"sub": "1", //该JWT所面向的用户
"iss": "http://localhost:8000/auth/login", //该JWT的签发者 
"iat": , //iat(issued at): 在什么时候签发的token
"exp": , //exp(expires): token什么时候过期
"nbf": , //nbf(not before)：token在此时间之前不能被接收处理
"jti": "" //JWT ID为web token提供唯一标识
}
```

当然，我们在具体使用时可以不需要这么多部分，可以定义自己需要的数据，如admin:false之类。

3. 签名(signature) 签名这里我们需要传入一个私钥(key),具体生成方法如下：

```py
# 定义私有密钥
key = 'secretkey'

# header和payload拼接生成令牌
unsignedToken = encodeBase64(header) + '.' + encodeBase64(payload)

#生成签名
signature = HMAC-SHA256(key, unsignedToken)
```

4. 最终生成jwt数据 当我们分别生成了头部，载荷，签名之后，我们就可以生成最终数据了。

```py
#最后拼接生成JWT
JWT = encodeBase64(header) + '.' + encodeBase64(payload) + '.' + encodeBase64(signature)

#最后生成的JWT大概就长这个样子:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.cAOIAifu3fykvhkHpbuhbvtH807-Z2rI1FS3vX1XMjE
```

5. jwt的验证 服务器应用在接受到JWT后，会首先对头部和载荷的内容用同一算法再次签名。如果服务器应用对头部和载荷再次以同样方法签名之后发现，自己计算出来的签名和接受到的签名不一样，那么就说明这个Token的内容被别人动过的，我们应该拒绝这个Token。

## Bypass JWT

### 暴力破解

当key的安全性不高时，容易被人爆破攻击。
jwt破解工具 
- [jwt_tool](https://github.com/ticarpi/jwt_tool)

### 修改算法攻击

将非对称加密算法改为对称加密算法

算法HS256使用秘密密钥对每条消息进行签名和验证。
算法RS256使用私钥对消息进行签名，并使用公钥进行验证。

如果将算法从RS256更改为HS256，后端代码会使用公钥作为秘密密钥，然后使用HS256算法验证签名。
如果我们可以获取到公钥，那么我们就可以通过将算法从RS256修改为HS256，然后使用RSA公钥对数据进行签名，后端代码会使用RSA公钥+HS256算法进行签名验证。从而达到了绕过的效果。

```py
import jwt
public = open('public.pem', 'r').read()
print jwt.encode({"user": "admin"}, key=public, algorithm='HS256')
```


## 参考资料

- https://www.v0n.top/2019/11/01/%E6%B5%85%E8%B0%88JWT%E7%BB%95%E8%BF%87/
- 
