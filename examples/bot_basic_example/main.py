import asyncio

from olvid import datatypes, OlvidBot, tools


class Bot(OlvidBot):
	# triggered every time a message arrive
	async def on_message_received(self, message: datatypes.Message):
		print(f"new message: {message.id}: {message.body}")

	async def on_message_body_updated(self, message: datatypes.Message, previous_body: str):
		print(f"message updated: {message.id}: {previous_body} -> {message.body}")

	async def on_message_reaction_added(self, message: datatypes.Message, reaction: datatypes.MessageReaction):
		print(f"reaction added: {message.id}: {reaction.reaction}")

	async def on_message_reaction_updated(self, message: datatypes.Message, reaction: datatypes.MessageReaction, previous_reaction: datatypes.MessageReaction):
		print(f"reaction updated: {message.id}: {previous_reaction.reaction} -> {reaction.reaction}")

	# triggered when you enter a group or have a new contact
	async def on_discussion_new(self, discussion: datatypes.Discussion):
		print(f"new discussion: {discussion.title}")

	# add a command
	@OlvidBot.command(regexp_filter="^!help")
	async def cmd(self, message: datatypes.Message):
		await message.reply("Help message")


async def main():
	# create bot instance
	bot: Bot = Bot()

	# create a bot to automatically accept every invitation you receive
	auto_invitation_bot: tools.AutoInvitationBot = tools.AutoInvitationBot()

	print("Let's start ! 🏁")

	# wait forever
	await bot.wait_for_listeners_end()

	# clean bots
	await auto_invitation_bot.stop()


# run asynchronous program
asyncio.run(main())
