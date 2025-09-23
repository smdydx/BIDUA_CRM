
import React, { useState } from 'react';
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
  Grid,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  Email,
  Lock,
  Business,
  Person
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));

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
    <Container 
      maxWidth="lg" 
      sx={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        py: { xs: 2, md: 4 },
        px: { xs: 1, sm: 2, md: 3 }
      }}
    >
      <Grid container spacing={{ xs: 2, md: 4 }} sx={{ width: '100%' }}>
        {/* Login Form - Mobile First */}
        <Grid item xs={12} md={6} order={{ xs: 1, md: 1 }}>
          <Paper 
            elevation={8} 
            sx={{ 
              p: { xs: 2, sm: 3, md: 4 }, 
              borderRadius: 3,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              height: { md: 'auto' },
              minHeight: { xs: 'auto', md: '500px' }
            }}
          >
            <Box sx={{ textAlign: 'center', mb: { xs: 2, md: 4 } }}>
              <Typography 
                variant={isMobile ? "h4" : "h3"} 
                component="h1" 
                fontWeight="bold" 
                sx={{ mb: { xs: 1, md: 2 } }}
              >
                BIDUA ERP
              </Typography>
              <Typography 
                variant={isMobile ? "body1" : "h6"} 
                sx={{ opacity: 0.9 }}
              >
                Enterprise Resource Planning System
              </Typography>
            </Box>

            <Card sx={{ borderRadius: 2 }}>
              <CardContent sx={{ p: { xs: 2, sm: 3, md: 4 } }}>
                <Typography 
                  variant={isMobile ? "h6" : "h5"} 
                  sx={{ mb: 3, textAlign: 'center', color: 'text.primary' }}
                >
                  Sign In to Your Account
                </Typography>

                {error && (
                  <Alert severity="error" sx={{ mb: 3, fontSize: { xs: '0.8rem', md: '1rem' } }}>
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
                    size={isMobile ? "small" : "medium"}
                    sx={{ mb: { xs: 2, md: 3 } }}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Email fontSize={isMobile ? "small" : "medium"} />
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
                    size={isMobile ? "small" : "medium"}
                    sx={{ mb: { xs: 3, md: 4 } }}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Lock fontSize={isMobile ? "small" : "medium"} />
                        </InputAdornment>
                      ),
                      endAdornment: (
                        <InputAdornment position="end">
                          <IconButton
                            onClick={() => setShowPassword(!showPassword)}
                            edge="end"
                            size={isMobile ? "small" : "medium"}
                          >
                            {showPassword ? 
                              <VisibilityOff fontSize={isMobile ? "small" : "medium"} /> : 
                              <Visibility fontSize={isMobile ? "small" : "medium"} />
                            }
                          </IconButton>
                        </InputAdornment>
                      ),
                    }}
                  />

                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    size={isMobile ? "medium" : "large"}
                    disabled={loading}
                    sx={{
                      py: { xs: 1.2, md: 1.5 },
                      fontSize: { xs: '0.9rem', md: '1rem' },
                      background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                      '&:hover': {
                        background: 'linear-gradient(45deg, #5a6fd8 30%, #6a4190 90%)',
                      },
                      '&:disabled': {
                        background: 'rgba(102, 126, 234, 0.5)',
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

        {/* Demo Accounts - Responsive */}
        <Grid item xs={12} md={6} order={{ xs: 2, md: 2 }}>
          <Paper 
            elevation={4} 
            sx={{ 
              p: { xs: 2, sm: 3, md: 4 }, 
              borderRadius: 3, 
              height: '100%',
              minHeight: { xs: 'auto', md: '500px' }
            }}
          >
            <Typography 
              variant={isMobile ? "h6" : "h5"} 
              sx={{ mb: { xs: 2, md: 3 }, fontWeight: 'bold', color: 'primary.main' }}
            >
              Demo Accounts
            </Typography>
            <Typography 
              variant={isMobile ? "caption" : "body2"} 
              sx={{ mb: { xs: 2, md: 3 }, color: 'text.secondary' }}
            >
              Click on any account to auto-fill login credentials
            </Typography>

            <Grid container spacing={{ xs: 1.5, sm: 2 }}>
              {demoAccounts.map((account, index) => (
                <Grid item xs={6} sm={6} md={6} key={index}>
                  <Card
                    sx={{
                      cursor: 'pointer',
                      transition: 'all 0.3s ease',
                      border: '2px solid transparent',
                      height: '100%',
                      '&:hover': {
                        borderColor: account.color,
                        transform: 'translateY(-2px)',
                        boxShadow: 4
                      }
                    }}
                    onClick={() => handleDemoLogin(account)}
                  >
                    <CardContent sx={{ 
                      textAlign: 'center', 
                      p: { xs: 1.5, sm: 2, md: 3 },
                      '&:last-child': { pb: { xs: 1.5, sm: 2, md: 3 } }
                    }}>
                      <Box sx={{ mb: { xs: 1, md: 2 } }}>
                        {React.cloneElement(account.icon, {
                          fontSize: isMobile ? 'medium' : 'large'
                        })}
                      </Box>
                      <Typography 
                        variant={isMobile ? "subtitle2" : "h6"} 
                        sx={{ 
                          mb: { xs: 0.5, md: 1 }, 
                          color: account.color,
                          fontSize: { xs: '0.9rem', sm: '1rem', md: '1.25rem' }
                        }}
                      >
                        {account.title}
                      </Typography>
                      <Typography 
                        variant={isMobile ? "caption" : "body2"} 
                        sx={{ 
                          mb: { xs: 0.5, md: 1 }, 
                          fontFamily: 'monospace',
                          fontSize: { xs: '0.7rem', sm: '0.8rem', md: '0.875rem' },
                          wordBreak: 'break-all'
                        }}
                      >
                        {account.email}
                      </Typography>
                      <Typography 
                        variant="caption" 
                        sx={{ 
                          color: 'text.secondary',
                          fontSize: { xs: '0.65rem', md: '0.75rem' }
                        }}
                      >
                        {account.role}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            {!isMobile && (
              <>
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
                        <Typography 
                          variant="body2" 
                          sx={{ 
                            color: 'text.secondary',
                            fontSize: { xs: '0.8rem', md: '0.875rem' }
                          }}
                        >
                          • {feature}
                        </Typography>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              </>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Login;
