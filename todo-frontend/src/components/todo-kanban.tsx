import { useState } from "react"
import { DragDropContext, Droppable, Draggable, DropResult } from "@hello-pangea/dnd"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { updateTodo } from "@/lib/api"

interface TodoKanbanProps {
  todos: Todo[];
  setTodos: React.Dispatch<React.SetStateAction<Todo[]>>;
}

type ColumnKey = "To Do" | "In Progress" | "Done";

type Columns = {
  [key in ColumnKey]: Todo[];
};


export function TodoKanban({ todos, setTodos }: TodoKanbanProps) {
  const [columns, setColumns] = useState<Columns>({
    "To Do": todos.filter(t => !t.completed && t.status !== "in-progress"),
    "In Progress": todos.filter(t => t.status === "in-progress"),
    "Done": todos.filter(t => t.completed)
  })

  const onDragEnd = async (result: DropResult) => {
    if (!result.destination) return

    const { source, destination } = result
    const sourceColumn = columns[source.droppableId as ColumnKey]
    const destColumn = columns[destination.droppableId as ColumnKey]
    const [removed] = sourceColumn.splice(source.index, 1)
    destColumn.splice(destination.index, 0, removed)

    setColumns({
      ...columns,
      [source.droppableId]: sourceColumn,
      [destination.droppableId]: destColumn
    })

    // Update todo status in the backend
    const newStatus = destination.droppableId === "Done" ? "completed" :
      destination.droppableId === "In Progress" ? "in-progress" : "todo"
    await updateTodo(removed.id, { status: newStatus, completed: newStatus === "completed" })

    // Update todos state
    setTodos(prev => prev.map(todo =>
      todo.id === removed.id ? { ...todo, status: newStatus, completed: newStatus === "completed" } : todo
    ))
  }

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <div className="flex gap-4 overflow-x-auto pb-4">
        {Object.entries(columns).map(([columnId, tasks]) => (
          <div key={columnId} className="flex-1 min-w-[300px]">
            <div className="bg-muted/50 p-3 rounded-t-lg border-b">
              <h3 className="font-semibold">{columnId}</h3>
              <p className="text-sm text-muted-foreground">{tasks.length} tasks</p>
            </div>
            <Droppable droppableId={columnId}>
              {(provided, snapshot) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className={`bg-muted/30 p-4 rounded-b-lg min-h-[500px] transition-colors ${snapshot.isDraggingOver ? "bg-muted" : ""
                    }`}
                >
                  {tasks.map((task, index) => (
                    <Draggable key={task.id} draggableId={String(task.id)} index={index}>
                      {(provided, snapshot) => (
                        <Card
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className={`mb-2 transition-shadow ${snapshot.isDragging ? "shadow-lg" : ""
                            }`}
                        >
                          <CardHeader className="p-3">
                            <CardTitle className="text-sm font-medium">
                              {task.title}
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="p-3 pt-0">
                            {task.description && (
                              <p className="text-sm text-muted-foreground mb-2">
                                {task.description}
                              </p>
                            )}
                            <div className="flex items-center gap-2">
                              <Badge
                                variant={
                                  task.priority === "high"
                                    ? "destructive"
                                    : task.priority === "medium"
                                      ? "default"
                                      : "secondary"
                                }
                              >
                                {task.priority}
                              </Badge>
                              {task.dueDate && (
                                <Badge variant="outline">
                                  Due {new Date(task.dueDate).toLocaleDateString()}
                                </Badge>
                              )}
                            </div>
                          </CardContent>
                        </Card>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </div>
        ))}
      </div>
    </DragDropContext>
  )
}

