def form_w(mode = ''):
    out_put = ''
    if mode == '2000':
        for i in range(2000):
            out_put += 'w'

    elif mode == 'random':
        import random
        for i in range(random.randrange(10)):
            out_put += 'w'

    return out_put