
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import {
  Box,
  Tabs,
  Tab,
  Typography,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import Employees from './Employees';
import Departments from './Departments';

const HR = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const getTabValue = () => {
    const path = location.pathname;
    if (path.includes('/employees')) return 0;
    if (path.includes('/departments')) return 1;
    return 0;
  };

  const handleTabChange = (event, newValue) => {
    const paths = ['/hr/employees', '/hr/departments'];
    navigate(paths[newValue]);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Human Resource Management
      </Typography>
      
      <Tabs value={getTabValue()} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Employees" />
        <Tab label="Departments" />
      </Tabs>

      <Routes>
        <Route path="/" element={<Employees />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/departments" element={<Departments />} />
      </Routes>
    </Box>
  );
};

export default HR;
