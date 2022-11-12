import math
num : int = 1


# This function should be on the Client side

def spliter(num2):
    
    # when get the input num2, condition: num2 >= 1

    if num2 == 1:
        return 1, 0

    elif num2 % 2 == 1:
        num_to_SV_01 = math.ceil(num2/2)
        num_to_SV_02 = math.floor(num2/2)
        return num_to_SV_01, num_to_SV_02

    elif num2 % 2 == 0:
        num_to_SV_01 = int(num2/2)
        num_to_SV_02 = int(num2/2)
        return num_to_SV_01, num_to_SV_02



# ceiling = math.ceil(num/2)
# flooring = math.floor(num/2)

# print(f'ceiling : {ceiling}, flooring : {flooring}')


# print(spliter(2))


# # print(7 % 2)

# # print(int(2/2))
# # print(2%2)

# print(spliter(11))

# print(spliter(1))

# print(f'{spliter(11)[0]} and {spliter(11)[1]}')


# x_01, x_02 = spliter(5)

# print(x_01, x_02)