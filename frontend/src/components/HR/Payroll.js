import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { Receipt } from '@mui/icons-material';

const Payroll = () => {
  return (
    <Box>
      <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <Receipt fontSize="large" color="primary" />
        Payroll Management
      </Typography>
      <Card>
        <CardContent>
          <Typography>Payroll module coming soon...</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Payroll;