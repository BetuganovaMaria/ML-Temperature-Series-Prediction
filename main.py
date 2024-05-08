import csv
import random
import matplotlib.pyplot as plt


data = []

with open('MLTempDataset.csv', 'r') as file:
    reader = csv.reader(file)
    reader = list(reader)
    for row in reader[1:]:
        data.append(float(row[2]))

plt.plot([i for i in range(len(data))], data)
plt.show()

data_train = data[:5341]
data_test = data[5341:]


num_train = len(data_train)
num_test = len(data_test)

print(num_train, num_test, len(data))

# ВЫБОР АВТОРЕГРЕССИИ

# x_i ср1
sr1 = sum(data_train) / num_train
# x_i * x_i - 1 ср2
sr2 = sum([data_train[i] * data_train[i - 1] for i in range(1, len(data_train))]) / (num_train - 1)
# x_i * x_i - 2 ср3
sr3 = sum([data_train[i] * data_train[i - 2] for i in range(2, len(data_train))]) / (num_train - 2)
# x_i * x_i - 3 ср4
sr4 = sum([data_train[i] * data_train[i - 3] for i in range(3, len(data_train))]) / (num_train - 3)
# x_i ** 2 ср5
sr5 = sum([i ** 2 for i in data_train]) / num_train

# Авторегрессия первого порядка

a1_1 = (sr2 - sr3) / (sr5 - sr2)
a0_1 = (sr2 - a1_1 * sr5) / sr1

data_test_y_1 = [0] * num_test
data_test_y_1[0] = a0_1 + a1_1 * data_train[-1]
for i in range(1, num_test):
    data_test_y_1[i] = a0_1 + a1_1 * data_test_y_1[i - 1]

deviation_1 = sum([(data_test[i] - data_test_y_1[i]) ** 2 for i in range(num_test)]) / num_test

# Авторегрессия второго порядка

a1_2 = (sr2 - sr4) / (sr5 - sr3)
a2_2 = (sr2 - sr3) / (sr2 - sr5) + a1_2
a0_2 = (sr2 - a1_2 * sr5 - a2_2 * sr2) / sr1

data_test_y_2 = [0] * num_test
data_test_y_2[0] = a0_2 + a1_2 * data_train[-1] + a2_2 * data_train[-2]
data_test_y_2[1] = a0_2 + a1_2 * data_test_y_2[0] + a2_2 * data_train[-1]
for i in range(2, num_test):
    data_test_y_2[i] = a0_2 + a1_2 * data_test_y_2[i - 1] + a2_2 * data_test_y_2[i - 2]

deviation_2 = sum([(data_test[i] - data_test_y_2[i]) ** 2 for i in range(num_test)]) / num_test

print(deviation_1, deviation_2)
print()

# deviation_1 > deviation_2  # True => выбираем авторегрессию второго порядка

# РАСЧЕТ ЭПСИЛОН ДЛЯ x_i ИЗ data_train

epsilon_train = [0] * num_train

for i in range(2, num_train):
    epsilon_train[i] = a0_2 + a1_2 * data_train[i - 1] + a2_2 * data_train[i - 2] - data_train[i]

# Гистограмма

plt.hist(epsilon_train, bins=80)
plt.show()

# получаем примерно от -2 до 2
# тогда формула epsilon = 4 * random.random() - 2
# (random.random() - от 0.0 до 1.0)
deviation = 0
for i in range(10):
    # epsilon
    epsilon_test = [4 * random.random() - 2 for _ in range(num_test)]
    data_test_y = [0] * num_test
    data_test_y[0] = data_test_y_2[0] + epsilon_test[0]
    data_test_y[1] = a0_2 + a1_2 * data_test[0] + a2_2 * data_train[-1] + epsilon_test[1]
    for j in range(2, num_test):
        data_test_y[j] = a0_2 + a1_2 * data_test[j - 1] + a2_2 * data_test[j - 2] + epsilon_test[j]

    # ср. кв. отклонение
    deviation += sum([(data_test[j] - data_test_y[j]) ** 2 for j in range(num_test)]) / num_test

    # график
    plt.plot([j for j in range(num_test)], data_test_y)

deviation /= 10
print(deviation)

plt.scatter([j for j in range(num_test)], data_test, zorder=2, s=7)

plt.show()
