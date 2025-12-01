from display_tools.display import draw_table_corrected
from math_tools.operations import gf2_divide
import connection_tools.connection as connect

# stage 0
conn = connect.start_client()
bin_encode_polinom = 0b1010110
bin_gener_polinom = 0b1011     # x^3 + x + 1
n = 7

# Составление словаря синдром - вектор ошибки
syndrome_to_error = {}
for i in range(n):
    error_vec = 1 << i
    synd = gf2_divide(error_vec, bin_gener_polinom)
    syndrome_to_error[synd] = error_vec

# stage 1
corrected_errors = [0]*n
found_errors = [0]*n
number_of_errors = [0]*n
i = 1
while True:
    # Прием бинарных данных
    data = conn.recv(1)  # получаем 1 байт
    
    # Проверка на завершение
    if data == b'END' or i >= 128:
        break
    
    # Преобразование байтов обратно в число
    bin_recived_polinom = int.from_bytes(data, byteorder='big')
    #print(f"Получено от сервера: {bin(bin_recived_polinom)}")

    # Исправление по таблице
    syndrome = gf2_divide(bin_recived_polinom, bin_gener_polinom)
    # Определяем класс ошибки для статистики
    error_class_ind = bin(i).count('1') - 1
    i += 1
    number_of_errors[error_class_ind] += 1
    if syndrome == 0:
        bin_corct_polinom = bin_recived_polinom
    else:
        bin_corct_polinom = bin_recived_polinom ^ syndrome_to_error[syndrome]
        found_errors[error_class_ind] += 1
        
    if (bin_encode_polinom == bin_corct_polinom):
        corrected_errors[error_class_ind] += 1
draw_table_corrected(n, number_of_errors, found_errors, corrected_errors)
connect.socket_termination(conn)