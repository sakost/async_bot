from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['app.models']}
    )
    await Tortoise.generate_schemas()


