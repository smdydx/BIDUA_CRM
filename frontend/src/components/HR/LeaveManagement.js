import React, { useState, useEffect } from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { CalendarToday } from '@mui/icons-material';

const LeaveManagement = () => {
  return (
    <Box>
      <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <CalendarToday fontSize="large" color="primary" />
        Leave Management
      </Typography>
      <Card>
        <CardContent>
          <Typography>Leave management module coming soon...</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default LeaveManagement;