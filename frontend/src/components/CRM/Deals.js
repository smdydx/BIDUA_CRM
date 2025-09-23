
import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Chip,
  MenuItem,
} from '@mui/material';
import { Add, Edit, Delete, AttachMoney } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';

const Deals = () => {
  const [deals, setDeals] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [open, setOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentDeal, setCurrentDeal] = useState({
    name: '',
    amount: '',
    company_id: '',
    stage: 'prospecting',
    probability: 0,
    expected_close_date: '',
    description: ''
  });

  const stageOptions = ['prospecting', 'qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost'];

  useEffect(() => {
    fetchDeals();
    fetchCompanies();
  }, []);

  const fetchDeals = async () => {
    try {
      const response = await axios.get('/api/v1/crm/deals/');
      setDeals(response.data);
    } catch (error) {
      toast.error('Error fetching deals');
    }
  };

  const fetchCompanies = async () => {
    try {
      const response = await axios.get('/api/v1/crm/companies/');
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies');
    }
  };

  const handleOpen = (deal = null) => {
    if (deal) {
      setCurrentDeal({
        ...deal,
        expected_close_date: deal.expected_close_date ? deal.expected_close_date.split('T')[0] : ''
      });
      setEditMode(true);
    } else {
      setCurrentDeal({
        name: '',
        amount: '',
        company_id: '',
        stage: 'prospecting',
        probability: 0,
        expected_close_date: '',
        description: ''
      });
      setEditMode(false);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentDeal({
      name: '',
      amount: '',
      company_id: '',
      stage: 'prospecting',
      probability: 0,
      expected_close_date: '',
      description: ''
    });
  };

  const handleSubmit = async () => {
    try {
      const dealData = {
        ...currentDeal,
        amount: parseFloat(currentDeal.amount) || 0,
        probability: parseInt(currentDeal.probability) || 0
      };

      if (editMode) {
        await axios.put(`/api/v1/crm/deals/${currentDeal.id}`, dealData);
        toast.success('Deal updated successfully');
      } else {
        await axios.post('/api/v1/crm/deals/', dealData);
        toast.success('Deal created successfully');
      }
      fetchDeals();
      handleClose();
    } catch (error) {
      toast.error('Error saving deal');
    }
  };

  const handleDelete = async (dealId) => {
    if (window.confirm('Are you sure you want to delete this deal?')) {
      try {
        await axios.delete(`/api/v1/crm/deals/${dealId}`);
        toast.success('Deal deleted successfully');
        fetchDeals();
      } catch (error) {
        toast.error('Error deleting deal');
      }
    }
  };

  const getStageColor = (stage) => {
    const colors = {
      prospecting: 'default',
      qualification: 'info',
      proposal: 'warning',
      negotiation: 'secondary',
      closed_won: 'success',
      closed_lost: 'error'
    };
    return colors[stage] || 'default';
  };

  const getCompanyName = (companyId) => {
    const company = companies.find(c => c.id === companyId);
    return company ? company.name : 'N/A';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount || 0);
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Deal
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Deal Name</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Company</TableCell>
              <TableCell>Stage</TableCell>
              <TableCell>Probability</TableCell>
              <TableCell>Expected Close</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deals.map((deal) => (
              <TableRow key={deal.id}>
                <TableCell>{deal.name}</TableCell>
                <TableCell>
                  <Box display="flex" alignItems="center">
                    <AttachMoney fontSize="small" />
                    {formatCurrency(deal.amount)}
                  </Box>
                </TableCell>
                <TableCell>{getCompanyName(deal.company_id)}</TableCell>
                <TableCell>
                  <Chip 
                    label={deal.stage.replace('_', ' ')} 
                    color={getStageColor(deal.stage)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{deal.probability}%</TableCell>
                <TableCell>
                  {deal.expected_close_date ? 
                    new Date(deal.expected_close_date).toLocaleDateString() : 
                    'N/A'
                  }
                </TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(deal)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(deal.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editMode ? 'Edit Deal' : 'Add New Deal'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Deal Name"
            fullWidth
            required
            value={currentDeal.name}
            onChange={(e) => setCurrentDeal({ ...currentDeal, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Amount"
            type="number"
            fullWidth
            required
            value={currentDeal.amount}
            onChange={(e) => setCurrentDeal({ ...currentDeal, amount: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Company"
            select
            fullWidth
            value={currentDeal.company_id}
            onChange={(e) => setCurrentDeal({ ...currentDeal, company_id: e.target.value })}
          >
            <MenuItem value="">Select Company</MenuItem>
            {companies.map((company) => (
              <MenuItem key={company.id} value={company.id}>
                {company.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Stage"
            select
            fullWidth
            value={currentDeal.stage}
            onChange={(e) => setCurrentDeal({ ...currentDeal, stage: e.target.value })}
          >
            {stageOptions.map((stage) => (
              <MenuItem key={stage} value={stage}>
                {stage.replace('_', ' ').charAt(0).toUpperCase() + stage.replace('_', ' ').slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Probability (%)"
            type="number"
            fullWidth
            inputProps={{ min: 0, max: 100 }}
            value={currentDeal.probability}
            onChange={(e) => setCurrentDeal({ ...currentDeal, probability: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Expected Close Date"
            type="date"
            fullWidth
            InputLabelProps={{ shrink: true }}
            value={currentDeal.expected_close_date}
            onChange={(e) => setCurrentDeal({ ...currentDeal, expected_close_date: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={currentDeal.description}
            onChange={(e) => setCurrentDeal({ ...currentDeal, description: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSubmit} variant="contained">
            {editMode ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Deals;
