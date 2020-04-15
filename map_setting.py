import numpy as np
import brain

class Assignment():
    def __init__(self, name):
        self.name = name
    
    def size_field(self):
        f = open(self.name + ".txt", "r")
        data = f.readline()
        f.close()
        for i in range(len(data)):
            if data[i] == "x":
                rows = int(data[:i])
                i += 1
                columbs = int(data[i:])
        return rows, columbs

    def read_picture(self):
        rows, columbs = Assignment.size_field(self)
        picture = [[0 for i in range(columbs)] for j in range(rows)]
        f = open(self.name + ".txt", "r")
        for i in range(rows + 1):
            data = f.readline()
            if i != 0:
                for j in range(columbs):
                    if int(data[j]) == 1:
                        picture[i - 1][j] = "#"
                    elif int(data[j]) == 0:
                        picture[i - 1][j] = "."
        f.close()
        return picture

    def display_picture(self):
        picture = Assignment.read_picture(self)
        rows_rule = Assignment.make_rows_play_field(self)
        columbs_rule = Assignment.make_columbs_play_field(self)
        print ("zadáno")
        print (repr(columbs_rule))
        for i in range(len(picture)):
            print (repr(picture[i]) + '||' + repr(rows_rule[i]))
        br = brain.Brain(rows_rule, columbs_rule)
        result = br.display()
        print ("vyřešeno")
        print (repr(columbs_rule))
        for i in range(len(result)):
            print (repr(result[i]) + '||' + repr(rows_rule[i]))

    def make_rows_play_field(self):
        picture = Assignment.read_picture(self)
        rows, columbs = Assignment.size_field(self)
        rows_rules = []
        for i in range(rows):
            count = 0
            row = []
            for j in range(columbs):
                if picture[i][j] == "#":
                    count += 1
                else:
                    if count != 0:
                        row.append(count)
                    count = 0
            if count != 0:
                row.append(count)
            rows_rules.append(row)
        return rows_rules

    def make_columbs_play_field(self):
        picture = Assignment.read_picture(self)
        rows, columbs = Assignment.size_field(self)
        columbs_rules = []
        for i in range(columbs):
            count = 0
            columb = []
            for j in range(rows):
                if picture[j][i] == "#":
                    count += 1
                else:
                    if count != 0:
                        columb.append(count)
                    count = 0
            if count != 0:
                columb.append(count)
            columbs_rules.append(columb)
        return columbs_rules
