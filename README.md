# NJUPT-wifi

It's a tool to login NJUPT wifi.

## How to use

Download the realse edition and double-click to run the file.

If it's the first time to run the file.It will generate a config file `account.json` under the current path.Remember to change the details in config file.

When you move the file,remember to move the config together.

After setting sonfig,run the file will try to connect NJUPT wifi.

## Setting

the account.json will as the follow.

```
{
    "account": "account",
    "mode": "mode",
    "password": "password"
}
```

Replace

account → "your account"

mode → "cmcc"(移动)/"njxy"(电信)/""(校园网)

password → "your password"

## Outputs

The file will return outputs to check whether the connection is successful.

Here are some outputs.

| Outputs                                                                   |             Meanings             | Status |
| ------------------------------------------------------------------------- | :-------------------------------: | :----: |
| Generated account.json.Change the information.                            | complete the config and run again |   ⭕   |
| dr1003({"result":0,"msg":"AC999","ret_code":2});                          |          have connected          |   ❌   |
| dr1003({"result":0,"msg":"从Radius获取错误代码出现异常！","ret_code":1}); |            mode wrong            |   ❌   |
| dr1003({"result":0,"msg":"账号或密码错误(ldap校验)","ret_code":1});       |     account or password wrong     |   ❌   |
| dr1003({"result":1,"msg":"Portal协议认证成功！"});                        |       successfully connect       |   ✔   |

## Others

Welcome issues and PRs.
