import jwt from "jsonwebtoken";

export const setToken = (token: string) => {
  localStorage.setItem("token", token);
};

export const getToken = () => {
  return localStorage.getItem("token");
};

// Function to decode a JWT token
export const decodeToken = (
  token: string | null
): Record<string, unknown> | null => {
  if (!token) {
    return null;
  }

  try {
    // Decode the token
    const decoded = jwt.decode(token, {complete: true}) as any;

    if (!decoded || !decoded.user) {
      return null;
    }

    // Return only the payload (without signature verification)
    return decoded.user;
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
};

export const isAuthenticatedUser = () => {
  return decodeToken(getToken()) ? true : false;
};

export const logout = () => {
  localStorage.removeItem("token");
  window.location.href = "/";
};
