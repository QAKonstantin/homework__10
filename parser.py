from subprocess import (
    run, PIPE
)
from datetime import datetime

file = open(f"{datetime.now().strftime('%d-%m-%Y-%H-%M')}-scan.txt", "w")
file_err = open("stderr.txt", "w")

file.write("Отчёт о состоянии системы:\n")
print("Отчёт о состоянии системы:")

command = run(["ubuntu", "run", "ps", "aux"], stdout=PIPE, stderr=file_err, shell=False)
processes = command.stdout.decode("utf-8").split('\n')
temp = []

for i in range(len(processes) - 1):
    temp.append(processes[i].split())
mas_processes = list(map(list, zip(*temp)))

dict_user = {}
for i in mas_processes[0][1:]:
    if i not in dict_user:
        dict_user[i] = 0

users_list = str(list(dict_user.keys())).replace("[", "").replace("]", "")
print("Пользователи системы:", users_list)
file.write("Пользователи системы: " + users_list)

print("Процессов запущено:", len(mas_processes[0]) - 1)
file.write(f"\nПроцессов запущено: {len(mas_processes[0]) - 1}\n")

print("Пользовательских процессов:")
file.write("Пользовательских процессов:\n")

for i in mas_processes[0][1:]:
    if i in dict_user.keys():
        dict_user[i] += 1
user_processes = str(dict_user).replace("{", "").replace("}", "").replace(", ", "\n")
print(user_processes)
file.write(user_processes + "\n")

memory = 0.0
max_memory = 0.0
max_memory_process = ''
for i in range(1, len(mas_processes[3])):
    memory += float(mas_processes[3][i])
    if max_memory <= float(mas_processes[3][i]):
        max_memory = float(mas_processes[3][i])
        max_memory_process = mas_processes[10][i]

print(f"Всего памяти используется: {memory}%")
file.write(f"Всего памяти используется: {memory}%\n")

cpu = 0.0
max_cpu = 0.0
max_cpu_process = ''
for i in range(1, len(mas_processes[2])):
    cpu += float(mas_processes[2][i])
    if max_cpu <= float(mas_processes[3][i]):
        max_cpu = float(mas_processes[3][i])
        max_cpu_process = mas_processes[10][i]
print(f"Всего CPU используется: {cpu}%")
file.write(f"Всего CPU используется: {cpu}%\n")

print(f"Больше всего памяти использует: {max_memory}% {max_memory_process[:20]}")
file.write(f"Больше всего памяти использует: {max_memory}% {max_memory_process[:20]}\n")

print(f"Больше всего CPU использует: {max_cpu}% {max_cpu_process[:20]}")
file.write(f"Больше всего CPU использует: {max_cpu}% {max_cpu_process[:20]}")

file.close()
file_err.close()
