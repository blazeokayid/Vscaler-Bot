import asyncio
from Vscaler import bot,bot_verion,config_dict,users,LOGGER
from hydrogram.types import InlineKeyboardButton,InlineKeyboardMarkup,Message
from hydrogram.enums.parse_mode import ParseMode
from hydrogram import filters




@bot.on_message(filters.command('start') & filters.private)
async def start(client,message: Message):
    user_id = message.from_user.id
    if not users.find_one({"_id": user_id}):
        users.insert_one({"_id": user_id, "username": message.from_user.username, "tasks": []})
    starttext = f""" <i>Hey <i>{message.from_user.mention}, \n
    It Is Powerful Video \n
    Upscaling Bot Created \n
    Using Video2x Use Help \n
    Command To Know How To Use."""
    startbutton = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Help',callback_data='help'),
            InlineKeyboardButton('About',callback_data='about'),
        ],
        [InlineKeyboardButton('Update Channel', url=config_dict.UPDATE_CHANNEL)]
    ])
    await message.reply_text(text=starttext, reply_markup=startbutton,parse_mode=ParseMode.HTML,disable_web_page_preview=True,)


@bot.on_message(filters.command('about') & filters.private)
async def about(client,message: Message):
    abouttext = f"""<b>My Name:</b> Vsacler Bot | Video Upscaler Bot\n
    <b>Verion: <b>{bot_verion}
    <b>Owner: <b>{config_dict.OWNER_UNAME}
    <b>Developer:</b> @Balapriyan  \n"""
    aboutbutton = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Help',callback_data='help'),
            InlineKeyboardButton('Home',callback_data='home'),
        ],
        [InlineKeyboardButton('Update Channel', url=config_dict.UPDATE_CHANNEL)]
    ])
    await message.reply_text(text=abouttext, reply_markup=aboutbutton,parse_mode=ParseMode.HTML,disable_web_page_preview=True,)



async def start_services():
    print("-------------------- Initializing Telegram Bot --------------------")
    await bot.start()


loop = asyncio.get_event_loop()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass