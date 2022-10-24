import random
import function

DATA = function.open_json("./cmds/tools_data/bullshit/bullshit.json")

def shuffle(l):
    pool = list(l) * 2
    while True:
        random.shuffle(pool)
        for element in pool:
            yield element

def form_famous():
    return 

def generate(xx, length):
    for x in xx:
        tmp = str()
        while ( len(tmp) < length ) :
            rd = random.randint(0,100)
            if rd < 5:
                tmp += "\n\n"
            elif rd < 19:
                tmp += next(shuffle(DATA["famous"])).replace("a", random.choice(DATA["before"])).replace("b", random.choice(DATA['after']))
            elif rd < 40:
                tmp += next(shuffle(DATA['bosh_comma'])) + next(shuffle(DATA['bosh']))
            elif rd < 98:
                tmp += next(shuffle(DATA['bosh']))
            else:
                tmp += next(shuffle(DATA['bosh_colon'])) + next(shuffle(DATA['bosh_comma'])) + next(shuffle(DATA['bosh']))
        tmp = tmp.replace("x",xx)
        return(tmp)