import random, asyncio, time, os
import pyautogui as p
from difflib import SequenceMatcher
import discord
from discord.ext import tasks
from ocr import ocr

if os.path.exists("resources/token.txt"):
    with open("resources/token.txt", 'r') as f:
        TOKEN = f.readlines()[0]
else:
    print("save your discord bot token in resource/token.txt")
    exit()

if os.path.exists("resources/channelID.txt"):
    with open("resources/channelID.txt", 'r') as f:
        CHANNEL_ID = int(f.readlines()[0])
else:
    CHANNEL_ID = ''


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = None
        self.last_user = ''
        self.last_msg = ''
        self.msg_to_send = []
        self.loop_counter = time.time()
        self.counter_reset = 500

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.dc_to_game.start()
#        self.game_to_dc.start()

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        if CHANNEL_ID:
            self.channel = self.get_channel(CHANNEL_ID)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content == "--config receiving channel":
            self.channel = message.channel
            with open("resources/channelID.txt", "w") as f:
                f.write(str(message.channel.id))
            return

        if len(message.content) > 1000:
            await self.channel.send(f"Message from {message.author.nick} is too long. Maximum length is 1000 characters (including space).")
            return
        self.msg_to_send.append(f"{message.author.nick}: {message.content}")
        print(f'From discord  -  {message.author.nick}: {message.content}')


    @tasks.loop(seconds=4)
    async def dc_to_game(self):

##        if p.locateOnScreen('resources/ok.png', region=(1000, 700, 1250, 800), confidence=0.8):
##                p.click(1050 + int(random.random() * 150), 720 + int(random.random() * 60))
##                time.sleep(0.5 + random.random()*0.3)
        if p.locateOnScreen('resources/cancel.png', region=(650, 700, 950, 800), confidence=0.8):
                p.click(700 + int(random.random() * 200), 720 + int(random.random() * 60))
                time.sleep(0.5 + random.random()*0.3)

        if time.time() > self.counter_reset + self.loop_counter:
            self.loop_counter = time.time()
            self.counter_reset = 400 + int(random.random() * 200)
            p.click(50 +int(random.random() * 200), 280 + int(random.random() * 40))
            time.sleep(0.5 + random.random()*0.5)
            p.click(50 +int(random.random() * 200), 280 + int(random.random() * 40))
##            p.click(1830 + int(random.random() * 40), 30 + int(random.random() * 40))
##            time.sleep(random.random()*0.2 + 0.1)
##            key_to_press = ['w', 'd', 's'][int(random.random() * 2.99)]
##            p.keyDown(key_to_press)
##            time.sleep(random.random()*0.1 + 0.1)
##            p.keyUp(key_to_press)
##            time.sleep(random.random()*0.1 + 0.05)
##            p.press('enter')
##            time.sleep(random.random()*0.2 + 0.1)
##            p.click(100 + int(random.random() * 300), 800 + int(random.random() * 160))
            time.sleep(random.random()*0.2 + 0.1)
            
        msg = self.to_send()
        if msg:
            await self.channel.send('\n'.join(map(lambda x: "**" + ":**  ".join(x), msg)))

        num_msg_to_send = len(self.msg_to_send)
        if num_msg_to_send > 0:
#            for i in range(max(3, num_msg_to_send)):
            sending_msg = self.msg_to_send.pop(0)
            await self.send_in_game(sending_msg)
#                await asyncio.sleep(3.5)

        
    @dc_to_game.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()


##    @tasks.loop(seconds=12)
##    async def game_to_dc(self):
##
##        msg = await self.to_send()
##        if msg:
##            await self.channel.send('\n'.join(map(lambda x: "**" + ":**  ".join(x), msg)))
##        
##
##    @game_to_dc.before_loop
##    async def before_my_task(self):
##        await self.wait_until_ready()


    def to_send(self):
        msg = ocr(channel="clan")
        for i in range(len(msg) - 1, -1, -1):
            if msg[i][0] == self.last_user and SequenceMatcher(a=msg[i][1].replace(' ', ''), b=self.last_msg).ratio() > 0.9:
                msg = msg[i+1:]
                break
        if msg:
            self.last_user = msg[-1][0]
            self.last_msg = msg[-1][1].replace(' ', '')
        return msg

    async def send_in_game(self, msg):
        p.click(1200 + int(random.random() * 100), 950 + int(random.random() * 50))
        await asyncio.sleep(random.random()*0.2 + 0.1)
        while len(msg) > 115:
            p.write(msg[:110] + " (cont.)")
            msg = msg[110:]
            await asyncio.sleep(0.2 + random.random() * 0.1)
            p.press('enter')
            await asyncio.sleep(0.5)
            p.press('backspace', presses=118)
            await asyncio.sleep(3)
        p.write(msg)
        await asyncio.sleep(0.2 + random.random() * 0.1)
        p.press('enter')
        await asyncio.sleep(0.2)
        p.press('backspace', presses=len(msg))


if __name__ == '__main__':
    p.getWindowsWithTitle('Diablo Immortal')[0].activate()
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(TOKEN)
