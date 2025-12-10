import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('token');
        const adminEmail = localStorage.getItem('admin_email');
        const orgName = localStorage.getItem('organization_name');

        if (token) {
            setUser({ email: adminEmail, organization_name: orgName });
        }
        setLoading(false);
    }, []);

    const login = async (email, password) => {
        const response = await api.post('/admin/login', { email, password });
        const { access_token, admin_email, organization_id } = response.data;

        localStorage.setItem('token', access_token);
        localStorage.setItem('admin_email', admin_email);
        localStorage.setItem('organization_name', organization_id);

        setUser({ email: admin_email, organization_name: organization_id });
    };

    const register = async (orgName, email, password) => {
        await api.post('/org/create', { organization_name: orgName, email, password });
        // Auto login after register
        await login(email, password);
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('admin_email');
        localStorage.removeItem('organization_name');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
