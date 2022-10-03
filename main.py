from toml import load
from math import sin, cos, tan, radians, sqrt


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
        return round((h1 + abs(h2)) / 2, 2), s1
    else:
        return round((abs(h1) + h2) / 2, 2) * (-1), s1


def get_x_y(initial_dir_angle, final_dir_angle, angles, S, start_x_y):
    n = len(angles)
    angles = list(map(convert_str_into_degrees, angles))
    E_angles = sum(angles)
    E_t_angles = (convert_str_into_degrees(initial_dir_angle) - convert_str_into_degrees(
        final_dir_angle)) - convert_str_into_degrees("180°0'") * n
    fb = E_angles + E_t_angles
    fddop = convert_str_into_degrees("0°1'") * sqrt(n)
    # Расчитать нормально db для каждого
    if abs(fb) <= fddop:
        db = - fb / n
    else:
        raise Exception("Ошибка abs(fb) <= fddop", abs(fb), fddop)
    new_angles = []
    for j in range(n):
        new_angles.append(convert_degrees_into_str(angles[j] + db))
    E_S = sum(S)
    dX = []
    dY = []
    direct_angles = [convert_str_into_degrees(initial_dir_angle)]
    for j in range(0, n - 1):
        direct_angles.append(direct_angles[j] + angles[j] + db - convert_str_into_degrees("180°0'"))
        dX.append(round(S[j] * cos(radians(direct_angles[j + 1])), 1))
        dY.append(round(S[j] * sin(radians(direct_angles[j + 1])), 1))
    direct_angles.append(convert_str_into_degrees(final_dir_angle))
    E_dXvi = sum(dX)
    E_dYvi = sum(dY)
    E_dXteo = round(start_x_y[2] - start_x_y[0], 1)
    E_dYteo = round(start_x_y[3] - start_x_y[1], 1)
    fs_x = round(E_dXvi - E_dXteo, 1)
    fs_y = round(E_dYvi - E_dYteo, 1)
    f_abs = round(sqrt(fs_x ** 2 + fs_y ** 2), 1)
    new_dX = []
    new_dY = []
    dfs_x = - fs_x / n
    dfs_y = - fs_y / n
    coords_x = [start_x_y[0]]
    coords_y = [start_x_y[1]]
    for j in range(0, n - 1):
        new_dX.append(round(dX[j] + dfs_x, 1))
        new_dY.append(round(dY[j] + dfs_y, 1))
        if j != n - 2:
            coords_x.append(round(coords_x[j] + new_dX[j], 1))
            coords_y.append(round(coords_y[j] + new_dY[j], 1))
    coords_x.append(start_x_y[2])
    coords_y.append(start_x_y[3])
    return direct_angles, coords_x, coords_y


def get_final_h(h_array, s_array, ini_and_fin_H):
    E_s = sum(s_array)
    n = len(s_array)
    E_h = sum(h_array)
    E_hteo = round(ini_and_fin_H[1] - ini_and_fin_H[0], 2)
    fh = round(E_hteo - E_h, 2)
    new_h_array = []
    H_array = [ini_and_fin_H[0]]
    for j in range(n):
        new_h_array.append(round(h_array[j] + fh / n, 2))
        if j != n - 1:
            H_array.append(round(H_array[j] + new_h_array[j], 2))
    H_array.append(ini_and_fin_H[1])
    return H_array


