import asyncio

from olvid import datatypes, OlvidBot


class EchoBot(OlvidBot):
	# triggered every time a message arrive
	async def on_message_received(self, message: datatypes.Message):
		print(f"new message: {message.body}")
		await message.reply(body=message.body)


async def main():
	bot: EchoBot = EchoBot()

	print("Let's start ! 🏁")

	# wait forever
	await bot.wait_for_listeners_end()


# run asynchronous program
asyncio.run(main())
