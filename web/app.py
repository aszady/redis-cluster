import asyncio

import redis.asyncio
import tornado.log
import tornado.web

cache = redis.asyncio.cluster.RedisCluster(
    host='redis', port=6379,
    socket_connect_timeout=2, socket_timeout=3, read_from_replicas=False,
    max_connections=3)


class MainHandler(tornado.web.RequestHandler):
    async def get(self, path):
        self.write(f"<h1>{path}</h1>")
        self.write(f"<ul>")
        self.write(f"<li>Slot: <samp>{cache.keyslot(path)}</samp></li>")
        try:
            self.write(f"<li>Expected node (cached): <samp>{cache.get_node_from_key(path)}</samp></li>")
        except Exception as e:
            self.write(f"<li>Error determining node: <samp>{e}</samp></li>")
        await self.flush()

        try:
            self.write(f"<li>Counter: <samp>{await cache.incr(path)}</samp></li>")
        except Exception as e:
            self.write(f"<li>Error: <samp>{e}</samp></li>")
        self.write("</ul>")
        self.flush()

        self.write('<pre>' + (await cache.execute_command('CLUSTER', 'INFO', target_nodes=[cache.get_default_node()])).decode() + '</pre>')


def make_app():
    return tornado.web.Application([
        (r"/([a-z]+)", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(80)
    await asyncio.Event().wait()

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    asyncio.run(main())
