FastAPI
=======

C.f. https://www.slingacademy.com/article/fastapi-how-to-disable-the-docs-swagger-ui-and-redoc/

Usage
=====

See: https://fastapi.tiangolo.com/#installation

::

    pip install fastapi "uvicorn[standard]"


Usage
=====

See: https://fastapi.tiangolo.com/#example

Run the server with::

    uvicorn main:app --reload

Then open your browser at http://127.0.0.1:8000 to test it.

With this snippet, http://127.0.0.1:8000/docs (Swagger UI) and http://127.0.0.1:8000/redoc (ReDoc) should return a "Not Found" error.
