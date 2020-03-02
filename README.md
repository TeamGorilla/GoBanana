# GoBanana

## Install Pipenv
[See here](https://github.com/pypa/pipenv)

## Install Redis 
[See here](https://redis.io/topics/quickstart)

For my version of redis, running `redis-server --version` gives me:

```
server v=5.0.7 sha=00000000:0 malloc=libc bits=64 build=295beb9462eefd91
```

## Create a Virtual Environment and Install Dependencies
```bash
pipenv install
```

To check if this works:
```bash
pipenv run python -c 'import gobanana as gb; gb.utils.hello()'
```

## Some Useful Stuff
[redis-py pub sub](https://github.com/andymccurdy/redis-py#publish--subscribe)

