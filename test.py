
import unittest
from dataclasses import dataclass, replace, field
from datetime import datetime

# Define the Task dataclass
@dataclass
class Task:
    description: str
    created_at: datetime
    deleted_at: datetime = field(default=None)

# Define the ToDoList class
class ToDoList:
    def __init__(self):
        self.todos = []

    # Add a new task to the list
    def add_task(self, task):
        self.todos.append(task)

    # Remove a task from the list by index
    def remove_task(self, idx):
        if 0 <= idx < len(self.todos):
            self.todos.pop(idx)
        else:
            print("Invalid index")

    # Mark a task as completed by index
    def complete_task(self, idx):
        if 0 <= idx < len(self.todos):
            task = self.todos[idx]
            self.todos[idx] = replace(task, deleted_at=datetime.now())
            print("Task completed!")
        else:
            print("Invalid index")

    # Rename a task by index
    def rename_task(self, idx, new_description):
        if 0 <= idx < len(self.todos):
            task = self.todos[idx]
            self.todos[idx] = replace(task, description=new_description)
        else:
            print("Invalid index")

    # Display the tasks in the list
    def display_list(self):
        output = "Here is your to-do list!\n"
        for i, todo in enumerate(self.todos):
            output += f"{i}: {todo.description} (Created at: {todo.created_at})\n"
        return output.strip()

# Define the TestToDoList unittest class
class TestToDoList(unittest.TestCase):
    def test_add_task(self):
        """
        Test adding task to the ToDoList
        """
        todo_list = ToDoList()
        todo_list.add_task(Task("Buy groceries", datetime.now()))
        self.assertEqual(len(todo_list.todos), 1)

    def test_remove_task(self):
        """
        Test removing task from the ToDoList
        """
        todo_list = ToDoList()
        todo_list.add_task(Task("Buy groceries", datetime.now()))
        todo_list.add_task(Task("Walk the dog", datetime.now()))
        todo_list.remove_task(0)
        self.assertEqual(len(todo_list.todos), 1)

    def test_complete_task(self):
        """
        Test marking a task as completed from the ToDoList
        """
        todo_list = ToDoList()
        todo_list.add_task(Task("Buy groceries", datetime.now()))
        todo_list.add_task(Task("Walk the dog", datetime.now()))
        todo_list.complete_task(0)
        self.assertIsNotNone(todo_list.todos[0].deleted_at)

    def test_rename_task(self):
        """
        Test renaming a task from the ToDoList
        """
        todo_list = ToDoList()
        todo_list.add_task(Task("Buy groceries", datetime.now()))
        todo_list.add_task(Task("Walk the dog", datetime.now()))
        todo_list.rename_task(0, "Pick up groceries")
        self.assertEqual(todo_list.todos[0].description, "Pick up groceries")

    def test_display_list(self):
        """
        Test displaying the to-do list from the ToDoList
        """
        todo_list = ToDoList()
        todo_list.add_task(Task("Buy groceries", datetime.now()))
        todo_list.add_task(Task("Walk the dog", datetime.now()))
        expected_output = "Here is your to-do list!\n0: Buy groceries (Created at: " + str(todo_list.todos[0].created_at) + ")\n1: Walk the dog (Created at: " + str(todo_list.todos[1].created_at) + ")"
        self.assertEqual(todo_list.display_list(), expected_output)

# Define the main application function
def run_application():
    todo_list = ToDoList()
    while True:
        print("1. Add task")
        print("2. Remove task")
        print("3. Complete task")
        print("4. Rename task")
        print("5. Display list")
        print("6. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            task = Task(description, datetime.now())
            todo_list.add_task(task)
        elif choice == "2":
            idx = int(input("Enter the index of the task you would like to remove: "))
            todo_list.remove_task(idx)
        elif choice == "3":
            idx = int(input("Enter the index of the task you would like to complete: "))
            todo_list.complete_task(idx)
        elif choice == "4":
            idx = int(input("Enter the index of the task you would like to rename: "))
            new_description = input("Enter the new description: ")
            todo_list.rename_task(idx, new_description)
        elif choice == "5":
            print(todo_list.display_list())
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_type = input("Enter 'unittest' to run unit tests or 'application' to run the application: ")
    if main_type == "unittest":
        unittest.main()
    elif main_type == "application":
        run_application()
    else:
        print("Invalid command")
