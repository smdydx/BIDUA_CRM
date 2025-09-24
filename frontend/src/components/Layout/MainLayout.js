import React, { useState } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  useTheme,
  Collapse
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  Analytics as AnalyticsIcon,
  AdminPanelSettings as AdminIcon,
  Notifications as NotificationsIcon,
  AccountCircle as AccountCircleIcon,
  Logout as LogoutIcon,
  ExpandLess,
  ExpandMore,
  ContactPhone,
  Handshake,
  TrendingUp,
  WorkOutline,
  Group,
  AccountTree,
  CalendarToday,
  Receipt,
  Assessment,
  Business
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const drawerWidth = 280;

const MainLayout = ({ children }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [crmOpen, setCrmOpen] = useState(true);
  const [hrOpen, setHrOpen] = useState(true);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleProfileMenuClose();
  };

  const menuItems = [
    {
      text: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/dashboard',
      color: '#1976d2'
    },
    {
      text: 'CRM',
      icon: <BusinessIcon />,
      color: '#2e7d32',
      children: [
        { text: 'Companies', icon: <Business />, path: '/crm/companies' },
        { text: 'Contacts', icon: <ContactPhone />, path: '/crm/contacts' },
        { text: 'Leads', icon: <TrendingUp />, path: '/crm/leads' },
        { text: 'Deals', icon: <Handshake />, path: '/crm/deals' },
        { text: 'Activities', icon: <Assessment />, path: '/crm/activities' }
      ]
    },
    {
      text: 'HRMS',
      icon: <PeopleIcon />,
      color: '#ed6c02',
      children: [
        { text: 'Employees', icon: <Group />, path: '/hr/employees' },
        { text: 'Departments', icon: <AccountTree />, path: '/hr/departments' },
        { text: 'Designations', icon: <WorkOutline />, path: '/hr/designations' },
        { text: 'Leave Management', icon: <CalendarToday />, path: '/hr/leave' },
        { text: 'Attendance', icon: <AssignmentIcon />, path: '/hr/attendance' },
        { text: 'Payroll', icon: <Receipt />, path: '/hr/payroll' }
      ]
    },
    {
      text: 'Projects',
      icon: <AssignmentIcon />,
      path: '/projects',
      color: '#9c27b0'
    },
    {
      text: 'Analytics',
      icon: <AnalyticsIcon />,
      path: '/analytics',
      color: '#f57c00'
    }
  ];

  if (user?.role === 'admin') {
    menuItems.push({
      text: 'Administration',
      icon: <AdminIcon />,
      path: '/admin',
      color: '#d32f2f'
    });
  }

  const drawer = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo and Company Name */}
      <Box sx={{ p: 2, textAlign: 'center', bgcolor: 'primary.main', color: 'white' }}>
        <Typography variant="h6" fontWeight="bold">
          Enterprise CRM+HRMS
        </Typography>
        <Typography variant="caption" sx={{ opacity: 0.8 }}>
          Professional Edition
        </Typography>
      </Box>

      <Divider />

      {/* Navigation Menu */}
      <List sx={{ flexGrow: 1, py: 1 }}>
        {menuItems.map((item) => (
          <React.Fragment key={item.text}>
            {item.children ? (
              // Parent item with children
              <>
                <ListItem disablePadding>
                  <ListItemButton
                    onClick={() => {
                      if (item.text === 'CRM') setCrmOpen(!crmOpen);
                      if (item.text === 'HRMS') setHrOpen(!hrOpen);
                    }}
                    sx={{
                      py: 1.5,
                      px: 2,
                      '&:hover': {
                        bgcolor: 'rgba(0,0,0,0.04)'
                      }
                    }}
                  >
                    <ListItemIcon sx={{ color: item.color, minWidth: 40 }}>
                      {item.icon}
                    </ListItemIcon>
                    <ListItemText
                      primary={item.text}
                      primaryTypographyProps={{ fontWeight: 500 }}
                    />
                    {item.text === 'CRM' ? (crmOpen ? <ExpandLess /> : <ExpandMore />) :
                     item.text === 'HRMS' ? (hrOpen ? <ExpandLess /> : <ExpandMore />) :
                     <ExpandMore />}
                  </ListItemButton>
                </ListItem>
                <Collapse in={item.text === 'CRM' ? crmOpen : hrOpen} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {item.children.map((child) => (
                      <ListItem key={child.text} disablePadding>
                        <ListItemButton
                          onClick={() => navigate(child.path)}
                          selected={location.pathname === child.path}
                          sx={{
                            pl: 4,
                            py: 1,
                            '&.Mui-selected': {
                              bgcolor: 'primary.light',
                              color: 'primary.contrastText',
                              '&:hover': {
                                bgcolor: 'primary.main',
                              }
                            }
                          }}
                        >
                          <ListItemIcon sx={{ minWidth: 36, color: 'inherit' }}>
                            {child.icon}
                          </ListItemIcon>
                          <ListItemText
                            primary={child.text}
                            primaryTypographyProps={{ fontSize: '0.875rem' }}
                          />
                        </ListItemButton>
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
              </>
            ) : (
              // Regular menu item
              <ListItem disablePadding>
                <ListItemButton
                  onClick={() => navigate(item.path)}
                  selected={location.pathname === item.path}
                  sx={{
                    py: 1.5,
                    px: 2,
                    '&.Mui-selected': {
                      bgcolor: 'primary.light',
                      color: 'primary.contrastText',
                      '&:hover': {
                        bgcolor: 'primary.main',
                      }
                    },
                    '&:hover': {
                      bgcolor: 'rgba(0,0,0,0.04)'
                    }
                  }}
                >
                  <ListItemIcon sx={{ color: item.color, minWidth: 40 }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.text}
                    primaryTypographyProps={{ fontWeight: 500 }}
                  />
                </ListItemButton>
              </ListItem>
            )}
          </React.Fragment>
        ))}
      </List>

      <Divider />

      {/* User Profile Section */}
      <Box sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>
            {user?.first_name?.[0] || user?.username?.[0] || 'U'}
          </Avatar>
          <Box sx={{ flexGrow: 1, minWidth: 0 }}>
            <Typography variant="subtitle2" noWrap>
              {user?.first_name} {user?.last_name}
            </Typography>
            <Typography variant="caption" color="text.secondary" noWrap>
              {user?.role?.toUpperCase()}
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { lg: `calc(100% - ${drawerWidth}px)` },
          ml: { lg: `${drawerWidth}px` },
          bgcolor: 'white',
          color: 'text.primary',
          boxShadow: '0 1px 3px rgba(0,0,0,0.12)',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { lg: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            {location.pathname === '/dashboard' && 'Executive Dashboard'}
            {location.pathname.startsWith('/crm') && 'Customer Relationship Management'}
            {location.pathname.startsWith('/hr') && 'Human Resource Management'}
            {location.pathname === '/projects' && 'Project Management'}
            {location.pathname === '/analytics' && 'Business Analytics'}
            {location.pathname === '/admin' && 'Administration'}
          </Typography>

          {/* Notifications */}
          <IconButton color="inherit" sx={{ mr: 1 }}>
            <Badge badgeContent={4} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          {/* Profile Menu */}
          <IconButton
            size="large"
            edge="end"
            aria-label="account of current user"
            aria-controls="primary-search-account-menu"
            aria-haspopup="true"
            onClick={handleProfileMenuOpen}
            color="inherit"
          >
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
              {user?.first_name?.[0] || user?.username?.[0] || 'U'}
            </Avatar>
          </IconButton>
        </Toolbar>
      </AppBar>

      {/* Profile Menu */}
      <Menu
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        keepMounted
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
        open={Boolean(anchorEl)}
        onClose={handleProfileMenuClose}
      >
        <MenuItem onClick={() => { navigate('/profile'); handleProfileMenuClose(); }}>
          <ListItemIcon>
            <AccountCircleIcon fontSize="small" />
          </ListItemIcon>
          Profile
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <LogoutIcon fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>

      {/* Drawer */}
      <Box
        component="nav"
        sx={{ width: { lg: drawerWidth }, flexShrink: { lg: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', lg: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', lg: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { lg: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          bgcolor: '#f5f5f5'
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout;