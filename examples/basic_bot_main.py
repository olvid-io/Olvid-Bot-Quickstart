import asyncio

from olvid import datatypes, OlvidBot


class Bot(OlvidBot):
	# triggered every time a message arrive
	async def on_message_received(self, message: datatypes.Message):
		print(f"new message: {message.body}")

	# add a command
	@OlvidBot.command(regexp_filter="^!help")
	async def help_cmd(self, message: datatypes.Message):
		await message.reply("Help message ...")


async def main():
	# create bot instance (we assume you OLVID_CLIENT_KEY env variable or you have .client_key in current working directory)
	bot: Bot = Bot()

	print("Let's start ! 🏁")

	# wait forever
	await bot.wait_for_listeners_end()


# run asynchronous program
asyncio.run(main())
