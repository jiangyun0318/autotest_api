# coding=utf-8

import os
import sys

base_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(base_path)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import smtplib
import time
from Util.handle_init import handle_ini
import datetime
from bs4 import BeautifulSoup
from lxml import etree
import matplotlib.pyplot as plt


# import logging
# logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)


class HandleMail:

    def anasize_maile(self, path):

        parser = etree.HTMLParser(encoding='utf-8')
        html = etree.parse(path, parser=parser)

        title = html.xpath('//*[@id="header_row"]/td/text()')[1:6]
        num = html.xpath('//*[@id="total_row"]/td/text()')[1:6]

        stime = html.xpath('//*[@id="div_base"]/div[2]/p[2]/text()')
        etime = html.xpath('//*[@id="div_base"]/div[2]/p[3]/text()')

        dict1 = dict(zip(title, num))
        # print(dict1)

        return dict1, title, num, stime, etime

    def result_mat(self, re):

        # 多个饼图展示，清空之前的数据
        if os.path.exists("../Config/123.png"):
            os.remove("../Config/123.png")

        # 生成数据
        labels, share = re[1:3]
        labels = labels[1:]
        share = share[1:]
        labels[2], labels[3] = labels[3], labels[2]
        share[2], share[3] = share[3], share[2]
        # print(labels, share)

        # 设置分裂属性
        explode = [0, 0, 0, 0]
        # explode = [0, 0.1, 0, 0, 0]

        # 分裂饼图
        plt.pie(share, explode=explode,
                labels=labels, autopct='%3.1f%%',
                startangle=180, shadow=True, pctdistance=0.6,
                colors=['c', 'r', 'gray', 'g'])

        # 标题
        plt.title('bug分布图')
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

        plt.savefig("../Config/123.png")
        # 清除plt缓存
        plt.cla()

    def send_mail(self, file_new):

        username = handle_ini.get_value("mail_user", "EMAIL")
        password = handle_ini.get_value("mail_pass", "EMAIL")
        sender = handle_ini.get_value("sender", "EMAIL")
        receiver = handle_ini.get_value("receiver", "EMAIL")
        receiver1 = handle_ini.get_value("receiver1", "EMAIL")
        receiver2 = handle_ini.get_value("receiver2", "EMAIL")
        receiver3 = handle_ini.get_value("receiver3", "EMAIL")
        receiver4 = handle_ini.get_value("receiver4", "EMAIL")
        receiver5 = handle_ini.get_value("receiver5", "EMAIL")
        receiver6 = handle_ini.get_value("receiver6", "EMAIL")
        receiver7 = handle_ini.get_value("receiver7", "EMAIL")
        receiver8 = handle_ini.get_value("receiver8", "EMAIL")
        host = handle_ini.get_value("mail_host", "EMAIL")

        print(username, password, sender, receiver)

        msg = MIMEMultipart()
        # 邮件对象
        msg['Subject'] = Header("接口自动化测试报告", 'utf-8').encode()
        msg['From'] = Header(u'江云')
        msg['To'] = Header(u'胡文鼎，方琍，张逢春，陈洪，张磊，张能，英辉')
        msg['Cc'] = Header(u'黄川川')
        msg['date'] = time.strftime("%a,%d %b %Y %H:%M:%S %z")

        msg.attach(MIMEText('Dear all:', 'plain', 'utf-8'))

        for path in file_new:

            # 多个饼图展示，清空之前的数据
            if os.path.exists("../Config/123.png"):
                os.remove("../Config/123.png")

            with open(path, 'rb') as f:
                mail_body = f.read()

            # 默认为test环境
            env_name = '      默认测试环境-'

            try:
                env = sys.argv[1]
                if env == 'prod':
                    env_name = '      生产环境-'
                elif env == 'beta':
                    env_name = '      预发环境-'
                else:
                    env_name = '      测试环境-'
            except:
                env_name = '      测试环境--'
            finally:
                # 邮件正文内容
                if '_ao' in path:
                    msg.attach(MIMEText(env_name + '资运相关接口自动化测试报告，附件为详细信息，请查收！', 'plain', 'utf-8'))
                    filename = 'crm_bug'
                elif '_cms' in path:
                    msg.attach(MIMEText(env_name + 'MO相关接口自动化测试报告，附件为详细信息，请查收！', 'plain', 'utf-8'))
                    filename = 'MO_bug'
                else:
                    msg.attach(MIMEText(env_name + 'BSS相关接口自动化测试报告，附件为详细信息，请查收！', 'plain', 'utf-8'))
                    filename = 'bss_bug'
            # 测试报告提纲

            re = self.anasize_maile(path)

            st = '      开始时间： ' + (re[3])[0]
            nt = '      运行时间： ' + (re[4])[0]

            res = re[0]
            n1 = '      用例总计--->' + res['总数'] + '条'
            n2 = '      通过用例--->' + res['通过'] + '条'
            n3 = '      失败用例--->' + res['失败'] + '条'
            n4 = '      错误用例--->' + res['错误'] + '条'
            n5 = '      跳过用例--->' + res['跳过'] + '条'
            n6 = '      通过率（通过/(总计-跳过)）--->' + ('%.2f'%(int(res['通过'])/(int(res['总数'])-int(res['跳过'])))) + '\n'

            msg.attach(MIMEText(st, 'plain', 'utf-8'))
            msg.attach(MIMEText(nt, 'plain', 'utf-8'))
            msg.attach(MIMEText(n1, 'plain', 'utf-8'))
            msg.attach(MIMEText(n2, 'plain', 'utf-8'))
            msg.attach(MIMEText(n3, 'plain', 'utf-8'))
            msg.attach(MIMEText(n4, 'plain', 'utf-8'))
            msg.attach(MIMEText(n5, 'plain', 'utf-8'))
            msg.attach(MIMEText(n6, 'plain', 'utf-8'))


            # 生成饼图
            self.result_mat(re)
            with open('../Config/123.png', 'rb') as fp:
                msgImage = MIMEImage(fp.read())

            msgImage.add_header('Content-ID', '<image>')
            msgImage.add_header('Content-Disposition', 'inline', filename=filename)
            msg.attach(msgImage)

            # html附件
            att1 = MIMEText(mail_body, 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # now = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
            # file_name = now + '_report.html'
            att1["Content-Disposition"] = 'attachment; filename={0}'.format(path.split('/')[-1])
            msg.attach(att1)

        # 发送邮件
        # smtp = smtplib.SMTP()
        smtp = smtplib.SMTP_SSL("smtp.mxhichina.com", 465)
        smtp.connect(host)  # 邮箱服务器
        smtp.login(username, password)  # 登录邮箱
        # receiver_all = receiver
        receiver_all = [receiver, receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7, receiver8]
        smtp.sendmail(sender, receiver_all, msg.as_string())  # 发送者和接收者
        smtp.quit()
        print("邮件已发出！注意查收。")

    # 此处为将HTML文件夹中的所有文件返回并取最新的一个HTML文件
    def new_file(self, flie_path):
        # lists=os.listdir(flie_path).sort()
        # file_path=os.path.join(flie_path, lists[-1])
        # return file_path

        for root, dirs, files in os.walk(flie_path):

            files.remove('2020-readme.txt')
            files.sort()

            # 取最新一份文件
            # file_path = os.path.join(root, files[-1])

            # 多个文件取今天生成的（多系统执行用例的时候）
            now = datetime.datetime.now().strftime('%Y%m%d')
            file_path = []
            for nfiles in files:
                if now in nfiles:
                 file_path.append(os.path.join(root, nfiles))

            return file_path


handle_mail = HandleMail()


if __name__ == "__main__":

    email = HandleMail()
    path111 = base_path + '/Report/'

    new_report_mail = email.new_file(path111)
    # email.anasize_maile(new_report_mail)

    # logger.info(new_report_mail)
    email.send_mail(new_report_mail)
