from contextlib import nullcontext

def identity(function):
    return function

@identity
def run(items, fail=False):
    events = []
    try:
        with nullcontext():
            for item in items:
                if item > 1:
                    pass
                    events.append((item, 'first'))
                    events.append((item, 'second'))
                elif item == 1:
                    events.append('one')
                else:
                    events.append('other')
            else:
                events.append('loop-else')
            if fail:
                raise ValueError('requested')
    except ValueError:
        events.append('caught')
    finally:
        events.append('finally')
    return (events, [item * item for item in items])
