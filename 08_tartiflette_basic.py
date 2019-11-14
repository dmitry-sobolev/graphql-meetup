import asyncio

from tartiflette import Resolver, create_engine

@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return "hello " + args["name"]


async def run():
    engine = await create_engine(
        """
        type Query {
            hello(name: String): String
        }
        """
    )

    result = await engine.execute(
        query='query { hello(name: "Chuck") }'
    )

    print(result)
    # {'data': {'hello': 'hello Chuck'}}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
