def is_list_of_dicts(obj) -> bool:
    return (
        isinstance(obj, list)
        and all(isinstance(item, dict) for item in obj)
    )