from functools import wraps
from transmute_core.exceptions import APIException, NoSerializerFound
from transmute_core.function.signature import NoDefault
from transmute_core import ParamExtractor, NoArgument


def create_handler(transmute_func, context):
	
	@wraps(transmute_func.raw_func)
	async def handler(request):
        exc, result = None, None
        try:
            args, kwargs = await extract_params(request, context,
                                                transmute_func)
            result = await transmute_func.raw_func(*args, **kwargs)
        except Exception as e:
            exc = e
        response = transmute_func.process_result(
            context, result, exc, request.mime_type
        )
        return request.Response(
            body=response["body"], code=response["code"],
            mime_type=response["content-type"]
        )

    handler.transmute_func = transmute_func
    return handler



async def extract_params(request, context, transmute_func):
    body = request.body
    content_type = request.mime_type
    extractor = ParamExtractorJapronto(request, body)
    return extractor.extract_params(
        context, transmute_func, content_type
    )


class ParamExtractorJapronto(ParamExtractor):

    def __init__(self, request, body):
        self._request = request
        self._body = body

    def _get_framework_args(self):
        return {"request": self._request}

    @property
    def body(self):
        return self._body

    def _query_argument(self, key, is_list):
        if key not in self._request.query:
            return NoArgument
        if is_list:
            return self._request.query[key]
        else:
            return self._request.query[key]

    def _header_argument(self, key):
        return self._request.headers.get(key, NoArgument)

    def _path_argument(self, key):
        return self._request.match_dict.get(key, NoArgument)
