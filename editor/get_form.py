from editor.Form import Form


def get_form(t: type) -> Form:
    return Form.instances[t]
