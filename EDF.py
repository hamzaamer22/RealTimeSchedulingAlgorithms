from tkinter import *

count = 0
process_array = []
unfinished = 0


class RunProcesses:
    def __init__(self, num_of_processes, exec_time, deadline):
        self.processes = num_of_processes
        self.schedulable = True
        self.executed = 0

        self.available = [1] * num_of_processes
        self.start_deadline = deadline.copy()
        self.deadline = deadline.copy()
        self.execution_time = exec_time.copy()
        self.remaining_execution = exec_time.copy()

    def check_min_deadline(self):
        min_deadline = 9999
        min_process = 99
        for i in range(self.processes):
            if self.deadline[i] < min_deadline and self.available[i]:
                min_deadline = self.deadline[i]
                min_process = i
        return min_process

    def check_availability_refresh(self):
        for i in range(self.processes):
            if self.deadline[i] == self.executed:
                if self.available[i]:
                    global unfinished
                    unfinished = i
                    return False
                else:
                    self.deadline[i] += self.start_deadline[i]
                    self.available[i] = 1
                    self.remaining_execution[i] = self.execution_time[i]
        return True

    def run(self, size):
        global count
        global process_array
        while self.executed < size:
            self.schedulable = self.check_availability_refresh()
            if not self.schedulable:
                return False

            curr = self.check_min_deadline()
            self.executed += 1
            if curr == 99:
                # print(f"{self.executed - 1}-{self.executed}: Stall")
                process_array.append('Stall')
                count = count + 1
            else:
                # print(f"{self.executed - 1}-{self.executed}: P{curr}")
                process_array.append(curr)
                count = count + 1
                self.remaining_execution[curr] -= 1
                if self.remaining_execution[curr] == 0:
                    self.available[curr] = 0
        return True


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def lcm(a, b):
    return (a * b) // gcd(a, b)


def lcm_array(arr, n):
    result = arr[0]
    for i in range(1, n):
        result = lcm(result, arr[i])
    return result


if __name__ == '__main__':
    print("Using Earliest Deadline First Algorithm")
    # processes = 4
    processes = int(input("Enter number of processes: "))
    dead = []
    exe = []
    for i in range(processes):
        print(f"Enter deadline for process {i}: ")
        dead.append(int(input()))
    for i in range(processes):
        print(f"Enter execution time for process {i}: ")
        exe.append(int(input()))

    result = lcm_array(dead, processes)
    # print(f"Processes will run for {result} seconds")

    rp = RunProcesses(processes, exe, dead)
    schedulable = rp.run(result)
    if not schedulable:
        print(f"Process {unfinished} was recreated before its previous entity could complete")
        print("\nThus given Process, Deadline and Execution time combination is not schedulable")
    else:
        print("\nGiven Process, Deadline and Execution time combination is schedulable")
    #     print()
    #     print()

    for i in range(count):
        print(process_array[i],end=" | ")

    # create a new tkinter window
    colors = ['blue', 'orange', 'coral', 'teal', 'pink', 'cyan', 'gray', 'brown', 'red']
    window = Tk()
    window.title("Earliest Deadline First Algorithm")
    window.minsize(height=500, width=800)
    window.config(padx=20, pady=20)
    if schedulable:
        # create 10 boxes with numbers
        labels = []
        for i in range(0, result):
            # print(process_array[i])
            if process_array[i] == "Stall":
                label = Label(window, text='P' + str(process_array[i]), width=10, height=5, relief="solid",
                              borderwidth=1, foreground="yellow", background="black")
            else:
                label = Label(window, text='P' + str(process_array[i]), width=10, height=5, relief="solid",
                              borderwidth=1,
                              background=f"{colors[process_array[i]]}")
            label.grid(row=i // 10, column=i % 10)

    else:
        # create 10 boxes with numbers
        labels = []
        for i in range(0, len(process_array)):
            if process_array[i] == "Stall":
                label = Label(window, text='P' + str(process_array[i]), width=10, height=5, relief="solid",
                              borderwidth=1, background="black", foreground="yellow")
            else:
                label = Label(window, text='P' + str(process_array[i]), width=10, height=5, relief="solid",
                              borderwidth=1,
                              background=f"{colors[process_array[i]]}")
            label.grid(row=i // 10, column=i % 10)

        # start the tkinter event loop
    head_label = Label(window, text="Earliest DeadLine First Algorithm", font=("Arial", 20, "bold"), fg="#36454F")
    head_label.place(relx=0.5, rely=1.0, anchor="s")

    window.mainloop()
