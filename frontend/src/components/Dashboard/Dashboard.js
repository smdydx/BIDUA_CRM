
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/v1/analytics/dashboard');
      setAnalytics(response.data);
      setError('');
    } catch (err) {
      console.error('Dashboard data fetch error:', err);
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon, color = "primary" }) => (
    <div className={`stat-card stat-card-${color}`}>
      <div className="stat-card-icon">
        <i className={`fas ${icon}`}></i>
      </div>
      <div className="stat-card-content">
        <h3>{loading ? '...' : value?.toLocaleString() || 0}</h3>
        <p>{title}</p>
      </div>
    </div>
  );

  const RevenueCard = ({ stage, amount }) => (
    <div className="revenue-card">
      <div className="revenue-stage">{stage}</div>
      <div className="revenue-amount">₹{amount?.toLocaleString() || 0}</div>
    </div>
  );

  if (loading && !analytics.total_users) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner"></div>
        <p>Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Welcome back, {user?.first_name || user?.username || 'User'}!</h1>
          <p>Here's your business overview</p>
        </div>
        <button 
          className="refresh-btn"
          onClick={fetchDashboardData}
          disabled={loading}
        >
          <i className={`fas fa-sync-alt ${loading ? 'fa-spin' : ''}`}></i>
          Refresh
        </button>
      </div>

      {error && (
        <div className="error-message">
          <i className="fas fa-exclamation-triangle"></i>
          {error}
          <button onClick={fetchDashboardData}>Retry</button>
        </div>
      )}

      {/* Stats Grid */}
      <div className="stats-grid">
        <StatCard 
          title="Total Users" 
          value={analytics.total_users} 
          icon="fa-users" 
          color="primary"
        />
        <StatCard 
          title="Employees" 
          value={analytics.total_employees} 
          icon="fa-user-tie" 
          color="success"
        />
        <StatCard 
          title="Companies" 
          value={analytics.total_companies} 
          icon="fa-building" 
          color="info"
        />
        <StatCard 
          title="Leads" 
          value={analytics.total_leads} 
          icon="fa-user-plus" 
          color="warning"
        />
        <StatCard 
          title="Deals" 
          value={analytics.total_deals} 
          icon="fa-handshake" 
          color="success"
        />
        <StatCard 
          title="Projects" 
          value={analytics.total_projects} 
          icon="fa-project-diagram" 
          color="primary"
        />
        <StatCard 
          title="Tasks" 
          value={analytics.total_tasks} 
          icon="fa-tasks" 
          color="info"
        />
        <StatCard 
          title="Revenue" 
          value={analytics.revenue_by_stage?.reduce((sum, stage) => sum + (stage.total_value || 0), 0)} 
          icon="fa-dollar-sign" 
          color="success"
        />
      </div>

      {/* Revenue Breakdown */}
      {analytics.revenue_by_stage && analytics.revenue_by_stage.length > 0 && (
        <div className="revenue-section">
          <h2>Revenue by Deal Stage</h2>
          <div className="revenue-grid">
            {analytics.revenue_by_stage.map((stage, index) => (
              <RevenueCard 
                key={index}
                stage={stage.stage || 'Unknown'}
                amount={stage.total_value || 0}
              />
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <div className="action-card">
            <i className="fas fa-user-plus"></i>
            <h3>Add Lead</h3>
            <p>Create new lead</p>
          </div>
          <div className="action-card">
            <i className="fas fa-handshake"></i>
            <h3>New Deal</h3>
            <p>Start new deal</p>
          </div>
          <div className="action-card">
            <i className="fas fa-user-tie"></i>
            <h3>Add Employee</h3>
            <p>Register employee</p>
          </div>
          <div className="action-card">
            <i className="fas fa-building"></i>
            <h3>Add Company</h3>
            <p>Register company</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
