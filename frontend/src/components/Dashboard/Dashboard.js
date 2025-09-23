
import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  LinearProgress,
  Avatar,
  Chip,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Divider
} from '@mui/material';
import {
  TrendingUp,
  People,
  Business,
  Assignment,
  AttachMoney,
  Notifications,
  MoreVert,
  ArrowUpward,
  ArrowDownward
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import axios from 'axios';

const Dashboard = () => {
  const [analytics, setAnalytics] = useState({
    total_users: 0,
    total_employees: 0,
    total_companies: 0,
    total_leads: 0,
    total_deals: 0,
    total_projects: 0,
    total_tasks: 0,
    revenue_by_stage: []
  });
  const [anchorEl, setAnchorEl] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('/api/v1/analytics/dashboard');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const statsCards = [
    {
      title: 'Total Revenue',
      value: '₹12,54,000',
      change: '+12.5%',
      changeType: 'positive',
      icon: <AttachMoney />,
      color: '#4CAF50',
      bgColor: '#E8F5E8'
    },
    {
      title: 'Active Employees',
      value: analytics.total_employees,
      change: '+8.2%',
      changeType: 'positive',
      icon: <People />,
      color: '#2196F3',
      bgColor: '#E3F2FD'
    },
    {
      title: 'Companies',
      value: analytics.total_companies,
      change: '+15.3%',
      changeType: 'positive',
      icon: <Business />,
      color: '#FF9800',
      bgColor: '#FFF3E0'
    },
    {
      title: 'Active Projects',
      value: analytics.total_projects,
      change: '-2.1%',
      changeType: 'negative',
      icon: <Assignment />,
      color: '#9C27B0',
      bgColor: '#F3E5F5'
    }
  ];

  const salesData = [
    { month: 'Jan', revenue: 400000, leads: 240, deals: 24 },
    { month: 'Feb', revenue: 300000, leads: 139, deals: 22 },
    { month: 'Mar', revenue: 200000, leads: 980, deals: 29 },
    { month: 'Apr', revenue: 278000, leads: 390, deals: 20 },
    { month: 'May', revenue: 189000, leads: 480, deals: 21 },
    { month: 'Jun', revenue: 239000, leads: 380, deals: 25 }
  ];

  const projectStatusData = [
    { name: 'Completed', value: 45, color: '#4CAF50' },
    { name: 'In Progress', value: 30, color: '#2196F3' },
    { name: 'Planning', value: 15, color: '#FF9800' },
    { name: 'On Hold', value: 10, color: '#F44336' }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'lead',
      title: 'New lead from Acme Corp',
      time: '5 mins ago',
      avatar: 'A',
      color: '#4CAF50'
    },
    {
      id: 2,
      type: 'project',
      title: 'Project Alpha milestone completed',
      time: '1 hour ago',
      avatar: 'P',
      color: '#2196F3'
    },
    {
      id: 3,
      type: 'employee',
      title: 'New employee John Doe joined',
      time: '2 hours ago',
      avatar: 'J',
      color: '#FF9800'
    },
    {
      id: 4,
      type: 'deal',
      title: 'Deal closed with TechStart Ltd',
      time: '3 hours ago',
      avatar: 'T',
      color: '#9C27B0'
    }
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 3, bgcolor: '#f5f5f5', minHeight: '100vh' }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#2c3e50', mb: 1 }}>
          Dashboard Overview
        </Typography>
        <Typography variant="subtitle1" sx={{ color: '#7f8c8d' }}>
          Welcome back! Here's what's happening with your business today.
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {statsCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card 
              elevation={0}
              sx={{ 
                borderRadius: 3,
                border: '1px solid #e0e0e0',
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4
                }
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar
                    sx={{
                      bgcolor: card.bgColor,
                      color: card.color,
                      width: 48,
                      height: 48,
                      mr: 2
                    }}
                  >
                    {card.icon}
                  </Avatar>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle2" color="text.secondary">
                      {card.title}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', color: '#2c3e50' }}>
                      {card.value}
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {card.changeType === 'positive' ? (
                    <ArrowUpward sx={{ color: '#4CAF50', fontSize: 16, mr: 0.5 }} />
                  ) : (
                    <ArrowDownward sx={{ color: '#F44336', fontSize: 16, mr: 0.5 }} />
                  )}
                  <Typography
                    variant="body2"
                    sx={{
                      color: card.changeType === 'positive' ? '#4CAF50' : '#F44336',
                      fontWeight: 'medium'
                    }}
                  >
                    {card.change}
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary', ml: 1 }}>
                    from last month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Revenue Chart */}
        <Grid item xs={12} md={8}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                  Revenue Overview
                </Typography>
                <IconButton
                  onClick={(e) => setAnchorEl(e.currentTarget)}
                  size="small"
                >
                  <MoreVert />
                </IconButton>
                <Menu
                  anchorEl={anchorEl}
                  open={Boolean(anchorEl)}
                  onClose={() => setAnchorEl(null)}
                >
                  <MenuItem onClick={() => setAnchorEl(null)}>Export Data</MenuItem>
                  <MenuItem onClick={() => setAnchorEl(null)}>View Details</MenuItem>
                </Menu>
              </Box>
              
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={salesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip 
                    formatter={(value) => [`₹${value.toLocaleString()}`, 'Revenue']}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="revenue" 
                    stroke="#667eea" 
                    fill="url(#colorRevenue)" 
                  />
                  <defs>
                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#667eea" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#667eea" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Project Status */}
        <Grid item xs={12} md={4}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                Project Status
              </Typography>
              
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={projectStatusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {projectStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              
              <Box sx={{ mt: 2 }}>
                {projectStatusData.map((item, index) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Box
                      sx={{
                        width: 12,
                        height: 12,
                        bgcolor: item.color,
                        borderRadius: '50%',
                        mr: 1
                      }}
                    />
                    <Typography variant="body2" sx={{ flex: 1 }}>
                      {item.name}
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                      {item.value}%
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} md={6}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                Recent Activities
              </Typography>
              
              {recentActivities.map((activity, index) => (
                <Box key={activity.id}>
                  <Box sx={{ display: 'flex', alignItems: 'center', py: 2 }}>
                    <Avatar
                      sx={{
                        bgcolor: activity.color,
                        width: 32,
                        height: 32,
                        fontSize: '0.875rem',
                        mr: 2
                      }}
                    >
                      {activity.avatar}
                    </Avatar>
                    <Box sx={{ flex: 1 }}>
                      <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                        {activity.title}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {activity.time}
                      </Typography>
                    </Box>
                  </Box>
                  {index < recentActivities.length - 1 && <Divider />}
                </Box>
              ))}
              
              <Button
                fullWidth
                variant="outlined"
                sx={{ mt: 2, borderRadius: 2 }}
              >
                View All Activities
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card elevation={0} sx={{ borderRadius: 3, border: '1px solid #e0e0e0' }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 3 }}>
                Quick Actions
              </Typography>
              
              <Grid container spacing={2}>
                {[
                  { label: 'Add Employee', color: '#2196F3' },
                  { label: 'Create Project', color: '#4CAF50' },
                  { label: 'New Lead', color: '#FF9800' },
                  { label: 'Generate Report', color: '#9C27B0' }
                ].map((action, index) => (
                  <Grid item xs={6} key={index}>
                    <Button
                      fullWidth
                      variant="contained"
                      sx={{
                        bgcolor: action.color,
                        color: 'white',
                        borderRadius: 2,
                        py: 1.5,
                        '&:hover': {
                          bgcolor: action.color,
                          opacity: 0.8
                        }
                      }}
                    >
                      {action.label}
                    </Button>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
