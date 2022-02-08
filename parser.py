import subprocess
from datetime import datetime

file = open(f"{datetime.now().strftime('%d-%m-%Y-%H-%M')}-scan.txt", "w")
file_err = open("stderr.txt", "w")
get_root = ["wsl", "cut", "-d:", "-f1", "/etc/passwd"]
get_processes = ["wsl", "ps", "-e", "|", "wc", "-l"]
get_memory_used = ["wsl", "free", "-m", "|", "awk", "/^Mem/ {print \$3}"]
get_cpu_used = ["wsl", "top", "-b", "-n", "1", "|", "head", "-2", "|", "awk", "/^CPU/ {print \$2}"]
get_max_memory_used = ["wsl", "ps", "-e", "-o", "comm=", "|", "sort", "-n", "-r", "-k", "1", "|", "head", "-1", "|",
                       "cut", "-c1-20"]
get_max_cpu_used = ["wsl", "top", "-b", "-n", "1", "|", "tail", "-2", "|", "awk", "{print \$9}", "|", "cut", "-c1-20"]
file.write("Отчёт о состоянии системы:\n")
print("Отчёт о состоянии системы:")

process = subprocess.Popen(get_root, stdout=subprocess.PIPE, stderr=file_err)
users = process.stdout.read().decode("utf-8").replace("\n", " ")
print("Пользователи системы:", users)
file.write("Пользователи системы: " + users)

process = subprocess.Popen(get_processes, stdout=subprocess.PIPE, stderr=file_err)
processes = process.stdout.read().decode("utf-8")
print("Процессов запущено:", processes.replace("\n", ""))
file.write("\nПроцессов запущено: " + processes)

print("Пользовательских процессов:")
file.write("Пользовательских процессов:\n")

for i in range(len(users.split())):
    process_users = ["wsl", "ps", "aux", "|", "grep", f"{users.split()[i]}", "|", "wc", "-l"]
    process = subprocess.Popen(process_users, stdout=subprocess.PIPE, stderr=file_err)
    std_out = process.stdout.read().decode("utf-8")
    print((users.split()[i] + ": " + std_out).replace("\n", ""))
    file.write(users.split()[i] + ": " + std_out)

process = subprocess.Popen(get_memory_used, stdout=subprocess.PIPE, stderr=file_err)
memory = process.stdout.read().decode("utf-8")
print("Всего памяти используется: " + memory.replace("\n", "") + " mb")
file.write("Всего памяти используется: " + memory.replace("\n", "") + " mb\n")

process = subprocess.Popen(get_cpu_used, stdout=subprocess.PIPE, stderr=file_err)
cpu = process.stdout.read().decode("utf-8")
print("Всего CPU используется: " + cpu.replace("\n", ""))
file.write("Всего CPU используется: " + cpu)

process = subprocess.Popen(get_max_memory_used, stdout=subprocess.PIPE, stderr=file_err)
max_memory = process.stdout.read().decode("utf-8")
print("Больше всего памяти использует: " + max_memory.replace("\n", ""))
file.write("Больше всего памяти использует: " + max_memory)

process = subprocess.Popen(get_max_cpu_used, stdout=subprocess.PIPE, stderr=file_err)
max_cpu = process.stdout.read().decode("utf-8")
print("Больше всего CPU использует: " + max_cpu)
file.write("Больше всего CPU использует: " + max_cpu)

file.close()
file_err.close()
