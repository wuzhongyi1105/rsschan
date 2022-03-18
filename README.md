# 🔥RSS Chan
资源推荐 
- https://github.com/feeddd/feeds
- https://rsshub.app/

#推送方式推荐

iOS - Bark  https://github.com/Finb/bark-server 支持自定义推送图标和链接自建服务器 免费

Android
- PUSH Deer&Server酱 iOS端可自建服务器免费，安卓端支持mipush
- FCM Toolbox https://github.com/SimonMarquis/FCM-toolbox fcm接口无限制

# 功能
🌟RSS酱 运行在github action上的rss自动更新通知项目
- 支持多rss订阅源
- 支持多种推送通知
- 支持Github Action
- 过滤重复消息
- 精准定时(云函数实现)
- 注意注意注意（rss内容无更新可能action失败 upload to this repo 错误可以无视）

# 目录文件
- main.py        主程序
- notify.py      通知库
- oldrss         rss记录
- rss_sub        rss订阅

# 使用方法
1. Fork本项目
2. 项目添加必须变量 Settings -> Secrets -> Actions -> New repository secret 添加GIthub的用户名和邮箱
    - USERNAME
    - USEREMAIL
3. 添加订阅至 rss_sub
4. 使用push推送 在notify.py下查看支持的通知方式。
```shell 
以fcm_toolbox为例子
添加变量 Settings -> Secrets -> Actions -> New repository secret 添加名为 FCM_KEY 变量。
内容为token（获取方式  https://github.com/SimonMarquis/FCM-toolbox 下载apk 右上三点 Topics 设置标签， share token 复制创建新变量 FCM_KEY即可，第一次需要梯子用来注册，后续不用挂这，后台建议关闭电池优化）保存，并运行一次检查是否成功（点亮star）

fcm为默认通知方式，其他方式请查看notify.py，切换通知方式在main.py。
```
6. 在action里启动或者 右上角 Star 启动并查看log
7. 已经默认启用定时在 rsschan/.github/workflows/main.yaml 修改 cron */30 * * * * （秒（可选）分 时 天 月 周） 每30分钟执行一次


# 云函数实现精准定时 （可选，私密库无法请求）
1. 创建 Github token，前往 https://github.com/settings/tokens/new
- Note： rss （可选）
- Expiration： No expiration  有效期不会过期
- Select scopes 勾选 workflow
- Generate token 创建token 请保存备用

2. 前往https://console.cloud.tencent.com/scf 登陆并新建函数新建 - 从头开始
- 函数类型：事件函数
- 函数名称：github-rss （随意）
- 地域：广州 （随意）
- 运行环境： Custom Runtime
- 函数代码 -> 在线编辑
- 执行方法：index.main_handler

```shell
function main_handler () {
    curl \
    -X POST \
    -H "Accept: application/vnd.github.v3+json" \
    -H "Authorization: token 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" \
    https://api.github.com/repos/n0raml/rsschan/actions/workflows/main.yaml/dispatches \
    -d '{"ref":"main"}'
}

修改#Authorization: token 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     替换token 后面的 token留着
修改#https://api.github.com/repos/用户名/项目/actions/workflows/main.yaml/dispatches
```

- 在线编辑代码，请修改信息
- 高级配置 - 环境配置 占用不多，修改内存提升免费额度
- 内存 64MB
- 超时时间 900秒
- 并发配置 64 配置内存
3. 创建完毕测试并查看日记 查看action是否有触发
4. 创建定时 找到刚刚的函数进入，触发管理
- 触发方式： 定时触发
- 触发周期： 自定义触发周期
- Cron表达式：*/6 * * * *          秒（可选）分 时 天 月 周
建议添加完rss_sub手动运行一次 （右上角Star🌟）
- 立即启用
5. 检查是否有触发日记 完美
