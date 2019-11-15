import asyncio
from typing import Any, Dict, Callable, Optional, Union

from tartiflette import Directive, create_engine
from tartiflette.language.ast import VariableDefinitionNode, \
    InputValueDefinitionNode

@Directive('model')
class ModelDirective:
    async def on_post_input_coercion(
        self,
        directive_args: Dict[str, Any],
        next_directive: Callable,
        parent_node: Union[VariableDefinitionNode, InputValueDefinitionNode],
        value: Any,
        ctx: Optional[Any],
    ) -> Any:
        model_cls = self._model_cls(parent_node)
        if model_cls is not None:
            value = model_cls(**value)

        return await next_directive(parent_node, value, ctx)

    def _model_cls(
            self,
            node: Union[VariableDefinitionNode, InputValueDefinitionNode]
    ):
        # Something happens here...
        return None

async def run():
    engine = await create_engine('13_input_coercion.graphql')

    result = await engine.execute(
        query='''
            mutation Create ($new: MapObject!) {
                createMapObject(new: $new)
            }
        ''',
        variables={
            'new': {'name': 'test', 'coordinates': {'lat': 0, 'lng': 0}}
        }
    )

    print(result)
    # ???

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
