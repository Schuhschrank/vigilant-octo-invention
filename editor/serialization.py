from typing import Any


def _value(s: str, env: dict[int, object]) -> Any:
    """
    Cast string to a value.

    :param s: String to cast (e.g. "'Hello'", '"Banana"', "-1.02", "None", etc.)
    :param env: Maps ids to objects.
    :return: Value of what is encoded in the given string.
    """

    if s == "''" or s == '""':
        return ""
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.startswith('"')):
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        if s == "[]":
            return []
        return [_value(ss, env) for ss in s[1:-1].split(", ")]
    if s.startswith("<") and s.endswith(">"):
        if s.startswith("<func"):
            return lambda: True
        identity = int(s[s.find(" at ")+4:-1], 16)
        return env[identity]
    if s == "None":
        return None
    if s == 'True':
        return True
    if s == 'False':
        return False
    try:
        number = float(s)
        if number.is_integer():
            return int(number)
        return number
    except ValueError:
        return None


_seperator = ":"


def serialize(obj: object) -> str:
    """
    Create a string representing the given object that can be saved to a file.

    :param obj: Object to serialize
    :return: String from which the object can be recovered.
    """

    result = f"{len(obj.__dict__)}\n{id(obj)}\n"
    for key, value in obj.__dict__.items():
        if isinstance(value, str):
            value = "'" + value + "'"
        result += key + _seperator + str(value) + "\n"
    return result


def deserialize_obj(lines: list[str], env: dict[int, object]) -> tuple[dict, int]:
    """
    Deserialize a single object.

    :param lines:
    :param env:
    :return:
    """

    identifier = int(lines[0])
    result = {}
    for line in lines[1:]:
        key, _, value = line.partition(_seperator)
        result[key] = _value(value, env)
    return result, identifier


def to_dict(s: str, env: dict) -> dict:
    """
    Return a dictionary based on the given string.

    :param s: String with the format "{key: value, ...}"
    :param env: Maps ids to objects.
    :return: Dictionary populated according to the given string.
    """

    result = {}
    pairs = s[1:-1].split(", ")
    for p in pairs:
        key, value = p.split(": ")
        result[_value(key, env)] = _value(value, env)
    return result


def main():
    class C:
        pass
    obj = C()
    obj.x = 0
    obj.y = None
    obj.z = -1.2
    obj.l = []
    obj.m = [1.2, None, "Hi"]
    print(serialize(obj))


if __name__ == '__main__':
    main()
