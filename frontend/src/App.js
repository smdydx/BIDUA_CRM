import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import AuthProvider from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import MainLayout from './components/Layout/MainLayout';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import CRM from './components/CRM/CRM';
import HR from './components/HR/HR';
import Users from './components/Users/Users';
import Projects from './components/Projects/Projects';
import Analytics from './components/Analytics/Analytics';

// CRM Components
import Companies from './components/CRM/Companies';
import Contacts from './components/CRM/Contacts';
import Leads from './components/CRM/Leads';
import Deals from './components/CRM/Deals';
import Activities from './components/CRM/Activities';

// HR Components
import Employees from './components/HR/Employees';
import Departments from './components/HR/Departments';
import Designations from './components/HR/Designations';
import LeaveManagement from './components/HR/LeaveManagement';
import Attendance from './components/HR/Attendance';
import Payroll from './components/HR/Payroll';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AuthProvider>
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <MainLayout><Dashboard /></MainLayout>
                  </ProtectedRoute>
                }
              />
              
              {/* CRM Routes */}
              <Route
                path="/crm"
                element={
                  <ProtectedRoute>
                    <MainLayout><CRM /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crm/companies"
                element={
                  <ProtectedRoute>
                    <MainLayout><Companies /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crm/contacts"
                element={
                  <ProtectedRoute>
                    <MainLayout><Contacts /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crm/leads"
                element={
                  <ProtectedRoute>
                    <MainLayout><Leads /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crm/deals"
                element={
                  <ProtectedRoute>
                    <MainLayout><Deals /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/crm/activities"
                element={
                  <ProtectedRoute>
                    <MainLayout><Activities /></MainLayout>
                  </ProtectedRoute>
                }
              />
              
              {/* HR Routes */}
              <Route
                path="/hr"
                element={
                  <ProtectedRoute>
                    <MainLayout><HR /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/employees"
                element={
                  <ProtectedRoute>
                    <MainLayout><Employees /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/departments"
                element={
                  <ProtectedRoute>
                    <MainLayout><Departments /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/designations"
                element={
                  <ProtectedRoute>
                    <MainLayout><Designations /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/leave"
                element={
                  <ProtectedRoute>
                    <MainLayout><LeaveManagement /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/attendance"
                element={
                  <ProtectedRoute>
                    <MainLayout><Attendance /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/hr/payroll"
                element={
                  <ProtectedRoute>
                    <MainLayout><Payroll /></MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/users"
                element={
                  <ProtectedRoute requiredRole="admin">
                    <MainLayout><Users /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/projects"
                element={
                  <ProtectedRoute>
                    <MainLayout><Projects /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/analytics"
                element={
                  <ProtectedRoute>
                    <MainLayout><Analytics /></MainLayout>
                  </ProtectedRoute>
                }
              />
              <Route path="/" element={<Navigate to="/login" replace />} />
            </Routes>
            <ToastContainer
              position="top-right"
              autoClose={3000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
            />
          </div>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;