def _isNumeric(v):
    return v in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def _splitup(text):
    fragments = []
    lastWasNumeric = None
    for char in text:
        if lastWasNumeric == _isNumeric(char):
            fragments[-1] += char
        else:
            lastWasNumeric = _isNumeric(char)
            fragments.append(char)
    return _convertNumbers(fragments)


def _safeConvert(fragment):
    try:
        return int(fragment)
    except:
        return fragment


def _convertNumbers(fragments):
    return map(_safeConvert, fragments)


def sortByFirstNumber(filenames):
    files = zip(map(_splitup, filenames), filenames)
    return [filename for (sortKey, filename) in sorted(files)]
