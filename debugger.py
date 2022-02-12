from abc import ABCMeta, abstractmethod


class SetOperation(object):
    __metaclass__ = ABCMeta

    def __init__(self, L, element):
        self.L = L
        self.element = element

    @abstractmethod
    def __call__(self):
        return

    @abstractmethod
    def undo(self):
        return


class Insert(SetOperation):
    def __call__(self):
        self.L.append(self.element)
        self.L.sort()

    def undo(self):
        self.L.remove(self.element)
        self.L.sort()


class Delete(SetOperation):
    def __call__(self):
        self.L.remove(self.element)
        self.L.sort()

    def undo(self):
        self.L.append(self.element)
        self.L.sort()


class UndoableList(object):
    def __init__(self):
        self.undo_commands = []
        self.redo_commands = []
        

    def push_undo_command(self, command):
        """Push the given command to the undo command stack."""
        self.undo_commands.append(command)

    def pop_undo_command(self):
        """Remove the last command from the undo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_undo_command = self.undo_commands.pop()
        except IndexError:
            return "Nothing to undo"
        return last_undo_command

    def push_redo_command(self, command):
        """Push the given command to the redo command stack."""
        self.redo_commands.append(command)

    def pop_redo_command(self):
        """Remove the last command from the redo command stack and return it.
        If the command stack is empty, EmptyCommandStackError is raised.

        """
        try:
            last_redo_command = self.redo_commands.pop()
        except IndexError:
            return "Nothing to redo"
            # raise EmptyCommandStackError()

        return last_redo_command

    def do(self, command):
        """Execute the given command. Exceptions raised from the command are
        not catched.

        """
        command()
        self.push_undo_command(command)
        # clear the redo stack when a new command was executed
        self.redo_commands[:] = []

    def undo(self, n=1):
        """Undo the last n commands. The default is to undo only the last
        command. If there is no command that can be undone because n is too big
        or because no command has been emitted yet, EmptyCommandStackError is
        raised.

        """
        for _ in range(n):
            command = self.pop_undo_command()
            command.undo()
            self.push_redo_command(command)

    def redo(self, n=1):
        """Redo the last n commands which have been undone using the undo
        method. The default is to redo only the last command which has been
        undone using the undo method. If there is no command that can be redone
        because n is too big or because no command has been undone yet,
        EmptyCommandStackError is raised.

        """
        for _ in range(n):
            command = self.pop_redo_command()
            command()
            self.push_undo_command(command)


my_List = [2, 5, 7]
L = UndoableList()
# manager.do(ElementAdder(my_List, 9))
L.do(Insert(my_List, 1))
print(my_List)