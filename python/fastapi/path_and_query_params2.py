# Run with: fastapi dev path_and_query_params2.py --port 8000
# then open http://localhost:8000/docs


import fastapi

app = fastapi.FastAPI()

@app.get('/hello/{lastname}/{firstname}')                       # 👈 *path paramètres* "firstname" et "lastname"
def foo(
    firstname : str,
    lastname : str,
    country : str,                                             # 👈 *query parameter* "country"
    title : str | None = None                                  # 👈 *query parameter* "title"
) -> str:
    if title is None:
        return f"Hello {firstname} {lastname} of {country}"
    else:
        return f"Hello {title} {firstname} {lastname} of {country}"