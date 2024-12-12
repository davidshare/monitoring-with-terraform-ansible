import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { updateTodo, deleteTodo } from "@/lib/api"

interface TodoGridProps {
  todos: Todo[];
  setTodos: React.Dispatch<React.SetStateAction<Todo[]>>;
}

export function TodoGrid({ todos, setTodos }: TodoGridProps) {
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
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {todos.map((todo) => (
        <Card key={todo.id} className={`${todo.completed ? "bg-muted" : ""}`}>
          <CardHeader>
            <CardTitle>{todo.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{todo.description}</p>
            <div className="mt-2">
              <Badge variant={todo.priority === "high" ? "destructive" : todo.priority === "medium" ? "default" : "secondary"}>
                {todo.priority}
              </Badge>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline" size="sm" onClick={() => handleStatusChange(todo.id, !todo.completed)}>
              {todo.completed ? "Mark Incomplete" : "Mark Complete"}
            </Button>
            <Button variant="destructive" size="sm" onClick={() => handleDelete(todo.id)}>
              Delete
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

