import json

filename = "todo.json"

def load_tasks():
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        initaldata = []
        with open(filename, "w") as file:
            json.dump(initaldata, file, indent = 4)
            print(f"[!] {filename} not found, so a file named {filename} created.\n")
            return initaldata

    except json.JSONDecodeError:
        initaldata = []
        with open(filename, "w") as file:
            json.dump(initaldata, file, indent = 4)
            print(f"[!] {filename} was empty or corrupted. Re-initalisating that file..")
            return initaldata

def save_tasks(tasks: list):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent = 4)


def main():
    print("===============================================\n")
    print("             TO DO LIST MANAGER            \n")
    print("===============================================\n")
    print(" 1. View Tasks\n 2. Add Tasks\n 3. Comlete Task\n 4. Delete Task\n 5. Exit.\n")
    print("===============================================\n")


    tasks = load_tasks()

    while True:
        ch = input("Your Choice(1-5):  ")

        if ch == "1":
            if not tasks:
                print("[!] currently the todo list is empty..!")
                continue
            else :
                print("\n------YOUR TODO LIST------")
                for indx, task in enumerate(tasks):
                    status = "✓" if task["completed"] else " "
                    print(f"{indx+1}. [{status}] {task["title"]}")

        elif ch == "2":
            st = input("Enter the task description:  ")
            task = {"title": st, "completed": False}
            if task:
                tasks.append(task)
                save_tasks(tasks)
                print(f"[✓] {st} added succesfully..!")
            else :
                print("Not valid tasks...!")

        elif ch == "3":
            if not tasks:
                print("[!] there is not tasks....!")
                continue
            else :
                print("\n------YOUR TODO LIST------")
                for indx, task in enumerate(tasks):
                    status = "✓" if task["completed"] else " "
                    print(f"{indx+1}. [{status}] {task["title"]}")

            num = int(input("Enter the task number to mark completed:  "))
            if 1 <= num <= len(tasks):
                tasks[num-1]["completed"] = True
                save_tasks(tasks)
                print(f"[✓] {tasks[num-1]["title"]}. marked as completed")
            else:
                print("Enter a valid task number...!")
                continue

        elif ch == "4":
            if not tasks:
                print("[!] there is no tasks to delete.")
                continue
            else :
                print("\n------YOUR TODO LIST------")
                for indx, task in enumerate(tasks):
                    status = "✓" if task["completed"] else " "
                    print(f"{indx+1}. [{status}] {task["title"]}")

                num = int(input("Enter the number of the task to delete:  "))
                if 1 <= num <= len(tasks):
                    removed_task = tasks.pop(num-1)
                    save_tasks(tasks)
                    print(f"{removed_task["title"]} has been removed from the todo list..")
                else :
                    print("Enter a valid task number..!")
                    continue

        elif ch == "5":
            print("\nThank You..:)\n")
            break

        else:
            print("Enter a valid choise....!")
            continue

if __name__ == "__main__":
    main()

