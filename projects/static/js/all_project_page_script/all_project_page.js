 // Project data
 const projectsData = [
    {
        name: "My discovery project",
        key: "MDP",
        type: "Product Discovery",
        lead: "Pratham Patel",
        leadInitials: "PP",
        product: "Jira",
        iconColor: "blue-bg"
    },
    {
        name: "Real-time Task Manager",
        key: "RTTM",
        type: "Product Discovery",
        lead: "Pratham Patel",
        leadInitials: "PP",
        product: "Jira",
        iconColor: "purple-bg"
    },
    {
        name: "Support",
        key: "SUP",
        type: "Service management",
        lead: "Pratham Patel",
        leadInitials: "PP",
        product: "Confluence",
        iconColor: "teal-bg"
    },
    {
        name: "Marketing Campaign",
        key: "MKTG",
        type: "Product Discovery",
        lead: "Sarah Johnson",
        leadInitials: "SJ",
        product: "Jira",
        iconColor: "green-bg"
    },
    {
        name: "Customer Feedback Portal",
        key: "CFP",
        type: "Service management",
        lead: "Alex Kim",
        leadInitials: "AK",
        product: "Confluence",
        iconColor: "orange-bg"
    },
    {
        name: "Mobile App Development",
        key: "MAD",
        type: "Product Discovery",
        lead: "Ryan Cooper",
        leadInitials: "RC",
        product: "Jira",
        iconColor: "red-bg"
    },
    {
        name: "IT Infrastructure",
        key: "ITI",
        type: "Service management",
        lead: "Maria Lopez",
        leadInitials: "ML",
        product: "Confluence",
        iconColor: "blue-bg"
    },
    {
        name: "Website Redesign",
        key: "WRD",
        type: "Product Discovery",
        lead: "James Wilson",
        leadInitials: "JW",
        product: "Jira",
        iconColor: "purple-bg"
    },
    {
        name: "Internal Training",
        key: "INT",
        type: "Service management",
        lead: "Emma Brown",
        leadInitials: "EB",
        product: "Confluence",
        iconColor: "teal-bg"
    }
];

// Pagination settings
const projectsPerPage = 6;
let currentPage = 1;
let filteredProjects = [...projectsData];

// Toggle dropdown menus
function setupDropdowns() {
    const productFilter = document.getElementById('product-filter');
    const productDropdown = document.getElementById('product-dropdown');
    const typeFilter = document.getElementById('type-filter');
    const typeDropdown = document.getElementById('type-dropdown');
    
    productFilter.addEventListener('click', () => {
        productDropdown.classList.toggle('show');
        // Close the other dropdown if open
        typeDropdown.classList.remove('show');
    });
    
    typeFilter.addEventListener('click', () => {
        typeDropdown.classList.toggle('show');
        // Close the other dropdown if open
        productDropdown.classList.remove('show');
    });
    
    // Close dropdowns when clicking elsewhere
    document.addEventListener('click', (event) => {
        if (!productFilter.contains(event.target) && !productDropdown.contains(event.target)) {
            productDropdown.classList.remove('show');
        }
        
        if (!typeFilter.contains(event.target) && !typeDropdown.contains(event.target)) {
            typeDropdown.classList.remove('show');
        }
    });
    
    // Product filter selection
    const productItems = productDropdown.querySelectorAll('.dropdown-item');
    productItems.forEach(item => {
        item.addEventListener('click', () => {
            const productValue = item.getAttribute('data-value');
            productFilter.textContent = item.textContent;
            productFilter.appendChild(document.createElement('span')).className = 'dropdown-arrow';
            productFilter.querySelector('.dropdown-arrow').textContent = '▼';
            filterProjects();
            productDropdown.classList.remove('show');
        });
    });
    
    // Type filter selection
    const typeItems = typeDropdown.querySelectorAll('.dropdown-item');
    typeItems.forEach(item => {
        item.addEventListener('click', () => {
            const typeValue = item.getAttribute('data-value');
            typeFilter.textContent = item.textContent;
            typeFilter.appendChild(document.createElement('span')).className = 'dropdown-arrow';
            typeFilter.querySelector('.dropdown-arrow').textContent = '▼';
            filterProjects();
            typeDropdown.classList.remove('show');
        });
    });
}

