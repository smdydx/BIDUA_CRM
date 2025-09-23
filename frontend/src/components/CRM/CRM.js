import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import Leads from './Leads';
import Companies from './Companies';
import Deals from './Deals';

const CRM = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Customer Relationship Management
        </Typography>
      </Box>

      <Routes>
        <Route path="/" element={<Navigate to="leads" replace />} />
        <Route path="leads" element={<Leads />} />
        <Route path="companies" element={<Companies />} />
        <Route path="deals" element={<Deals />} />
      </Routes>
    </Container>
  );
};

export default CRM;