import { useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { updateTodo, deleteTodo } from "@/lib/api"

interface TodoListProps {
  todos: Todo[];
  setTodos: React.Dispatch<React.SetStateAction<Todo[]>>;
}

export function TodoList({ todos, setTodos }: TodoListProps) {
  const [editingId, setEditingId] = useState<number | null>(null);

  const handleStatusChange = async (id: number, completed: boolean) => {
    try {
      await updateTodo(id, { completed })
      setTodos(todos.map(todo => todo.id === id ? { ...todo, completed } : todo))
    } catch (error) {
      console.error("Failed to update todo status:", error)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await deleteTodo(id)
      setTodos(todos.filter(todo => todo.id !== id))
    } catch (error) {
      console.error("Failed to delete todo:", error)
    }
  }

  return (
    <div className="space-y-4">
      {todos.map((todo: Todo) => (
        <div key={todo.id} className="flex items-center justify-between p-4 bg-card rounded-lg shadow">
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={todo.completed}
              onCheckedChange={(checked) => handleStatusChange(todo.id, checked as boolean)}
            />
            <span className={todo.completed ? "line-through text-muted-foreground" : ""}>
              {todo.title}
            </span>
          </div>
          <div className="space-x-2">
            <Button variant="outline" size="sm" onClick={() => setEditingId(todo.id)}>
              Edit
            </Button>
            <Button variant="destructive" size="sm" onClick={() => handleDelete(todo.id)}>
              Delete
            </Button>
          </div>
        </div>
      ))}
    </div>
  )
}

