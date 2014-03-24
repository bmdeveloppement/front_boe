import json
from functools import wraps


def load_response(arg):
    """ A magic wrapper for Dolead API functions. The return type of the wrapped
    function has to be a response object from the requests module.

    It can work in two ways :

    >>> @load_response
    >>> def my_api_call(*args):
    >>>     return requests.put(*args)

    In a case like this, the wrapper will handle status code that are not 2XX
    and raise error on it. If the status code is considered to be a valid answer
    it will decode the payload assuming it's json encoded.
    By default, the code 204 is interpreted as an empty answer and return value
    will be None.

    >>> @load_response({404: False, 502: MyCustomException('an instance btw')})
    >>> def my_api_call(*args):
    >>>     return requests.put(*args)

    In that second case the wrapper will pretty much act like on the first case,
    except it will first interpret the response status as it's demanded in the
    dict passed in arguments.

    In the above example, a 404 response will not raise and return False
    and a 502 will raise the special Exception passed.
    """
    special_answers = arg if isinstance(arg, dict) else {204: None}

    def metawrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.status_code in special_answers:
                if isinstance(special_answers[response.status_code], Exception):
                    raise special_answers[response.status_code]
                return special_answers[response.status_code]
            # hack to be compatible with both requests library
            # and flask test client
            body = response.text if hasattr(response, 'text') else response.data
            if 200 <= response.status_code < 300:
                return json.loads(body)
            if hasattr(response, 'raise_for_status'):
                response.raise_for_status()
            raise Exception("Status code is: %d; Body is: %s;"
                    % (response.status_code, body))
        return wrapper

    if not isinstance(arg, dict):
        return metawrapper(arg)
    return metawrapper