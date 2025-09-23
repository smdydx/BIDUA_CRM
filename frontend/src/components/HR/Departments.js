
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
} from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';

const Departments = () => {
  const [departments, setDepartments] = useState([]);
  const [open, setOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentDepartment, setCurrentDepartment] = useState({
    name: '',
    description: '',
    manager_id: null
  });

  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
    try {
      const response = await axios.get('/api/v1/hr/departments/');
      setDepartments(response.data);
    } catch (error) {
      toast.error('Error fetching departments');
    }
  };

  const handleOpen = (department = null) => {
    if (department) {
      setCurrentDepartment(department);
      setEditMode(true);
    } else {
      setCurrentDepartment({
        name: '',
        description: '',
        manager_id: null
      });
      setEditMode(false);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentDepartment({
      name: '',
      description: '',
      manager_id: null
    });
  };

  const handleSubmit = async () => {
    try {
      if (editMode) {
        await axios.put(`/api/v1/hr/departments/${currentDepartment.id}`, currentDepartment);
        toast.success('Department updated successfully');
      } else {
        await axios.post('/api/v1/hr/departments/', currentDepartment);
        toast.success('Department created successfully');
      }
      fetchDepartments();
      handleClose();
    } catch (error) {
      toast.error('Error saving department');
    }
  };

  const handleDelete = async (departmentId) => {
    if (window.confirm('Are you sure you want to delete this department?')) {
      try {
        await axios.delete(`/api/v1/hr/departments/${departmentId}`);
        toast.success('Department deleted successfully');
        fetchDepartments();
      } catch (error) {
        toast.error('Error deleting department');
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
          Add Department
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Department Name</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Created Date</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {departments.map((department) => (
              <TableRow key={department.id}>
                <TableCell>{department.name}</TableCell>
                <TableCell>{department.description}</TableCell>
                <TableCell>
                  {department.created_at ? 
                    new Date(department.created_at).toLocaleDateString() : 
                    'N/A'
                  }
                </TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(department)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(department.id)} color="error">
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
          {editMode ? 'Edit Department' : 'Add New Department'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Department Name"
            fullWidth
            required
            value={currentDepartment.name}
            onChange={(e) => setCurrentDepartment({ ...currentDepartment, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={currentDepartment.description}
            onChange={(e) => setCurrentDepartment({ ...currentDepartment, description: e.target.value })}
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

export default Departments;
