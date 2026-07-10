import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { apiRequest, tokenStorage } from "../infrastructure/apiClient";

export type AuthUser = {
  id: number;
  nickname?: string;
  phone?: string;
  scopes: string[];
};

type LoginResponse = {
  token: string;
  user_id: number;
  user?: AuthUser;
};

type AuthContextValue = {
  user: AuthUser | null;
  isAuthenticated: boolean;
  sendCode(phone: string): Promise<void>;
  login(phone: string, code: string): Promise<void>;
  logout(): void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

const userStorageKey = "heaotang_user";

function readStoredUser(): AuthUser | null {
  const stored = sessionStorage.getItem(userStorageKey);
  if (!stored || !tokenStorage.get()) return null;
  try {
    const parsed = JSON.parse(stored) as Partial<AuthUser>;
    if (typeof parsed.id !== "number") {
      throw new Error("stored user id is invalid");
    }
    return {
      ...parsed,
      id: parsed.id,
      scopes: Array.isArray(parsed.scopes)
        ? parsed.scopes.filter((scope): scope is string => typeof scope === "string")
        : [],
    };
  } catch {
    sessionStorage.removeItem(userStorageKey);
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(readStoredUser);

  const sendCode = useCallback(async (phone: string) => {
    await apiRequest("/api/v1/auth/send-code", {
      method: "POST",
      body: JSON.stringify({ phone }),
    });
  }, []);

  const login = useCallback(async (phone: string, code: string) => {
    const result = await apiRequest<LoginResponse>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ phone, code }),
    });
    const authenticatedUser = result.user ?? {
      id: result.user_id,
      phone,
      nickname: `用户${phone.slice(-4)}`,
      scopes: [],
    };
    tokenStorage.set(result.token);
    sessionStorage.setItem(userStorageKey, JSON.stringify(authenticatedUser));
    setUser(authenticatedUser);
  }, []);

  const logout = useCallback(() => {
    tokenStorage.clear();
    sessionStorage.removeItem(userStorageKey);
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, isAuthenticated: Boolean(user && tokenStorage.get()), sendCode, login, logout }),
    [login, logout, sendCode, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
