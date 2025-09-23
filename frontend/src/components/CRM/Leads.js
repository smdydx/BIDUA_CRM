
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
import { Add, Edit, Delete } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';

const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [open, setOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentLead, setCurrentLead] = useState({
    name: '',
    email: '',
    phone: '',
    company_id: '',
    status: 'new',
    source: '',
    notes: ''
  });

  const statusOptions = ['new', 'contacted', 'qualified', 'unqualified', 'converted'];
  const sourceOptions = ['website', 'referral', 'social_media', 'email_campaign', 'trade_show', 'cold_call'];

  useEffect(() => {
    fetchLeads();
    fetchCompanies();
  }, []);

  const fetchLeads = async () => {
    try {
      const response = await axios.get('/api/v1/crm/leads/');
      setLeads(response.data);
    } catch (error) {
      toast.error('Error fetching leads');
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

  const handleOpen = (lead = null) => {
    if (lead) {
      setCurrentLead(lead);
      setEditMode(true);
    } else {
      setCurrentLead({
        name: '',
        email: '',
        phone: '',
        company_id: '',
        status: 'new',
        source: '',
        notes: ''
      });
      setEditMode(false);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentLead({
      name: '',
      email: '',
      phone: '',
      company_id: '',
      status: 'new',
      source: '',
      notes: ''
    });
  };

  const handleSubmit = async () => {
    try {
      if (editMode) {
        await axios.put(`/api/v1/crm/leads/${currentLead.id}`, currentLead);
        toast.success('Lead updated successfully');
      } else {
        await axios.post('/api/v1/crm/leads/', currentLead);
        toast.success('Lead created successfully');
      }
      fetchLeads();
      handleClose();
    } catch (error) {
      toast.error('Error saving lead');
    }
  };

  const handleDelete = async (leadId) => {
    if (window.confirm('Are you sure you want to delete this lead?')) {
      try {
        await axios.delete(`/api/v1/crm/leads/${leadId}`);
        toast.success('Lead deleted successfully');
        fetchLeads();
      } catch (error) {
        toast.error('Error deleting lead');
      }
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      new: 'primary',
      contacted: 'info',
      qualified: 'success',
      unqualified: 'error',
      converted: 'secondary'
    };
    return colors[status] || 'default';
  };

  const getCompanyName = (companyId) => {
    const company = companies.find(c => c.id === companyId);
    return company ? company.name : 'N/A';
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Lead
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Phone</TableCell>
              <TableCell>Company</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Source</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leads.map((lead) => (
              <TableRow key={lead.id}>
                <TableCell>{lead.name}</TableCell>
                <TableCell>{lead.email}</TableCell>
                <TableCell>{lead.phone}</TableCell>
                <TableCell>{getCompanyName(lead.company_id)}</TableCell>
                <TableCell>
                  <Chip 
                    label={lead.status} 
                    color={getStatusColor(lead.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{lead.source}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(lead)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(lead.id)} color="error">
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
          {editMode ? 'Edit Lead' : 'Add New Lead'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Lead Name"
            fullWidth
            required
            value={currentLead.name}
            onChange={(e) => setCurrentLead({ ...currentLead, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Email"
            type="email"
            fullWidth
            required
            value={currentLead.email}
            onChange={(e) => setCurrentLead({ ...currentLead, email: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={currentLead.phone}
            onChange={(e) => setCurrentLead({ ...currentLead, phone: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Company"
            select
            fullWidth
            value={currentLead.company_id}
            onChange={(e) => setCurrentLead({ ...currentLead, company_id: e.target.value })}
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
            label="Status"
            select
            fullWidth
            value={currentLead.status}
            onChange={(e) => setCurrentLead({ ...currentLead, status: e.target.value })}
          >
            {statusOptions.map((status) => (
              <MenuItem key={status} value={status}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Source"
            select
            fullWidth
            value={currentLead.source}
            onChange={(e) => setCurrentLead({ ...currentLead, source: e.target.value })}
          >
            {sourceOptions.map((source) => (
              <MenuItem key={source} value={source}>
                {source.replace('_', ' ').charAt(0).toUpperCase() + source.replace('_', ' ').slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Notes"
            fullWidth
            multiline
            rows={3}
            value={currentLead.notes}
            onChange={(e) => setCurrentLead({ ...currentLead, notes: e.target.value })}
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

export default Leads;
