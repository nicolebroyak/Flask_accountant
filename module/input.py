inputlist = []

def input_list():
    try:
        input = inputlist[-1]
        inputlist.pop()
        return input
    except:
        "End of input"

def input_mode(ALLOWED_COMMANDS):
    mode = input_list()
    while mode not in ALLOWED_COMMANDS:
        mode = input_list()
    return mode