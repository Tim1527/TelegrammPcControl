import telebot, Telega,pyautogui
import cv2Code

connection = False
user_id = 0
HotkeyMode = False
ScrollMode = False

KEYBOARD_KEYS = str(['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright'])
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
        TL.Reply_btns("Connection established",True,4, "/LKM","/2LKM","/Enter","/Bcksp",
                      "/RKM","/Scroll","/Hotkey","/Shift","/PrtSc", "/Cam","/session")
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
    TL = Telega.Telega(message)

    global HotkeyMode
    if connection and message.from_user.id == id:
        TL.Reply_btns("Enter hotkey", True, 3, "Esc", "Alt+Shift","Alt+Tab","Win+r",
                      "Ctrl+Shift+Esc","ctrl+alt+del","Show_keyboard_keys") #По каким-то волшебным причинам Ctrl+Alt+Delete не равботает)
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
    TL = Telega.Telega(message)
    text = message.text
    if connection:
        if HotkeyMode:
            if text != "Show_keyboard_keys":
                pyautogui.hotkey(text.split("+"))
            else:
                bot.send_message(message.chat.id, KEYBOARD_KEYS)
            HotkeyMode = False
            TL.Reply_btns("Hotkey mode off", True, 4, "/LKM", "/2LKM", "/Enter", "/Bcksp", "/RKM", "/Scroll",
                          "/Hotkey", "/Shift", "/PrtSc", "/Cam", "/session")
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