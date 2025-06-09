class MiddlewareSalvar:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/static') and not request.path.startswith('/admin'):
            request.session['ultima_url'] = request.path
        response = self.get_response(request)

        return response