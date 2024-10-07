def calc_pi_leibniz(n):
    pi = 0
    for i in range(n):
        pi += 4.0 * (-1)**i / (2*i + 1)
    return pi


if __name__ == "__main__":
    print(calc_pi_leibniz(1000000))