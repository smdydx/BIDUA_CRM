
import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import {
  Box,
  Tabs,
  Tab,
  Typography,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import Companies from './Companies';
import Leads from './Leads';
import Deals from './Deals';

const CRM = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const getTabValue = () => {
    const path = location.pathname;
    if (path.includes('/companies')) return 0;
    if (path.includes('/leads')) return 1;
    if (path.includes('/deals')) return 2;
    return 0;
  };

  const handleTabChange = (event, newValue) => {
    const paths = ['/crm/companies', '/crm/leads', '/crm/deals'];
    navigate(paths[newValue]);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Customer Relationship Management
      </Typography>
      
      <Tabs value={getTabValue()} onChange={handleTabChange} sx={{ mb: 3 }}>
        <Tab label="Companies" />
        <Tab label="Leads" />
        <Tab label="Deals" />
      </Tabs>

      <Routes>
        <Route path="/" element={<Companies />} />
        <Route path="/companies" element={<Companies />} />
        <Route path="/leads" element={<Leads />} />
        <Route path="/deals" element={<Deals />} />
      </Routes>
    </Box>
  );
};

export default CRM;