def get_matrix(coords, H_arr):
    import csv
    n = len(coords)
    coords2 = []

    for i in range(n):
        coords2.append([int(coords[i][0]), int(coords[i][1]), H_arr[i]])
    print(coords2)
    # coords2 = [
    #     [21686, 15921, 636.84],
    #     [20783, 15458, 639.61],
    #     [19767, 15877, 643.46],
    #     [20260, 17775, 647.4],
    #     [18505, 17065, 640.52]
    # ]

    coords2 = sorted(coords2, key=lambda y: y[1])

    max_x = max([round(x[0]) for x in coords2])

    min_x = min([round(x[0]) for x in coords2])
    s = min_x - 2
    e = max_x + 2
    fieldnames = [str(i) for i in range(s, e)]

    cor = []
    f = None
    d = {}
    for i in range(n):
        if coords2[i][1] != f:
            f = coords2[i][1]
            if i != 0:
                for j in fieldnames:
                    if not j in d.keys():
                        d[j] = 0
                cor.append(d)
                d = {}
                if i != 0:
                    if coords2[i - 1][1] != coords2[i][1] - 1:
                        for j in range(coords2[i - 1][1]+1, coords2[i][1]):
                            for z in fieldnames:
                                d[z] = 0
                            cor.append(d)
                            d = {}
        d[str(coords2[i][0])] = str(coords2[i][2])
    else:
        for j in fieldnames:
            if not j in d.keys():
                d[j] = 0
        cor.append(d)

    with open('eggs.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(cor)):
            writer.writerow(cor[i])


def get_x_y_points_on_station(station_direct_angle, doc, station_coords):
    i = doc["i"]
    H = doc["H"]
    L = doc["L"]
    R = doc["R"]


    k = list(doc)[5:]
    dX = []
    dY = []
    print(station_direct_angle, '----------------')
    for point in k:
        v = convert_str_into_degrees(doc[point]["vert_angle"]) + convert_str_into_degrees(doc["M0"])
        S = round(doc[point]["D"] * cos(radians(v)) ** 2, 1)
        local_direct_angle = station_direct_angle + convert_str_into_degrees(doc[point]["hor_angle"]) - convert_str_into_degrees("180°0'")
        dX.append(round(-1 * S * cos(radians(local_direct_angle)), 1))
        dY.append(round(-1 * S * sin(radians(local_direct_angle)), 1))

    coords = []
    for i in range(len(dX)):
        coords.append([round(dX[i]+station_coords[0], 1), round(dY[i]+station_coords[1], 1)])
    return coords[:11]


if __name__ == "__main__":
    with open('data.toml', 'r', encoding='utf-8') as fp:
        doc = load(fp)
        k = list(doc)[5:]
    an = []
    for point in k:
        a = get_mean_hor_angle(doc[point]["hor_angle"]["l_prev_angle"], doc[point]["hor_angle"]["l_next_angle"],
                               doc[point]["hor_angle"]["r_prev_angle"], doc[point]["hor_angle"]["r_next_angle"])
        an.append(a)

    h_arr = []
    s_arr = []

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
        h, s = get_mean_h(l_prev_angle, r_prev_angle, l_next_angle, r_next_angle, l_prev_length, r_prev_length,
                          l_next_length,
                          r_next_length, D_dict, i, V)
        h_arr.append(h)
        s_arr.append(s)

    initial_x_y = [doc["coords"]["initial_x"], doc["coords"]["initial_y"], doc["coords"]["final_x"],
                   doc["coords"]["final_y"]]
    D_angles, x, y = get_x_y(doc["dir_angles"]["initial_angle"], doc["dir_angles"]["final_angle"], an, s_arr, initial_x_y)
    coords = []
    for i in range(len(x)):
        coords.append([x[i], y[i]])
    initial_and_final_H = [doc["heights"]["initial_h"], doc["heights"]["final_h"]]
    H_arr = get_final_h(h_arr, s_arr, initial_and_final_H)
    print(coords)
    for i in range(1, 4):
        coords.extend(get_x_y_points_on_station(D_angles[i], doc["ПП26"]["data"], coords[i]))
        print(coords)
        # H_arr.append(634.34)
    H_arr = [1, 1, 1, 1, 1, 3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
    # H_arr = [1, 1, 1, 1, 1]
    get_matrix(coords, H_arr)

    # plate_coords = [round(doc["coords"]["initial_x"] - doc["coords"]["final_x"]),
    #                 round(doc["coords"]["initial_y"] - doc["coords"]["final_y"])]
    #
    # print(plate_coords)
