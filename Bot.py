import telebot
import Telega
import pyautogui
import pickle
import cv2Code

connection = False
user_id = 0
HotkeyMode = False
ScrollMode = False

with open("Keyboard_keys.txt") as f:
    KEYBOARD_KEYS = f.read()

with open(r"teletoken.txt") as token:
    token = token.readline()

with open('Translit.pkl', 'rb') as f:
    Translit = pickle.load(f)

bot = telebot.TeleBot(token)


Session_name = input("Name: ")
Session_passw = input("Password: ")
print(f"Session {Session_name} started")

#эхо функция
@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id,"Bot enabled")
    TL = Telega.Telega(message)
    TL.Reply_btns("///",True,1,"/session")

#Проверка на доступ
@bot.message_handler(commands = ["session"])
def sesion_connect(message):
    if not(connection):
        bot.send_message(message.chat.id,f"Session name: {Session_name}")
        password_check(message)
    if connection:
        TL = Telega.Telega(message)
        TL.Reply_btns(f"Session name: {Session_name}",True,1, "/disconnect")

#запрашивает пароль и через next_step_handler вызывает функцию проверки пароля
def password_check(message):
    bot.send_message(message.chat.id,"Enter password:")
    bot.register_next_step_handler(message, password_enter)

#Функция проверки пароля
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

#Нажатие кнопки Enter
@bot.message_handler(commands = ["Enter"])
def enter(message):
    pyautogui.press('enter')

#Нажатие кнопки Shift
@bot.message_handler(commands = ["Shift"])
def shift(message):
    pyautogui.press('shift')

#Нажатие кнопки Backspace
@bot.message_handler(commands = ["Bcksp"])
def bcksp(message):
    pyautogui.press('backspace')

#Отключение пользователя от бота
@bot.message_handler(commands = ["disconnect"])
def disconnect(message):
    global connection, id
    if message.from_user.id == id:
        TL = Telega.Telega(message)
        TL.Reply_btns("Disconnected", True, 1, "/session", "/start")
        connection = False
        id = 0

#Делает скриншот, сохраняет его и отправляет пользователю.
@bot.message_handler(commands = ["PrtSc"])
def prtsc(message):
    if connection and message.from_user.id == id:
        screen = pyautogui.screenshot('screenshot1.png')
        cv2Code.add_cursor('screenshot1.png')
        with open("screenshot1.png","rb") as screen:
            bot.send_photo(message.chat.id, screen)

#Делает снимок со всех камер, сохраняет его и отправляет пользователю.
@bot.message_handler(commands = ["Cam"])
def cam(message):
    if connection and message.from_user.id == id:
        for i in range(4,-1,-1):
            if cv2Code.PhotoCam(i):
                with open("cam_old.png", "rb") as screen:
                    bot.send_photo(message.chat.id, screen,timeout=100)

#Нажатие левой кнопки мыши
@bot.message_handler(commands = ["LKM"])
def lkm(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Lclick'")
        pyautogui.click(button='left')
        prtsc(message)

#Двойное нажатие левой кнопки мыши
@bot.message_handler(commands = ["2LKM"])
def double_lkm(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'2Lclick'")
        pyautogui.click(clicks = 2,button='left')
        prtsc(message)

#Нажатие правой кнопки мыши
@bot.message_handler(commands = ["RKM"])
def rkm(message):
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"'Rclick'")
        pyautogui.click(button='right')
        prtsc(message)

#Включает режим ввода горячих клавиш
@bot.message_handler(commands = ["Hotkey"])
def hotkey(message):
    TL = Telega.Telega(message)

    global HotkeyMode
    if connection and message.from_user.id == id:
        TL.Reply_btns("Enter hotkey", True, 3, "Esc", "Alt+Shift","Alt+Tab","Win+r",
                      "Ctrl+Shift+Esc","ctrl+alt+del","Show_keyboard_keys") #По каким-то волшебным причинам Ctrl+Alt+Delete не равботает)
        HotkeyMode = True

#Включает режим пролистывания страницы
@bot.message_handler(commands = ["Scroll"])
def scroll(message):
    global ScrollMode
    if connection and message.from_user.id == id:
        bot.send_message(message.chat.id,"Enter Steps (>0 up, <0 down)")
        ScrollMode = True

#Обработчик текстовых сообщений
@bot.message_handler(content_types = ["text"])
def message_check(message):
    global HotkeyMode, ScrollMode
    TL = Telega.Telega(message)
    text = message.text
    if connection:
        if HotkeyMode: #Обработка горячих клавиш
            if text != "Show_keyboard_keys":
                pyautogui.hotkey(text.split("+"))
            else:
                bot.send_message(message.chat.id, KEYBOARD_KEYS)
            HotkeyMode = False
            TL.Reply_btns("Hotkey mode off", True, 4, "/LKM", "/2LKM", "/Enter",
                          "/Bcksp", "/RKM", "/Scroll", "/Hotkey", "/Shift", "/PrtSc", "/Cam", "/session")
        elif ScrollMode: #Пролистывание страницы
            try:
                steps = int(text)
                pyautogui.scroll(steps)
            except ValueError:
                bot.send_message(message.chat.id, "Try again, input error 'not int'")
            except:
                bot.send_message(message.chat.id, "Fatal error, shutting down.")
                raise
            ScrollMode = False
        else: #Печатает текст отправленный пользователем
            translited_text = ""
            for letter in text:
                if letter.lower in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                    translited_text += Translit[letter]
                else: translited_text += letter
            pyautogui.write(translited_text)
        #PrtSc(message)

#обрабатывает фото отправленное пользователем с помощью cv2Code
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
    prtsc(message)


bot.polling(none_stop=True,interval = 0,long_polling_timeout = 200)