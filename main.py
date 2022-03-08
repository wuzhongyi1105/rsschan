import feedparser
import re
import notify

#删除多余html标签和超过2048字节数的字
def delhtml(t):
    pattern = re.compile(r'<[^>]+>',re.S)
    nohtml = pattern.sub('', t)
    
    #无视字数发送
    #return nohtml
    

    #一个汉字占2字节
    if len(nohtml) > 256:
        return '\n文章过长请查看原文'
    else:
        return '\n'+nohtml

#获取最新内容
def GetNewRSS(url):
    f=feedparser.parse(url)
    #按每篇文章进行操作
    for post in f.entries:
        #读取之前的rss 作为对比文件
        with open("oldrss",errors='ignore') as file:
            old = file.read()
            
        #检查文章链接是否存在如果不存在则
        if not post.link in old:
            """
            f.feed.title     媒体名称
            post.title       文章标题
            post.description 文章内容
            post.link        文章链接
            post.published   文章时间
            <a href="url">   超链接
            """

            #打印文章标题
            print(f.feed.title,post.title)

            #<a 超链接套住标题 /a> 文章发布时间 删除html转义了的文章内容
            notify.send('<a href="'+post.link+'">'+f.feed.title+' - '+post.title+'</a>\n', delhtml(post.description))
            #notify.send(f.feed.title+post.title, delhtml(post.description), post.link)

            #使用fcm方式发送 这个消息带链接只可用这种方式 不带链接用send即可
            #notify.fcm(f.feed.title+'  |  '+post.published, post.title+delhtml(post.description), post.link)
            
            #notify.mipush(f.feed.title+post.published, post.title+delhtml(post.description))

            #写入oldrss记录
            oldrss=open('oldrss',mode='a+',errors='ignore')
            oldrss.writelines([f.feed.title,'  ',post.link,'  ',post.title,'\n'])
            oldrss.close

if __name__ == '__main__':
    #防止ACTION同步失败
    oldrss=open('oldrss',mode='a+',errors='ignore')
    oldrss.writelines('Update Start')
    oldrss.close
            
    #订阅地址在rss_sub文件，每行填一个网址。    
    for line in open("rss_sub",errors='ignore'):
        GetNewRSS(line)
