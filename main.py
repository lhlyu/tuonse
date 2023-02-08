import os
import hashlib
import telebot
from pytube import YouTube
from moviepy.editor import VideoFileClip, vfx

# token
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
# 管理员
BOT_ADMIN = os.environ.get('BOT_ADMIN', '')

# 创建机器人
bot = telebot.TeleBot(BOT_TOKEN)

admins = BOT_ADMIN.split(',')

# 命令
commands = {
    'start': '开始使用',
    'help': '获取机器人支持的命令',
    'yt': '下载指定的油管视频并处理',
}


def get_file_md5(file_path):
    """
    获取文件的MD5值
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        temp_md5 = hashlib.md5()
        temp_md5.update(file.read())
        hash_code = str(temp_md5.hexdigest()).lower()
    return hash_code


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, '欢迎使用Tuonse~')


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "欢迎使用本机器人，你可以使用以下指令: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


youtubeVideoUrlRegexp = r'^(https://youtube.com/)(shorts/)?\w+(\?.+)*'


@bot.message_handler(regexp=youtubeVideoUrlRegexp)
def on_youtube_video(message):
    command_yt(message)


@bot.message_handler(commands=['yt'])
def command_yt(message):
    uid = str(message.from_user.id)
    if uid not in admins:
        return
    videoUrl = message.text.lstrip('/yt ')
    if videoUrl.startswith('https://youtube.com/') is False:
        bot.reply_to(message, '仅支持youtube视频')
        return
    cid = str(message.chat.id)
    # 去除后面的问号参数
    videoUrl = videoUrl[:videoUrl.find('?')]
    # 文件名
    name = os.path.basename(videoUrl)
    tip = bot.send_message(cid, f"*正在处理*：`{name}`", parse_mode='markdown')
    # 撤回之前的消息
    bot.delete_message(cid, message.id)
    # 下载视频
    video = f'{name}.mp4'

    # 下载视频
    yt = YouTube(videoUrl)
    yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first().download(filename=video)

    video2 = f'{name}_2.mp4'
    # 视频处理
    VideoFileClip(video).fx(vfx.colorx, 0.9).write_videofile(video2)
    # 删除文件
    os.remove(video)

    bot.delete_message(cid, tip.id)
    tip = bot.send_message(cid, f"*正在上传视频*：`{name}`", parse_mode='markdown')
    print(f'{yt.video_id} - 处理好了，发送中...')

    # 发送视频
    with open(video2, 'rb') as f:
        caption = f"*{yt.title}*\n观看次数: `{yt.views}`, 视频评分: `{yt.rating}`"
        if yt.description.strip() != '':
            caption += f'\n{yt.description}'
        caption += f'\n[视频原地址]({videoUrl})'
        bot.send_video(cid, f, caption=caption, parse_mode='markdown')

    # 删除文件
    os.remove(video2)
    bot.delete_message(cid, tip.id)


if __name__ == '__main__':
    print('bot start running')
    bot.infinity_polling()
