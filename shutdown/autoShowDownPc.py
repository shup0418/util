# coding=utf-8
import EmailUtil
import ConfigParser
import time
import os


def auto_shutdown():
    #读取配置文件参数
    config = ConfigParser.ConfigParser()
    config.readfp(open("config.ini", "rb"))
    from_mail = config.get("master", "fromMail")
    shutdown_commend = config.get("master","shutDownCommand")
    retuen_msg = config.get("master","returnMessage")
    username = config.get("to","username")
    passwd = config.get("to","passwd")
    waittime = config.get("to","waittime")

    ISOTIMEFORMAT = '%Y-%m-%d %H:%M:%S'

    while True:
        msg = EmailUtil.get_msg(username, passwd)
        mail_sub = EmailUtil.get_mail_content(msg, 'Subject')
        mail_from = EmailUtil.get_mail_content(msg, 'From')
        if mail_from == from_mail and mail_sub == shutdown_commend:
            message = "计算机将在" + waittime + "秒之后关机！若要取消关机请在" +  str(int(waittime) - 40) + "秒之内回复 off"
            EmailUtil.send_mail(username,passwd,username,retuen_msg)   #给自己发送一封邮件用来隔开关机命令的邮件，不然下次启动程序会直接关机
            EmailUtil.send_mail(username,passwd,from_mail,retuen_msg,message)  #发送回执邮件
            print "计算机将在" + waittime + "秒之后关机！"
            os.system('shutdown -s -t ' + waittime)
        elif mail_from == from_mail and mail_sub == "off":
            message = "计划关机任务已经取消！"
            EmailUtil.send_mail(username, passwd, username, retuen_msg)  # 给自己发送一封邮件用来隔开关机命令的邮件
            EmailUtil.send_mail(username, passwd, from_mail, "off", message)  # 发送回执邮件
            os.system("shutdown -a")
            print message
        else:
            print "next\t" + time.strftime(ISOTIMEFORMAT, time.localtime())
        time.sleep(30)

auto_shutdown()