import numpy as np
import math

def _read_target_file(file):
    number = []
    element_num = {}

    with open(file, 'r') as str_file:
        POSCAR_lines = str_file.readlines()
        element_line = POSCAR_lines[5]
        num_line = POSCAR_lines[6]
        element = element_line.split()
        for num in num_line.split():
            number.append(int(num))
    for order in range(0,len(element)):
        element_num[element[order]] = number[order]
    # print(element_num)
    print('Reading file successfully!')
    return number, element_num, POSCAR_lines

def _dividing_layers(layer_distance, number, element_num, POSCAR_lines):
    # element_kind_total_num = len(element_num)
    element_position = {}
    key_list = list(element_num.keys())
    for key in element_num:
        tem_position = []
        if key == list(element_num.keys())[0]:
            for tem_n in range(8, element_num[key] + 8):
                tem_coordinate = []
                for tem_xyz in POSCAR_lines[tem_n].split():
                    tem_coordinate.append(float(tem_xyz))
                tem_position.append(tem_coordinate)
        else:
            if key in key_list:
                index = key_list.index(key)
            # print(index)
            # print(type(index))
            # print(number)
            # print(type(number[0]))
            start_atom = int(np.sum(number[:index]))
            # print(number[index-1])
            # print(start_atom)
            end_atom   = int(np.sum(number[:index+1]))
            # print(end_atom)
            for tem_n in range(start_atom + 8, end_atom + 8):
                tem_coordinate = []
                for tem_xyz in POSCAR_lines[tem_n].split():
                    tem_coordinate.append(float(tem_xyz))
                tem_position.append(tem_coordinate)

        element_position[key] = tem_position

    def __group_coordinates(coords):
        coords.sort(key=lambda x: x[2])  # 根据 z 坐标对坐标集进行排序
        groups = []
        current_layer = []  # 初始化当前层为空列表

        for coord in coords:
            if len(current_layer) == 0 or abs(coord[2] - current_layer[0][2]) <= 0.5:
                current_layer.append(coord)  # 在当前层中添加坐标
            else:
                groups.append(current_layer)  # 当前层结束，添加到结果列表中
                current_layer = [coord]  # 开始新的一层

        groups.append(current_layer)  # 添加最后一层

        num_of_layers = len(groups)  # 层数
        return num_of_layers, groups

    # 示例
    with open('fix_POSCAR.vasp','w') as fix_file:
        for j in range(0,len(POSCAR_lines) + 1):
            if j < 7:
                fix_file.write(POSCAR_lines[j])
            if j == 7:
                fix_file.write('Selective Dynamics\n')
            if j == 8:
                fix_file.write('Cartesian\n')
            if j == 9:
                for key in element_position:
                    coords = element_position[key]
                    index = key_list.index(key)
                    num_of_layers, layers = __group_coordinates(coords)
                    # print(layers)
                    print(f"No.{index + 1}  element {num_of_layers}  layers")
                    # fix_layers = []
                    min_fix_layers = int(input('Input fix min layer(e.g 4) :  '))   #if you want to fix all atoms input 1 in min_fix_layers and max in max_fix_layers 
                    max_fix_layers = int(input('Input fix max layer(e.g 10) :  '))  #if you want to move all atoms input 0 in min_fix_layers and 0 in max_fix_layers            
                    for i, layer in enumerate(layers):
                        if min_fix_layers <= i+1 <= max_fix_layers:
                            for fixcoordin in layer:
                                fix_file.write("        {0:^9.10f}        {1:^9.10f}        {2:^9.10f}  F F F\n".format(fixcoordin[0], fixcoordin[1], fixcoordin[2]))
                        else:
                            for movecoordin in layer:
                                fix_file.write("        {0:^9.10f}        {1:^9.10f}        {2:^9.10f}  T T T\n".format(movecoordin[0], movecoordin[1], movecoordin[2]))
                break
                        # print(f"第{i+1}层为{layer}")    

file_name = input('Input taget file :  ')
number, element_num, POSCAR_lines = _read_target_file(file_name)

layer_distance = float(input('Input dividing distance :  '))
_dividing_layers(layer_distance, number, element_num, POSCAR_lines)