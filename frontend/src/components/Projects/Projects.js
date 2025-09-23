
import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
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
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import { Add, Edit, Delete, Assignment } from '@mui/icons-material';
import axios from 'axios';
import { toast } from 'react-toastify';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [openProject, setOpenProject] = useState(false);
  const [openTask, setOpenTask] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentProject, setCurrentProject] = useState({
    name: '',
    description: '',
    budget: '',
    status: 'active',
    start_date: '',
    end_date: ''
  });
  const [currentTask, setCurrentTask] = useState({
    title: '',
    project_id: '',
    priority: 'Medium',
    estimated_hours: '',
    status: 'pending',
    description: ''
  });

  const statusOptions = ['active', 'on_hold', 'completed', 'cancelled'];
  const priorityOptions = ['Low', 'Medium', 'High', 'Critical'];
  const taskStatusOptions = ['pending', 'in_progress', 'completed', 'cancelled'];

  useEffect(() => {
    fetchProjects();
    fetchTasks();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await axios.get('/api/v1/projects/projects/');
      setProjects(response.data);
    } catch (error) {
      toast.error('Error fetching projects');
    }
  };

  const fetchTasks = async () => {
    try {
      const response = await axios.get('/api/v1/projects/tasks/');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks');
    }
  };

  const handleOpenProject = (project = null) => {
    if (project) {
      setCurrentProject({
        ...project,
        start_date: project.start_date ? project.start_date.split('T')[0] : '',
        end_date: project.end_date ? project.end_date.split('T')[0] : ''
      });
      setEditMode(true);
    } else {
      setCurrentProject({
        name: '',
        description: '',
        budget: '',
        status: 'active',
        start_date: '',
        end_date: ''
      });
      setEditMode(false);
    }
    setOpenProject(true);
  };

  const handleOpenTask = (task = null) => {
    if (task) {
      setCurrentTask(task);
      setEditMode(true);
    } else {
      setCurrentTask({
        title: '',
        project_id: '',
        priority: 'Medium',
        estimated_hours: '',
        status: 'pending',
        description: ''
      });
      setEditMode(false);
    }
    setOpenTask(true);
  };

  const handleCloseProject = () => {
    setOpenProject(false);
    setCurrentProject({
      name: '',
      description: '',
      budget: '',
      status: 'active',
      start_date: '',
      end_date: ''
    });
  };

  const handleCloseTask = () => {
    setOpenTask(false);
    setCurrentTask({
      title: '',
      project_id: '',
      priority: 'Medium',
      estimated_hours: '',
      status: 'pending',
      description: ''
    });
  };

  const handleSubmitProject = async () => {
    try {
      const projectData = {
        ...currentProject,
        budget: parseFloat(currentProject.budget) || 0
      };

      if (editMode) {
        await axios.put(`/api/v1/projects/projects/${currentProject.id}`, projectData);
        toast.success('Project updated successfully');
      } else {
        await axios.post('/api/v1/projects/projects/', projectData);
        toast.success('Project created successfully');
      }
      fetchProjects();
      handleCloseProject();
    } catch (error) {
      toast.error('Error saving project');
    }
  };

  const handleSubmitTask = async () => {
    try {
      const taskData = {
        ...currentTask,
        estimated_hours: parseInt(currentTask.estimated_hours) || 0
      };

      if (editMode) {
        await axios.put(`/api/v1/projects/tasks/${currentTask.id}`, taskData);
        toast.success('Task updated successfully');
      } else {
        await axios.post('/api/v1/projects/tasks/', taskData);
        toast.success('Task created successfully');
      }
      fetchTasks();
      handleCloseTask();
    } catch (error) {
      toast.error('Error saving task');
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await axios.delete(`/api/v1/projects/projects/${projectId}`);
        toast.success('Project deleted successfully');
        fetchProjects();
      } catch (error) {
        toast.error('Error deleting project');
      }
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await axios.delete(`/api/v1/projects/tasks/${taskId}`);
        toast.success('Task deleted successfully');
        fetchTasks();
      } catch (error) {
        toast.error('Error deleting task');
      }
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'success',
      on_hold: 'warning',
      completed: 'info',
      cancelled: 'error',
      pending: 'default',
      in_progress: 'primary'
    };
    return colors[status] || 'default';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Low: 'success',
      Medium: 'info',
      High: 'warning',
      Critical: 'error'
    };
    return colors[priority] || 'default';
  };

  const getProjectName = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    return project ? project.name : 'N/A';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount || 0);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Project Management
      </Typography>

      <Grid container spacing={3}>
        {/* Projects Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Projects</Typography>
                <Button
                  variant="contained"
                  startIcon={<Add />}
                  onClick={() => handleOpenProject()}
                >
                  Add Project
                </Button>
              </Box>

              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Project Name</TableCell>
                      <TableCell>Budget</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Start Date</TableCell>
                      <TableCell>End Date</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {projects.map((project) => (
                      <TableRow key={project.id}>
                        <TableCell>{project.name}</TableCell>
                        <TableCell>{formatCurrency(project.budget)}</TableCell>
                        <TableCell>
                          <Chip 
                            label={project.status.replace('_', ' ')} 
                            color={getStatusColor(project.status)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          {project.start_date ? 
                            new Date(project.start_date).toLocaleDateString() : 
                            'N/A'
                          }
                        </TableCell>
                        <TableCell>
                          {project.end_date ? 
                            new Date(project.end_date).toLocaleDateString() : 
                            'N/A'
                          }
                        </TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleOpenProject(project)} color="primary">
                            <Edit />
                          </IconButton>
                          <IconButton onClick={() => handleDeleteProject(project.id)} color="error">
                            <Delete />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Tasks Section */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Tasks</Typography>
                <Button
                  variant="contained"
                  startIcon={<Assignment />}
                  onClick={() => handleOpenTask()}
                >
                  Add Task
                </Button>
              </Box>

              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Task Title</TableCell>
                      <TableCell>Project</TableCell>
                      <TableCell>Priority</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Estimated Hours</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {tasks.map((task) => (
                      <TableRow key={task.id}>
                        <TableCell>{task.title}</TableCell>
                        <TableCell>{getProjectName(task.project_id)}</TableCell>
                        <TableCell>
                          <Chip 
                            label={task.priority} 
                            color={getPriorityColor(task.priority)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={task.status.replace('_', ' ')} 
                            color={getStatusColor(task.status)}
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{task.estimated_hours}h</TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleOpenTask(task)} color="primary">
                            <Edit />
                          </IconButton>
                          <IconButton onClick={() => handleDeleteTask(task.id)} color="error">
                            <Delete />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Project Dialog */}
      <Dialog open={openProject} onClose={handleCloseProject} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editMode ? 'Edit Project' : 'Add New Project'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Project Name"
            fullWidth
            required
            value={currentProject.name}
            onChange={(e) => setCurrentProject({ ...currentProject, name: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={currentProject.description}
            onChange={(e) => setCurrentProject({ ...currentProject, description: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Budget"
            type="number"
            fullWidth
            value={currentProject.budget}
            onChange={(e) => setCurrentProject({ ...currentProject, budget: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Status"
            select
            fullWidth
            value={currentProject.status}
            onChange={(e) => setCurrentProject({ ...currentProject, status: e.target.value })}
          >
            {statusOptions.map((status) => (
              <MenuItem key={status} value={status}>
                {status.replace('_', ' ').charAt(0).toUpperCase() + status.replace('_', ' ').slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Start Date"
            type="date"
            fullWidth
            InputLabelProps={{ shrink: true }}
            value={currentProject.start_date}
            onChange={(e) => setCurrentProject({ ...currentProject, start_date: e.target.value })}
          />
          <TextField
            margin="dense"
            label="End Date"
            type="date"
            fullWidth
            InputLabelProps={{ shrink: true }}
            value={currentProject.end_date}
            onChange={(e) => setCurrentProject({ ...currentProject, end_date: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseProject}>Cancel</Button>
          <Button onClick={handleSubmitProject} variant="contained">
            {editMode ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Task Dialog */}
      <Dialog open={openTask} onClose={handleCloseTask} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editMode ? 'Edit Task' : 'Add New Task'}
        </DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Task Title"
            fullWidth
            required
            value={currentTask.title}
            onChange={(e) => setCurrentTask({ ...currentTask, title: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Project"
            select
            fullWidth
            value={currentTask.project_id}
            onChange={(e) => setCurrentTask({ ...currentTask, project_id: e.target.value })}
          >
            <MenuItem value="">Select Project</MenuItem>
            {projects.map((project) => (
              <MenuItem key={project.id} value={project.id}>
                {project.name}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Priority"
            select
            fullWidth
            value={currentTask.priority}
            onChange={(e) => setCurrentTask({ ...currentTask, priority: e.target.value })}
          >
            {priorityOptions.map((priority) => (
              <MenuItem key={priority} value={priority}>
                {priority}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Status"
            select
            fullWidth
            value={currentTask.status}
            onChange={(e) => setCurrentTask({ ...currentTask, status: e.target.value })}
          >
            {taskStatusOptions.map((status) => (
              <MenuItem key={status} value={status}>
                {status.replace('_', ' ').charAt(0).toUpperCase() + status.replace('_', ' ').slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            margin="dense"
            label="Estimated Hours"
            type="number"
            fullWidth
            value={currentTask.estimated_hours}
            onChange={(e) => setCurrentTask({ ...currentTask, estimated_hours: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={3}
            value={currentTask.description}
            onChange={(e) => setCurrentTask({ ...currentTask, description: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseTask}>Cancel</Button>
          <Button onClick={handleSubmitTask} variant="contained">
            {editMode ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Projects;
