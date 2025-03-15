from pytest import fixture

@fixture(scope="session")
def mongo_client():
    # Setup code for MongoDB client connection
    pass

@fixture(scope="function")
def db(mongo_client):
    # Setup code for database connection for each test
    pass

@fixture(scope="function")
def redis_client():
    # Setup code for Redis client connection
    pass

@fixture(scope="function")
def cache(redis_client):
    # Setup code for cache for each test
    pass