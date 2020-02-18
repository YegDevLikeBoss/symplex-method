import math_model
import symplex_table

raw_data = open("data.txt", encoding='utf-8')

model = math_model.MathModel(raw_data)
table = symplex_table.SymplexTable(model)

print("коэффиценты задачи линейного программирования", model.get_function())
print("коэффиценты неравенства")
for row in model.get_tresholds():
    print('%s\n' % row)

table.iterate()