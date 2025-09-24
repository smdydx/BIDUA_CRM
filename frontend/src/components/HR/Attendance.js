import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { Assignment } from '@mui/icons-material';

const Attendance = () => {
  return (
    <Box>
      <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <Assignment fontSize="large" color="primary" />
        Attendance Management
      </Typography>
      <Card>
        <CardContent>
          <Typography>Attendance module coming soon...</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Attendance;