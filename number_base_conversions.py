def reverse_list(list):
    new_list = [None] * len(list)
    for i in range(0, len(list)):
        new_list[i] = list[len(list) - i - 1]
    print(new_list)

def decimal2binary(decimal):
    num_list = []
    while(decimal !=0 ):
        num_list += [decimal%2]
        decimal = int(decimal/2)
    return reverse_list(num_list)


decimal2binary(100)
decimal2binary(77)
decimal2binary(1999)

