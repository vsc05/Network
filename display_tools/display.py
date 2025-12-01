def drawLine():
    print('+-----+-------+-------+-------+')

def draw_table_corrected(n, combin_array, found_array, corrected_array):
    drawLine()
    print('| {:>3} | {:>5} | {:>5} | {:>5} |'.format('i', 'Cni', 'Co', 'No'))
    drawLine()
    for i in range(n):
        percent = corrected_array[i] * 100 / combin_array[i] if combin_array[i] != 0 else 0
        print('| {:>3} | {:>5} | {:>5} | {:>5} |'.format(
            i + 1,
            combin_array[i],
            found_array[i],
            corrected_array[i]
        ))
    drawLine()
