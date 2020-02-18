class MathModel:

    def __init__(self, file):
        model = self.parse_from_file(file)
        self.function = model['function']
        self.tresholds = model['tresholds']

    def parse_from_file(self, file):
        data = []
        for line in file:
            data.append([x for x in line.split(',')])

        tresholds = data[:-1]
        function=data[len(data)-1]

        function = [float(i) for i in function]
        tresholds = [[float(j) for j in i] for i in tresholds]

        return {'function': function, 'tresholds': tresholds}

    def get_function(self):
        """
        Получение разрешающей функции
        """
        return self.function

    def get_tresholds(self):
        return self.tresholds