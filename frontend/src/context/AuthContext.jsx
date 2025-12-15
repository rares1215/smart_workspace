import { createContext, useContext, useState } from "react";
import { logout as logoutAPI } from "../api/auth";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuth, setIsAuth] = useState(
        localStorage.getItem("isAuth") === "true"
    );

    const loginSuccess = () => {
        setIsAuth(true);
        localStorage.setItem("isAuth", "true");
    };

    const logout = async () => {
        await logoutAPI();
        setIsAuth(false);
        localStorage.removeItem("isAuth");
    };

    return (
        <AuthContext.Provider value={{ isAuth, loginSuccess, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);

