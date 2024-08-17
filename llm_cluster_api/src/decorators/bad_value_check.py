import functools
from fastapi import HTTPException
from src.exceptions.bad_value_exception import BadValueException


def bad_value_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadValueException as e:
            if not e.private:
                raise HTTPException(status_code=400, detail= e.detail)
            raise HTTPException(status_code=500, detail=e.mask_detail)
        except Exception as e:
            if e is HTTPException:
                raise e
            print(e)
            raise HTTPException( status_code=500, detail="The server encountered a unexpected error")
    return wrapper
