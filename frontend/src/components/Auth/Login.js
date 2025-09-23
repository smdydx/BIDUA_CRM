
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  InputAdornment,
  IconButton,
  Card,
  CardContent,
  Divider,
  Grid
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  Business,
  Person
} from '@mui/icons-material';
import { AuthContext } from '../../contexts/AuthContext';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  // Demo accounts data
  const demoAccounts = [
    {
      title: 'Administrator',
      email: 'admin@company.com',
      password: 'admin123',
      role: 'Full System Access',
      icon: <Business color="primary" />,
      color: '#1976d2'
    },
    {
      title: 'HR Manager',
      email: 'hr@company.com',
      password: 'hr123',
      role: 'HR Management',
      icon: <Person color="success" />,
      color: '#2e7d32'
    },
    {
      title: 'Sales Rep',
      email: 'sales@company.com',
      password: 'sales123',
      role: 'CRM & Sales',
      icon: <Business color="warning" />,
      color: '#ed6c02'
    },
    {
      title: 'Employee',
      email: 'employee@company.com',
      password: 'emp123',
      role: 'Basic Access',
      icon: <Person color="info" />,
      color: '#0288d1'
    }
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const success = await login(formData.email, formData.password);
      if (success) {
        navigate('/dashboard');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (account) => {
    setFormData({
      email: account.email,
      password: account.password
    });
  };

  return (
    <Container maxWidth="lg" sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', py: 4 }}>
      <Grid container spacing={4} sx={{ width: '100%' }}>
        {/* Left side - Login Form */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={8} 
            sx={{ 
              p: 4, 
              borderRadius: 3,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white'
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography variant="h3" component="h1" fontWeight="bold" sx={{ mb: 2 }}>
                BIDUA ERP
              </Typography>
              <Typography variant="h6" sx={{ opacity: 0.9 }}>
                Enterprise Resource Planning System
              </Typography>
            </Box>

            <Card sx={{ borderRadius: 2 }}>
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h5" sx={{ mb: 3, textAlign: 'center', color: 'text.primary' }}>
                  Sign In to Your Account
                </Typography>

                {error && (
                  <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                  </Alert>
                )}

                <Box component="form" onSubmit={handleSubmit}>
                  <TextField
                    fullWidth
                    name="email"
                    type="email"
                    label="Email Address"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    sx={{ mb: 3 }}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Email />
                        </InputAdornment>
                      ),
                    }}
                  />

                  <TextField
                    fullWidth
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    label="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    sx={{ mb: 4 }}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Lock />
                        </InputAdornment>
                      ),
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowPassword(!showPassword)}
                            edge="end"
                          >
                            {showPassword ? <VisibilityOff /> : <Visibility />}
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />

                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    size="large"
                    disabled={loading}
                    sx={{
                      py: 1.5,
                      background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                      }
                    }}
                  >
                    {loading ? 'Signing In...' : 'Sign In'}
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Paper>
        </Grid>

        {/* Right side - Demo Accounts */}
        <Grid item xs={12} md={6}>
          <Paper elevation={4} sx={{ p: 4, borderRadius: 3, height: '100%' }}>
            <Typography variant="h5" sx={{ mb: 3, fontWeight: 'bold', color: 'primary.main' }}>
              Demo Accounts
            </Typography>
            <Typography variant="body2" sx={{ mb: 3, color: 'text.secondary' }}>
              Click on any account to auto-fill login credentials
            </Typography>

            <Grid container spacing={2}>
              {demoAccounts.map((account, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Card
                    sx={{
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      border: '2px solid transparent',
                      '&:hover': {
                        borderColor: account.color,
                        transform: 'translateY(-2px)',
                        boxShadow: 4
                      }
                    }}
                    onClick={() => handleDemoLogin(account)}
                  >
                    <CardContent sx={{ textAlign: 'center', p: 3 }}>
                      <Box sx={{ mb: 2 }}>
                        {account.icon}
                      </Box>
                      <Typography variant="h6" sx={{ mb: 1, color: account.color }}>
                        {account.title}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1, fontFamily: 'monospace' }}>
                        {account.email}
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                        {account.role}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Divider sx={{ my: 3 }} />

            <Box sx={{ p: 2, bgcolor: 'grey.50', borderRadius: 2 }}>
              <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 'bold' }}>
                System Features:
              </Typography>
              <Grid container spacing={1}>
                {[
                  'Customer Relationship Management',
                  'Human Resource Management',
                  'Project Management',
                  'Financial Management',
                  'Inventory Management',
                  'Analytics & Reporting'
                ].map((feature, index) => (
                  <Grid item xs={12} sm={6} key={index}>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      • {feature}
                    </Typography>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Login;
