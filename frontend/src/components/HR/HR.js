import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container, Typography, Box } from '@mui/material';
import Employees from './Employees';
import Departments from './Departments';

const HR = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Human Resources Management
        </Typography>
      </Box>

      <Routes>
        <Route path="/" element={<Navigate to="employees" replace />} />
        <Route path="employees" element={<Employees />} />
        <Route path="departments" element={<Departments />} />
      </Routes>
    </Container>
  );
};

export default HR;