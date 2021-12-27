# import telebot
#
# bot = telebot.TeleBot('')
#
#
# @bot.message_handler(content_types=['text'])
# # Сделать по id только для Маши
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, красавица!")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши Привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
#
# bot.polling(none_stop=True, interval=0)


kek = {'122111': 'https://ruz.narfu.ru/?timetable&group=15913'}
if '122111' in kek.keys():
    print(kek['122111'])
