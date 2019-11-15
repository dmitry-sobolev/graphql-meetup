import random
from tartiflette import TypeResolver


@TypeResolver('IPet')
def resolve_pet_type(result, context, info, abstract_type):
    if 'isWhite' in result:
        return 'Pigeon'

    return random.choice(['Cat', 'Dog'])
