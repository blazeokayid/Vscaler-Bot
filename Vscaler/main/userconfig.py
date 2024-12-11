from hydrogram import Client,filters
from hydrogram.types import InlineKeyboardMarkup,InlineKeyboardButton,Message,CallbackQuery
from Vscaler.plugins.database import get_user_settings,save_user_settings
from hydrogram.enums.parse_mode import ParseMode
from Vscaler import bot


@bot.on_message(filters.command("settings"))
async def settings(client, message: Message):
    user_id = message.from_user.id

    settings = get_user_settings(user_id) | {"model":"Anime4k", "width": 1920, "height": 1080}

    stext = f"""<b>Settings</b> 
    <b>Hey </b> {message.from_user.first_name}\n
    <b>Model: </b>{settings['model']} \n
    <b>Width: </b>{settings['width']} \n
    <b>Height: </b>{settings['height']} \n"""
    
    sbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Model", callback_data="change_model")]
            [InlineKeyboardButton("Height", callback_data="change_height"),
            InlineKeyboardButton("Width", callback_data="change_width")]
            [InlineKeyboardButton("Save", callback_data="save_changes")]
        ]
        )
    
    await message.reply_text(text=stext, reply_markup=sbtn, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@bot.on_message(filters.command("settings") & filters.regex("settings"))
async def settings(client, message: Message):
    user_id = message.from_user.id

    settings = get_user_settings(user_id) | {"model":"Anime4k", "width": 1920, "height": 1080}

    stext = f"""<b>Settings</b> 
    <b>Hey </b> {message.from_user.first_name}\n
    <b>Model: </b>{settings['model']} \n
    <b>Width: </b>{settings['width']} \n
    <b>Height: </b>{settings['height']} \n"""
    
    sbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Model", callback_data="change_model")]
            [InlineKeyboardButton("Height", callback_data="change_height"),
            InlineKeyboardButton("Width", callback_data="change_width")]
            [InlineKeyboardButton("Save", callback_data="save_changes")]
        ]
        )
    
    await message.reply_text(text=stext, reply_markup=sbtn, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@bot.on_callback_query(filters.regex("change_model"))
async def change_model(client, callback_query:CallbackQuery):
    cmbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("realesrgan", callback_data="smodel_realesrgan"),
            InlineKeyboardButton("libplacebo", callback_data="smodel_libplacebo")],
            [InlineKeyboardButton("Back", callback_data="settings")]
        ]
        )
    
    await callback_query.message.edit_text("Select Model FrameWork",reply_markup=cmbtn)


@bot.on_callback_query(filters.regex("smodel_"))
async def set_framwork(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    framwork =callback_query.data.split("_")[-1]
    settings = get_user_settings(user_id) or {}
    settings["framework"] = framwork
    save_user_settings(user_id,settings)
    btnkey = InlineKeyboardMarkup([InlineKeyboardButton("Back",callback_data="settings")])
    await callback_query.message.edit_text("framework Set TO: {framework}",reply_markup=btnkey)


@bot.on_callback_query(filters.regex("smodel_libplacebo"))
async def select_anime4k(client, callback_query: CallbackQuery):
    cmbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Anime4k 1080p", callback_data="cmodelto_anime4k-v4-a")]
            [InlineKeyboardButton("Anime4k 720p", callback_data="cmodelto_anime4k-v4-b"),
             InlineKeyboardButton("Anime4k 480p", callback_data="cmodelto_anime4k-v4-c")]
            [InlineKeyboardButton("Anime4k a+a", callback_data="cmodelto_anime4k-v4-a+a"),
             InlineKeyboardButton("Anime4k b+b", callback_data="cmodelto_anime4k-v4-b+b")]
            [InlineKeyboardButton("Anime4k c+a", callback_data="cmodelto_anime4k-v4-c+a")],
            [InlineKeyboardButton("Back", callback_data="settings")]
        ]
        )
    
    await callback_query.message.edit_text("Select Model",reply_markup=cmbtn)


@bot.on_callback_query(filters.regex("smodel_realesrgan"))
async def select_realesrgan(client, callbackquery: CallbackQuery):
    scrbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("realesr animevideov3",callback_data="cmodelto_realesr-animevideov3")],
            [InlineKeyboardButton("realesrgan plus", callback_data="cmodelto_realesrgan-plus"),
             InlineKeyboardButton("realesrgan-plus anime",callback_data="cmodelto_realesrgan-plus-anime")],
            [InlineKeyboardButton("Back", callback_data="settings")]
        ]
    )
    await callbackquery.message.edit_text("Select Model", reply_markup=scrbtn)


@bot.on_callback_query(filters.regex("cmodelto_"))
async def set_model(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    model =callback_query.data.split("_")[-1]
    settings = get_user_settings(user_id) or {}
    settings["model"] = model
    save_user_settings(user_id,settings)
    btnkey = InlineKeyboardMarkup([InlineKeyboardButton("Back",callback_data="settings")])
    await callback_query.message.edit_text("Model Set TO: {model}",reply_markup=btnkey)


@bot.on_callback_query(filters.regex("change_width"))
async def chawidth(client,callback_query:CallbackQuery):
    chbtn = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("1920", callback_data="setwidth_1920")],
            [InlineKeyboardButton("1280", callback_data="setwidth_1280"),
            InlineKeyboardButton("960", callback_data="setwidth_960")],
            [InlineKeyboardButton("Back", callback_data="settings")]
        ]
    )

    await callback_query.message.edit_text("Select Width", reply_markup=chbtn)


@bot.on_callback_query(filters.regex("setwidth_"))
async def set_width(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    width =callback_query.data.split("_")[-1]
    settings = get_user_settings(user_id) or {}
    settings["width"] = width
    save_user_settings(user_id,settings)
    btnkey = InlineKeyboardMarkup([InlineKeyboardButton("Back",callback_data="settings")])
    await callback_query.message.edit_text("Width Set TO: {width}",reply_markup=btnkey)
    


@bot.on_callback_query(filters.regex("change_height"))
async def chaheight(client, callback_query:CallbackQuery):
    hebtn = InlineKeyboardButton(
        [
            [InlineKeyboardButton("1080",callback_data="setheight_1080")],
            [InlineKeyboardButton("720", callback_data="setheight_720"),
            InlineKeyboardButton("480", callback_data="setheight_480")],
            [InlineKeyboardButton("Back", callback_data="settings")]
        ]
    )

    await callback_query.message.edit_text("Select height", reply_markup=hebtn)


@bot.on_callback_query(filters.regex("setheight_"))
async def set_height(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    height =callback_query.data.split("_")[-1]
    settings = get_user_settings(user_id) or {}
    settings["height"] = height
    save_user_settings(user_id,settings)
    btnkey = InlineKeyboardMarkup([InlineKeyboardButton("Back",callback_data="settings")])
    await callback_query.message.edit_text("Height Set TO: {height}",reply_markup=btnkey)

@bot.on_callback_query(filters.regex("save_changes"))
async def save_settings(client, callback_query:CallbackQuery):
    await callback_query.message.reply("settings Saved !")