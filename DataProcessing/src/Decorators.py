import functools
import logging as log
import Logging


def BookImplementation(book, reference):
    def decorator_BookImplementation(func):
        @functools.wraps(func)
        def wrapper_BookImplementation(*args, **kwargs):
            log.info("The following method is referenced from the book - {}".format(book))
            log.info("Reference for the implementation - {}".format(reference))
            return func(*args, **kwargs)
        return wrapper_BookImplementation
    return decorator_BookImplementation
