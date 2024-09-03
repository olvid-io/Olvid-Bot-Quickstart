import asyncio

from olvid import datatypes, OlvidClient


async def main():
	# create client instance (we assume you OLVID_CLIENT_KEY env variable or you have .client_key in current working directory)
	client: OlvidClient = OlvidClient()

	# show current identity
	identity: datatypes.Identity = await client.identity_get()
	print(f"Current identity: {identity.id}: {identity.display_name}")


# run asynchronous program
asyncio.run(main())
