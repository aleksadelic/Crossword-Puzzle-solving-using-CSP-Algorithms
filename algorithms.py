import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]
        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class BacktrackingAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        moves_list = []

        matrix = []
        for i in range(len(tiles)):
            matrix.append([])
            for j in range(len(tiles[0])):
                matrix[i].append('?')

        domains = {}
        for var in variables:
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        keys = {}
        i = 0
        for var in variables:
            keys[i] = var
            i += 1

        done = []
        for var in variables:
            done.append(False)

        self.backtrack_search(variables, domains, moves_list, keys, 0, matrix, done)

        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution

    def backtrack_search(self, variables, domains, moves_list, keys, lvl, matrix, done):
        # print_matrix(matrix)
        if lvl == len(variables):
            return True

        # find min remaining values
        min = float('inf')
        key = keys[0]
        key_ind = 0
        for i in keys:
            if len(domains[keys[i]]) < min and not done[i]:
                min = len(domains[keys[i]])
                key = keys[i]
                key_ind = i

        # key = keys[lvl]
        num = int(key[:-1])
        index = 0
        for val in domains[key]:
            # print(key, val)
            i = int(num / len(matrix[0]))
            j = int(num % len(matrix[0]))
            # print("i, j =", i, j)

            fits = True
            if key[-1] == 'h':
                for k in range(len(val)):
                    if matrix[i][j + k] != '?' and matrix[i][j + k] != val[k]:
                        fits = False
                        break
            else:
                for k in range(len(val)):
                    if matrix[i + k][j] != '?' and matrix[i + k][j] != val[k]:
                        fits = False
                        break

            if fits:
                moves_list.append([key, index])
                done[key_ind] = True
                # print(moves_list)
                # insert word into matrix
                old_val = []
                if key[-1] == 'h':
                    for k in range(len(val)):
                        old_val.append(matrix[i][j + k])
                        matrix[i][j + k] = val[k]
                else:
                    for k in range(len(val)):
                        old_val.append(matrix[i + k][j])
                        matrix[i + k][j] = val[k]
                new_dom = copy.deepcopy(domains)
                new_dom[key] = [val]
                if self.backtrack_search(variables, new_dom, moves_list, keys, lvl + 1, matrix, done):
                    return True
                if key[-1] == 'h':
                    for k in range(len(val)):
                        matrix[i][j + k] = old_val[k]
                else:
                    for k in range(len(val)):
                        matrix[i + k][j] = old_val[k]

            # print(moves_list)
            index += 1
        moves_list.append([key, None])
        done[key_ind] = False
        return False


def print_matrix(matrix: list):
    for row in matrix:
        print(row)


class ForwardCheckingAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        moves_list = []

        matrix = []
        for i in range(len(tiles)):
            matrix.append([])
            for j in range(len(tiles[0])):
                matrix[i].append('?')

        domains = {}
        for var in variables:
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        keys = {}
        i = 0
        for var in variables:
            keys[i] = var
            i += 1

        done = []
        for var in variables:
            done.append(False)

        solution = []

        self.backtrack_search(variables, domains, moves_list, keys, 0, matrix, tiles, solution, done)

        return solution

    def backtrack_search(self, variables, domains, moves_list, keys, lvl, matrix, tiles, solution, done):
        # print_matrix(matrix)
        if lvl == len(variables):
            return True

        # find min remaining values
        '''min = float('inf')
        key = keys[0]
        key_ind = 0
        for i in keys:
            if len(domains[keys[i]]) < min and not done[i]:
                min = len(domains[keys[i]])
                key = keys[i]
                key_ind = i'''

        # find most constrained var
        max = 0
        key = keys[0]
        key_ind = 0
        for i in keys:
            cur = num_cons(variables, domains, keys, i, matrix, tiles)
            if cur > max:
                max = cur
                key = keys[i]
                key_ind = i

        key = keys[lvl]
        num = int(key[:-1])
        index = 0
        for val in domains[key]:
            # print(key, val)
            i = int(num / len(matrix[0]))
            j = int(num % len(matrix[0]))
            # print("i, j =", i, j)

            fits = True
            if key[-1] == 'h':
                for k in range(len(val)):
                    if matrix[i][j + k] != '?' and matrix[i][j + k] != val[k]:
                        fits = False
                        break
            else:
                for k in range(len(val)):
                    if matrix[i + k][j] != '?' and matrix[i + k][j] != val[k]:
                        fits = False
                        break

            if fits:
                moves_list.append([key, index])
                # solution.append([key, index, domains])
                # print(moves_list)
                # insert word into matrix
                old_val = []
                if key[-1] == 'h':
                    for k in range(len(val)):
                        old_val.append(matrix[i][j + k])
                        matrix[i][j + k] = val[k]
                else:
                    for k in range(len(val)):
                        old_val.append(matrix[i + k][j])
                        matrix[i + k][j] = val[k]
                new_dom = copy.deepcopy(domains)
                new_dom[key] = [val]

                # Forward Checking
                forward_checking(variables, new_dom, matrix, tiles, key, val)

                solution.append([key, 0, new_dom])
                done[key_ind] = True

                continue_flag = False
                for var in variables:
                    if var != key and len(new_dom[var]) == 0:
                        if val != domains[key][len(domains[key]) - 1]:
                            moves_list.append([key, None])
                            solution.append([key, None, domains])
                            done[key_ind] = True
                        index += 1
                        continue_flag = True
                        break
                if continue_flag:
                    if key[-1] == 'h':
                        for k in range(len(val)):
                            matrix[i][j + k] = old_val[k]
                    else:
                        for k in range(len(val)):
                            matrix[i + k][j] = old_val[k]
                    continue

                if self.backtrack_search(variables, new_dom, moves_list, keys, lvl + 1, matrix, tiles, solution, done):
                    return True
                if key[-1] == 'h':
                    for k in range(len(val)):
                        matrix[i][j + k] = old_val[k]
                else:
                    for k in range(len(val)):
                        matrix[i + k][j] = old_val[k]

            # print(moves_list)
            index += 1
        moves_list.append([key, None])
        solution.append([key, None, domains])
        done[key_ind] = True
        return False


def num_cons(variables, new_dom, keys, ind, matrix, tiles):
    key = keys[ind]
    num = int(key[:-1])
    i = int(num / len(matrix[0]))
    j = int(num % len(matrix[0]))
    cons = 0
    for val in new_dom[key]:
        for var in variables:
            if var != key:
                # Check if constrained
                # Update domain
                num_var = int(var[:-1])
                i_var = int(num_var / len(matrix[0]))
                j_var = int(num_var % len(matrix[0]))
                continue_flag = False
                if key[-1] == 'h' and var[-1] == 'v':
                    i_intersect = i
                    j_intersect = j_var
                    if not tiles[i_intersect][j_intersect]:
                        index_h = j_intersect - j
                        index_v = i_intersect - i_var
                        if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(
                                val) and index_v < len(
                                new_dom[var][0]):
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, index_h, val2, index_v)
                                if val[index_h] != val2[index_v]:
                                    cons += 1
                                    continue_flag = True
                                    break
                            if continue_flag:
                                continue
                elif key[-1] == 'v' and var[-1] == 'h':
                    i_intersect = i_var
                    j_intersect = j
                    if not tiles[i_intersect][j_intersect]:
                        index_h = j_intersect - j_var
                        index_v = i_intersect - i
                        if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(
                                new_dom[var][0]) and index_v < len(val):
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, index_v, val2, index_h)
                                if val[index_v] != val2[index_h]:
                                    cons += 1
                                    continue_flag = True
                                    break
                            if continue_flag:
                                continue
                elif key[-1] == 'v' and var[-1] == 'v':
                    if j == j_var:
                        num_var = int(var[:-1])
                        i_var = int(num_var / len(matrix[0]))
                        j_var = int(num_var % len(matrix[0]))
                        tile_between = False
                        low = min(i, i_var)
                        high = max(i, i_var)
                        while low < high:
                            if tiles[low][j]:
                                tile_between = True
                                break
                            low += 1
                        if not tile_between:
                            i_intersect = max(i, i_var)
                            if len(val) < len(new_dom[var][0]):
                                offset = i - i_var
                                for val2 in new_dom[var]:
                                    # print(key, var, "->", val, val2)
                                    same = True
                                    for k in range(len(val)):
                                        if val[k] != val2[k + offset]:
                                            same = False
                                            break
                                    if not same:
                                        cons += 1
                                        continue_flag = True
                                        break
                                if continue_flag:
                                    continue

                            else:
                                offset = i_var - i
                                for val2 in new_dom[var]:
                                    # print(key, var, "->", val, val2)
                                    same = True
                                    for k in range(len(val)):
                                        if val[k + offset] != val2[k]:
                                            same = False
                                            break
                                    if not same:
                                        cons += 1
                                        continue_flag = True
                                        break
                                if continue_flag:
                                    continue
                elif key[-1] == 'h' and var[-1] == 'h':
                    if i == i_var:
                        num_var = int(var[:-1])
                        i_var = int(num_var / len(matrix[0]))
                        j_var = int(num_var % len(matrix[0]))
                        tile_between = False
                        low = min(j, j_var)
                        high = max(j, j_var)
                        while low < high:
                            if tiles[i][low]:
                                tile_between = True
                                break
                            low += 1
                        if not tile_between:
                            if len(val) < len(new_dom[var][0]):
                                offset = j - j_var
                                for val2 in new_dom[var]:
                                    same = True
                                    for k in range(len(val)):
                                        if val[k] != val2[k + offset]:
                                            same = False
                                            break
                                    if not same:
                                        cons += 1
                                        continue_flag = True
                                        break
                                if continue_flag:
                                    continue
                            else:
                                offset = j_var - j
                                for val2 in new_dom[var]:
                                    same = True
                                    for k in range(len(val)):
                                        if val[k + offset] != val2[k]:
                                            same = False
                                            break
                                    if not same:
                                        cons += 1
                                        continue_flag = True
                                        break
                                if continue_flag:
                                    continue
            return cons


class ArcConsistencyAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):

        moves_list = []

        matrix = []
        for i in range(len(tiles)):
            matrix.append([])
            for j in range(len(tiles[0])):
                matrix[i].append('?')

        domains = {}
        for var in variables:
            domains[var] = []
            for word in words:
                if len(word) == variables[var]:
                    domains[var].append(word)

        keys = {}
        i = 0
        for var in variables:
            keys[i] = var
            i += 1

        solution = []

        self.backtrack_search(variables, domains, moves_list, keys, 0, matrix, tiles, solution)

        return solution

    def backtrack_search(self, variables, domains, moves_list, keys, lvl, matrix, tiles, solution):
        # print_matrix(matrix)
        if lvl == len(variables):
            return True
        key = keys[lvl]
        num = int(key[:-1])
        index = 0
        for val in domains[key]:
            # print(key, val)
            i = int(num / len(matrix[0]))
            j = int(num % len(matrix[0]))
            # print("i, j =", i, j)

            fits = True
            if key[-1] == 'h':
                for k in range(len(val)):
                    if matrix[i][j + k] != '?' and matrix[i][j + k] != val[k]:
                        fits = False
                        break
            else:
                for k in range(len(val)):
                    if matrix[i + k][j] != '?' and matrix[i + k][j] != val[k]:
                        fits = False
                        break

            if fits:
                moves_list.append([key, index])
                # solution.append([key, index, domains])
                # print(moves_list)
                # insert word into matrix
                old_val = []
                if key[-1] == 'h':
                    for k in range(len(val)):
                        old_val.append(matrix[i][j + k])
                        matrix[i][j + k] = val[k]
                else:
                    for k in range(len(val)):
                        old_val.append(matrix[i + k][j])
                        matrix[i + k][j] = val[k]
                new_dom = copy.deepcopy(domains)
                new_dom[key] = [val]

                # Forward Checking
                forward_checking(variables, new_dom, matrix, tiles, key, val)

                solution.append([key, 0, new_dom])

                continue_flag = False
                for var in variables:
                    if var != key and len(new_dom[var]) == 0:
                        if val != domains[key][len(domains[key]) - 1]:
                            moves_list.append([key, None])
                            solution.append([key, None, domains])
                        index += 1
                        continue_flag = True
                        break
                if continue_flag:
                    if key[-1] == 'h':
                        for k in range(len(val)):
                            matrix[i][j + k] = old_val[k]
                    else:
                        for k in range(len(val)):
                            matrix[i + k][j] = old_val[k]
                    continue

                # Arc Consistency
                for var in variables:
                    to_delete = []
                    for val2 in new_dom[var]:
                        arc_consistency(variables, new_dom, matrix, tiles, var, val2, to_delete)
                    for val_to_delete in to_delete:
                        new_dom[var].remove(val_to_delete)

                continue_flag = False
                for var in variables:
                    if var != key and len(new_dom[var]) == 0:
                        if val != domains[key][len(domains[key]) - 1]:
                            moves_list.append([key, None])
                            solution.append([key, None, domains])
                        index += 1
                        continue_flag = True
                        break
                if continue_flag:
                    if key[-1] == 'h':
                        for k in range(len(val)):
                            matrix[i][j + k] = old_val[k]
                    else:
                        for k in range(len(val)):
                            matrix[i + k][j] = old_val[k]
                    continue

                if self.backtrack_search(variables, new_dom, moves_list, keys, lvl + 1, matrix, tiles, solution):
                    return True
                if key[-1] == 'h':
                    for k in range(len(val)):
                        matrix[i][j + k] = old_val[k]
                else:
                    for k in range(len(val)):
                        matrix[i + k][j] = old_val[k]

            # print(moves_list)
            index += 1
        moves_list.append([key, None])
        solution.append([key, None, domains])
        return False


