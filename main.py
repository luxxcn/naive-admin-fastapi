from app import app


def application(env, start_response):

    return app(env, start_response)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8085)
