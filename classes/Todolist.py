global global_ID
global_ID = 0

def increment_global_ID():
    global global_ID
    global_ID += 1

class Todolist:
    # Method run when this object instantiated
    def __init__(self):
        self.Tasks = [] # Tasks [[Task1, isCompleted?],[Task2, isCompleted?]]
        self.ID = global_ID
        increment_global_ID()
        self.TimeLeft = 0
        
    # ------ PRINT OBJECT STATE ------- #
    
    # Print all the TodoList attributes
    def print_state(self):
        print(
            'ID:', self.ID,
            'Tasks:', self.Tasks
            )
    
    # ------ GETTERS ------- #
    
    # Return the ID of the TodoList
    def get_ID(self):
        return self.ID
    
    # Return the task list of the TodoList
    def get_Tasks(self):
        return self.Tasks
    
    # Return the task with its completion state
    def get_task(self, index:int):
        return self.Tasks[index]
    
    # Return the task without its completion state
    def get_task_text(self, index:int):
        return self.Tasks[index][0]
    
    # Return the completion state of a task
    def get_task_completion(self, index:int):
        return self.Tasks[index][1]
    
    def get_time_left(self):
        return self.TimeLeft
    
    def get_nb_completed(self):
        completed = 0
        for task in self.get_Tasks():
            if (task[1] == True):
                completed += 1
        return completed        
            
    # ------ SETTERS ------- #
    
    # Set the ID, only used for recovering data
    def set_ID(self, new_ID):
        self.ID = new_ID
    
    def set_time_left(self, newTimeLeft):
        self.TimeLeft = newTimeLeft
        
    def decrement_time_left(self):
        self.TimeLeft -= 1
    
    # TODO: Ajouter des try and catch sur les methodes qui en necessite
    # ------ METHODS ------- #
    
    # Add a task at the end of the tasks list
    def add_task(self, task:str, completion=False):
        self.Tasks.append([task, completion]) 
        
    # Add several tasks contained in the parameter in the the tasks list
    def add_tasks(self, tasks:list):
        for t in tasks:
            self.Tasks.append([t[0],t[1]])
    
    # Remove a task at the specified index    
    def remove_task(self, index:int):
        self.Tasks.remove(self.Tasks[index])
        
    # Remove all the tasks of the todolist  
    def clear_tasks(self):
        self.Tasks = []
        
    # Mark a task at the specified index as completed    
    def mark_task_as_completed(self, index):
        self.Tasks[index][1] = True
    
    # Unmark a task at the specified index      
    def unmark_completed_task(self, index):
        self.Tasks[index][1] = False    
    
    def time_is_set(self):
        if (self.TimeLeft > 0):
            return True
        return False