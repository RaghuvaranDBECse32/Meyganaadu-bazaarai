const API_BASE = "http://127.0.0.1:8000";

function showPanel(panel) {
  document.querySelectorAll('.panel').forEach(p => p.style.display = 'none');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  if (panel === 'login') {
    document.getElementById('login-panel').style.display = 'block';
  } else if (panel === 'dashboard') {
    document.getElementById('dashboard-panel').style.display = 'block';
    const btn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.textContent.includes('Hot'));
    if (btn) btn.classList.add('active');
  } else if (panel === 'product') {
    document.getElementById('product-panel').style.display = 'block';
    const btn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.textContent.includes('Spend'));
    if (btn) btn.classList.add('active');
  } else if (panel === 'food') {
    document.getElementById('food-panel').style.display = 'block';
    const btn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.textContent.includes('Price'));
    if (btn) btn.classList.add('active');
  } else if (panel === 'analytics') {
    document.getElementById('analytics-panel').style.display = 'block';
    const btn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.textContent.includes('Grocery'));
    if (btn) btn.classList.add('active');
  } else if (panel === 'map') {
    document.getElementById('map-section').style.display = 'block';
    const btn = Array.from(document.querySelectorAll('.nav-btn')).find(b => b.textContent.includes('Ride'));
    if (btn) btn.classList.add('active');
  }
}

function saveToken(token) {
  localStorage.setItem('bz-token', token);
}

function getToken() {
  return localStorage.getItem('bz-token');
}

function setUser(userEmail) {
  localStorage.setItem('bz-user', userEmail);
  document.getElementById('user-display').textContent = userEmail;
  document.getElementById('btn-logout').style.display = 'inline-block';
  document.getElementById('login-panel').style.display = 'none';
  document.getElementById('dashboard-panel').style.display = 'block';
  showPanel('dashboard');
}

function logout() {
  localStorage.removeItem('bz-user');
  localStorage.removeItem('bz-token');
  document.getElementById('user-display').textContent = 'Guest';
  document.getElementById('btn-logout').style.display = 'none';
  document.getElementById('login-panel').style.display = 'block';
  document.getElementById('dashboard-panel').style.display = 'none';
}

async function callAPI(path, options = {}) {
  const token = getToken();
  options.headers = options.headers || {};
  options.headers['Content-Type'] = 'application/json';
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => null);
    throw new Error(err?.detail || 'API Error');
  }
  return res.json();
}

