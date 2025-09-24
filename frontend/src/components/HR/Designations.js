import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { WorkOutline } from '@mui/icons-material';

const Designations = () => {
  return (
    <Box>
      <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <WorkOutline fontSize="large" color="primary" />
        Designations Management
      </Typography>
      <Card>
        <CardContent>
          <Typography>Designations module coming soon...</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Designations;