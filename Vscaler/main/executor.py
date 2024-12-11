from Vscaler import bot
from Vscaler.plugins.database import get_user_settings
from Vscaler.plugins.progress import work_progress_barg
from hydrogram.types import Message
from hydrogram import filters
import os
import subprocess
import asyncio
import re


async def progress_callback(current, total, message):
    """
    Updates the progress bar for file download.
    """
    pct = int((current / total) * 100)
    progress_bar = work_progress_barg(f"{pct}%")
    await message.edit_text(f"Downloading video...\n{progress_bar} {pct}%")


@bot.on_message(filters.command("upscale"))
async def upscale_vid(client, message: Message):
    user_id = message.from_user.id
    settings = get_user_settings(user_id)

    if not settings:
        await message.reply("No settings found. Please configure using /settings.")
        return

    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply("Reply to a video to upscale.")
        return

    # Set input and output paths
    input_path = f"{user_id}_input.mp4"
    output_path = f"{user_id}_output.mp4"

    # Initial progress message
    progress_message = await message.reply("Starting download...")

    # Download the video with progress callback
    await message.reply_to_message.download(
        input_path,
        progress=progress_callback,
        progress_args=(progress_message,),
    )

    # Notify that download is complete
    await progress_message.edit_text("Download complete. Starting upscale process...")

    # Build the command for Video2X
    command = ["video2x", "-i", input_path, "-o", output_path]
    if settings['framework'] == "realesrgan":
        command.extend(["-f", settings['framework'], "-r", "4", "-m", settings['model']])
    elif settings['framework'] == "libplacebo":
        command.extend([
            "-f", settings['framework'], 
            "-s", settings['model'], 
            "-w", str(settings['width']), 
            "-h", str(settings['height'])
        ])

    try:
        # Start the subprocess and monitor progress
        process = await asyncio.create_subprocess_exec(
            *command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        while True:
            output = await process.stdout.readline()
            if not output:
                break

            # Check for progress info (update this logic based on Video2X output format)
            output_str = output.decode("utf-8").strip()
            match = re.search(r"Progress: (\d+)%", output_str)
            if match:
                progress = int(match.group(1))
                progress_bar = work_progress_barg(f"{progress}%")
                await progress_message.edit_text(
                    f"Upscaling...\n{progress_bar} {progress}%"
                )

        # Wait for the process to finish
        await process.communicate()

        if process.returncode != 0:
            stderr = (await process.stderr.read()).decode("utf-8")
            await progress_message.edit_text(f"Upscale failed:\n{stderr}")
            return

        # Notify user and send the upscaled video
        await message.reply_video(
            output_path,
            caption=f"Upscaled using model: {settings['model']} "
                    f"({settings['width']}x{settings['height']})!"
        )
    finally:
        # Clean up temporary files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
