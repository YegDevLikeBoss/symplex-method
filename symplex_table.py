class SymplexTable:

    def __init__(self, model):
        self.table = [i for i in model.get_tresholds()]
        self.table.append([ 0-i for i in model.get_function() ])
        self.table[-1].append(0.0)
        self.function_vector = [0 for i in range(len(model.get_tresholds()))]
        self.function_coeff_vector = [i for i in model.get_function()]
        
    def get_table(self):
        return self.table

    def _get_alowing_element(self):
        """
        Поиск разрешающего элемента
        """
        table = self.table

        max_evaluation = self._get_max_abs_f_string()
        try:
            max_evaluation_index = table[-1].index(max_evaluation * -1) # Индекс максимального по модулю элемента f-строки
        except ValueError:
            max_evaluation_index = table[-1].index(max_evaluation)

        # Получение отношения свободных членов к положительным элементам разрешающего столбца
        сolumn_data = []
        column_relationship = []
        for i in table[:-1]:
            сolumn_data.append(i[max_evaluation_index])
        for i in range(len(table)-1):
            try:
                column_relationship.append(table[i][-1] / сolumn_data[i])
            except ZeroDivisionError:
                column_relationship.append(999999)
            if column_relationship[i] < 0:
                column_relationship[i] = 999999

        print(column_relationship) 

        min_row_index = column_relationship.index(min(column_relationship))

        print(table[min_row_index][max_evaluation_index])
        return {'value': table[min_row_index][max_evaluation_index], 'indexes': [min_row_index, max_evaluation_index]}

    def _get_max_abs_f_string(self):
        """
        Получение максимального по модулю элемента f-строки
        """
        #return max([abs(i) for i in self.table[-1][:-1]])
        print(abs(min([i for i in self.table[-1][:-1]])))
        return abs(min([i for i in self.table[-1][:-1]]))

    def _rect_method(self, data):
        """
        Рассчёт значения по правилу прямоугольника
        """
        return ((data[0] * data[1]) - (data[2] * data[3])) / data[1]

    def iterate_once(self):
        alowing_element = self._get_alowing_element()
        table = [x[:] for x in self.table]

        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if i != alowing_element['indexes'][0] and j != alowing_element['indexes'][1]:
                    self.table[i][j] = round(self._rect_method([table[i][j], alowing_element['value'], table[i][alowing_element['indexes'][1]], table[alowing_element['indexes'][0]][j]]), 3)
                elif i == alowing_element['indexes'][0] and j != alowing_element['indexes'][1]:
                    self.table[i][j] = round(table[i][j] / alowing_element['value'], 3)
                elif i != alowing_element['indexes'][0] and j == alowing_element['indexes'][1]:
                    self.table[i][j] = round(table[i][j] / alowing_element['value'] * -1, 3)
                else:
                    self.table[i][j] = round(1 / alowing_element['value'], 3)

        # Меняем местами коэффициенты
        temp = self.function_vector[alowing_element['indexes'][0]]
        self.function_vector[alowing_element['indexes'][0]] = self.function_coeff_vector[alowing_element['indexes'][1]]
        self.function_coeff_vector[alowing_element['indexes'][1]] = temp

        return self.id_f_string_positive()

    def iterate(self):
        is_positive = False
        while is_positive == False:
            is_positive = self.iterate_once()
            print(self.to_string())

    def id_f_string_positive(self):
        """
        Проверка f-строки на положительность
        """
        return all(item >= 0 for item in self.table[-1])

    def to_string(self):
        """
        Получить таблицу в виде строки
        """
        string = ""
        for row in self.table:
            for item in row:
                string += "%.3f " % item
            string += "\n"

        return string