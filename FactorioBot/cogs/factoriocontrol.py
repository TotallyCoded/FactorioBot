import os
import io
import asyncio
from discord.ext import commands
import discord
import pyautogui as p
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from FactorioBot import config


class FactorioControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_queue = []
        self.currently_executing = False

    '''Queue functions'''

    async def enqueue(self, message_id, func_name, *args):
        # Adds the message id, function name and arguments as a flat list to end of queue
        self.command_queue.append([message_id, func_name, *args])

        # Starts executing queue if not already
        if not self.currently_executing:
            await self.execute_command_queue()

    async def execute_command_queue(self):
        # Sets the currently_executing flag so that enqueue doesn't launch multiple of these functions
        self.currently_executing = True

        while self.command_queue:
            # Gets next function and args to execute
            current_command = self.command_queue.pop()

            # Calls function which is first index and unpacks the arguments and pass them into the function.
            await current_command[0](*current_command[1:])

            await self.screenshot(current_command[1])
        self.currently_executing = False

    @commands.command()
    async def walk(self, ctx, direction, length: int):

        key = None

        if direction == "north" or direction == "n":
            key = "w"
        elif direction == "south" or direction == "s":
            key = "s"
        elif direction == "west" or direction == "w":
            key = "a"
        elif direction == "east" or direction == "e":
            key = "d"

        if key is not None and 0 < length < 11:
            await self.enqueue(self.exec_walk, ctx, direction, key, length)

        else:
            await ctx.send("Invalid direction or length limit reached.")

    @commands.command()
    async def sayInGame(self, ctx, *, message):
        if len(message) < 100:
            await self.enqueue(self.exec_sayInGame, ctx, message)

    # Test command
    @commands.command()
    async def long_command(self, ctx):
        print("long command")
        await self.enqueue(self.exec_long_command, ctx, "dave")

    @commands.command()
    async def mod_output_test(self, ctx, *, message):
        await self.enqueue(self.exec_mod_output_test, ctx, message)

    '''Executes the commands in factorio'''

    async def exec_walk(self, ctx, direction, key, length):
        await ctx.send("Moving {0} for {1} seconds.".format(direction, length))
        p.keyDown(key)
        await asyncio.sleep(length)
        p.keyUp(key)

    async def exec_sayInGame(self, ctx, message):
        p.press("`")
        p.typewrite(message, interval=0)
        p.press("enter")
        await ctx.send("Message sent.")

    # Test exec
    async def exec_long_command(self, ctx, bob):
        await asyncio.sleep(2)
        await ctx.send(bob)

    async def exec_mod_output_test(self, ctx, message):
        observer: Observer = self.setup_read_txt()
        p.press("`")
        p.typewrite("/write_test_d " + message, interval=0)
        p.press("enter")
        await ctx.send(await self.read_ouput_txt(observer))

    # Helper functions
    async def screenshot(self, ctx):
        shot = p.screenshot()  # Returns a PIL Image
        imgbytes = io.BytesIO()

        shot.save(imgbytes, format="JPEG")

        imgbytes.seek(0)
        await ctx.send(file=discord.File(fp=imgbytes, filename="file.jpg"))

    def setup_read_txt(self):
        dirpath = config.factorio_user_data + "\script-output"
        dirpath = os.path.expandvars(dirpath)
        path = dirpath + '\output.txt'

        print(path)

        if os.path.exists(path):
            observer = Observer()
            read_on_modified = ReadOnModified(path, observer)
            observer.schedule(read_on_modified, dirpath, recursive=False)
            observer.start()
            return observer

    async def read_ouput_txt(self, observer: Observer):
        path = config.factorio_user_data + '\script-output\output.txt'
        path = os.path.expandvars(path)

        while observer.isAlive() is True:
            await asyncio.sleep(0.1)
        print(observer.isAlive())
        with open(path) as fp:
            return fp.read()


class ReadOnModified(FileSystemEventHandler):

    def __init__(self, file_to_check, observer):
        self.file_to_check = file_to_check
        self.observer = observer

    def on_modified(self, event):
        super(ReadOnModified, self).on_modified(event)

        if event.src_path == self.file_to_check:
            self.observer.stop()


# Setups cog
def setup(bot):
    bot.add_cog(FactorioControl(bot))
