def gray_scale(image):
    return image.convert("L")


def get_float_data(image):
    return image.convert("F").getdata()


def normalize(data):
    return [d / 255 for d in data]


def difference(data1, data2):
    if len(data1) != len(data2):
        raise Exception("Size don't match!")

    manhattan_norm = sum([abs(data1[i] - data2[i]) for i in range(len(data1))])
    return manhattan_norm / len(data1) * 100