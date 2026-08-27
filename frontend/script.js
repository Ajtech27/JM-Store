const API_BASE_URL = 'https://jm-store-wvua.onrender.com'; // Replace with your Render URL

let currentUser = null;

async function checkAuth() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/status`, { credentials: 'include' });
        const data = await res.json();
        currentUser = data.logged_in ? data.user : null;
        updateUI();
        if (currentUser) {
            loadOwnedItems();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
    }
}

async function loadItems() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/items`, { credentials: 'include' });
        const items = await res.json();
        renderItems(items, 'items-list', 'Buy', buyItem);
    } catch (error) {
        console.error('Failed to load items:', error);
        document.getElementById('items-list').innerHTML = `<p class="text-danger">Could not load items. Please try again.</p>`;
    }
}

async function loadOwnedItems() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/owned`, { credentials: 'include' });
        const items = await res.json();
        renderItems(items, 'owned-list', 'Sell', sellItem);
    } catch (error) {
        console.error('Failed to load owned items:', error);
    }
}

function renderItems(items, containerId, buttonText, actionFn) {
    const container = document.getElementById(containerId);
    if (!items || items.length === 0) {
        container.innerHTML = `<p class="text-muted">No items here.</p>`;
        return;
    }
    container.innerHTML = items.map(item => `
        <div class="col-md-4">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">${item.name}</h5>
                    <p class="card-text">$${item.price}</p>
                    <button class="btn btn-primary" onclick="window.${actionFn.name}(${item.id})">${buttonText}</button>
                </div>
            </div>
        </div>
    `).join('');
}

async function buyItem(itemId) {
    if (!currentUser) {
        window.location.href = `${API_BASE_URL}/login`;
        return;
    }
    try {
        const res = await fetch(`${API_BASE_URL}/api/buy/${itemId}`, {
            method: 'POST',
            credentials: 'include'
        });
        const data = await res.json();
        alert(data.message);
        loadItems();
        loadOwnedItems();
    } catch (error) {
        console.error('Failed to buy:', error);
        alert('Could not purchase item.');
    }
}

async function sellItem(itemId) {
    try {
        const res = await fetch(`${API_BASE_URL}/api/sell/${itemId}`, {
            method: 'POST',
            credentials: 'include'
        });
        const data = await res.json();
        alert(data.message);
        loadItems();
        loadOwnedItems();
    } catch (error) {
        console.error('Failed to sell:', error);
        alert('Could not sell item.');
    }
}

function updateUI() {
    const authDiv = document.getElementById('auth-buttons');
    if (currentUser) {
        authDiv.innerHTML = `
            <span class="text-light me-3">Welcome, ${currentUser.username}</span>
            <a href="${API_BASE_URL}/logout" class="btn btn-outline-light btn-sm">Logout</a>
        `;
    } else {
        authDiv.innerHTML = `
            <a href="${API_BASE_URL}/login" class="btn btn-outline-light btn-sm me-2">Login</a>
            <a href="${API_BASE_URL}/register" class="btn btn-primary btn-sm">Register</a>
        `;
    }
}

// Initial load
checkAuth();
loadItems();