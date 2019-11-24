import logging
from dataclasses import is_dataclass, asdict
from typing import Dict, Any, Union

from tartiflette import Resolver, create_engine, Scalar, Directive
from tartiflette.constants import UNDEFINED_VALUE
from tartiflette.language.ast import StringValueNode
from tartiflette.scalar.builtins.string import ScalarString


@Resolver("Query.users")
async def resolver_user_list(parent, args, ctx, info):
    return await get_users(limit=args.get('limit', 10))

@Resolver("User.friends")
async def resolver_user_friends(parent, args, ctx, info):
    return await get_friends(parent['id'], limit=args.get('limit', 5))

@Resolver("Mutation.createUser")
async def resolver_create_user(parent, args, ctx, info):
    return await create_user(user=args['new'])

async def run(query: str, variables: Dict[str, Any]):
    engine = await create_engine("01_schema.graphql")

    return await engine.execute(
        query=query,
        variables=variables
    )

@Scalar('Email')
class ScalarDateTime(ScalarString):
    def coerce_input(self, val: str) -> str:
        try:
            result = super().coerce_input(val)
            validate_email(result)
            return result
        except Exception:
            logging.error('Invalid email', exc_info=True)

        raise TypeError(f'Email cannot represent value: < {val} >.')

    def parse_literal(self, ast: "Node") -> Union[str, "UNDEFINED_VALUE"]:
        if not isinstance(ast, StringValueNode):
            return UNDEFINED_VALUE

        try:
            validate_email(ast.value)
            return ast.value
        except Exception:
            logging.error('Cannot parse DateTime', exc_info=True)

        return UNDEFINED_VALUE

@Directive('model')
class ModelDirective:
    async def on_pre_output_coercion(
        self, directive_args, next_directive, value, ctx, info
    ) -> Any:
        if is_dataclass(value):
            value = asdict(value)
        return await next_directive(value, ctx, info)

    async def on_post_input_coercion(
        self, directive_args, next_directive, parent_node, value, ctx
    ) -> Any:
        model_cls = self._model_cls(parent_node)
        if model_cls is not None:
            value = model_cls(**value)

        return await next_directive(parent_node, value, ctx)


def validate_email(email):
    return True


async def get_users(limit: int):
    return []


async def get_friends(user_id: int, limit: int):
    return []


async def create_user(user: Dict[str, Any]):
    return {}
