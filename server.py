from display_tools.display import draw_table_corrected
from math_tools.operations import gf2_divide
import connection_tools.connection as connect

# stage 0 - input
conn, server_socket = connect.start_server()
bin_basic_polinom = 0b1010     # 1001
bin_gener_polinom = 0b1011     # x^3 + x + 1
n = 7

# stage 1 - encode
bin_encode_polinom = (bin_basic_polinom << 3) # bitwise shift
bin_encode_polinom = bin_encode_polinom + gf2_divide(bin_encode_polinom, bin_gener_polinom) # key-vector

# stage 2 - set error & decode & count
number_of_errors = [0]*n
for i in range(1, 2**n):
    bin_wrong_polinom = bin_encode_polinom ^ i
    # sending
    binary_data = bin_wrong_polinom.to_bytes(1, byteorder='big')
    conn.send(binary_data)

conn.send(b'END')
connect.connection_termination(conn)
connect.socket_termination(server_socket)