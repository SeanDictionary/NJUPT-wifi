# NJUPT-wifi
![Release](https://img.shields.io/github/v/release/SeanDictionary/NJUPT-wifi) ![Platform](https://img.shields.io/badge/platform-Windows-green) ![License](https://img.shields.io/github/license/SeanDictionary/NJUPT-wifi) ![Built with Python](https://img.shields.io/badge/Built%20with-Python-blue?logo=python)

It's a tool to auto login NJUPT wifi.

## How to use

❗ Warning: If you are using a proxy,remember to add `p.njupt.edu.cn` to the proxy whitelist.

1. Download the realse edition and double-click to run the file.

2. If it's the first time to run the file.It will generate a config file `account.json` 和 `wifi.log` under the current path.Remember to change the details in config file.(Next session is about how to set the config.)

⭕ Tips: When you move the file,remember to move the config together.

3. After setting config,run the file will try to connect NJUPT wifi.If it connected there will be a System notification

⭕ Tips: If you want to exit the software,please use TaskManager.

## Setting

the account.json will as the follow.

```
{
    "account": "account",
    "mode": "mode",
    "password": "password",
    "step": 5
}
```

Replace

1. account → "your account"

2. mode → "cmcc"(移动)/"njxy"(电信)/""(校园网)

3. password → "your password"

4. Step: It's the time interval between two connections, default is 5 seconds.

If you want use/change other parameters please rebuild the file.

## Outputs

The file will return outputs in log to check whether the connection is successful.

Here are some outputs.

| Outputs                                                                                                                                                                           |             Meanings              | Status |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------: | :----: |
| Generated account.json.Change the information.                                                                                                                                    | complete the config and run again |   ⭕   |
| dr1003({"result":0,"msg":"AC999","ret_code":2});                                                                                                                                  |         already connected         |   ✔    |
| dr1003({"result":0,"msg":"从 Radius 获取错误代码出现异常！","ret_code":1});                                                                                                       |            mode wrong             |   ❌   |
| dr1003({"result":0,"msg":"账号或密码错误(ldap 校验)","ret_code":1});                                                                                                              |     account or password wrong     |   ❌   |
| ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None)))                                                                                            |        turn off your proxy        |   ❌   |
| (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x00000239E5903A00>:<br /> Failed to establish a new connection: [Errno 11001] getaddrinfo failed')) |     connect the correct wifi      |   ❌   |
| dr1003({"result":1,"msg":"Portal 协议认证成功！"});                                                                                                                               |       successfully connect        |   ✔    |

## Builds

Under the path, use `pyinstaller` to build the file.

```bash
pyinstaller --onefile --noconsole --clean --hidden-import plyer.platforms.win.notification wifi.py
```

## Others

Welcome Issues and PRs.
