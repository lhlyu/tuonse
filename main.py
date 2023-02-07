import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
print('BOT_TOKEN', BOT_TOKEN)

# 创建机器人
bot = telebot.TeleBot(BOT_TOKEN)

# 命令
commands = {
    'start': '开始使用',
    'help': '获取机器人支持的命令',
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, '欢迎使用Tuonse~')


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "欢迎使用本机器人，你可以使用以下指令: \n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


if __name__ == '__main__':
    print('bot start running')
    bot.infinity_polling()
