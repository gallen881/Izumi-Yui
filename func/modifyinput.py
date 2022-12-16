def IsZhInput(words):
    bpmf = [49, 113, 97, 122, 50, 119, 115, 120, 101, 100, 99, 114, 102, 118, 53, 116, 103, 98, 121, 104, 110]
    iwu = [117, 106, 109]
    aouh = [56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 47]
    tone = [32, 54, 51, 52, 55]

    words = [ord(word) for word in words]
    if len(words) == 2:
        if words[0] in [53, 116, 103, 98, 121, 104, 110, 117, 106, 109, 56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 45]:
            if words[1] in tone:
                return True
    if len(words) == 3:
        if (words[0] in bpmf) and (words[1] in iwu + aouh) and (words[2] in tone):
            return True
    if len(words) == 3:
        if (words[0] in iwu) and (words[1] in aouh) and (words[2] in tone):
            return True
    if len(words) == 4:
        if (words[0] in bpmf) and (words[1] in iwu) and (words[2] in aouh) and (words[3] in tone):
            return True
    return False


def IsZhInputs(words: str) -> int:
    if len(words) >= 8:
        if IsZhInput(words[-4:]) and IsZhInput(words[-8:-4]):
            return 8
    if len(words) >= 7:
        if IsZhInput(words[-3:]) and IsZhInput(words[-7:-3]):
            return 7
        elif IsZhInput(words[-4:]) and IsZhInput(words[-7:-4]):
            return 7
    if len(words) >= 6:
        if IsZhInput(words[-2:]) and IsZhInput(words[-6:-2]):
            return 6
        elif IsZhInput(words[-3:]) and IsZhInput(words[-6:-3]):
            return 6
        elif IsZhInput(words[-4:]) and IsZhInput(words[-6:-4]):
            return 6
    if len(words) >= 5:
        if IsZhInput(words[-2:]) and IsZhInput(words[-5:-2]):
            return 5
        elif IsZhInput(words[-3:]) and IsZhInput(words[-5:-3]):
            return 5
    if len(words) >= 4:
        if IsZhInput(words[-2:]) and IsZhInput(words[-4:-2]):
            return 4

    return 0