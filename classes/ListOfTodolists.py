# List of Todolist
class ListOfTodolists:
    
    # Method run when this object instantiated
    def __init__(self):
        self.Todos = []
        self.Selected = None

    # ------ PRINT OBJECT STATE ------- #
    
    # Print the state of all the todolists
    def print_states(self):
        for todo in self.Todos:
            todo.print_state()
            
    # ------ GETTERS ------- #
        
    def get_Todos(self):
        return self.Todos        
            
    def get_Loaded(self):
        return self.Selected  

    def get_selected_todolist(self):
        return self.Todos[self.Selected]
            
    # ------ METHODS ------- #
    
    # Add a todolist in the list
    def add_todolist(self, todo:list):
        self.Todos.append(todo)

    
    # Delete a todolist in the list and all the bounded tasks
    def delete_todolist(self, index:int):
        self.Todos[index].clear_tasks()
        self.Todos.remove(self.Todos[index])


    # Delete the selected todolist in the list and all its tasks
    def delete_selected_todolist(self):
        if (not self.Selected == None):
            self.Todos[self.Selected].clear_tasks()
            self.Todos.remove(self.Todos[self.Selected])
        else:
            print('No todolist has been selected')
            
    # Select a todolist in the list
    def select_todolist(self, index:int):
        self.Selected = index
