import {decodeToken, getToken, logout, setToken} from "./jwtHandlers";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_URL) {
  throw new Error(
    "NEXT_PUBLIC_API_URL is not defined in the environment variables"
  );
}

const formatTags = (tags: string): string[] => {
  const trimmedTags = tags.trim();
  const tagArray = trimmedTags.split(",").filter((tag) => tag.trim() !== "");
  const formattedTags = tagArray.map((tag) => tag.toLowerCase());

  return formattedTags;
};

const formatDate = (dateString: string | null): string => {
  if (!dateString) {
    return "";
  }

  const date = new Date(dateString);

  return date.toISOString().slice(0, 19);
};

// Fetch with Authentication
async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getToken();

  if (!token || decodeToken(token)) {
    logout();
    throw new Error("Token expired or not found");
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...options.headers,
  };

  try {
    const response = await fetch(`${API_URL}${url}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API request failed with status ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Fetch request failed:", error);
    throw error;
  }
}

// Login Function
export async function login(email: string, password: string) {
  try {
    const response = await fetch(`${API_URL}/auth/login/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({email, password}),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();
    setToken(data.access_token);
    return data;
  } catch (error) {
    console.error("Login request failed:", error);
    throw error;
  }
}

// Register Function
export async function register(
  username: string,
  email: string,
  password: string
) {
  try {
    const response = await fetch(`${API_URL}/auth/register/`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({username, email, password}),
    });

    if (!response.ok) {
      throw new Error("Registration failed");
    }

    const data = await response.json();
    localStorage.setItem("token", data.access_token);
    return data;
  } catch (error) {
    console.error("Registration request failed:", error);
    throw error;
  }
}

// CRUD Functions for Todos
export async function getTodos() {
  const todos = await fetchWithAuth("/todos/");
  return todos;
}

export async function createTodo(todo: any) {
  todo.tags = formatTags(todo.tags);
  todo.start_date = formatDate(todo.start_date);
  todo.due_date = formatDate(todo.due_date);
  console.log(todo);
  return fetchWithAuth("/todos/", {
    method: "POST",
    body: JSON.stringify(todo),
  });
}

export async function updateTodo(id: number, updates: any) {
  return fetchWithAuth(`/todos/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  });
}

export async function deleteTodo(id: number) {
  return fetchWithAuth(`/todos/${id}/`, {
    method: "DELETE",
  });
}
