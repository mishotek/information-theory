import sys
import math


def get_file_info_string(fileName_to_read):
    result = ''
    with open(fileName_to_read, "rb") as to_read:
        data = to_read.read(1024)
        while data != b"":
            result += (''.join('{0:08b}'.format(int(x), 'b') for x in data))
            data = to_read.read(1024)

    stringLength = len(result) - 1
    while stringLength >= 0:
        if result[stringLength] == '0':
            stringLength -= 1
        else:
            finalRes = result[0:stringLength]
            return finalRes


def split_code(file_into_string):
    num_of_zeros = 0
    index = 0
    while file_into_string[index] != '1':
        num_of_zeros += 1
        index += 1
    elias_code_len = 2*num_of_zeros + 1
    elias_size = file_into_string[0:elias_code_len]
    return elias_size, file_into_string[elias_code_len:]


def get_size(elias_gamma_size):
    num_of_zeros = 0
    index = 0
    while elias_gamma_size[index] != '1':
        num_of_zeros += 1
        index += 1
    substring = elias_gamma_size[num_of_zeros:]
    power_index = len(substring)-1
    result = 0
    curr_index = 0
    while curr_index <= len(substring)-1:
        if substring[curr_index] == '1':
            result += int(math.pow(2, power_index))
        power_index -= 1
        curr_index += 1
    return result


def power_function(string):
    result = 0
    curr_index = 0
    while curr_index < len(string):
        if string[curr_index] == '1':
            power_num = len(string)-curr_index-1
            power = int(math.pow(2, power_num))
            result += power
        curr_index += 1
    return result

# es erti nawili vnaxe orobitidan stringshi rom gadameyvana


def code_to_string(file_info, size):
    result = ""
    chunck_index = 0
    for index in range(size):
        chunck = file_info[chunck_index*8: (chunck_index+1)*8]
        char_pow = 0
        for i in range(len(chunck)):
            if chunck[i] == '1':
                pow = int(math.pow(2, len(chunck)-i-1))
                char_pow += pow
        result += chr(char_pow)
        chunck_index += 1
    return result


def write_file(fileName_to_write, string):
    res = ''.join('{0:08b}'.format(ord(x), 'b') for x in string)
    to_write = open(fileName_to_write, "wb")
    index = 0
    data = res[index: index+8]
    while data != "":
        v = int(data, 2).to_bytes(len(data) // 8, byteorder='big')
        to_write.write(v)
        index += 8
        data = res[index: index+8]

    to_write.close()


def start_decode(file_info, size, lexicon, fileName_to_write):
    result = ''
    index = 0
    while index < len(file_info):
        curr_len = int(math.ceil(math.log(len(lexicon), 2)))
        curr_str = file_info[index: index + curr_len]
        lexicon_index = power_function(curr_str)
        lexicon_index_value = lexicon[lexicon_index]
        result += lexicon_index_value
        lexicon[lexicon_index] = lexicon_index_value + '0'
        lexicon[len(lexicon)] = lexicon_index_value + '1'
        index += len(curr_str)

    result = result[0: size*8]
    print(result)
    text = code_to_string(result, size)
    write_file(fileName_to_write, text)


def main():
    fileName_to_read = sys.argv[1]
    fileName_to_write = sys.argv[2]
    file_info_string = get_file_info_string(fileName_to_read)
    elias_gamma_size, file_info = split_code(file_info_string)
    size = get_size(elias_gamma_size)

    lexicon = dict()
    lexicon[0] = '0'
    lexicon[1] = '1'
    start_decode(file_info, size, lexicon, fileName_to_write)


if __name__ == "__main__":
    main()
