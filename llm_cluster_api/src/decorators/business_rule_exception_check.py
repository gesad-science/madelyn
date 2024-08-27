import functools
from fastapi import HTTPException
from src.exceptions.business_rule_exception import BusinessRuleException


def business_rule_exception_check(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BusinessRuleException as e:
            if not e.private:
                raise HTTPException(status_code=400, detail= e.detail)
            
            print(e.detail)
            raise HTTPException(status_code=500, detail=e.mask_detail)
        except Exception as e:
            print(e)
            if e is HTTPException:
                raise e
            raise HTTPException( status_code=500, detail="The server encountered a unexpected error")
    return wrapper
