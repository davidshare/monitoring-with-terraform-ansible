interface Todo {
  id: number;
  title: string;
  description: string;
  status: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  dueDate?: string;
}

interface CreateTodoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreateTodo: (todo: Todo) => void;
}
