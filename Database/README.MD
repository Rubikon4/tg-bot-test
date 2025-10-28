Если возникает ошибка "No 'script_location' key found in configuration" при попытке сделать
 alembic revision --autogenerate -m "message", попробуйте указать полный путь к папке migrations, например:
alembic -c Database/alembic.ini revision --autogenerate -m "message".