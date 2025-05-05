const projectForm = document.querySelector('.create-project-form');
const projectNameInput = document.getElementById('project-name');
const projectDescInput = document.getElementById('project-description');
const projectTypeInput = document.getElementById('project-type'); // NEW: get type selector
const accessToken = localStorage.getItem('access_token'); // get from localStorage

projectForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  if (!accessToken) {
    alert('You are not logged in. Please log in first.');
    return;
  }

  if (!projectNameInput.value.trim()) {
    alert('Please enter a project name');
    projectNameInput.focus();
    return;
  }
  
  if (!projectDescInput.value.trim()) {
    alert('Please enter a project description');
    projectDescInput.focus();
    return;
  }
  
  if (!projectTypeInput.value) {
    alert('Please select a project type');
    projectTypeInput.focus();
    return;
  }
  
  const formData = {
    name: projectNameInput.value.trim(),
    description: projectDescInput.value.trim(),
    type: projectTypeInput.value, // send selected type key (WEB, API, etc.)
    team_members: []
  };
  
  try {
    const response = await fetch('http://127.0.0.1:8000/projects/api/projects/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      const result = await response.json();
      alert('Project created successfully!');
      console.log('API response:', result);
      window.location.href = '/dashboard'; // Redirect to dashboard
    } else {
      const errorData = await response.json();
      console.error('Error:', errorData);
      alert('Failed to create project: ' + (errorData.detail || 'Unknown error'));
    }
  } catch (error) {
    console.error('Request error:', error);
    alert('An error occurred. Please try again.');
  }
});
