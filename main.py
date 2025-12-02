import math

def info_to_coded_vector(info_vector: str, count_of_check_category: int, n: int):
    code_vector = str(info_vector)
    for category in range(count_of_check_category-1, -1, -1):
        check_razryad = (2**category) - 1
        check_category = 0
        for razryad in range(n-check_razryad-1):
            if (((n-razryad) >> category) % 2 == 1):
                check_category ^= int(code_vector[razryad])
        code_vector = code_vector[:n-check_razryad-1] + str(check_category) + code_vector[n-check_razryad-1:]
    return code_vector

def syndrome_razryad(code_combination: str, category: int, n: int):
    check_category = 0
    for razryad in range(n):
        if (((razryad+1) >> category) % 2 == 1):
            check_category ^= int(code_combination[n-razryad-1])
    return str(check_category)

def main():
    info_vector = input("Введите информационный вектор: ")
    k = len(info_vector)
    n = 2**math.ceil(math.log2(k+1)) - 1
    count_of_check_category = n - k

    code_vector = info_to_coded_vector(info_vector, count_of_check_category, n)
    print(code_vector)

    detectedErrors = [0] * n
    corrections = [0] * n

    for error in range(1, 2**n):
        code_combination = bin(int(code_vector, 2) ^ error)[2:]
        code_combination = '0' * (n - len(code_combination)) + code_combination
        syndrome = ""

        for category in range(count_of_check_category):
            syndrome = syndrome_razryad(code_combination, category, n) + syndrome
        syndrome = int(syndrome, 2)

        if syndrome != 0:
            if syndrome == 1:
                inverse_code_combination = code_combination[:n-syndrome] + str((int(code_combination[n-syndrome]) + 1) % 2)
            else:
                inverse_code_combination = code_combination[:n-syndrome] + str((int(code_combination[n-syndrome]) + 1) % 2) + code_combination[n-syndrome+1:]
            
            decoded_vector = inverse_code_combination
            for check_razryad in range(count_of_check_category-1, -1, -1):
                razryad = (2**check_razryad) - 1
                decoded_vector = decoded_vector[:n-razryad-1-(count_of_check_category-1-check_razryad)] + decoded_vector[n-razryad-(count_of_check_category-1-check_razryad):]
            
            category = bin(error)[2:].count('1')
            detectedErrors[category-1] += 1
            if decoded_vector == str(info_vector):
                corrections[category-1] += 1

    print('i | Сочетания | N0 | С0')
    print('---')
    for i in range(n):
        combinations = math.comb(n, i+1)
        print(f"{i+1} | {combinations} | {detectedErrors[i]} | {round(detectedErrors[i]/combinations, 1)}")

if __name__ == '__main__':
    main()