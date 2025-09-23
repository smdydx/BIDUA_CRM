
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
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [open, setOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentCompany, setCurrentCompany] = useState({
    name: '',
    industry: '',
    size: '',
    website: '',
    phone: '',
    email: '',
    address: ''
  });

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await axios.get('/api/v1/crm/companies/');
      setCompanies(response.data);
    } catch (error) {
      toast.error('Error fetching companies');
    }
  };

  const handleOpen = (company = null) => {
    if (company) {
      setCurrentCompany(company);
      setEditMode(true);
    } else {
      setCurrentCompany({
        name: '',
        industry: '',
        size: '',
        website: '',
        phone: '',
        email: '',
        address: ''
      });
      setEditMode(false);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentCompany({
      name: '',
      industry: '',
      size: '',
      website: '',
      phone: '',
      email: '',
      address: ''
    });
  };

  const handleSubmit = async () => {
    try {
      if (editMode) {
        await axios.put(`/api/v1/crm/companies/${currentCompany.id}`, currentCompany);
        toast.success('Company updated successfully');
      } else {
        await axios.post('/api/v1/crm/companies/', currentCompany);
        toast.success('Company created successfully');
      }
      fetchCompanies();
      handleClose();
    } catch (error) {
      toast.error('Error saving company');
    }
  };

  const handleDelete = async (companyId) => {
    if (window.confirm('Are you sure you want to delete this company?')) {
      try {
        await axios.delete(`/api/v1/crm/companies/${companyId}`);
        toast.success('Company deleted successfully');
        fetchCompanies();
      } catch (error) {
        toast.error('Error deleting company');
      }
    }
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Company
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Industry</TableCell>
              <TableCell>Size</TableCell>
              <TableCell>Website</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {companies.map((company) => (
              <TableRow key={company.id}>
                <TableCell>{company.name}</TableCell>
                <TableCell>{company.industry}</TableCell>
                <TableCell>
                  <Chip label={company.size} size="small" />
                </TableCell>
                <TableCell>{company.website}</TableCell>
                <TableCell>{company.email}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(company)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(company.id)} color="error">
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
          {editMode ? 'Edit Company' : 'Add New Company'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Company Name"
            fullWidth
            required
            value={currentCompany.name}
            onChange={(e) => setCurrentCompany({ ...currentCompany, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Industry"
            fullWidth
            value={currentCompany.industry}
            onChange={(e) => setCurrentCompany({ ...currentCompany, industry: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Company Size"
            fullWidth
            value={currentCompany.size}
            onChange={(e) => setCurrentCompany({ ...currentCompany, size: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Website"
            fullWidth
            value={currentCompany.website}
            onChange={(e) => setCurrentCompany({ ...currentCompany, website: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Email"
            type="email"
            fullWidth
            value={currentCompany.email}
            onChange={(e) => setCurrentCompany({ ...currentCompany, email: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={currentCompany.phone}
            onChange={(e) => setCurrentCompany({ ...currentCompany, phone: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Address"
            fullWidth
            multiline
            rows={2}
            value={currentCompany.address}
            onChange={(e) => setCurrentCompany({ ...currentCompany, address: e.target.value })}
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

export default Companies;
