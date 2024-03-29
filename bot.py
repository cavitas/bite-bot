from pyrogram.errors import FloodWait, SlowmodeWait, ChatWriteForbidden, UserBannedInChannel, ReactionInvalid
from pyrogram import Client, filters, enums
import datetime
import asyncio
import random
import time
import cfg


chance = list(range(1, cfg.chance+1))
app = Client(
    name="alice",
    api_id=cfg.api_id,
    api_hash=cfg.api_hash,
    device_model=cfg.device_model,
    app_version=cfg.app_version,
    system_version=cfg.system_version,
    lang_code=cfg.lang_code
)
now = datetime.datetime.now()
n = str(now).replace(" ", "_").replace(":", "-").split(".")[0]
log_path = f"logs/log_{n}.txt"

def write_log(info):
    print(info)
    f = open(log_path, "at", encoding='utf-8', errors='ignore')
    f.write(str(info)+"\n")
    f.close()

ignorechats = {}
f = open("words.txt", encoding="utf-8", errors="ignore")
data = f.read()
f.close()
my_id = cfg.my_id
msgs = [ms for ms in data.split("\n") if ms]
ignoreusers = cfg.ignoreusers
chats = cfg.chats

@app.on_message(filters.all)
async def hello(client, message):
    msg_id = message.id
    user = message.from_user
    if user:
        try:
            bot = message.from_user.is_bot
        except:
            bot = False
        time_now = int(time.time())
        u_id = user.id
        first_name = user.first_name
        username = user.username
        chat_id = message.chat.id
        msg = message.text
        try:
            ignorechats[chat_id]
        except KeyError:
            ignorechats[chat_id] = 0
        ch = random.choice(chance)
        if chat_id > 0:
            write_log("*"*50)
            write_log(f"Айди чата: {chat_id}")
            write_log(f"От кого: [{u_id}]({username}){first_name}")
            write_log(f"Сообщение: {msg}")
            
        if message.reply_to_message:
            if message.reply_to_message.from_user:
                rep_id = message.reply_to_message.from_user.id
                if rep_id == my_id:
                    ch = 1
                    write_log("*"*50)
                    write_log(f"Айди чата: {chat_id}")
                    write_log(f"От кого: [{u_id}]({username}){first_name}")
                    write_log(f"Сообщение: {msg}")
        if ch == 1 and not bot and message.from_user.id not in ignoreusers and message.from_user.id > 0 and chat_id not in chats:
            await app.read_chat_history(chat_id)
            if ignorechats[chat_id] < time_now:
                try:
                    await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
                    await asyncio.sleep(random.randint(3, 5))
                    msg = random.choice(msgs)
                    await app.send_message(chat_id, msg, reply_to_message_id=msg_id)
                except SlowmodeWait as e:
                    write_log(e)
                    ignorechats[chat_id] = time_now+e.value+2
                except FloodWait as e:
                    write_log(e)
                    ignorechats[chat_id] = time_now+e.value+2
                except ChatWriteForbidden:
                    try:
                        await app.send_reaction(chat_id, msg_id, random.choice(cfg.reactions))
                    except FloodWait as e:
                        write_log(e)
                        ignorechats[chat_id] = time_now+e.value+30
                    except Exception as e:
                        write_log(e)
                except UserBannedInChannel:
                    try:
                        await app.send_reaction(chat_id, msg_id, random.choice(cfg.reactions))
                    except FloodWait as e:
                        write_log(e)
                        ignorechats[chat_id] = time_now+e.value+30
                    except Exception as e:
                        write_log(e)


app.run()
