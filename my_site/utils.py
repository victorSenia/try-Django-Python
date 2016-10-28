def getDictionary(object, exclude=[], rename={}):
    """
    Get dictionary from model
    Args:
         object (django.db.models.Model) - model or iterable of models
         exclude (list): list of keys to exclude from dictionary
         rename (dict): dict of keys to rename in dictionary from key: to value:
         Note:
             Be careful choosing name of keys, you can replays existent ones
    Returns:
        dict: return dictionary with all fields of model except those, that was excluded
        """
    exclude += ["_state"]
    if "_state" in object.__dict__:
        data = renameKeys(deleteKey(object.__dict__, exclude), rename)
    else:
        data = [renameKeys(deleteKey(o.__dict__, exclude), rename) for o in object]
    return data


def deleteKey(data, keys):
    for key in keys:
        if key in data: del data[key]
    return data


def renameKeys(data, keys):
    for oldKey, newKey in keys.items():
        if oldKey in data:
            data[newKey] = data[oldKey]
            del data[oldKey]
    return data
