import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import { Assessment } from '@mui/icons-material';

const Activities = () => {
  return (
    <Box>
      <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <Assessment fontSize="large" color="primary" />
        Activities Management
      </Typography>
      <Card>
        <CardContent>
          <Typography>Activities module coming soon...</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Activities;