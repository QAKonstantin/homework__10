from subprocess import (
    run, PIPE
)
from datetime import datetime

file = open(f"{datetime.now().strftime('%d-%m-%Y-%H-%M')}-scan.txt", "w")
file_err = open("stderr.txt", "w")

# get_cpu_used = ["wsl", "top", "-b", "-n", "1", "|", "head", "-2", "|", "awk", "/^CPU/ {print \$2}"]
file.write("Отчёт о состоянии системы:\n")
print("Отчёт о состоянии системы:")

list_users = run(["wsl", "ps", "-o", "user"], stdout=PIPE, stderr=file_err)
users = list_users.stdout.decode("utf-8").replace("\n", " ").split()[1:]
dict_user = {}
for i in users:
    if i not in dict_user:
        dict_user[i] = 0

users_list = str(list(dict_user.keys())).replace("[", "").replace("]", "")
print("Пользователи системы:", users_list)
file.write("Пользователи системы: " + users_list)

print("Процессов запущено:", len(users))
file.write("\nПроцессов запущено: " + str(len(users)) + "\n")

print("Пользовательских процессов:")
file.write("Пользовательских процессов:\n")

for i in users:
    if i in dict_user.keys():
        dict_user[i] += 1
user_processes = str(dict_user).replace("{", "").replace("}", "").replace(", ", "\n")
print(user_processes)
file.write(user_processes + "\n")

process = run(["wsl", "free", "-m", "|", "awk", "/^Mem/ {print \$3}"], stdout=PIPE, stderr=file_err)
used_memory = int(process.stdout.decode("utf-8"))
process = run(["wsl", "free", "-m", "|", "awk", "/^Mem/ {print \$2}", "|", "head", "-2", "|", "tail", "-1"],
              stdout=PIPE, stderr=file_err)
total_memory = int(process.stdout.decode("utf-8"))
print("Всего памяти используется: " + str(round(used_memory * 100 / total_memory, 1)).replace("\n", "") + "%")
file.write("Всего памяти используется: " + str(round(used_memory * 100 / total_memory, 1)).replace("\n", "") + "%\n")

process = run(["wsl", "top", "-b", "-n", "1", "|", "head", "-2", "|", "awk", "/^CPU/ {print \$2}"], stdout=PIPE,
              stderr=file_err)

cpu = process.stdout.decode("utf-8")
print("Всего CPU используется: " + cpu.replace("\n", ""))
file.write("Всего CPU используется: " + cpu)

process = run(
    ["wsl", "ps", "-e", "-o", "comm=", "|", "sort", "-n", "-r", "-k", "1", "|", "head", "-1", "|", "cut", "-c1-20"],
    stdout=PIPE, stderr=file_err)
max_memory = process.stdout.decode("utf-8")
print("Больше всего памяти использует: " + max_memory.replace("\n", ""))
file.write("Больше всего памяти использует: " + max_memory)

process = run(["wsl", "top", "-b", "-n", "1", "|", "tail", "-2", "|", "awk", "{print \$8, \$9}"],
              stdout=PIPE, stderr=file_err)
max_cpu = process.stdout.decode("utf-8").split()
print("Больше всего CPU использует: " + max_cpu[0] + " " + max_cpu[1][0:20])
file.write("Больше всего CPU использует: " + max_cpu[0] + " " + max_cpu[1][0:20])

file.close()
file_err.close()
