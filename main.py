import feedparser
import re
import notify

#删除多余html标签和超过2048字节数的字
def delhtml(t):
    pattern = re.compile(r'<[^>]+>',re.S)
    nohtml = pattern.sub('', t)

    #最大微信推送可传输字节数2048 太多信息导致信息流太长 一个汉字占2字节
    if len(nohtml) > 256:
        return '\n文章过长请查看原文'
    else:
        return '\n'+nohtml

#获取最新内容
def GetNewRSS(url):
    f=feedparser.parse(url)
    for post in f.entries:
        oldrss=open('oldrss',mode='a+')

        #读取之前的rss
        with open("oldrss") as file:
            old = file.read()
        #检查文章链接是否存在如果不存在则发送
        if not post.link in old:
            #打印文章标题
            print(f.feed.title,post.title)
            notify.send('<a href="'+post.link+'">'+f.feed.title+' - '+post.title+'</a>\n'+post.published,delhtml(post.description))
            oldrss.writelines([f.feed.title,'  ',post.link,'  ',post.title,'\n'])

        oldrss.close()

if __name__ == '__main__':
    #订阅地址在rss_sub文件，每行填一个网址。

    #读取rss_sub文件，获取订阅地址。并逐行订阅
    #添加记录
    oldrss=open('oldrss',mode='a+')
    oldrss.writelines(['\n'])
    oldrss.close()
    for line in open("rss_sub"):
        GetNewRSS(line)
