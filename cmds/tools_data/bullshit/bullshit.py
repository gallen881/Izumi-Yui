#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import function

data = function.open_json("./cmds/tools_data/bullshit/bullshit.json")
famous = data["famous"] # a 代表前面墊話，b代表後面墊話
before = data["before"] # 在名人名言前面弄點廢話
after = data['after']  # 在名人名言後面弄點廢話
bosh = data['bosh'] # 代表文章主要廢話來源

def shuffle(l):
    pool = list(l) * 2
    while True:
        random.shuffle(pool)
        for element in pool:
            yield element

next_bosh = shuffle(bosh)
next_famous = shuffle(famous)

def form_famous():
    global next_famous
    return next(next_famous).replace("a", random.choice(before)).replace("b", random.choice(after))

def generate(xx, length):
    for x in xx:
        tmp = str()
        while ( len(tmp) < length ) :
            rd = random.randint(0,100)
            if rd < 5:
                tmp += "\r\n"
            elif rd < 19 :
                tmp += form_famous()
            else:
                tmp += next(next_bosh)
        tmp = tmp.replace("x",xx)
        return(tmp)