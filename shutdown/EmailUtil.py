# coding=utf-8
import poplib
import smtplib
import sys

from email.mime.text import MIMEText
from email.header import Header
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


#获取邮件内容
def get_msg(user,passwd):
    mail_host = "pop.qq.com"
    mail_user = user
    mail_pass = passwd

    try:
        p = poplib.POP3_SSL(mail_host, 995)
        p.user(mail_user)
        p.pass_(mail_pass)
        p.stat()
        # list()返回所有邮件的编号:
        resp, mails, octets = p.list()
        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        resp, lines, octets = p.retr(index)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = '\r\n'.join(lines)
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        # 关闭连接:
        p.quit()
        #解析打印邮件内容
        return msg
    except poplib.error_proto, e:
        print "Login failed:", e
        sys.exit(1)


# 取得邮件标题信息
def get_mail_content(msg,type,indent=0):
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        for header in [type]:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = addr
            return value
    return ""


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


#发送邮件
def send_mail(name,passwd,sendMailName,title="",message=""):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = name # 用户名
    mail_pass = passwd  # 口令

    sender = mail_user
    receivers = [sendMailName]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header(name, 'utf-8')
    message['To'] = Header(sendMailName, 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)  # 465 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException, e:
        print e.args
