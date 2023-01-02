import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException

if __name__ == '__main__':
    # 通过parammiko创建一个ssh短连接客户端实例对象
    ssh = paramiko.SSHClient()
    # 自动在本机第一次连接远程服务器时，记录主机指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 1. 直接密码远程连接的方式
        ssh.connect(hostname='82.157.160.123', port=22, username='root', password='Python123456', timeout=10)
        # 注意，如果你测试某个服务器的连接时，如果你本地已经配置了这个远程服务器的免密登录(公私钥模式)，那么就不能测试出密码是否正确了，因为首先会通过公私钥模式登录，不会使用你的密码的。

        # 2. 使用秘钥免密登录的方式
        # pkey = PkeyModel.objects.get(name='xxxxxxx').private
        # pkey = RSAKey.from_private_key(StringIO(pkey))
        # ssh.connect(hostname='47.98.130.212', port=22, username='root', pkey=pkey, timeout=10)

        while True:
            # 保存本次ssh的连接的回话状态
            cli = ssh.get_transport().open_session()
            # 设置回话超时时间
            cli.settimeout(120)

            command = input("请输入您要发送的指令：")
            if command == "exit":
                break
            # 发送指令
            cli.exec_command(command)
            # 接受操作指令以后，远程主机返回的结果
            stdout = cli.makefile("rb", -1)
            # 读取结果并转换编码
            content = stdout.read().decode()
            print(content)
            # 关闭连接
            ssh.close()
    except AuthenticationException as e:
        print(e.message)
        print(traceback.format_exc())