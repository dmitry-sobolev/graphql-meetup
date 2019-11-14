from dataclasses import is_dataclass, asdict
from typing import Any, Dict, Callable, Optional

from tartiflette import Directive

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
            value['_typename'] = value.__class__.__name__
        return await next_directive(value, ctx, info)
