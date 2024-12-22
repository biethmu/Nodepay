一个用于自动化 Nodepay 空投交互的机器人，包括会话管理和带代理支持的 Ping 功能。

1.获取 nodepay 的 token

在浏览器中打开 开发者工具（右键 > 检查 或 按 Ctrl+Shift+I，或 F12）。

进入开发者工具中的“控制台”或“Console”标签。

输入以下命令获取令牌：

localStorage.getItem('np_webapp_token')

![image](https://github.com/user-attachments/assets/a806a4c5-0a7b-40e1-ac04-b0907b3552b8)


红色的就是 token

并将您的 token 粘贴到文件中（每行一个令牌）。token.txt

![image](https://github.com/user-attachments/assets/fe09bfe9-cd25-48c7-aff7-fd6a871960ad)

例：token.txt

示例

ey...

ey...

ey...

2. 添加代理

将代理信息添加到 proxy.txt 中。每行的格式如下：

http://username:pass@ip:port

![image](https://github.com/user-attachments/assets/b3a4b3bf-9add-45f8-9b7c-ad52df4ae3ec)

token.txt 里面一个 token 复制三遍，对应三个不同 IP

tokens.txt 一行一个 token 不用复制，这个文件用来检查代理的运行情况
