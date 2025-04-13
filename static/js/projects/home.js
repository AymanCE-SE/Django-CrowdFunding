document.addEventListener('DOMContentLoaded', function() {
    const projectsContainer = document.getElementById('projectsContainer');
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.querySelector('input[name="q"]');
    const categoryLinks = document.querySelectorAll('.category-filter');
    
    function updateProjects(url) {
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            projectsContainer.innerHTML = html;
            // Update URL without reload
            window.history.pushState({}, '', url);
        })
        .catch(error => console.error('Error:', error));
    }

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const searchQuery = searchInput.value;
        const categoryId = document.getElementById('categoryInput').value;
        
        const params = new URLSearchParams(window.location.search);
        if (searchQuery) params.set('q', searchQuery);
        if (categoryId) params.set('category', categoryId);
        
        updateProjects(`${window.location.pathname}?${params.toString()}`);
    });

    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const categoryId = this.dataset.category;
            const params = new URLSearchParams(window.location.search);
            
            if (categoryId === 'all') {
                params.delete('category');
            } else {
                params.set('category', categoryId);
            }
            
            // Keep existing search query if any
            const searchQuery = searchInput.value;
            if (searchQuery) params.set('q', searchQuery);
            
            updateProjects(`${window.location.pathname}?${params.toString()}`);
            
            // Update active state
            categoryLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    document.getElementById('clearBtn')?.addEventListener('click', function() {
        searchInput.value = '';
        const params = new URLSearchParams(window.location.search);
        params.delete('q');
        updateProjects(`${window.location.pathname}?${params.toString()}`);
    });
});
