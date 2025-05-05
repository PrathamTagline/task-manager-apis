// main.js
import { addMemberBtn, addMemberModal, modalClose, cancelAddMember, confirmAddMember, userSearchInput, userList, teamMembersList, roleSelect, imageUpload, imagePreview, previewContainer, removeImage, uploadLabel } from './elements.js';
import { validateProjectForm, isUserAlreadyAdded } from './validation.js';
import { fetchUsers, submitProject, submitProjectWithImage } from './apiService.js';

let selectedUser = null;
let selectedUserItem = null;
let teamMembers = [];

addMemberBtn.addEventListener('click', function() {
  addMemberModal.classList.add('active');
  selectedUser = null;
  selectedUserItem = null;
  confirmAddMember.disabled = true;
  userSearchInput.value = '';
  userList.innerHTML = '<p>Start typing to search for users...</p>';
});

modalClose.addEventListener('click', function() {
  addMemberModal.classList.remove('active');
});

cancelAddMember.addEventListener('click', function() {
  addMemberModal.classList.remove('active');
});

addMemberModal.addEventListener('click', function(e) {
  if (e.target === addMemberModal) {
    addMemberModal.classList.remove('active');
  }
});

userSearchInput.addEventListener('input', async function() {
  const searchTerm = this.value.trim();
  
  if (searchTerm.length === 0) {
    userList.innerHTML = '<p>Start typing to search for users...</p>';
    return;
  }
  
  const data = await fetchUsers(searchTerm);
  
  if (data) {
    userList.innerHTML = '';
    if (data.length > 0) {
      data.forEach(user => {
        const userItem = document.createElement('div');
        userItem.className = 'user-item';
        userItem.dataset.id = user.id;
        userItem.dataset.email = user.email;
        userItem.dataset.firstName = user.first_name || '';
        userItem.dataset.lastName = user.last_name || '';
        
        let initials = '';
        if (user.first_name && user.first_name.length > 0) {
          initials += user.first_name[0].toUpperCase();
        }
        if (user.last_name && user.last_name.length > 0) {
          initials += user.last_name[0].toUpperCase();
        }
        if (initials === '') {
          initials = user.email[0].toUpperCase();
        }
        
        userItem.dataset.avatar = initials;
        
        const displayName = (user.first_name || user.last_name) ? 
                           `${user.first_name} ${user.last_name}`.trim() : 
                           user.email;
        
        userItem.innerHTML = `
          <div class="member-avatar">${initials}</div>
          <div class="member-info">
            <div class="member-name">${displayName}</div>
            <div class="member-email">${user.email}</div>
          </div>
        `;
        
        userItem.addEventListener('click', function() {
          document.querySelectorAll('.user-item').forEach(item => item.classList.remove('selected'));
          this.classList.add('selected');
          selectedUser = {
            id: this.dataset.id,
            email: this.dataset.email,
            first_name: this.dataset.firstName,
            last_name: this.dataset.lastName,
            avatar: this.dataset.avatar
          };
          selectedUserItem = this;
          confirmAddMember.disabled = false;
        });
        
        userList.appendChild(userItem);
      });
    } else {
      userList.innerHTML = '<p>No users found.</p>';
    }
  }
});

confirmAddMember.addEventListener('click', function() {
  if (selectedUser) {
    if (!isUserAlreadyAdded(teamMembers, selectedUser.id)) {
      const memberData = {
        user: selectedUser.id,
        role: roleSelect.value.toUpperCase()
      };
      
      const userData = {
        id: selectedUser.id,
        email: selectedUser.email,
        first_name: selectedUser.first_name,
        last_name: selectedUser.last_name,
        avatar: selectedUser.avatar,
        role: roleSelect.value.toUpperCase()
      };
      
      teamMembers.push(memberData);
      const memberItem = createTeamMemberItem(userData);
      teamMembersList.appendChild(memberItem);
    } else {
      alert('User is already added to the team.');
    }
    
    addMemberModal.classList.remove('active');
  }
});

function createTeamMemberItem(userData) {
  const memberItem = document.createElement('div');
  memberItem.className = 'team-member-item';
  memberItem.dataset.id = userData.id;
  
  let initials = userData.avatar || '';
  if (!initials) {
    if (userData.first_name && userData.first_name.length > 0) {
      initials += userData.first_name[0].toUpperCase();
    }
    if (userData.last_name && userData.last_name.length > 0) {
      initials += userData.last_name[0].toUpperCase();
    }
    if (initials === '') {
      initials = userData.email[0].toUpperCase();
    }
  }
  
  const displayName = (userData.first_name || userData.last_name) ? 
                     `${userData.first_name} ${userData.last_name}`.trim() : 
                     userData.email;
  
  const memberAvatar = document.createElement('div');
  memberAvatar.className = 'member-avatar';
  memberAvatar.textContent = initials;
  
  const memberInfo = document.createElement('div');
  memberInfo.className = 'member-info';
  
  const memberName = document.createElement('div');
  memberName.className = 'member-name';
  memberName.textContent = displayName;
  
  const memberEmail = document.createElement('div');
  memberEmail.className = 'member-email';
  memberEmail.textContent = userData.email;
  
  memberInfo.appendChild(memberName);
  memberInfo.appendChild(memberEmail);
  
  const memberControls = document.createElement('div');
  memberControls.className = 'member-controls';
  
  const removeButton = document.createElement('button');
  removeButton.className = 'remove-member';
  removeButton.innerHTML = '&times;';
  
  removeButton.addEventListener('click', function() {
    const memberId = memberItem.dataset.id;
    
    teamMembers = teamMembers.filter(member => member.user !== memberId);
    memberItem.remove();
  });
  
  memberControls.appendChild(removeButton);
  
  memberItem.appendChild(memberAvatar);
  memberItem.appendChild(memberInfo);
  memberItem.appendChild(memberControls);
  
  return memberItem;
}

// Project form submission
const projectForm = document.getElementById('project-form');
projectForm.addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const title = document.getElementById('project-title').value.trim();
  const description = document.getElementById('project-description').value.trim();
  const projectType = document.getElementById('project-type-select').value;
  
  if (!validateProjectForm(title, description, projectType)) return;

  const projectData = {
    name: title,
    description: description,
    type: projectType.toUpperCase(),
    team_members: teamMembers
  };

  const imageFile = imageUpload.files[0];
  
  if (imageFile) {
    const formData = new FormData();
    formData.append('name', title);
    formData.append('description', description);
    formData.append('type', projectType.toUpperCase());
    formData.append('image', imageFile);
    formData.append('team_members', JSON.stringify(teamMembers));

    await submitProjectWithImage(formData);
  } else {
    await submitProject(projectData);
  }
});
