import asyncio
from dataclasses import dataclass, is_dataclass, asdict
from typing import Any, Dict, Callable, Optional

from tartiflette import Resolver, Directive, create_engine

@Directive('model')
class ModelDirective:
    def __init__(self, schema_name='default'):
        self._schema_name = schema_name

    async def on_pre_output_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        value: Any,
        ctx: Optional[Any],
        info: "ResolveInfo",
    ) -> Any:
        if is_dataclass(value):
            value = asdict(value)
        return await next_directive(value, ctx, info)


@Resolver("Query.hello")
async def resolver_hello(parent, args, ctx, info):
    return World(name=f"hello {args['name']}")


@dataclass
class World:
    name: str

async def run():
    engine = await create_engine(
        """
        directive @model on OBJECT | INPUT_OBJECT
        
        type World @model {
            name: String!
        }
        
        type Query {
            hello(name: String): String
        }
        """
    )

    result = await engine.execute(
        query='query { hello(name: "Chuck") { name } }'
    )

    print(result)
    # {'data': {'hello': {'name': 'hello Chuck'}}}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
