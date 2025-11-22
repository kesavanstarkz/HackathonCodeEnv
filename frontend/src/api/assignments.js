import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const getAssignments = () => axios.get(`${API_BASE_URL}/assignments/`);

export const getAssignment = (id) => axios.get(`${API_BASE_URL}/assignments/${id}`);

export const createAssignment = (assignment) => axios.post(`${API_BASE_URL}/assignments/`, assignment);

export const getAssignmentStats = (id) => axios.get(`${API_BASE_URL}/assignments/${id}/stats`);

export const getSubmissionsForAssignment = (id) => axios.get(`${API_BASE_URL}/assignments/${id}/submissions`);

export const getTestCasesForAssignment = (id) => axios.get(`${API_BASE_URL}/assignments/${id}/testcases`);

export const createTestCaseForAssignment = (id, testcase) => axios.post(`${API_BASE_URL}/assignments/${id}/testcases`, testcase);

export const getCompletionStats = () => axios.get(`${API_BASE_URL}/assignments/completion-stats`);
