import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Avatar,
  Chip,
  IconButton,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  useTheme,
  alpha
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  People,
  Business,
  AttachMoney,
  Assignment,
  Timeline,
  Notifications,
  MoreVert,
  CheckCircle,
  Schedule,
  Warning
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { useAuth } from '../../contexts/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const theme = useTheme();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState({
    kpis: {},
    recentActivities: [],
    upcomingTasks: [],
    teamPerformance: [],
    salesPipeline: [],
    monthlyRevenue: []
  });

  // Professional Color Palette
  const colors = {
    primary: '#1976d2',
    secondary: '#dc004e',
    success: '#2e7d32',
    warning: '#ed6c02',
    error: '#d32f2f',
    info: '#0288d1',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  };

  const pieColors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const fetchDashboardData = useCallback(async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch('/api/v1/analytics/dashboard/overview', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Set real data from API response
      setDashboardData({
        kpis: data.kpis || {
          totalRevenue: { value: '₹0L', change: 0, trend: 'up' },
          totalEmployees: { value: '0', change: 0, trend: 'up' },
          activeClients: { value: '0', change: 0, trend: 'up' },
          projectsCompleted: { value: '0', change: 0, trend: 'up' },
          customerSatisfaction: { value: '0%', change: 0, trend: 'up' },
          avgDealSize: { value: '₹0L', change: 0, trend: 'up' }
        },
        recentActivities: data.recentActivities || [],
        upcomingTasks: data.upcomingTasks || [],
        teamPerformance: data.teamPerformance || [],
        salesPipeline: data.salesPipeline || [],
        monthlyRevenue: data.monthlyRevenue || []
      });

      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const KPICard = ({ title, value, change, trend, icon: Icon, color }) => (
    <Card
      sx={{
        height: '100%',
        background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
        border: `1px solid ${alpha(color, 0.1)}`,
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: theme.shadows[8],
          transition: 'all 0.3s ease'
        }
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h4" fontWeight="bold" color={color}>
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            <Box display="flex" alignItems="center">
              {trend === 'up' ? (
                <TrendingUp sx={{ color: colors.success, fontSize: 16, mr: 0.5 }} />
              ) : (
                <TrendingDown sx={{ color: colors.error, fontSize: 16, mr: 0.5 }} />
              )}
              <Typography
                variant="caption"
                color={trend === 'up' ? colors.success : colors.error}
                fontWeight="medium"
              >
                {change > 0 ? '+' : ''}{change}%
              </Typography>
            </Box>
          </Box>
          <Avatar
            sx={{
              bgcolor: alpha(color, 0.1),
              color: color,
              width: 56,
              height: 56
            }}
          >
            <Icon />
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <Typography>Loading Enterprise Dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3, bgcolor: '#f5f7fa', minHeight: '100vh' }}>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" fontWeight="bold" color="text.primary" gutterBottom>
          Executive Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome back, {user?.first_name}! Here's what's happening at your company today.
        </Typography>
      </Box>

      {/* KPI Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Total Revenue"
            value={dashboardData.kpis.totalRevenue?.value}
            change={dashboardData.kpis.totalRevenue?.change}
            trend={dashboardData.kpis.totalRevenue?.trend}
            icon={AttachMoney}
            color={colors.success}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Total Employees"
            value={dashboardData.kpis.totalEmployees?.value}
            change={dashboardData.kpis.totalEmployees?.change}
            trend={dashboardData.kpis.totalEmployees?.trend}
            icon={People}
            color={colors.primary}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Active Clients"
            value={dashboardData.kpis.activeClients?.value}
            change={dashboardData.kpis.activeClients?.change}
            trend={dashboardData.kpis.activeClients?.trend}
            icon={Business}
            color={colors.info}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Projects Completed"
            value={dashboardData.kpis.projectsCompleted?.value}
            change={dashboardData.kpis.projectsCompleted?.change}
            trend={dashboardData.kpis.projectsCompleted?.trend}
            icon={Assignment}
            color={colors.warning}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Customer Satisfaction"
            value={dashboardData.kpis.customerSatisfaction?.value}
            change={dashboardData.kpis.customerSatisfaction?.change}
            trend={dashboardData.kpis.customerSatisfaction?.trend}
            icon={CheckCircle}
            color={colors.success}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4} lg={2}>
          <KPICard
            title="Avg Deal Size"
            value={dashboardData.kpis.avgDealSize?.value}
            change={dashboardData.kpis.avgDealSize?.change}
            trend={dashboardData.kpis.avgDealSize?.trend}
            icon={Timeline}
            color={colors.secondary}
          />
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} mb={4}>
        {/* Revenue Trend */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Revenue vs Target - Monthly Performance
              </Typography>
              <ResponsiveContainer width="100%" height={320}>
                <AreaChart data={dashboardData.monthlyRevenue}>
                  <defs>
                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={colors.primary} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={colors.primary} stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorTarget" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={colors.warning} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={colors.warning} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="revenue"
                    stroke={colors.primary}
                    fillOpacity={1}
                    fill="url(#colorRevenue)"
                    name="Revenue (₹L)"
                  />
                  <Area
                    type="monotone"
                    dataKey="target"
                    stroke={colors.warning}
                    fillOpacity={1}
                    fill="url(#colorTarget)"
                    name="Target (₹L)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Sales Pipeline */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Sales Pipeline Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={320}>
                <PieChart>
                  <Pie
                    data={dashboardData.salesPipeline}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {dashboardData.salesPipeline.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Team Performance & Activities */}
      <Grid container spacing={3} mb={4}>
        {/* Team Performance */}
        <Grid item xs={12} lg={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Team Performance vs Targets
              </Typography>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={dashboardData.teamPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="target" fill={colors.info} name="Target" />
                  <Bar dataKey="achieved" fill={colors.success} name="Achieved" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12} lg={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Recent Activities
              </Typography>
              <List sx={{ maxHeight: 300, overflow: 'auto' }}>
                {dashboardData.recentActivities.map((activity, index) => (
                  <React.Fragment key={activity.id}>
                    <ListItem>
                      <ListItemAvatar>
                        <Avatar sx={{
                          bgcolor: activity.status === 'success' ? colors.success :
                                  activity.status === 'warning' ? colors.warning :
                                  activity.status === 'info' ? colors.info : colors.primary
                        }}>
                          {activity.type === 'deal' && <AttachMoney />}
                          {activity.type === 'employee' && <People />}
                          {activity.type === 'project' && <Assignment />}
                          {activity.type === 'meeting' && <Schedule />}
                        </Avatar>
                      </ListItemAvatar>
                      <ListItemText
                        primary={activity.title}
                        secondary={
                          <Box>
                            <Typography variant="caption" color="text.secondary">
                              {activity.time}
                            </Typography>
                            {activity.amount && (
                              <Chip
                                size="small"
                                label={activity.amount}
                                color="success"
                                sx={{ ml: 1 }}
                              />
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < dashboardData.recentActivities.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Upcoming Tasks */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Upcoming Tasks & Deadlines
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Task</TableCell>
                      <TableCell>Due In</TableCell>
                      <TableCell>Priority</TableCell>
                      <TableCell>Assignee</TableCell>
                      <TableCell>Action</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {dashboardData.upcomingTasks.map((task) => (
                      <TableRow key={task.id} hover>
                        <TableCell>
                          <Typography fontWeight="medium">{task.title}</Typography>
                        </TableCell>
                        <TableCell>{task.due}</TableCell>
                        <TableCell>
                          <Chip
                            size="small"
                            label={task.priority.toUpperCase()}
                            color={task.priority === 'high' ? 'error' : 'default'}
                            variant={task.priority === 'high' ? 'filled' : 'outlined'}
                          />
                        </TableCell>
                        <TableCell>{task.assignee}</TableCell>
                        <TableCell>
                          <IconButton size="small">
                            <MoreVert />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;