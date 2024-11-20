import telebot
from telebot import types

token = open(r"Text files/teletoken.txt").readline()
bot = telebot.TeleBot(token)

class Telega:
#Писать обработчик кнопки в классе бесполезно, так как универсализировать дейсьвия кнопки нельзя.
    def __init__(self, message):
        self.message = message

    #Сщздание Reply кнопок
    def Reply_btns(self,bot_say,resize ,row_width: int=3,*names):
        if type(names[0]) is type([]):names = names[0]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=resize, row_width = row_width)
        BtnList = []
        for btn in names:
            btn = types.KeyboardButton(f"{btn}")
            BtnList.append(btn)
        markup.add(*BtnList)
        bot.send_message(self.message.chat.id, bot_say, reply_markup=markup)

    #Очистка Reply клавиатуры
    def CleanReplyBtns(self,bot_say):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(self.message.chat.id, bot_say, reply_markup=markup)

    #Cсоздание Inline кнопок
    def Inline_btns(self,bot_say,row_width,*names,callback_add=""):
        if type(names[0]) is type([]):names = names[0]
        markup = types.InlineKeyboardMarkup(row_width=row_width)
        BtnList = []
        BtnReady = []
        for btn in names:
            if btn in BtnReady:
                k = 0
                for i in BtnReady:
                    if i == btn: k+=1
                BtnReady.append(btn)
                btn = types.InlineKeyboardButton(f"{btn} ({k})", callback_data=f"{btn} ({k})"+callback_add)
            else:
                BtnReady.append(btn)
                btn = types.InlineKeyboardButton(f"{btn}", callback_data=f"{btn}"+callback_add)
            BtnList.append(btn)
        markup.add(*BtnList)
        bot.send_message(self.message.chat.id, bot_say, reply_markup=markup)
    """
    names - это параметр, который можно заполнить аргументами через запятую (  bot_say, row_width, '1', '2', '3'] 
    или с помощью массива.
    Для второго случая перед массивом нужно будет поставить звездочку '*' (  bot_say, row_width, *['1','2','3']
    """