def forward_checking(variables, new_dom, matrix, tiles, key, val):
    num = int(key[:-1])
    i = int(num / len(matrix[0]))
    j = int(num % len(matrix[0]))
    for var in variables:
        if var != key:
            # Check if constrained
            # Update domain
            num_var = int(var[:-1])
            i_var = int(num_var / len(matrix[0]))
            j_var = int(num_var % len(matrix[0]))
            to_remove = []
            if key[-1] == 'h' and var[-1] == 'v':
                i_intersect = i
                j_intersect = j_var
                if not tiles[i_intersect][j_intersect]:
                    index_h = j_intersect - j
                    index_v = i_intersect - i_var
                    if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(val) and index_v < len(
                            new_dom[var][0]):
                        for val2 in new_dom[var]:
                            # print(key, var, "->", val, index_h, val2, index_v)
                            if val[index_h] != val2[index_v]:
                                to_remove.append(val2)
            elif key[-1] == 'v' and var[-1] == 'h':
                i_intersect = i_var
                j_intersect = j
                if not tiles[i_intersect][j_intersect]:
                    index_h = j_intersect - j_var
                    index_v = i_intersect - i
                    if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(
                            new_dom[var][0]) and index_v < len(val):
                        for val2 in new_dom[var]:
                            # print(key, var, "->", val, index_v, val2, index_h)
                            if val[index_v] != val2[index_h]:
                                to_remove.append(val2)
            elif key[-1] == 'v' and var[-1] == 'v':
                if j == j_var:
                    num_var = int(var[:-1])
                    i_var = int(num_var / len(matrix[0]))
                    j_var = int(num_var % len(matrix[0]))
                    tile_between = False
                    low = min(i, i_var)
                    high = max(i, i_var)
                    while low < high:
                        if tiles[low][j]:
                            tile_between = True
                            break
                        low += 1
                    if not tile_between:
                        i_intersect = max(i, i_var)
                        if len(val) < len(new_dom[var][0]):
                            offset = i - i_var
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, val2)
                                same = True
                                for k in range(len(val)):
                                    if val[k] != val2[k + offset]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
                        else:
                            offset = i_var - i
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, val2)
                                same = True
                                for k in range(len(val)):
                                    if val[k + offset] != val2[k]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
            elif key[-1] == 'h' and var[-1] == 'h':
                if i == i_var:
                    num_var = int(var[:-1])
                    i_var = int(num_var / len(matrix[0]))
                    j_var = int(num_var % len(matrix[0]))
                    tile_between = False
                    low = min(j, j_var)
                    high = max(j, j_var)
                    while low < high:
                        if tiles[i][low]:
                            tile_between = True
                            break
                        low += 1
                    if not tile_between:
                        if len(val) < len(new_dom[var][0]):
                            offset = j - j_var
                            for val2 in new_dom[var]:
                                same = True
                                for k in range(len(val)):
                                    if val[k] != val2[k + offset]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
                        else:
                            offset = j_var - j
                            for val2 in new_dom[var]:
                                same = True
                                for k in range(len(val)):
                                    if val[k + offset] != val2[k]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
            for val_to_remove in to_remove:
                new_dom[var].remove(val_to_remove)


