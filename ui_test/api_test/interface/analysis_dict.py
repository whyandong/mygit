# -*- coding: utf-8 -*-
def res(dataset, key):
    """
    递归字典取值
    """
    result = []
    if isinstance(dataset, dict) and key in dataset.keys():
        value = dataset[key]
        return str(value)
    elif isinstance(dataset, (list, tuple)):
        for item in dataset:
            value = res(item, key)
            if value == "None" or value is None:
                pass
            elif len(value) == 0:
                pass
            else:
                result.append(value)
        return result
    else:
        if isinstance(dataset, dict):
            for k in dataset:
                value = res(dataset[k], key)
                if value == "None" or value is None:
                    pass
                elif len(value) == 0:
                    pass
                elif value.isdigit():
                    return value
                elif value.isalpha():
                    return value
                else:
                    for item in value:
                        result.append(item)
            return result
