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
  const [loading, setLoading] = useState(true);

  // Set axios default headers and base URL
  useEffect(() => {
    // Set base URL for development
    if (process.env.NODE_ENV === 'development') {
      axios.defaults.baseURL = 'http://localhost:8000';
    }
    
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');

      if (storedToken && storedUser && storedUser !== 'undefined' && storedUser !== 'null') {
        try {
          const parsedUser = JSON.parse(storedUser);
          if (parsedUser && typeof parsedUser === 'object') {
            setToken(storedToken);
            setUser(parsedUser);
            axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
          } else {
            // Clear invalid data
            localStorage.removeItem('token');
            localStorage.removeItem('user');
          }
        } catch (error) {
          console.error('Error parsing stored user data:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      } else if (storedUser === 'undefined' || storedUser === 'null') {
        // Clean up invalid data
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/v1/auth/login', {
        username: email,
        password: password
      });

      if (response.data.access_token) {
        const { access_token } = response.data;

        // Get user info from backend after successful login
        setToken(access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        try {
          const userResponse = await axios.get('/api/v1/auth/me');
          const userData = userResponse.data;
          
          setUser(userData);
          localStorage.setItem('token', access_token);
          localStorage.setItem('user', JSON.stringify(userData));

          toast.success('Login successful!');
          return true;
        } catch (userError) {
          console.error('Error fetching user info:', userError);
          // Fallback user data for demo
          const fallbackUser = {
            id: 1,
            username: email,
            email: email,
            first_name: 'Demo',
            last_name: 'User',
            role: 'admin',
            is_active: true
          };
          setUser(fallbackUser);
          localStorage.setItem('token', access_token);
          localStorage.setItem('user', JSON.stringify(fallbackUser));

          toast.success('Login successful!');
          return true;
        }
      }
      return false;
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
        const { access_token } = response.data;

        setToken(access_token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        
        try {
          const userResponse = await axios.get('/api/v1/auth/me');
          const newUser = userResponse.data;
          
          setUser(newUser);
          localStorage.setItem('token', access_token);
          localStorage.setItem('user', JSON.stringify(newUser));

          toast.success('Registration successful!');
          return true;
        } catch (userError) {
          // Fallback user data for demo
          const fallbackUser = {
            id: 1,
            username: userData.username,
            email: userData.email,
            first_name: userData.first_name,
            last_name: userData.last_name,
            role: 'employee',
            is_active: true
          };
          setUser(fallbackUser);
          localStorage.setItem('token', access_token);
          localStorage.setItem('user', JSON.stringify(fallbackUser));

          toast.success('Registration successful!');
          return true;
        }
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

// Export AuthContext as well for backward compatibility
export { AuthContext };
export default AuthProvider;