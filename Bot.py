import telebot, Telega,pyautogui
import cv2Code

connection = False
user_id = 0
HotkeyMode = False
ScrollMode = False

ru,eng = [],[]
for x in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя":
    ru.append(x)
for y in 'F<DULT~:PBQRKVYJGHCNEA{WXIO}SM">Zf,dult`;pbqrkvyjghcnea[wxio]sm'+"'"+'.z':
    eng.append(y)
Translit = dict(zip(ru,eng))

with open(r"teletoken.txt") as token:
    token = token.readline()
bot = telebot.TeleBot(token)

print("Session started: {}")
Session_name = input("Name: ")
Session_passw = input("Password: ")

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id,"Bot enabled")
    TL = Telega.Telega(message)
    TL.Reply_btns("///",True,1,"/session")


@bot.message_handler(commands = ["session"])
def sesion_connect(message):

    if not(connection):
        bot.send_message(message.chat.id,f"Session name: {Session_name}")
        password_check(message)
    if connection:
        TL = Telega.Telega(message)
        TL.Reply_btns(f"Session name: {Session_name}",True,1, "/disconnect")

def password_check(message):
    bot.send_message(message.chat.id,"Enter password:")
    bot.register_next_step_handler(message, password_enter)

def password_enter(message):
    global connection, id
    if message.text == Session_passw:
        connection = True
        TL = Telega.Telega(message)
        id = message.from_user.id
        TL.Reply_btns("Connection established",True,4, "/LKM","/2LKM","/Enter","/Bcksp","/RKM","/Scroll","/Hotkey","/Shift","/PrtSc", "/Cam","/session")
        bot.delete_message(message.chat.id, message.id)
    else:
        bot.send_message(message.chat.id,"Wrong password, try again.")
        bot.delete_message(message.chat.id, message.id)
        password_check(message)
@bot.message_handler(commands = ["Enter"])
def Enter(message):
    pyautogui.press('enter')

@bot.message_handler(commands = ["Shift"])
def Shift(message):
    pyautogui.press('shift')
@bot.message_handler(commands = ["Bcksp"])
def Bcksp(message):
    pyautogui.press('backspace')


@bot.message_handler(commands = ["disconnect"])
def disconnect(message):
    global connection, id
    if message.from_user.id == id:
        TL = Telega.Telega(message)
        TL.Reply_btns("Disconnected", True, 1, "/session", "/start")
        connection = False
        id = 0

@bot.message_handler(commands = ["PrtSc"])
def PrtSc(message):
    if connection and message.from_user.id == id:
        screen = pyautogui.screenshot('screenshot1.png')
        cv2Code.add_cursor('screenshot1.png')
        with open("screenshot1.png","rb") as screen:
            bot.send_photo(message.chat.id, screen)

@bot.message_handler(commands = ["Cam"])
def Cam(message):
    if connection and message.from_user.id == id:
        for i in range(4,-1,-1):
            if cv2Code.PhotoCam(i):
                with open("cam_old.png", "rb") as screen:
                    bot.send_photo(message.chat.id, screen,timeout=100)

@bot.message_handler(commands = ["LKM"])
def LKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Lclick'")
        pyautogui.click(button='left')
        PrtSc(message)

@bot.message_handler(commands = ["2LKM"])
def double_LKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'2Lclick'")
        pyautogui.click(clicks = 2,button='left')
        PrtSc(message)

@bot.message_handler(commands = ["RKM"])
def RKM(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Rclick'")
        pyautogui.click(button='right')
        PrtSc(message)

@bot.message_handler(commands = ["Hotkey"])
def Hotkey(message):
    global HotkeyMode
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"Enter hotkey")
        HotkeyMode = True

@bot.message_handler(commands = ["Scroll"])
def Scroll(message):
    global ScrollMode
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"Enter Steps (>0 up, <0 down)")
        ScrollMode = True

@bot.message_handler(content_types = ["text"])
def message_check(message):
    global HotkeyMode, ScrollMode
    text = message.text
    if connection:
        if HotkeyMode:
            pyautogui.hotkey(text.split("+"))
            HotkeyMode = False
        elif ScrollMode:
            try:
                steps = int(text)
                pyautogui.scroll(steps)
            except:
                bot.send_message(message.chat.id, "Try again, input error 'not int'")
            ScrollMode = False
        else:
            translited_text = ""
            for letter in text:
                if letter in ru:
                    translited_text += Translit[letter]
                else: translited_text += letter
            pyautogui.write(translited_text)
        #PrtSc(message)

@bot.message_handler(content_types = ["photo"])
def message_check(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("screenshot.png", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Catched")
    x,y = cv2Code.coords("screenshot.png")
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(x,y)
    PrtSc(message)


bot.polling(none_stop=True,interval = 0,long_polling_timeout = 200)