from aiohttp import web


class HealthServer:

    def __init__(self, port: int = 8080):
        self.port = port

        self.app = web.Application()
        self.app.router.add_get("/health", self._handle_health)
        self._runner: web.AppRunner | None = None

    async def _handle_health(self, _: web.Request) -> web.Response:
        return web.Response(text="OK", status=200)

    async def start(self) -> None:
        self._runner = web.AppRunner(self.app)
        await self._runner.setup()

        site = web.TCPSite(self._runner, "0.0.0.0", self.port)
        await site.start()

    async def stop(self) -> None:
        if self._runner:
            await self._runner.cleanup()
