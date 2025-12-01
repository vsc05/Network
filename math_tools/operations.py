def gf2_divide(dividend, divisor):
    # Убираем ведущие нули (старшие биты)
    def bit_len(x):
        return x.bit_length()

    if divisor == 0:
        raise ValueError("Делитель не может быть нулём")

    dividend = dividend  # копия
    divisor_len = divisor.bit_length()
    shift = dividend.bit_length() - divisor_len

    while shift >= 0:
        if dividend & (1 << (shift + divisor_len - 1)):
            dividend ^= divisor << shift
        shift -= 1

    remainder = dividend
    return remainder