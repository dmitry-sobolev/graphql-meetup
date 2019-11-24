from dataclasses import is_dataclass, asdict
from typing import Any

from tartiflette import Directive


@Directive('model')
class ModelDirective:
    async def on_pre_output_coercion(
        self, directive_args, next_directive, value, ctx, info
    ) -> Any:
        if is_dataclass(value):
            cls_name = value.__class__.__name__
            value = asdict(value)
            value['_typename'] = cls_name
        return await next_directive(value, ctx, info)

    async def on_post_input_coercion(
        self, directive_args, next_directive, parent_node, value, ctx
    ) -> Any:
        cls_name = directive_args.get('cls')
        model_cls = self._model_cls(cls_name)
        if model_cls is not None:
            value = model_cls(**value)

        return await next_directive(parent_node, value, ctx)
