x = 10

# print(x + 2)

my_string = 'lu hou yang'

# print(my_string)

my_float = 3.142

# print(my_float)

my_bool = True

# print(my_bool)

my_list = [1, 1.25, 'hi', False]

# print(my_list[2])

my_list = [1, 2, 3, 4, 5]

# print(my_list[0])

my_list = [
    [1, 2],
    [3, 4],
    [5, 6],
]

# print(my_list[1][0])

my_dict = {
    'key': 40,
    'k2': 50,
    'k3': 60,
}

# print(my_dict)

# print(2 * 2 + 3 * 2)
# print(6 * 2 + 8 * 2)
# print(4 * 2 + 3 * 2)
# print(8 * 2 + 2 * 2)
# print(1 * 2 + 2 * 2)
# print(3 * 2 + 6 * 2)


def calc_perimeter(height, width):
    perimeter = height * 2 + width * 2
    return perimeter


# print(calc_perimeter(2, 3))
# print(calc_perimeter(5, 5))

my_int = 4

if (my_int > 4):
    print('Greater than 4')
elif (my_int == 4):
    print('Equal 4')
else:
    print('Less than 4')
