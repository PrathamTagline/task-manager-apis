// apiService.js

import { API_ENDPOINTS } from '../dashboard_const.js';

// apiService.js
export async function fetchProjects() {
    const token = localStorage.getItem('access_token');  // Retrieve JWT token from localStorage
    
    
    if (!token) {
        console.error('No token found!');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/projects/api/projects/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Send the token in the Authorization header
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching projects data:', error);
    }
}

export async function logoutUser() {
    try {
        return await fetch(API_ENDPOINTS.LOGOUT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        console.error('API Error (logoutUser):', error);
        throw error;
    }
}