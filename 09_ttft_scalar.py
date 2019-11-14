import asyncio
import logging
from datetime import datetime
from typing import Union

from tartiflette import Resolver, Scalar, create_engine
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode
from tartiflette.scalar.builtins.string import ScalarString

@Resolver("Query.now")
async def resolver_hello(parent, args, ctx, info):
    return datetime.now()

Scalar('DateTime')
class ScalarDateTime(ScalarString):
    def coerce_output(self, val: datetime) -> str:
        return val.isoformat()

    def coerce_input(self, val: str) -> datetime:
        try:
            result = super().coerce_input(val)
            return datetime.fromisoformat(result)
        except Exception:
            logging.error('Cannot parse DateTime', exc_info=True)

        raise TypeError(f'DateTime cannot represent value: < {val} >.')

    def parse_literal(self, ast: "Node") -> Union[datetime, "UNDEFINED_VALUE"]:
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE

        try:
            return datetime.fromisoformat(ast.value)
        except Exception:
            logging.error('Cannot parse DateTime', exc_info=True)

        return UNDEFINED_VALUE

async def run():
    engine = await create_engine(
        """
        type Query {
            now: DateTime!
        }
        """
    )

    result = await engine.execute(
        query='query { now }'
    )

    print(result)
    # {'data': {'now': '2019-11-14T23:32:31.695702'}}


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
