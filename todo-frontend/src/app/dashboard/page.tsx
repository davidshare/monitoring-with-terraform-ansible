"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { TodoList } from "@/components/todo-list";
import { TodoGrid } from "@/components/todo-grid";
import { TodoKanban } from "@/components/todo-kanban";
import { CreateTodoModal } from "@/components/create-todo-modal";
import { getTodos } from "@/lib/api";
import withAuth from "@/components/hoc/withClientAuth";

const DashboardPage = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [view, setView] = useState("list");

  useEffect(() => {
    const fetchTodos = async () => {
      try {
        const fetchedTodos = await getTodos();
        setTodos(fetchedTodos);
      } catch (error) {
        console.error("Failed to fetch todos:", error);
      }
    };

    fetchTodos();
  }, []);

  const handleCreateTodo = (newTodo: Todo) => {
    setTodos([...todos, newTodo]);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="space-x-2">
          <Button
            variant={view === "list" ? "default" : "outline"}
            onClick={() => setView("list")}
          >
            List
          </Button>
          <Button
            variant={view === "grid" ? "default" : "outline"}
            onClick={() => setView("grid")}
          >
            Grid
          </Button>
          <Button
            variant={view === "kanban" ? "default" : "outline"}
            onClick={() => setView("kanban")}
          >
            Kanban
          </Button>
          <Button onClick={() => setIsCreateModalOpen(true)}>Create Todo</Button>
        </div>
      </div>
      {view === "list" && <TodoList todos={todos} setTodos={setTodos} />}
      {view === "grid" && <TodoGrid todos={todos} setTodos={setTodos} />}
      {view === "kanban" && <TodoKanban todos={todos} setTodos={setTodos} />}
      <CreateTodoModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreateTodo={handleCreateTodo}
      />
    </div>
  );
};

export default withAuth(DashboardPage);
