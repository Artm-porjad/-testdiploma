from toml import load
from math import sin, cos, tan, radians


# реализовать округение к ближайшему четному
def convert_degrees_into_str(angle):
    flag = False
    if angle < 0:
        angle = -angle
        flag = True
    degree = int(angle)
    minutes = round((angle - degree) * 60, 1)
    if flag:
        return "-" + str(degree) + "°" + str(minutes) + "'"
    else:
        return str(degree) + "°" + str(minutes) + "'"


def convert_str_into_degrees(angle):
    degrees = float(angle[:angle.find("°")])
    minutes = float(angle[angle.find("°") + 1:angle.find("'")]) / 60
    if angle[0] == "-":
        return degrees - minutes
    return degrees + minutes


def get_mean_hor_angle(l_prev_angle, l_next_angle, r_prev_angle, r_next_angle):
    l_angle = convert_str_into_degrees(l_next_angle) - convert_str_into_degrees(l_prev_angle)
    if l_angle < 0:
        l_angle = 360 + l_angle
    r_angle = convert_str_into_degrees(r_next_angle) - convert_str_into_degrees(r_prev_angle)
    if r_angle < 0:
        r_angle = 360 + r_angle
    return convert_degrees_into_str(round(((l_angle + r_angle) / 2), 3))


def get_mean_h(l_prev_angle, r_prev_angle, l_next_angle, r_next_angle, l_prev_length, r_prev_length, l_next_length,
               r_next_length, D_dict, i, V):
    M01 = (convert_str_into_degrees(l_prev_angle) + convert_str_into_degrees(r_prev_angle)) / 2
    v1 = (convert_str_into_degrees(l_prev_angle) - convert_str_into_degrees(r_prev_angle)) / 2
    l1 = round((float(l_prev_length) + float(r_prev_length)) / 2, 1)
    if l1 <= 100:
        D = l1 + D_dict['D100']
    elif l1 <= 150:
        D = l1 + D_dict['D150']
    else:
        D = l1 + D_dict['D200']
    s1 = round(D * cos(radians(v1)) ** 2, 1)
    h_1 = round(s1 * tan(radians(v1)), 2)
    d = round(i[0] - V[0], 2)
    h1 = h_1 + d

    M02 = (convert_str_into_degrees(l_prev_angle) + convert_str_into_degrees(r_prev_angle)) / 2
    v2 = (convert_str_into_degrees(l_next_angle) - convert_str_into_degrees(r_next_angle)) / 2
    l2 = round((float(l_next_length) + float(r_next_length)) / 2, 1)
    if l2 <= 100:
        D = l2 + D_dict['D100']
    elif l2 <= 150:
        D = l2 + D_dict['D150']
    else:
        D = l2 + D_dict['D200']
    s2 = round(D * cos(radians(v2)) ** 2, 1)
    h_2 = round(s2 * tan(radians(v2)), 2)
    d = i[1] - V[1]
    h2 = h_2 + d
    if h1 > 0:
        return round((h1 + abs(h2)) / 2, 2)
    else:
        return round((abs(h1) + h2) / 2, 2) * (-1)


if __name__ == "__main__":
    with open('data.toml', 'r', encoding='utf-8') as fp:
        doc = load(fp)
        k = list(doc)[2:]
    for point in k:
        print(get_mean_hor_angle(doc[point]["hor_angle"]["l_prev_angle"], doc[point]["hor_angle"]["l_next_angle"],
                                 doc[point]["hor_angle"]["r_prev_angle"], doc[point]["hor_angle"]["r_next_angle"]))

    for j in range(len(k) - 1):
        l_prev_angle = doc[k[j]]["vert_angle"]["l_next_angle"]
        r_prev_angle = doc[k[j]]["vert_angle"]["r_next_angle"]
        l_next_angle = doc[k[j + 1]]["vert_angle"]["l_prev_angle"]
        r_next_angle = doc[k[j + 1]]["vert_angle"]["r_prev_angle"]
        l_prev_length = doc[k[j]]["l"]["l_next_length"]
        r_prev_length = doc[k[j]]["l"]["r_next_length"]
        l_next_length = doc[k[j + 1]]["l"]["l_prev_length"]
        r_next_length = doc[k[j + 1]]["l"]["r_prev_length"]
        D_dict = doc["D"]
        i = [doc[k[j]]["i"], doc[k[j + 1]]["i"]]
        V = [doc[k[j]]["vert_angle"]["next_V"], doc[k[j + 1]]["vert_angle"]["prev_V"]]
        print(get_mean_h(l_prev_angle, r_prev_angle, l_next_angle, r_next_angle, l_prev_length, r_prev_length,
                         l_next_length,
                         r_next_length, D_dict, i, V))
