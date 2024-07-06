from database import new_session, TaskOrm
from chemas import STaskAdd, STask
from sqlalchemy import select


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()  # приводим таску к словарику с помощью функции model_dump

            task = TaskOrm(**task_dict)  # раскрытый словарик передаём
            session.add(task)
            await session.flush()  # отправит изменения в базу, получит id и только потом отправит в базу
            await session.commit()  # здесь все изменения, которые были добавлены будут отправлены в базу данных
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)  # делаем простейший запрос в базу данных
            result = await session.execute(query)  # обратись к базе данных через сессию и выполни данный запрос
            task_models = result.scalars().all()  # обращаемся к scalars, чтобы не было ошибок
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas
