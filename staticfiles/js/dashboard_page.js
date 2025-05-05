import { elements } from './dashboard_page_scripts/elements.js';
import { toggleView, setActiveNavItem, toggleSubNav } from './dashboard_page_scripts/functions.js';
import { fetchProjects, logoutUser } from './dashboard_page_scripts/apiService.js';

document.addEventListener('DOMContentLoaded', async function () {
    // Ensure elements exist before attaching event listeners
    if (elements.projectsNavItem) {
        elements.projectsNavItem.addEventListener('click', function () {
            setActiveNavItem(this);
            toggleView('projects-view');
            toggleSubNav('projects-sub-nav', 'projects-chevron');
        });
    }

    if (elements.viewAllProjectsLink) {
        elements.viewAllProjectsLink.addEventListener('click', function (e) {
            e.preventDefault();
            toggleView('projects-view');
            setActiveNavItem(elements.projectsNavItem);

            if (!elements.subNav.classList.contains('expanded')) {
                elements.subNav.classList.add('expanded');
                elements.chevron.classList.add('expanded');
            }
        });
    }

    if (elements.viewAllProjects) {
        elements.viewAllProjects.addEventListener('click', function () {
            toggleView('projects-view');
            elements.subNavItems.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
        });
    }

    elements.navItems.forEach(item => {
        if (item.id !== 'projects-nav-item') {
            item.addEventListener('click', function () {
                setActiveNavItem(this);
                toggleView('dashboard-view');
            });
        }
    });

    elements.subNavItems.forEach(item => {
        if (item.id !== 'view-all-projects') {
            item.addEventListener('click', function () {
                setActiveNavItem(elements.projectsNavItem);
                elements.subNavItems.forEach(sub => sub.classList.remove('active'));
                this.classList.add('active');
                toggleView('dashboard-view');
            });
        }
    });

    elements.projectListItems.forEach(item => {
        item.addEventListener('click', function () {
            const projectId = this.dataset.project;

            setActiveNavItem(elements.projectsNavItem);

            if (!elements.subNav.classList.contains('expanded')) {
                elements.subNav.classList.add('expanded');
                elements.chevron.classList.add('expanded');
            }

            elements.subNavItems.forEach(navItem => {
                navItem.dataset.project === projectId
                    ? navItem.classList.add('active')
                    : navItem.classList.remove('active');
            });

            toggleView('dashboard-view');
        });
    });

    // Profile popup
    if (elements.avatar) {
        elements.avatar.addEventListener('click', () => {
            elements.popupMenu.style.display = elements.popupMenu.style.display === 'block' ? 'none' : 'block';
        });
    }

    document.addEventListener('click', (event) => {
        if (elements.avatar && elements.popupMenu) {
            if (!elements.avatar.contains(event.target) && !elements.popupMenu.contains(event.target)) {
                elements.popupMenu.style.display = 'none';
            }
        }
    });

    if (elements.profileLink) {
        elements.profileLink.addEventListener('click', () => {
            window.location.href = '/accounts/profile/';
        });
    }

    if (elements.logoutLink) {
        elements.logoutLink.addEventListener('click', () => {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');

            logoutUser()
                .then(() => window.location.href = '/accounts/signin/')
                .catch(err => console.error('Logout error:', err));
        });
    }

    const projectsContainer = document.getElementById('projects-grid'); // Main container for projects



    // Function to update projects in the main container
    async function updateProjects() {
        try {
            const projects = await fetchProjects(); // Fetch projects from the backend

            // Clear the main projects container
            projectsContainer.innerHTML = '';

            // Loop through the projects and create project cards
            projects.forEach(project => {
                const projectCard = document.createElement('div');
                projectCard.classList.add('project-card');

                // Add project details to the card
                projectCard.innerHTML = `
                   <a href="/projects/${project.key}" class="project-link"> 
                         <div class="project-header">
                        <div class="project-icon">${project.name.charAt(0).toUpperCase()}</div>
                        <div class="project-info">
                            <h3>${project.name}</h3>
                            <p>${project.description || 'No description available.'}</p>
                        </div>
                    </div>
                    <div class="project-content">
                        <div class="content-header">Recent queues</div>
                        <div class="content-list">
                            <div class="content-item">
                                <span>All open</span>
                                <span class="content-item-count">${project.all_open || 0}</span>
                            </div>
                            <div class="content-item">
                                <span>Open tasks</span>
                                <span class="content-item-count">${project.open_tasks || 0}</span>
                            </div>
                        </div>
                        <div class="dropdown">
                            <span>${project.queues || 0} queues</span>
                            <span style="margin-left: 4px;">▼</span>
                        </div>
                    </div>
                   </a>
                `;

                // Append the project card to the main container
                projectsContainer.appendChild(projectCard);
            });
        } catch (error) {
            console.error('Error updating projects:', error);
            projectsContainer.innerHTML = '<p>Error loading projects. Please try again later.</p>';
        }
    }

    // Initial calls to load projects into the sidebar and main container

    await updateProjects();
    setInterval(updateProjects, 5000);

    const CONFIG = {
        BASE_API_URL: 'http://127.0.0.1:8000',
        DEFAULT_ERROR_MESSAGE: 'An error occurred. Please try again later.'
    };
    
    const AUTH = {
        accessToken: localStorage.getItem("access_token"),
        refreshToken: localStorage.getItem("refresh_token")
    };
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationPopup = document.getElementById('notificationPopup');
    const closeBtn = document.getElementById('closeBtn');
    const notificationCount = document.getElementById('notificationCount');
    
    // Initial notification count (could be fetched from API)
    let count = 3;
    notificationCount.textContent = count;
    
    // Toggle popup when button is clicked
    notificationBtn.addEventListener('click', function() {
      notificationPopup.classList.toggle('show');
      
      // Only fetch notifications when opening
      if (notificationPopup.classList.contains('show')) {
        fetchNotifications();
      }
    });
    
    // Close popup when close button is clicked
    closeBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      notificationPopup.classList.remove('show');
    });
    
    // Close popup when clicking outside
    document.addEventListener('click', function(e) {
      if (!notificationBtn.contains(e.target) && !notificationPopup.contains(e.target)) {
        notificationPopup.classList.remove('show');
      }
    });
    
    // Your provided fetch function
    async function fetchNotifications() {
      const notificationContent = document.getElementById('notificationContent');
      notificationContent.innerHTML = '<div class="loading">Loading notifications...</div>';
      
      try {
        const res = await fetch(`${CONFIG.BASE_API_URL}/notifications/`, {
          headers: {
            'Authorization': `Bearer ${AUTH.accessToken}`
          }
        });
        
        const data = await res.json();
        
        // Update the notification count
        count = data.length;
        notificationCount.textContent = count;
        
        // Create the notification list
        if (data.length > 0) {
          const ul = document.createElement('ul');
          ul.className = 'notification-list';
          
          data.forEach(notif => {
            const li = document.createElement('li');
            li.textContent = notif.message + ' (' + new Date(notif.created_at).toLocaleString() + ')';
            ul.appendChild(li);
          });
          
          notificationContent.innerHTML = '';
          notificationContent.appendChild(ul);
        } else {
          notificationContent.innerHTML = '<div class="empty-notification">No new notifications</div>';
        }
      } catch (error) {
        console.error('Error fetching notifications:', error);
        notificationContent.innerHTML = '<div class="empty-notification">Failed to load notifications</div>';
      }
    }
});