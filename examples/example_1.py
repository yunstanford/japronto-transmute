from japronto import Application


def hello(request):
    return request.Response(
    	json={
    		"method": request.method,
    		"content-type": request.mime_type,
    		"content": request.body,
    		"match-dict": request.match_dict,
    		"form": request.form,
    		"query": request.query,
    		# "keys": request.GET,
    		"headers": request.headers,
    	}
    )


app = Application()
app.router.add_route('/{hello}/', hello)
app.run(debug=True)
