// validation.js
export function validateProjectForm(title, description, projectType) {
    if (!title || !description || !projectType) {
      alert('Please fill out all required fields.');
      return false;
    }
    return true;
  }
  
  export function isUserAlreadyAdded(teamMembers, userId) {
    return teamMembers.some(member => member.user === userId);
  }
  