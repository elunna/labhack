class ThinDict(dict):
    def __init__(self, allowed_keys, initial_val=None):
        super(ThinDict, self).__init__()
        self._allowed_keys = tuple(allowed_keys)

        # Initialize all keys to initial_val
        for key in allowed_keys:
            self[key] = initial_val

    def __setitem__(self, key, val):
        """Checks if the key is allowed before setting the value"""
        if key not in self._allowed_keys:
            raise KeyError("%s is not allowed as key" % key)
        dict.__setitem__(self, key, val)
