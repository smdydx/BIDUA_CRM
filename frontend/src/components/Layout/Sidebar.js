
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Avatar,
  Divider,
  Collapse,
  Badge,
  Chip,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Dashboard,
  People,
  Business,
  Assignment,
  Analytics,
  Person,
  ExpandLess,
  ExpandMore,
  Groups,
  AccountBalance,
  Inventory,
  Settings,
  Notifications,
  Support
} from '@mui/icons-material';

const Sidebar = ({ open, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [expandedMenus, setExpandedMenus] = useState({});
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const toggleMenu = (menuId) => {
    setExpandedMenus(prev => ({
      ...prev,
      [menuId]: !prev[menuId]
    }));
  };

  const menuItems = [
    {
      id: 'dashboard',
      text: 'Dashboard',
      icon: <Dashboard />,
      path: '/dashboard',
      color: '#667eea'
    },
    {
      id: 'crm',
      text: 'CRM',
      icon: <Business />,
      color: '#4CAF50',
      children: [
        { text: 'Leads', path: '/crm/leads', badge: '12' },
        { text: 'Companies', path: '/crm/companies' },
        { text: 'Deals', path: '/crm/deals', badge: '5' },
        { text: 'Activities', path: '/crm/activities' }
      ]
    },
    {
      id: 'hr',
      text: 'Human Resources',
      icon: <People />,
      color: '#2196F3',
      children: [
        { text: 'Employees', path: '/hr/employees' },
        { text: 'Departments', path: '/hr/departments' },
        { text: 'Attendance', path: '/hr/attendance' },
        { text: 'Payroll', path: '/hr/payroll' },
        { text: 'Leave Management', path: '/hr/leave' }
      ]
    },
    {
      id: 'projects',
      text: 'Project Management',
      icon: <Assignment />,
      color: '#FF9800',
      children: [
        { text: 'Projects', path: '/projects' },
        { text: 'Tasks', path: '/projects/tasks' },
        { text: 'Time Tracking', path: '/projects/time' },
        { text: 'Resources', path: '/projects/resources' }
      ]
    },
    {
      id: 'finance',
      text: 'Finance',
      icon: <AccountBalance />,
      color: '#9C27B0',
      children: [
        { text: 'Invoices', path: '/finance/invoices' },
        { text: 'Expenses', path: '/finance/expenses' },
        { text: 'Budget', path: '/finance/budget' },
        { text: 'Reports', path: '/finance/reports' }
      ]
    },
    {
      id: 'inventory',
      text: 'Inventory',
      icon: <Inventory />,
      color: '#795548',
      children: [
        { text: 'Products', path: '/inventory/products' },
        { text: 'Stock', path: '/inventory/stock' },
        { text: 'Suppliers', path: '/inventory/suppliers' },
        { text: 'Orders', path: '/inventory/orders' }
      ]
    },
    {
      id: 'analytics',
      text: 'Analytics',
      icon: <Analytics />,
      path: '/analytics',
      color: '#FF5722'
    },
    {
      id: 'users',
      text: 'User Management',
      icon: <Person />,
      path: '/users',
      color: '#607D8B'
    }
  ];

  const handleNavigation = (path) => {
    navigate(path);
    if (onClose) onClose();
  };

  const isActive = (path) => location.pathname === path;

  const drawerWidth = 280;

  return (
    <Drawer
      anchor="left"
      open={open}
      onClose={onClose}
      variant={isMobile ? "temporary" : "persistent"}
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          borderRight: 'none'
        },
      }}
    >
      {/* Header */}
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 1 }}>
          BIDUA ERP
        </Typography>
        <Typography variant="caption" sx={{ opacity: 0.8 }}>
          Enterprise Resource Planning
        </Typography>
      </Box>

      {/* User Profile */}
      <Box sx={{ px: 3, pb: 2 }}>
        <Box
          sx={{
            bgcolor: 'rgba(255,255,255,0.1)',
            borderRadius: 2,
            p: 2,
            display: 'flex',
            alignItems: 'center'
          }}
        >
          <Avatar
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              mr: 2,
              width: 40,
              height: 40
            }}
          >
            A
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
              Administrator
            </Typography>
            <Typography variant="caption" sx={{ opacity: 0.8 }}>
              admin@company.com
            </Typography>
          </Box>
          <Badge badgeContent={3} color="error">
            <Notifications fontSize="small" />
          </Badge>
        </Box>
      </Box>

      <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)' }} />

      {/* Navigation Menu */}
      <List sx={{ px: 2, py: 1, flex: 1 }}>
        {menuItems.map((item) => (
          <Box key={item.id}>
            <ListItem disablePadding>
              <ListItemButton
                onClick={() => {
                  if (item.children) {
                    toggleMenu(item.id);
                  } else {
                    handleNavigation(item.path);
                  }
                }}
                sx={{
                  borderRadius: 2,
                  mb: 0.5,
                  bgcolor: isActive(item.path) ? 'rgba(255,255,255,0.15)' : 'transparent',
                  '&:hover': {
                    bgcolor: 'rgba(255,255,255,0.1)',
                  },
                }}
              >
                <ListItemIcon
                  sx={{
                    color: item.color,
                    minWidth: 40,
                    '& svg': {
                      filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
                    }
                  }}
                >
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.text}
                  sx={{
                    '& .MuiTypography-root': {
                      fontWeight: isActive(item.path) ? 'bold' : 'medium',
                      fontSize: '0.9rem'
                    }
                  }}
                />
                {item.children && (
                  expandedMenus[item.id] ? <ExpandLess /> : <ExpandMore />
                )}
              </ListItemButton>
            </ListItem>

            {/* Submenu */}
            {item.children && (
              <Collapse in={expandedMenus[item.id]} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                  {item.children.map((child) => (
                    <ListItem key={child.path} disablePadding>
                      <ListItemButton
                        onClick={() => handleNavigation(child.path)}
                        sx={{
                          pl: 4,
                          borderRadius: 2,
                          mb: 0.5,
                          bgcolor: isActive(child.path) ? 'rgba(255,255,255,0.15)' : 'transparent',
                          '&:hover': {
                            bgcolor: 'rgba(255,255,255,0.1)',
                          },
                        }}
                      >
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <Typography
                                variant="body2"
                                sx={{
                                  fontWeight: isActive(child.path) ? 'bold' : 'normal',
                                  opacity: 0.9
                                }}
                              >
                                {child.text}
                              </Typography>
                              {child.badge && (
                                <Chip
                                  label={child.badge}
                                  size="small"
                                  sx={{
                                    bgcolor: 'rgba(255,255,255,0.2)',
                                    color: 'white',
                                    fontSize: '0.7rem',
                                    height: 20
                                  }}
                                />
                              )}
                            </Box>
                          }
                        />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Collapse>
            )}
          </Box>
        ))}
      </List>

      {/* Footer */}
      <Box sx={{ p: 2, mt: 'auto' }}>
        <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', mb: 2 }} />
        <Box sx={{ display: 'flex', justifyContent: 'space-around' }}>
          <Avatar
            sx={{
              bgcolor: 'rgba(255,255,255,0.1)',
              cursor: 'pointer',
              '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
            }}
          >
            <Settings fontSize="small" />
          </Avatar>
          <Avatar
            sx={{
              bgcolor: 'rgba(255,255,255,0.1)',
              cursor: 'pointer',
              '&:hover': { bgcolor: 'rgba(255,255,255,0.2)' }
            }}
          >
            <Support fontSize="small" />
          </Avatar>
        </Box>
        <Typography variant="caption" sx={{ display: 'block', textAlign: 'center', mt: 1, opacity: 0.6 }}>
          Version 1.0.0
        </Typography>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