async function login() {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const msg = document.getElementById('login-message');

  if (!email || !password) {
    msg.style.color = '#c91a23';
    msg.textContent = 'Enter email and password.';
    return;
  }

  try {
    const payload = new URLSearchParams();
    payload.append('username', email);
    payload.append('password', password);

    const res = await fetch(`${API_BASE}/auth/token`, {
      method: 'POST',
      body: payload,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }

    const body = await res.json();
    saveToken(body.access_token);
    setUser(email);
    msg.style.color = 'green';
    msg.textContent = 'Login successful!';
    populateTopDemand();
  } catch (error) {
    msg.style.color = '#c91a23';
    msg.textContent = error.message;
  }
}

async function signup() {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const msg = document.getElementById('login-message');

  if (!email || !password) {
    msg.style.color = '#c91a23';
    msg.textContent = 'Enter email and password to register.';
    return;
  }

  try {
    const data = await callAPI('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    saveToken(data.access_token);
    setUser(email);
    msg.style.color = 'green';
    msg.textContent = 'Account created and logged in!';
    populateTopDemand();
  } catch (error) {
    msg.style.color = '#c91a23';
    msg.textContent = error.message;
  }
}

async function populateTopDemand() {
  try {
    const data = await callAPI('/forecast?skip=0&limit=10');
    const sorted = data.forecast
      .slice()
      .sort((a, b) => b.sales - a.sales)
      .slice(0, 3);

    const list = document.getElementById('top-demand');
    list.innerHTML = '';
    sorted.forEach(item => {
      const li = document.createElement('li');
      li.textContent = `${item.product} (${item.sales}) - ${item.forecast}`;
      list.appendChild(li);
    });
  } catch (err) {
    document.getElementById('top-demand').innerHTML = '<li>Unable to load data</li>';
  }
}

async function analyzeProduct() {
  const q = document.getElementById('prod-query').value.trim();
  const message = document.getElementById('product-message');

  if (!q) {
    message.textContent = 'Enter a product name to analyze.';
    return;
  }

  try {
    const data = await callAPI(`/compare/product?query=${encodeURIComponent(q)}&skip=0&limit=20`);
    const table = document.querySelector('#product-table tbody');
    table.innerHTML = '';

    if (!data.items.length) {
      message.textContent = 'No related results from dataset.';
      document.getElementById('product-table').style.display = 'none';
      return;
    }

    data.items.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${item.name}</td><td>${item.sales}</td><td>${item.price}</td><td>${item.forecast}</td><td>${item.amazon_price || 'N/A'}</td><td>${item.flipkart_price || 'N/A'}</td><td>${item.best_store || 'N/A'}</td>`;
      table.appendChild(tr);
    });

    document.getElementById('product-table').style.display = 'table';
    message.textContent = '';
  } catch (err) {
    message.textContent = err.message;
    document.getElementById('product-table').style.display = 'none';
  }
}

async function analyzeFood() {
  const q = document.getElementById('food-query').value.trim();
  const message = document.getElementById('food-message');

  if (!q) {
    message.textContent = 'Enter a dish or hotel name.';
    return;
  }

  try {
    const data = await callAPI(`/compare/food?query=${encodeURIComponent(q)}`);
    const foodTable = document.querySelector('#food-table tbody');
    foodTable.innerHTML = '';

    data.results.forEach(item => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td>${item.hotel}</td><td>${item.swiggy_price}</td><td>${item.zomato_price}</td><td>${item.rating}</td><td>${item.recommendation}</td>`;
      foodTable.appendChild(tr);
    });

    document.getElementById('food-table').style.display = 'table';
    message.textContent = '';
  } catch (err) {
    message.textContent = err.message;
    document.getElementById('food-table').style.display = 'none';
  }
}

async function loadAnalytics() {
  const message = document.getElementById('analytics-message');
  message.textContent = 'Loading analytics...';

  try {
    const [demandData, priceData] = await Promise.all([
      callAPI('/analytics/demand-trends'),
      callAPI('/analytics/price-comparison')
    ]);

    renderDemandChart(demandData.trends);
    renderPriceChart(priceData.comparisons);
    message.textContent = '';
  } catch (err) {
    message.textContent = err.message;
  }
}

function renderDemandChart(trends) {
  const ctx = document.getElementById('demandChart').getContext('2d');
  const labels = trends.map(t => t.forecast);
  const data = trends.map(t => t.count);

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Demand Distribution',
        data: data,
        backgroundColor: [
          '#ff9900',
          '#146eb4',
          '#232f3e',
          '#5f27cd'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
        }
      }
    }
  });
}

function renderPriceChart(comparisons) {
  const ctx = document.getElementById('priceChart').getContext('2d');
  const labels = comparisons.map(c => c.category);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Average Price',
          data: comparisons.map(c => c.avg_price),
          backgroundColor: '#ff9900',
          borderColor: '#ff9900',
          borderWidth: 1
        },
        {
          label: 'Amazon Avg',
          data: comparisons.map(c => c.avg_amazon || 0),
          backgroundColor: '#146eb4',
          borderColor: '#146eb4',
          borderWidth: 1
        },
        {
          label: 'Flipkart Avg',
          data: comparisons.map(c => c.avg_flipkart || 0),
          backgroundColor: '#232f3e',
          borderColor: '#232f3e',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

window.addEventListener('load', () => {
  const user = localStorage.getItem('bz-user');
  if (user && getToken()) {
    setUser(user);
    populateTopDemand();
  } else {
    showPanel('dashboard');
    document.getElementById('dashboard-panel').style.display = 'none';
    document.getElementById('login-panel').style.display = 'block';
  }
});
