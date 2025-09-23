
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

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [open, setOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentEmployee, setCurrentEmployee] = useState({
    name: '',
    email: '',
    phone: '',
    position: '',
    department_id: '',
    salary: '',
    hire_date: '',
    status: 'active'
  });

  useEffect(() => {
    fetchEmployees();
    fetchDepartments();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await axios.get('/api/v1/hr/employees/');
      setEmployees(response.data);
    } catch (error) {
      toast.error('Error fetching employees');
    }
  };

  const fetchDepartments = async () => {
    try {
      const response = await axios.get('/api/v1/hr/departments/');
      setDepartments(response.data);
    } catch (error) {
      console.error('Error fetching departments');
    }
  };

  const handleOpen = (employee = null) => {
    if (employee) {
      setCurrentEmployee({
        ...employee,
        hire_date: employee.hire_date ? employee.hire_date.split('T')[0] : ''
      });
      setEditMode(true);
    } else {
      setCurrentEmployee({
        name: '',
        email: '',
        phone: '',
        position: '',
        department_id: '',
        salary: '',
        hire_date: '',
        status: 'active'
      });
      setEditMode(false);
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentEmployee({
      name: '',
      email: '',
      phone: '',
      position: '',
      department_id: '',
      salary: '',
      hire_date: '',
      status: 'active'
    });
  };

  const handleSubmit = async () => {
    try {
      const employeeData = {
        ...currentEmployee,
        salary: parseFloat(currentEmployee.salary) || 0
      };

      if (editMode) {
        await axios.put(`/api/v1/hr/employees/${currentEmployee.id}`, employeeData);
        toast.success('Employee updated successfully');
      } else {
        await axios.post('/api/v1/hr/employees/', employeeData);
        toast.success('Employee created successfully');
      }
      fetchEmployees();
      handleClose();
    } catch (error) {
      toast.error('Error saving employee');
    }
  };

  const handleDelete = async (employeeId) => {
    if (window.confirm('Are you sure you want to delete this employee?')) {
      try {
        await axios.delete(`/api/v1/hr/employees/${employeeId}`);
        toast.success('Employee deleted successfully');
        fetchEmployees();
      } catch (error) {
        toast.error('Error deleting employee');
      }
    }
  };

  const getDepartmentName = (departmentId) => {
    const department = departments.find(d => d.id === departmentId);
    return department ? department.name : 'N/A';
  };

  const formatSalary = (salary) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(salary || 0);
  };

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpen()}
        >
          Add Employee
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Position</TableCell>
              <TableCell>Department</TableCell>
              <TableCell>Salary</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees.map((employee) => (
              <TableRow key={employee.id}>
                <TableCell>{employee.name}</TableCell>
                <TableCell>{employee.email}</TableCell>
                <TableCell>{employee.position}</TableCell>
                <TableCell>{getDepartmentName(employee.department_id)}</TableCell>
                <TableCell>{formatSalary(employee.salary)}</TableCell>
                <TableCell>
                  <Chip 
                    label={employee.status} 
                    color={employee.status === 'active' ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton onClick={() => handleOpen(employee)} color="primary">
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(employee.id)} color="error">
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
          {editMode ? 'Edit Employee' : 'Add New Employee'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Employee Name"
            fullWidth
            required
            value={currentEmployee.name}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Email"
            type="email"
            fullWidth
            required
            value={currentEmployee.email}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, email: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Phone"
            fullWidth
            value={currentEmployee.phone}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, phone: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Position"
            fullWidth
            required
            value={currentEmployee.position}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, position: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Department"
            select
            fullWidth
            value={currentEmployee.department_id}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, department_id: e.target.value })}
          >
            <MenuItem value="">Select Department</MenuItem>
            {departments.map((department) => (
              <MenuItem key={department.id} value={department.id}>
                {department.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Salary"
            type="number"
            fullWidth
            value={currentEmployee.salary}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, salary: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Hire Date"
            type="date"
            fullWidth
            InputLabelProps={{ shrink: true }}
            value={currentEmployee.hire_date}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, hire_date: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Status"
            select
            fullWidth
            value={currentEmployee.status}
            onChange={(e) => setCurrentEmployee({ ...currentEmployee, status: e.target.value })}
          >
            <MenuItem value="active">Active</MenuItem>
            <MenuItem value="inactive">Inactive</MenuItem>
            <MenuItem value="terminated">Terminated</MenuItem>
          </TextField>
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

export default Employees;
