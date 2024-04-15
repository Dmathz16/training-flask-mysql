import flask


def request_input(name):
    return flask.request.form.get(name)
