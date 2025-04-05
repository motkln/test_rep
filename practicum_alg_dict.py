class My_dict():
    def __init__(self):
        self.key_val = []

    def __setitem__(self, key, value):
        for i in self.key_val:
            if i[0] == key:
                el_index = self.key_val.index(i)
                self.key_val.remove(i)
                self.key_val.insert(el_index, (key, value))
                break
        else:
            self.key_val.append((key, value))

    def __str__(self):
        res = '{'
        for i in self.key_val:
            res += (f"'{i[0]}': '{i[1]}', ")
        return res[:-2] + '}'

    def __getitem__(self, item):
        for i in self.key_val:
            if i[0] == item:
                return i[1]
        else:
            return False

    def __delitem__(self, key):
        for i in self.key_val:
            if i[0] == key:
                self.key_val.remove(i)

    def keys(self):
        dict_keys = []
        for i in self.key_val:
            dict_keys.append(i[0])
        return f'dict_keys({dict_keys})'

    def values(self):
        dict_values = []
        for i in self.key_val:
            dict_values.append(i[1])
        return f'dict_values({dict_values})'

    def items(self):
        return f'dict_items({self.key_val})'

    def __contains__(self, item):
        for i in self.key_val:
            if i[0] == item:
                return True
        else:
            return False
if __name__ == '__main__':
    slovar = My_dict()
    slovar['Name'] = 'Mot'
    print(slovar)
    slovar['Lastname'] = 'Jackobs'
    print(slovar)
    slovar['Name'] = 'Mat'
    print(slovar)
    print(slovar['Name'])
    # del slovar['Lastname']
    print(slovar)
    print(slovar.keys())
    print(slovar.values())
    print(slovar.items())
    print('Name' in slovar)
