import numpy as np
import heapq as hp

class Brain():
    def __init__(self, rows_par, columbs_para):
        self.rows_par = rows_par
        self.colums_par = columbs_para
        self.rows_len = len(self.rows_par)
        self.colums_len = len(self.colums_par)
        self.result = [["@" for i in range(self.colums_len)] for j in range(self.rows_len)]
        self.colums = [["@" for i in range(self.rows_len)] for j in range(self.colums_len)]
        self.variation_rows = []
        self.variation_colums = []

    def display(self):
        x = True
        count = 0
        while x == True:
            x = False
            for i in range(self.rows_len):
                for j in range(self.colums_len):
                    if self.result[i][j] == "@":
                        x = True
                        count += 1
                        break
                if x == True:
                    break
            if x == True and count == 1:
                Brain.kickoff(self)
                Brain.check_full(self)
                print (count, ". Iterace")
                print (repr(self.colums_par))
                for i in range(len(self.result)):
                    print (repr(self.result[i]) + '||' + repr(self.rows_par[i]))
            elif x == True and count > 1:
                Brain.thinker(self)
                Brain.check_full(self)
                print (count, ". Iterace")
                print (repr(self.colums_par))
                for i in range(len(self.result)):
                    print (repr(self.result[i]) + '||' + repr(self.rows_par[i]))
        return self.result

    def thinker(self):
        for i in range(self.rows_len):
            index = 0
            for j in range(len(self.rows_par[i])):
                index += self.rows_par[i][j]
            index += len(self.rows_par[i]) - 1
            z = Brain.rating(self, True, i)
            count_1, count_0= Brain.reading_result(self, True, i)
            count = count_0 + count_1
            if count > z and count != self.colums_len:
                Brain.finding_common_properties(self, True, i)
            elif count > (0.25 * self.colums_len) and count != self.colums_len:
                Brain.finding_common_properties(self, True, i)
        
        for i in range(self.colums_len):
            index = 0
            for j in range(len(self.colums_par[i])):
                index += self.colums_par[i][j]
            index += len(self.colums_par[i]) - 1
            z = Brain.rating(self, False, i)
            count_1, count_0= Brain.reading_result(self, False, i)
            count = count_0 + count_1
            if count > z and count != self.rows_len:
                Brain.finding_common_properties(self, False, i)
            elif count > (0.25 * self.colums_len) and count != self.rows_len:
                Brain.finding_common_properties(self, False, i)

    def write(self, x, y):
        self.result[x][y] = "#"
        self.colums[y][x] = "#"
    
    def write_pause(self, x, y):
        self.result[x][y] = "."
        self.colums[y][x] = "."

    def check_full(self):
        for i in range(self.rows_len):
            list = []
            count = 0
            for j in range(self.colums_len):
                if self.result[i][j] == "#":
                    count += 1
                elif self.result[i][j] != "#" and count != 0:
                    list.append(count)
                    count = 0
            if count != 0:
                list.append(count)
            if list == self.rows_par[i]:
                Brain.complete(self, True, i)

        for i in range(self.colums_len):
            list = []
            count = 0
            for j in range(self.rows_len):
                if self.colums[i][j] == "#":
                    count += 1
                elif self.colums[i][j] != "#" and count != 0:
                    list.append(count)
                    count = 0
            if count != 0:
                list.append(count)
            if list == self.colums_par[i]:
                Brain.complete(self, False, i) 

    def complete(self, row, i):
        if row == True:
            for j in range(self.colums_len):
                if self.result[i][j] == "@":
                    Brain.write_pause(self, i, j)
        else:
            for j in range(self.rows_len):
                if self.colums[i][j] == "@":
                    Brain.write_pause(self, j, i)

    def kickoff(self):
        for i in range(self.rows_len):
        #pro radky
            index = 0
            for j in range(len(self.rows_par[i])):
                index += self.rows_par[i][j]
            index += len(self.rows_par[i]) - 1
            if index == self.colums_len:
                Brain.partical_fill_row(self, i)
            elif index < 0:
                if len(self.rows_par[i]) == 0:
                    Brain.easy_fill_row(self, False, i)
            else:
                z = Brain.rating(self, True, i)
                if z > 0:
                    Brain.finding_common_properties(self, True, i)
        #pro sloupce
        for i in range(self.colums_len):
            index = 0
            for j in range(len(self.colums_par[i])):
                index += self.colums_par[i][j]
            index += len(self.colums_par[i]) - 1
            if index == self.rows_len:
                Brain.partical_fill_columbs(self, i)
            elif index < 0:
                if len(self.colums_par[i]) == 0:
                    Brain.easy_fill_columbs(self, False, i)
            else:
                z = Brain.rating(self, False, i)
                if z > 0:
                    Brain.finding_common_properties(self, False, i)

    def reading_result(self, row, i):
        if row == True:
            count = 0
            cout = 0
            for j in range(self.colums_len):
                if self.result[i][j] == "#":
                    count += 1
                elif self.result[i][j] == ".":
                    cout += 1
            return count, cout
        else:
            count = 0
            cout = 0
            for j in range(self.rows_len):
                if self.colums[i][j] == "#":
                    count += 1
                elif self.colums[i][j] == ".":
                    cout += 1
            return count, cout

    def rating(self, raw, i):
        if raw == True:
            H = 0
            for j in range(len(self.rows_par[i])):
                H += self.rows_par[i][j]
            H += len(self.rows_par[i]) - 1
            p = self.colums_len - H
            return H - (p + (len(self.rows_par[i]) - 1)*(p + 1))
        else:
            H = 0
            for j in range(len(self.colums_par[i])):
                H += self.colums_par[i][j]
            H += len(self.colums_par[i]) - 1
            p = self.colums_len - H
            return H - (p + (len(self.colums_par[i]) - 1)*(p + 1))

    def easy_fill_row(self, full, i):
        #řádky plně obsazené buď # nebo *
        if full == False:
            for k in range(self.colums_len):
                Brain.write_pause(self, i, k)
        if full == True:
            for k in range(self.colums_len):
                Brain.write(self, i, k)

        #sloupce plně obsazené buď # nebo *
    def easy_fill_columbs(self, full, i):
        if full == False:
            for k in range(self.rows_len):
                Brain.write_pause(self, k, i)
        if full == True:
            for k in range(self.rows_len):
                Brain.write(self, k, i)

    def partical_fill_row(self, i):
        #řádky plně obsazené kombinaci #
        # i = znamena radek
            l = 0
            for j in range(len(self.rows_par[i])):
                for k in range(self.rows_par[i][j]):
                    Brain.write(self, i, l)
                    l += 1
                if l < self.colums_len:
                    Brain.write_pause(self, i, l)
                    l += 1

        #sloupce plně obsazené kombinaci #
        #i znamena sloupec
    def partical_fill_columbs(self, i):
            l = 0
            for j in range(len(self.colums_par[i])):
                for k in range(self.colums_par[i][j]):
                    Brain.write(self, l, i)
                    l += 1
                if l < self.rows_len:
                    Brain.write_pause(self, l, i)
                    l += 1

    def find_group(self, variations):
        ball = 0
        group = 0
        for l in range(len(variations)):
            if variations[l] == 1 and ball == 0:
                ball = 1
            elif variations[l] == 0 and ball == 1:
                ball = 0
            elif variations[l] == 0 and ball == 0:
                group = l
                ball = 2
            elif ball == 2 and variations[l] == 1:
                return group, l - 1
        return group, 0

    def variations_row(self, i):
        H = 0
        for j in range(len(self.rows_par[i])):
            H += self.rows_par[i][j]
        H += len(self.rows_par[i]) - 1
        p = self.colums_len - H
        if p < 0:
            list = []
            for j in range(len(self.rows_par[i])-1):
                list.append(1)
                list.append(0)
            list.append(1)
            return list
        variations = []
        list = []
        for j in range(p - 1):
            list.append(0)
        for j in range(len(self.rows_par[i])):
            list.append(0)
            list.append(1)
        variations.append(list)
        j = 0
        same = False
        while True:
            list = [0 for i in range(len(variations[j-1]))]
            swap = False
            for k in range(len(self.rows_par[i]) * 2 + p - 1):
                if swap == True:
                    list[k] = variations[j][k]
                else:
                    list[k] = variations[j][k]
                    if list[0] == 0:
                        trans = 0
                    else: 
                        trans = 1
                    if variations[j][k] == 1 and trans == 0:
                        list[k - 1] = 1
                        list[k] = 0
                        swap = True
                        trans = 1
                    elif trans == 1 and k == 0:
                        group, pozition = Brain.find_group(self, variations[j])
                        index = 0
                        if pozition == 0:
                            same = True
                            break
                        else:
                            while index < (len(self.rows_par[i]) * 2 + p - 1):
                                if index == pozition - group:
                                    for h in range(group):
                                        list[index + h] = variations[j][h]
                                    index += group
                                elif index == pozition:
                                    list[index] = 1
                                    index += 1
                                    continue
                                elif index < pozition - group:
                                    list[index] = 0
                                    index += 1
                                elif index == pozition + 1:
                                    list[index] = 0
                                    index += 1
                                else:
                                    list[index] = variations[j][index]
                                    index += 1
                            break
                    else:
                        list[k] = variations[j][k]
            if same == True:
                break
            else:
                j += 1
                variations.append(list)
        return variations

    def variations_colums(self, i):
        H = 0
        for j in range(len(self.colums_par[i])):
            H += self.colums_par[i][j]
        H += len(self.colums_par[i]) - 1
        p = self.rows_len - H
        if p <= 0:
            list = []
            for j in range(len(self.colums_par[i])-1):
                list.append(1)
                list.append(0)
            list.append(1)
            return list
        variations = []
        list = []
        for j in range(p - 1):
            list.append(0)
        for j in range(len(self.colums_par[i])):
            list.append(0)
            list.append(1)
        variations.append(list)
        j = 0
        same = False
        while True:
            list = [0 for i in range(len(variations[j-1]))]
            swap = False
            for k in range(len(self.colums_par[i]) * 2 + p - 1):
                if swap == True:
                    list[k] = variations[j][k]
                else:
                    list[k] = variations[j][k]
                    if list[0] == 0:
                        trans = 0
                    else: 
                        trans = 1
                    if variations[j][k] == 1 and trans == 0:
                        list[k - 1] = 1
                        list[k] = 0
                        swap = True
                        trans = 1
                    elif trans == 1 and k == 0:
                        group, pozition = Brain.find_group(self, variations[j])
                        index = 0
                        if pozition == 0:
                            same = True
                            break
                        else:
                            while index < (len(self.colums_par[i]) * 2 + p - 1):
                                if index == pozition - group:
                                    for h in range(group):
                                        list[index + h] = variations[j][h]
                                    index += group
                                elif index == pozition:
                                    list[index] = 1
                                    index += 1
                                    continue
                                elif index < pozition - group:
                                    list[index] = 0
                                    index += 1
                                elif index == pozition + 1:
                                    list[index] = 0
                                    index += 1
                                else:
                                    list[index] = variations[j][index]
                                    index += 1
                            break
                    else:
                        list[k] = variations[j][k]
            if same == True:
                break
            else:
                j += 1
                variations.append(list)
        return variations

    def creating_all_state(self, row, i):
        storage = []
        if row == True:
            var = Brain.variations_row(self, i)
            storage.append(i)
            magazin = []
            for j in range(len(var)):
                list = []
                index = 0
                for k in range(len(var[j])):
                    if var[j][k] == 0:
                        list.append(".")
                    else:
                        for g in range(self.rows_par[i][index]):
                            list.append("#")
                        index += 1
                magazin.append(list)
            storage.append(magazin)
            self.variation_rows.append(storage)
        else:
            var = Brain.variations_colums(self, i)
            storage.append(i)
            magazin = []
            for j in range(len(var)):  
                list = []
                index = 0
                for k in range(len(var[j])):
                    if var[j][k] == 0:
                        list.append(".")
                    else:
                        for g in range(self.colums_par[i][index]):
                            list.append("#")
                        index += 1
                magazin.append(list)
            storage.append(magazin)
            self.variation_colums.append(storage)

    def playfield_regognicion(self, row, i):
        if row == True:
            notes = []
            for j in range(len(self.result[i])):
                list = []
                if self.result[i][j] == "#":
                    list.append("#")
                    list.append(j)
                    notes.append(list)
                elif self.result[i][j] == ".":
                    list.append(".")
                    list.append(j)
                    notes.append(list)
            return notes
        else:
            notes = []
            for j in range(len(self.colums[i])):
                list = []
                if self.colums[i][j] == "#":
                    list.append("#")
                    list.append(j)
                    notes.append(list)
                elif self.colums[i][j] == ".":
                    list.append(".")
                    list.append(j)
                    notes.append(list)
            return notes
    
    def finding_common_properties(self, row, i):
        if row == True:
            index = -1
            for j in range(len(self.variation_rows)):
                if self.variation_rows[j][0] == i:
                    index = j
            if index == - 1:
                Brain.creating_all_state(self, True, i)
                for j in range(len(self.variation_rows)):
                    if self.variation_rows[j][0] == i:
                        index = j
            notes = Brain.playfield_regognicion(self, True, i)
            k = 0 
            while k < len(self.variation_rows[index][1]):
                count = 0
                for j in range(len(notes)):
                    if self.variation_rows[index][1][k][notes[j][1]] == notes[j][0]:
                        count += 1
                if count != len(notes):
                    del self.variation_rows[index][1][k]
                else: 
                    k += 1
            for j in range(len(self.variation_rows[index][1][0])):
                count = 0    
                for k in range(len(self.variation_rows[index][1])):
                    if self.variation_rows[index][1][k][j] == "#":
                        count += 1
                    elif self.variation_rows[index][1][k][j] == ".":
                        count -= 1
                if count == len(self.variation_rows[index][1]):
                    Brain.write(self, i, j)
                elif abs(count) == len(self.variation_rows[index][1]):
                    Brain.write_pause(self, i, j)
        else:
            index = -1
            for j in range(len(self.variation_colums)):
                if self.variation_colums[j][0] == i:
                    index = j
            if index == - 1:
                Brain.creating_all_state(self, False, i)
                for j in range(len(self.variation_colums)):
                    if self.variation_colums[j][0] == i:
                        index = j
            notes = Brain.playfield_regognicion(self, False, i)
            k = 0 
            while k < len(self.variation_colums[index][1]):
                count = 0
                for j in range(len(notes)):
                    if self.variation_colums[index][1][k][notes[j][1]] == notes[j][0]:
                        count += 1
                if count != len(notes):
                    del self.variation_colums[index][1][k]
                else:
                    k += 1
            for j in range(len(self.variation_colums[index][1][0])):
                count = 0    
                for k in range(len(self.variation_colums[index][1])):
                    if self.variation_colums[index][1][k][j] == "#":
                        count += 1
                    elif self.variation_colums[index][1][k][j] == ".":
                        count -= 1
                if count ==len(self.variation_colums[index][1]):
                    Brain.write(self, j, i)
                elif abs(count) == len(self.variation_colums[index][1]):
                    Brain.write_pause(self, j, i)
                
