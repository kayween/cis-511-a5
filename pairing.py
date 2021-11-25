def pairing(inputs):
    if len(inputs) == 1:
        return inputs[0]

    elif len(inputs) == 2:
        x = inputs[0]
        y = inputs[1]
        return ((x + y) ** 2 + 3 * x + y) / 2

    else:
        return pairing([inputs[0], pairing(inputs[1:])])


if __name__ == "__main__":
    print(pairing([2, 5, 7, 17]))
