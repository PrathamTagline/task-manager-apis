import { elements } from './dashboard_page_scripts/elements.js';
import { toggleView, setActiveNavItem, toggleSubNav } from './dashboard_page_scripts/functions.js';
import { fetchProjects } from './dashboard_page_scripts/apiService.js';

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
    setInterval(updateProjects, 5000)
});