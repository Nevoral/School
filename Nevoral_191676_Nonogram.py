import map_setting

def switch_demo(num):
    switcher = {
        1: "question_mark",
        2: "cat",
        3: "VAI",
        4: "monkey",
        5: "king_kong",
    }
    return switcher.get(num, "mimo rozsah") 

if __name__ == '__main__':
    k = 1
    while k == 1:
        print('Vyberte obrázek, který chcete testnout:')
        for i in range(4):
            print (i + 1, ": ", switch_demo(i + 1))
        num = input()
        a = switch_demo(int(num))
        x = map_setting.Assignment(a)
        x.display_picture()
        print ('Chcete pokračovat a zkusit jiný obrázek? --> 1 jinak --> 0')
        k = input()
        int(k)
    

