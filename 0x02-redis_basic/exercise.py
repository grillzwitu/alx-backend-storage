#!/usr/bin/env python3
"""Module declares a redis class and methods"""
import redis
from typing import Union, Callable, Optional
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''counts the number of times methods of Cache class are called'''
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wraps the decorated function and return the wrapper'''
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''stores the history of inputs and outputs for a function'''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        '''wraps the decorated function and returns the wrapper'''
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    '''displays the history of calls of a function.'''
    fun_name = fn.__qualname__
    cl = redis.Redis().get(fun_name)
    try:
        cl = int(cl.decode("utf-8"))
    except Exception:
        cl = 0
    print("{} was called {} times:".format(fun_name, cl))
    inputs = redis.Redis().lrange("{}:inputs".format(fun_name), 0, -1)
    outputs = redis.Redis().lrange("{}:outputs".format(fun_name), 0, -1)
    for inp, outp in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(fun_name, inp, outp))


class Cache:
    '''declares a Cache redis class'''
    def __init__(self):
        '''upon init to store an instance and flush'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''takes a data argument and returns a string'''
        ran_key = str(uuid4())
        self._redis.set(ran_key, data)
        return ran_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        '''converts the data back to the desired format'''
        output = self._redis.get(key)
        if fn:
            output = fn(output)
        return output

    def get_str(self, key: str) -> str:
        '''parametrize Cache.get with correct conversion function'''
        output = self._redis.get(key)
        return output.decode("utf-8")

    def get_int(self, key: str) -> int:
        '''parametrize Cache.get with correct conversion function'''
        output = self._redis.get(key)
        try:
            output = int(output.decode("utf-8"))
        except Exception:
            output = 0
        return output
