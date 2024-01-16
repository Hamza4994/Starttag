#Copyright ©️ 2022 TeLe TiPs. All Rights Reserved
#You are free to use this code in any of your project, but you MUST include the following in your README.md (Copy & paste)
# ##Credits - [Ping All Telegram bot by TeLe TiPs] (https://github.com/teletips/PingAllBot-teletips)

# Changing the code is not allowed! Read GNU AFFERO GENERAL PUBLIC LICENSE: https://github.com/teletips/PingAllBot-teletips/blob/main/LICENSE

from pyrogram import Client, filters
from pyrogram.types import Message
import os
import requests
import yt_dlp
from pyrogram import filters
from youtube_search import YoutubeSearch
import asyncio
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

teletips=Client(
    "PingAllBot",
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    bot_token = os.environ["BOT_TOKEN"]
)

chatQueue = []

stopProcess = False

@teletips.on_message(filters.command(["ping","all"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 50:
        await message.reply("⛔️ | I'm already working on my maximum number of 50 chats at the moment. Please try again shortly.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 | There's already an ongoing process in this chat. Please /stop to start a new one.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.command[1]
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in teletips.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await teletips.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(10) 
              i+=10
            except IndexError:
              try:
                await teletips.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅ | Successfully mentioned **total number of {i} members**.\n❌ | Bots and deleted accounts were rejected.") 
          else:
            await message.reply(f"✅ | Successfully mentioned **{i} members.**\n❌ | Bots and deleted accounts were rejected.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)
      

@teletips.on_message(filters.command(["song", "music"]))
def song(client, message):

    message.delete()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chutiya = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    m = message.reply("» ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ.")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        # print(results)
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)

        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "sᴏɴɢ ɴᴏᴛ ғᴏᴜɴᴅ ᴏɴ ʏᴏᴜᴛᴜʙᴇ"
        )
        print(str(e))
        return
    m.edit("» ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ..")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**ᴛɪᴛʟᴇ :** {title[:25]}\n**ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}`\n**ᴠɪᴇᴡs :** `{views}`\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ​ »** {chutiya}"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        message.reply_audio(
            audio_file,
            caption=rep,
            thumb=thumb_name,
            title=title,
            duration=dur,
        )
        m.delete()
    except Exception as e:
        m.edit(
            f"» ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴇʀʀᴏʀ"
        )
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
        
@teletips.on_message(filters.command(["stop","cancel"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await teletips.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | There is no ongoing process to stop.")
      else:
        stopProcess = True
        await message.reply("🛑 | Stopped.")
    else:
      await message.reply("👮🏻 | Sorry, **only admins** can execute this command.")
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command(["admins","staff"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Owner\n└ {owner.mention}\n\n👮🏻 Admins\n"
      else:
        text2 += f"👑 Owner\n└ @{owner.username}\n\n👮🏻 Admins\n"
    except:
      text2 += f"👑 Owner\n└ <i>Hidden</i>\n\n👮🏻 Admins\n"
    if len(adminList) == 0:
      text2 += "└ <i>Admins are hidden</i>"  
      await teletips.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **Total number of admins**: {lenAdminList}\n❌ | Bots and hidden admins were rejected."  
      await teletips.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@teletips.on_message(filters.command("bots"))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in teletips.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LIST - {message.chat.title}**\n\n🤖 Bots\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | **Total number of bots**: {lenBotList}"  
      await teletips.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)

@teletips.on_message(filters.command("start") & filters.private)
async def start(client, message):
  text = f'''
Heya {message.from_user.mention},
My name is **PingAll**. I'm here to help you to get everyone's attention by mentioning all members in your chat.

I have some additional cool features and also I can work in channels.

Don't forget to join my [channel](http://t.me/teletipsofficialchannel) to recieve information on all the latest updates.

Hit /help to find out my commands and the use of them.
'''

buttons = [
    [
        InlineKeyboardButton(
            text="Owner",
            url="t.me/CerennyFlexQ",
    [
        InlineKeyboardButton(
            text="Aᴅᴅ Mᴇ ᴛᴏ Yᴏᴜʀ Gʀᴏᴜᴘ",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs", callback_data="Main_help"),
    ],
    

]


@teletips.on_message(filters.command("help"))
async def help(client, message):
  text = '''
Hey, let's have a quick look at my commands.

**Commands**:
- /ping "input": <i>Mention all members.</i>
- /remove: <i>Remove all deleted accounts.</i>
- /admins: <i>Mention all admins.</i>
- /bots: <i>Get the full bot list.</i>
- /stop: <i>Stop an on going process.</i>

If you have any questions on how to use me, feel free to ask in my [support group](https://t.me/teletipsofficialontopicchat). More on my [page](https://github.com/teletips/PingAllBot-TeLeTiPs).
'''
  await teletips.send_message(message.chat.id, text, disable_web_page_preview=True)

print("PingAll is alive!")  
teletips.run()
 
#Copyright ©️ 2021 TeLe TiPs. All Rights Reserved 
