from tartiflette import TypeResolver


@TypeResolver('IPet')
def resolve_pet_type(result, context, info, abstract_type):
    if 'isWhite' in result:
        return 'Pigeon'

    if 'meowVolume' in result:
        return 'Cat'

    return 'IPet'