def arc_consistency(variables, new_dom, matrix, tiles, key, val, to_delete):
    num = int(key[:-1])
    i = int(num / len(matrix[0]))
    j = int(num % len(matrix[0]))
    for var in variables:
        if var != key:
            # Check if constrained
            # Update domain
            num_var = int(var[:-1])
            i_var = int(num_var / len(matrix[0]))
            j_var = int(num_var % len(matrix[0]))
            to_remove = []
            if key[-1] == 'h' and var[-1] == 'v':
                i_intersect = i
                j_intersect = j_var
                if not tiles[i_intersect][j_intersect]:
                    index_h = j_intersect - j
                    index_v = i_intersect - i_var
                    if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(val) and index_v < len(
                            new_dom[var][0]):
                        for val2 in new_dom[var]:
                            # print(key, var, "->", val, index_h, val2, index_v)
                            if val[index_h] != val2[index_v]:
                                to_remove.append(val2)
            elif key[-1] == 'v' and var[-1] == 'h':
                i_intersect = i_var
                j_intersect = j
                if not tiles[i_intersect][j_intersect]:
                    index_h = j_intersect - j_var
                    index_v = i_intersect - i
                    if len(new_dom[var]) > 0 and index_h >= 0 and index_v >= 0 and index_h < len(
                            new_dom[var][0]) and index_v < len(val):
                        for val2 in new_dom[var]:
                            # print(key, var, "->", val, index_v, val2, index_h)
                            if val[index_v] != val2[index_h]:
                                to_remove.append(val2)
            elif key[-1] == 'v' and var[-1] == 'v':
                if j == j_var:
                    num_var = int(var[:-1])
                    i_var = int(num_var / len(matrix[0]))
                    j_var = int(num_var % len(matrix[0]))
                    tile_between = False
                    low = min(i, i_var)
                    high = max(i, i_var)
                    while low < high:
                        if tiles[low][j]:
                            tile_between = True
                            break
                        low += 1
                    if not tile_between:
                        i_intersect = max(i, i_var)
                        if len(val) < len(new_dom[var][0]):
                            offset = i - i_var
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, val2)
                                same = True
                                for k in range(len(val)):
                                    if val[k] != val2[k + offset]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
                        else:
                            offset = i_var - i
                            for val2 in new_dom[var]:
                                # print(key, var, "->", val, val2)
                                same = True
                                for k in range(len(val)):
                                    if val[k + offset] != val2[k]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
            elif key[-1] == 'h' and var[-1] == 'h':
                if i == i_var:
                    num_var = int(var[:-1])
                    i_var = int(num_var / len(matrix[0]))
                    j_var = int(num_var % len(matrix[0]))
                    tile_between = False
                    low = min(j, j_var)
                    high = max(j, j_var)
                    while low < high:
                        if tiles[i][low]:
                            tile_between = True
                            break
                        low += 1
                    if not tile_between:
                        if len(val) < len(new_dom[var][0]):
                            offset = j - j_var
                            for val2 in new_dom[var]:
                                same = True
                                for k in range(len(val)):
                                    if val[k] != val2[k + offset]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
                        else:
                            offset = j_var - j
                            for val2 in new_dom[var]:
                                same = True
                                for k in range(len(val)):
                                    if val[k + offset] != val2[k]:
                                        same = False
                                        break
                                if not same:
                                    to_remove.append(val2)
            if len(new_dom[var]) == len(to_remove):
                to_delete.append(val)
                return
