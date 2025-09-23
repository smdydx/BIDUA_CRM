import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Avatar,
  TablePagination,
  InputAdornment,
  Alert,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  TrendingUp as LeadIcon,
  AttachMoney as MoneyIcon,
  CalendarToday as CalendarIcon,
  Person as PersonIcon,
  Business as BusinessIcon
} from '@mui/icons-material';
import axios from 'axios';
import { useAuth } from '../../contexts/AuthContext';
import { toast } from 'react-toastify';

const Leads = () => {
  const { token } = useAuth();
  const [leads, setLeads] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [contacts, setContacts] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingLead, setEditingLead] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [formData, setFormData] = useState({
    title: '',
    company_id: '',
    contact_id: '',
    source: '',
    status: 'new',
    estimated_value: '',
    probability: 0,
    expected_close_date: '',
    assigned_to_id: '',
    description: '',
    notes: ''
  });

  const leadStatuses = [
    { value: 'new', label: 'New', color: 'info' },
    { value: 'contacted', label: 'Contacted', color: 'warning' },
    { value: 'qualified', label: 'Qualified', color: 'primary' },
    { value: 'proposal', label: 'Proposal', color: 'secondary' },
    { value: 'negotiation', label: 'Negotiation', color: 'warning' },
    { value: 'closed_won', label: 'Closed Won', color: 'success' },
    { value: 'closed_lost', label: 'Closed Lost', color: 'error' }
  ];

  const leadSources = [
    'Website', 'Email Campaign', 'Cold Call', 'Referral', 'Social Media',
    'Trade Show', 'Advertisement', 'Partner', 'Direct Mail', 'Other'
  ];

  useEffect(() => {
    fetchLeads();
    fetchCompanies();
    fetchContacts();
    fetchUsers();
  }, [searchTerm, statusFilter]);

  const fetchLeads = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (statusFilter) params.append('status', statusFilter);
      
      const response = await axios.get(`/api/v1/crm/leads/?${params}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setLeads(response.data);
    } catch (error) {
      console.error('Error fetching leads:', error);
      toast.error('Failed to fetch leads');
    } finally {
      setLoading(false);
    }
  };

  const fetchCompanies = async () => {
    try {
      const response = await axios.get('/api/v1/crm/companies/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const fetchContacts = async () => {
    try {
      const response = await axios.get('/api/v1/crm/contacts/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setContacts(response.data);
    } catch (error) {
      console.error('Error fetching contacts:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/v1/users/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        estimated_value: formData.estimated_value ? parseFloat(formData.estimated_value) : null,
        probability: parseInt(formData.probability) || 0
      };

      if (editingLead) {
        await axios.put(`/api/v1/crm/leads/${editingLead.id}`, submitData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lead updated successfully');
      } else {
        await axios.post('/api/v1/crm/leads/', submitData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lead created successfully');
      }
      setOpenDialog(false);
      resetForm();
      fetchLeads();
    } catch (error) {
      console.error('Error saving lead:', error);
      toast.error(error.response?.data?.detail || 'Failed to save lead');
    }
  };

  const handleEdit = (lead) => {
    setEditingLead(lead);
    setFormData({
      title: lead.title || '',
      company_id: lead.company_id || '',
      contact_id: lead.contact_id || '',
      source: lead.source || '',
      status: lead.status || 'new',
      estimated_value: lead.estimated_value || '',
      probability: lead.probability || 0,
      expected_close_date: lead.expected_close_date || '',
      assigned_to_id: lead.assigned_to_id || '',
      description: lead.description || '',
      notes: lead.notes || ''
    });
    setOpenDialog(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this lead?')) {
      try {
        await axios.delete(`/api/v1/crm/leads/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        toast.success('Lead deleted successfully');
        fetchLeads();
      } catch (error) {
        console.error('Error deleting lead:', error);
        toast.error('Failed to delete lead');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      title: '',
      company_id: '',
      contact_id: '',
      source: '',
      status: 'new',
      estimated_value: '',
      probability: 0,
      expected_close_date: '',
      assigned_to_id: '',
      description: '',
      notes: ''
    });
    setEditingLead(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const getStatusInfo = (status) => {
    return leadStatuses.find(s => s.value === status) || leadStatuses[0];
  };

  const getCompanyName = (companyId) => {
    const company = companies.find(c => c.id === companyId);
    return company ? company.name : '';
  };

  const getContactName = (contactId) => {
    const contact = contacts.find(c => c.id === contactId);
    return contact ? `${contact.first_name} ${contact.last_name}` : '';
  };

  const getUserName = (userId) => {
    const user = users.find(u => u.id === userId);
    return user ? `${user.first_name} ${user.last_name}` : '';
  };

  const filteredLeads = leads.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <LeadIcon fontSize="large" color="primary" />
          Leads Management
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            resetForm();
            setOpenDialog(true);
          }}
          sx={{ borderRadius: 2 }}
        >
          Add Lead
        </Button>
      </Box>

      {/* Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Search leads..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={statusFilter}
                  label="Status"
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <MenuItem value="">All Statuses</MenuItem>
                  {leadStatuses.map((status) => (
                    <MenuItem key={status.value} value={status.value}>
                      {status.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Leads Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Lead</TableCell>
                      <TableCell>Company/Contact</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Value</TableCell>
                      <TableCell>Probability</TableCell>
                      <TableCell>Assigned To</TableCell>
                      <TableCell>Close Date</TableCell>
                      <TableCell align="center">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredLeads.map((lead) => {
                      const statusInfo = getStatusInfo(lead.status);
                      return (
                        <TableRow key={lead.id} hover>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Avatar sx={{ bgcolor: 'primary.main' }}>
                                {lead.title?.[0]?.toUpperCase()}
                              </Avatar>
                              <Box>
                                <Typography variant="subtitle2" fontWeight={600}>
                                  {lead.title}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  {lead.source}
                                </Typography>
                              </Box>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 0.5 }}>
                                <BusinessIcon fontSize="small" color="action" />
                                <Typography variant="body2">
                                  {getCompanyName(lead.company_id)}
                                </Typography>
                              </Box>
                              {lead.contact_id && (
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                  <PersonIcon fontSize="small" color="action" />
                                  <Typography variant="caption">
                                    {getContactName(lead.contact_id)}
                                  </Typography>
                                </Box>
                              )}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={statusInfo.label}
                              color={statusInfo.color}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                              <MoneyIcon fontSize="small" color="action" />
                              <Typography variant="body2">
                                {lead.estimated_value 
                                  ? `₹${Number(lead.estimated_value).toLocaleString()}`
                                  : '-'
                                }
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                              <LinearProgress
                                variant="determinate"
                                value={lead.probability || 0}
                                sx={{ flexGrow: 1, height: 6, borderRadius: 3 }}
                              />
                              <Typography variant="caption">
                                {lead.probability || 0}%
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">
                              {getUserName(lead.assigned_to_id)}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                              <CalendarIcon fontSize="small" color="action" />
                              <Typography variant="caption">
                                {lead.expected_close_date || '-'}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell align="center">
                            <IconButton onClick={() => handleEdit(lead)} size="small">
                              <EditIcon />
                            </IconButton>
                            <IconButton 
                              onClick={() => handleDelete(lead.id)} 
                              size="small"
                              color="error"
                            >
                              <DeleteIcon />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </TableContainer>
              <TablePagination
                rowsPerPageOptions={[5, 10, 25]}
                component="div"
                count={leads.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={(e, newPage) => setPage(newPage)}
                onRowsPerPageChange={(e) => {
                  setRowsPerPage(parseInt(e.target.value, 10));
                  setPage(0);
                }}
              />
            </>
          )}
        </CardContent>
      </Card>

      {/* Add/Edit Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingLead ? 'Edit Lead' : 'Add New Lead'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Lead Title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  required
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Company</InputLabel>
                  <Select
                    name="company_id"
                    value={formData.company_id}
                    label="Company"
                    onChange={handleInputChange}
                  >
                    {companies.map((company) => (
                      <MenuItem key={company.id} value={company.id}>
                        {company.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Contact</InputLabel>
                  <Select
                    name="contact_id"
                    value={formData.contact_id}
                    label="Contact"
                    onChange={handleInputChange}
                  >
                    {contacts.map((contact) => (
                      <MenuItem key={contact.id} value={contact.id}>
                        {contact.first_name} {contact.last_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Source</InputLabel>
                  <Select
                    name="source"
                    value={formData.source}
                    label="Source"
                    onChange={handleInputChange}
                  >
                    {leadSources.map((source) => (
                      <MenuItem key={source} value={source}>
                        {source}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Status</InputLabel>
                  <Select
                    name="status"
                    value={formData.status}
                    label="Status"
                    onChange={handleInputChange}
                  >
                    {leadStatuses.map((status) => (
                      <MenuItem key={status.value} value={status.value}>
                        {status.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Estimated Value (₹)"
                  name="estimated_value"
                  type="number"
                  value={formData.estimated_value}
                  onChange={handleInputChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Probability (%)"
                  name="probability"
                  type="number"
                  inputProps={{ min: 0, max: 100 }}
                  value={formData.probability}
                  onChange={handleInputChange}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Expected Close Date"
                  name="expected_close_date"
                  type="date"
                  value={formData.expected_close_date}
                  onChange={handleInputChange}
                  margin="normal"
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth margin="normal">
                  <InputLabel>Assigned To</InputLabel>
                  <Select
                    name="assigned_to_id"
                    value={formData.assigned_to_id}
                    label="Assigned To"
                    onChange={handleInputChange}
                  >
                    {users.map((user) => (
                      <MenuItem key={user.id} value={user.id}>
                        {user.first_name} {user.last_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  margin="normal"
                  multiline
                  rows={3}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Notes"
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  margin="normal"
                  multiline
                  rows={3}
                />
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button type="submit" variant="contained">
              {editingLead ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  );
};

export default Leads;