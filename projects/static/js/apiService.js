// apiService.js
export async function fetchUsers(searchTerm) {
    try {
      const response = await fetch(`/accounts/api/users/?email=${encodeURIComponent(searchTerm)}`, {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json'
        }
      });
      return await response.json();
    } catch (error) {
      console.error('Request failed', error);
      return null;
    }
  }
  
  export async function submitProject(projectData) {
    try {
      const response = await fetch('/projects/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify(projectData)
      });
      return await response.json();
    } catch (err) {
      console.error('Request failed', err);
      alert('An error occurred while creating the project. Please try again.');
    }
  }
  
  export async function submitProjectWithImage(formData) {
    try {
      const response = await fetch('/projects/api/projects/', {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: formData
      });
      return await response.json();
    } catch (err) {
      console.error('Request failed', err);
      alert('An error occurred while creating the project. Please try again.');
    }
  }
  