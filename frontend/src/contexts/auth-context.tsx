import React, { createContext, useEffect, ReactNode, useState } from "react";
import { User } from "firebase/auth";
import { FirebaseService, ILogin } from "../services/firebase-service";
import { Button } from "semantic-ui-react";
import { getCookie, setCookie } from "typescript-cookie";

interface IContext {
  fb?: FirebaseService;
  login?: () => Promise<void>;
  logout?: () => Promise<void>;
}

export const AuthContext = createContext<ILogin & IContext>({});

export const AuthProvider = (props: { children?: ReactNode }) => {
  const [user, setUser] = useState<User | undefined>();
  const [token, setToken] = useState<string | undefined>();
  const firebaseService = new FirebaseService();

  const onLogin = (auth: ILogin) => {
    const { user, token, expiration } = auth;
    setUser(user);
    setToken(token);
    setCookie("oauth-token", token, { expires: expiration });
  };

  const login = async () => {
    await firebaseService.login(onLogin);
  };

  const logout = async () => {
    await firebaseService.logout();
    setUser(undefined);
    setToken(undefined);
  };

  useEffect(() => {
    const unsubscribe = firebaseService.auth.onAuthStateChanged(
      async (user: User | null) => {
        if (user) {
          console.log("logged in!", user);
          try {
            setUser(user);
          } catch (error) {
            console.error(error);
          }
          if (!token) {
            const newToken = getCookie("oauth-token");
            setToken(newToken);
          }
        } else {
          setUser(undefined);
          console.log("Not logged in.");
        }
      }
    );
    return () => {
      unsubscribe();
    };
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, token, fb: firebaseService, login, logout }}
    >
      {user ? (
        <>
          {props.children}
          <Button onClick={logout}>logout</Button>
        </>
      ) : (
        <h1>
          Please <Button onClick={login}>login</Button>
        </h1>
      )}
    </AuthContext.Provider>
  );
};