// Project search and filtering functionality
function setupSearch() {
    const searchInput = document.getElementById('search-input');
    
    searchInput.addEventListener('input', () => {
        filterProjects();
    });
}

// Filter projects based on search and filters
function filterProjects() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const typeFilter = document.getElementById('type-filter').textContent.trim().replace('▼', '');
    const productFilter = document.getElementById('product-filter').textContent.trim().replace('▼', '');
    
    filteredProjects = projectsData.filter(project => {
        const matchesSearch = project.name.toLowerCase().includes(searchTerm) || 
                             project.key.toLowerCase().includes(searchTerm);
        const matchesType = typeFilter === 'All types' || project.type === typeFilter;
        const matchesProduct = productFilter === 'All products' || project.product === productFilter;
        
        return matchesSearch && matchesType && matchesProduct;
    });
    
    // Reset to first page after filtering
    currentPage = 1;
    
    // Update UI
    renderProjects();
    renderPagination();
}

// Render project rows
function renderProjects() {
    const tableBody = document.getElementById('project-table-body');
    const noResults = document.getElementById('no-results');
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    if (filteredProjects.length === 0) {
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    
    // Calculate start and end indices for current page
    const startIndex = (currentPage - 1) * projectsPerPage;
    const endIndex = Math.min(startIndex + projectsPerPage, filteredProjects.length);
    
    // Add project rows for current page
    for (let i = startIndex; i < endIndex; i++) {
        const project = filteredProjects[i];
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="star-icon">☆</span></td>
            <td>
                <a href="#" class="project-name">
                    <span class="project-icon ${project.iconColor}">${project.name.charAt(0)}</span>
                    ${project.name}
                </a>
            </td>
            <td>
                <a href="/project/${project.key}" class="project-key">${project.key}</a>
            </td>
            <td>${project.type}</td>
            <td>
                <div class="avatar">${project.leadInitials}</div>
                ${project.lead}
            </td>
            <td></td>
            <td><span class="more-actions">⋯</span></td>
        `;
        
        tableBody.appendChild(row);
    }
}

// Render pagination buttons
function renderPagination() {
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';
    
    const totalPages = Math.ceil(filteredProjects.length / projectsPerPage);
    
    // Previous button
    const prevButton = document.createElement('button');
    prevButton.className = `pagination-button ${currentPage === 1 ? 'disabled' : ''}`;
    prevButton.textContent = '‹';
    if (currentPage > 1) {
        prevButton.addEventListener('click', () => {
            currentPage--;
            renderProjects();
            renderPagination();
        });
    }
    paginationContainer.appendChild(prevButton);
    
    // Page number buttons
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = `pagination-button ${i === currentPage ? 'active' : ''}`;
        pageButton.textContent = i;
        pageButton.addEventListener('click', () => {
            currentPage = i;
            renderProjects();
            renderPagination();
        });
        paginationContainer.appendChild(pageButton);
    }
    
    // If no pages or only one page, still show page 1
    if (totalPages === 0) {
        const pageButton = document.createElement('button');
        pageButton.className = 'pagination-button active';
        pageButton.textContent = '1';
        paginationContainer.appendChild(pageButton);
    }
    
    // Next button
    const nextButton = document.createElement('button');
    nextButton.className = `pagination-button ${currentPage === totalPages || totalPages === 0 ? 'disabled' : ''}`;
    nextButton.textContent = '›';
    if (currentPage < totalPages) {
        nextButton.addEventListener('click', () => {
            currentPage++;
            renderProjects();
            renderPagination();
        });
    }
    paginationContainer.appendChild(nextButton);
}

// Initialize functionality
document.addEventListener('DOMContentLoaded', () => {
    setupDropdowns();
    setupSearch();
    renderProjects();
    renderPagination();
    
    // Set up star functionality
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('star-icon')) {
            if (event.target.textContent === '☆') {
                event.target.textContent = '★';
                event.target.style.color = '#FFAB00';
            } else {
                event.target.textContent = '☆';
                event.target.style.color = '#6b778c';
            }
        }
    });
});