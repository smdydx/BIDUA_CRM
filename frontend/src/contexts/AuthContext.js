
import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

// Create the AuthContext
const AuthContext = createContext();

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  // Set axios default headers
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');
    
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
    }
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/v1/auth/login', {
        username: email,
        password: password
      });
      
      if (response.data.access_token) {
        const { access_token, user: userData } = response.data;
        
        setToken(access_token);
        setUser(userData);
        
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(userData));
        
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        toast.success('Login successful!');
        return true;
      }
    } catch (error) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.detail || 'Login failed';
      toast.error(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
    toast.success('Logged out successfully!');
  };

  const register = async (userData) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/v1/auth/register', userData);
      
      if (response.data.access_token) {
        const { access_token, user: newUser } = response.data;
        
        setToken(access_token);
        setUser(newUser);
        
        localStorage.setItem('token', access_token);
        localStorage.setItem('user', JSON.stringify(newUser));
        
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        toast.success('Registration successful!');
        return true;
      }
    } catch (error) {
      console.error('Registration error:', error);
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      toast.error(errorMessage);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    token,
    login,
    logout,
    register,
    loading,
    isAuthenticated: !!token
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
