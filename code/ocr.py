import PIL.Image, PIL.ImageGrab
import pytesseract
import pyautogui as p
import numpy as np
import re


FRAME_COLOR = np.array([37, 25, 22])
USER_COLOR = np.array([142, 115, 92])
TEXT_COLOR_WORLD = np.array([176, 176, 176])
TEXT_COLOR_CLAN = np.array([58, 209, 58])
TEXT_COLOR_ZONE = np.array([179, 121,  98])
TEXT_COLOR_IMMORTAL = np.array([32, 191, 251])
TEXT_COLOR_ITEM = np.array([248, 174, 117])
BLACK = 0
WHITE = 255
CUTOFF = np.ones(3) * 10
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
te_config = "-c tessedit_char_whitelist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.:!?@#<>$%^&*()[]_-+=/ '"


def get_chat_im(top):
    if not top:
        top = 165
    return PIL.ImageGrab.grab((1178, top, 1646, 910))


def get_bw_im(chat_im, channel):

    if channel == "world":
        text_color = TEXT_COLOR_WORLD
    elif channel == "clan":
        text_color = TEXT_COLOR_CLAN
    elif channel == "zone":
        text_color = TEXT_COLOR_ZONE
    elif channel == "immortal":
        text_color = TEXT_COLOR_IMMORTAL
    else:
        return None, None

    chat_data = np.array(chat_im)
    
    user_im_data = np.uint8(np.where((np.abs(chat_data - USER_COLOR) < CUTOFF).all(axis=2), BLACK, WHITE))
    bw_user_im = PIL.Image.fromarray(user_im_data)
    text_im_data = np.uint8(np.where((np.abs(chat_data - text_color) < CUTOFF).all(axis=2) | (np.abs(chat_data - TEXT_COLOR_ITEM) < CUTOFF).all(axis=2) , BLACK, WHITE))
    bw_text_im = PIL.Image.fromarray(text_im_data)
    
    # bw_user_im.save("temp1.png")
    # bw_text_im.save("temp2.png")
    return bw_user_im, bw_text_im


def read_im(bw_im):
    data = pytesseract.image_to_data(bw_im, output_type="dict", config=te_config)
    pos_top = []
    text = []
    for i in range(len(data["word_num"])):
        if data["word_num"][i] > 0 and data["top"][i] > 5:
            pos_top.append(data["top"][i])
            text.append(data["text"][i])
    return pos_top, text


def match_user_text(users, user_pos, texts, text_pos):

    msg = []
    user_pos.append(1000)
        
    user_ind = 0
    text_ind = 0

    while text_ind < len(text_pos) and user_ind < len(user_pos) - 1:
        if user_pos[0] > text_pos[text_ind]:
            text_ind += 1
            continue
        if text_pos[text_ind] < user_pos[user_ind + 1]:
            if text_ind == 0 or text_pos[text_ind] - text_pos[text_ind - 1] > 60:
                msg.append([users[user_ind], texts[text_ind]])
            else:
                msg[-1][1] += " " + texts[text_ind]
            text_ind += 1
        else:
            user_ind += 1
        
    msg = list(filter(lambda x: x[0] != "DiscordForward", msg))
    return msg


def ocr(channel="clan"):
    chat_history = p.locateOnScreen('../resources/chathistory.png', region=(1260, 245, 1440, 1000), confidence=0.75)
    top = chat_history.top if chat_history else None
    chat_im = get_chat_im(top)
    bw_user_im, bw_text_im = get_bw_im(chat_im, channel)
    user_pos, users = read_im(bw_user_im)
    text_pos, texts = read_im(bw_text_im)
    return match_user_text(users, user_pos, texts, text_pos)



