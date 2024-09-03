from aiohttp import web
from olvid import OlvidClient


SERVER_HOSTNAME: str = "0.0.0.0"
SERVER_PORT: int = 8080


async def webhook_handler(request: web.Request) -> web.Response:
	client = OlvidClient()
	body: str = await request.text()
	if not body.strip():
		return web.Response(status=400)
	print(f"Broadcasting message: {body}")

	async for discussion in client.discussion_list():
		await discussion.post_message(await request.text())
	return web.Response(status=200)


app = web.Application()
app.add_routes([web.post("/", webhook_handler)])
web.run_app(app, host=SERVER_HOSTNAME, port=SERVER_PORT)
