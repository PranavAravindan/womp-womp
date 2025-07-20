def add_tasks(tasks):
    print()
    n_tasks = int(input("How many tasks do you want to add? "))
    for i in range(n_tasks):
        while True:
            task = input("Enter the task name: ")
            # Check if the task already exists
            task_exists = False
            for existing_task in tasks:
                if existing_task["task"] == task:
                    task_exists = True
                    print("Task already exists. Please re-enter.")
                    break  # Stop checking if a duplicate is found

            if not task_exists:
                tasks.append({"task": task, "done": False})
                print("Task added!")
                break  # Exit the inner loop since a unique task is added
# Display all tasks and their status
def show_tasks(tasks):
    print("\nTasks:")
    # Loop through each task and print its status (Done/Not Done)
    for index, task in enumerate(tasks):
        status = "Done" if task["done"] else "Not Done"
        print(f"{index + 1}. {task['task']} - {status}")

# Mark a task as done
def mark_task_done(tasks):
    task_index = int(input("Enter the task number to mark as done: ")) - 1
    # Check if the input is valid
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = True
        print("Task marked as done!")
    else:
        print("Invalid task number.")
        
def remove_task(tasks):
    task_index = int(input("Enter the task number to remove: ")) - 1
    if 0 <= task_index < len(tasks):
        del tasks[task_index]  # Remove the task at the specified index
        print("Task removed!")
    else:
        print("Invalid task number.")
    

# Main to manage the to-do list operations
def main():
    tasks = []  # Store tasks
    while True:
        print("\nTo Do List: ")
        print("1. Add Tasks")
        print("2. Show Tasks")
        print("3. Mark Task Complete")
        print("4. Remove Task")
        print("5. Exit")

        choice = input("Enter your choice (number): ")

        # Handle the user's choice
        if choice == '1':
            add_tasks(tasks) 
        elif choice == '2':
            show_tasks(tasks)  
        elif choice == '3':
            mark_task_done(tasks)
        elif choice == '4':
            remove_task(tasks)
        elif choice == '5':
            print("Exiting the To-Do List.")
            break 
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()