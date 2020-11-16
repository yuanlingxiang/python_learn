#! usr/bin/env/python
# -*- coding:utf-8 -*-

import paramiko

from time import sleep

hostname = '192.168.1.90'
port = 22
password=username='root'


class ExecLinuxCmd(object):
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

        self.transport = paramiko.Transport((self.hostname, self.port))
        self.transport.start_client()
        self.transport.auth_password(username, password)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.channel = self.transport.open_session()
        self.channel.settimeout(7200)
        self.channel.get_pty()
        self.channel.invoke_shell()

    def disconnect_transport(self):
        if self.channel:
            self.channel.close()
        if self.transport:
            self.transport.close()

    def send_cmd(self, cmd):
        self.channel.send(cmd+'\n')
        for i in range(100):
            result = self.channel.recv(65535)
            if ']#' not in result:
                sleep(0.1)
            else:
                break
        else:
            raise ValueError('10S内命令未发送成功')

        return result


class SftpUploadDownload(ExecLinuxCmd):
    def __init__(self):
        super(SftpUploadDownload, self).__init__(hostname, port, username, password)
        self.sftp = paramiko.SFTP.from_transport(self.transport)

    def sftp_upload_file(self, localpath, remotepath):
        self.sftp.put(localpath, remotepath)

    def sftp_down_file(self, remotepath, localpath):
        self.sftp.get(remotepath, localpath)

if __name__ == '__main__':
    # m = ExecLinuxCmd(hostname, port, username, password)
    # m.connect_transport()
    # print m.send_cmd('pwd')
    # m.disconnect_transport()
    m = SftpUploadDownload()
    m.sftp_upload_file(r'C:\Users\Administrator\Desktop\websites.sql', r'/root/yuanlx/websites.sql')
    n = ExecLinuxCmd(hostname, port, username, password)

    m.send_cmd('cd yuanlx')
    print m.send_cmd('ll')
    m.disconnect_transport()