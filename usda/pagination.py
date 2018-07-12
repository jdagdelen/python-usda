
class RawListPaginator(object):
    """
    Generator to paginate over list results and return JSON data
    """

    def __init__(self, client, *request_args, **request_kwargs):
        self.client = client
        self.data = {}
        self.request_args = request_args
        self.request_kwargs = request_kwargs
        self.current_offset = 0
        self.max = request_kwargs.get('max', 30)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.data.get('item', [])) < 1:
            if 'item' in self.data and self.current_offset >= self.data['end']:
                raise StopIteration
            self._fetch_next()
        return self.data['item'].pop(0)

    def _fetch_next(self):
        self.request_kwargs['offset'] = self.current_offset
        self.data = self.client.run_request(
            *self.request_args, **self.request_kwargs)['list']
        self.current_offset += self.max


class ModelListPaginator(object):
    """
    Generator to paginate over list results and get custom models
    """

    def __init__(self, model, raw):
        assert isinstance(raw, RawListPaginator)
        self.model = model
        self.raw = raw

    def __iter__(self):
        return self

    def __next__(self):
        return self.model.from_response_data(next(self.raw))
