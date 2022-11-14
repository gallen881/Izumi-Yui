import random
import function

DATA = function.open_json("./cmds/tools_data/bullshit/bullshit.json")

def shuffle(l):
    pool = list(l) * 2
    while True:
        random.shuffle(pool)
        for element in pool:
            yield element

def generate(xx, length):
    for x in xx:
        temp = '    '
        while ( len(temp) < length ) :
            rd = random.randint(0,100)
            if rd < 10:
                temp += '\n\n    '
            elif rd < 24:
                temp += next(shuffle(DATA["famous"])).replace("a", random.choice(DATA["before"])).replace("b", random.choice(DATA['after']))
            elif rd < 45:
                temp += next(shuffle(DATA['bosh_comma'])) + next(shuffle(DATA['bosh']))
            elif rd < 98:
                temp += next(shuffle(DATA['bosh']))
            else:
                temp += next(shuffle(DATA['bosh_colon'])) + next(shuffle(DATA['bosh_comma'])) + next(shuffle(DATA['bosh']))
        temp = temp.replace("x",xx)
        return(temp)