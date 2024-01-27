FastAPI
=======

Documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/

Usage
=====

See: https://fastapi.tiangolo.com/#installation

::

    pip install fastapi "uvicorn[standard]" sqlalchemy


Usage
=====

See: https://fastapi.tiangolo.com/#example

Run the server with::

    uvicorn sql_app.main:app --reload

Then open your browser at http://127.0.0.1:8000 to test it.

To see the automatic interactive API documentation (provided by Swagger UI), open your browser at: http://127.0.0.1:8000/docs

To see the alternative automatic documentation (provided by ReDoc), open your browser at: http://127.0.0.1:8000/redoc
