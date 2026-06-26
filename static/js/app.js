/**
 * Grocery Store - Frontend Application
 * Handles CRUD operations with humorous animations and sound effects.
 */
(function () {
  'use strict';

  // --- DOM References ---
  const appContainer = document.getElementById('app');

  // --- State ---
  let products = [];

  // --- Sound Engine ---
  /**
   * Play a humorous "poof" sound using the Web Audio API.
   * Generates a short burst of filtered noise that simulates
   * a cartoon-style puff/disappearance effect.
   */
  function playPoofSound() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;

      const ctx = new AudioContext();
      const duration = 0.35; // seconds

      // Create a buffer of white noise
      const sampleRate = ctx.sampleRate;
      const length = Math.floor(sampleRate * duration);
      const buffer = ctx.createBuffer(1, length, sampleRate);
      const data = buffer.getChannelData(0);

      // Fill with white noise, with a quick decay envelope
      for (let i = 0; i < length; i++) {
        const t = i / sampleRate;
        // Exponential decay envelope
        const envelope = Math.exp(-t * 14);
        data[i] = (Math.random() * 2 - 1) * envelope * 0.4;
      }

      const source = ctx.createBufferSource();
      source.buffer = buffer;

      // Low-pass filter to make it sound soft and "poofy"
      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(800, ctx.currentTime);
      filter.frequency.exponentialRampToValueAtTime(200, ctx.currentTime + duration);

      // Gain node for master volume
      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.5, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);

      source.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      source.start(ctx.currentTime);
      source.stop(ctx.currentTime + duration);

      // Clean up context after playback
      source.onended = function () {
        ctx.close();
      };
    } catch (e) {
      // Silently fail if audio is not available
    }
  }

  // --- API Helpers ---
  async function apiFetch(url, options) {
    const resp = await fetch(url, options);
    if (!resp.ok) {
      const errBody = await resp.json().catch(function () { return {}; });
      throw new Error(errBody.detail || 'Request failed');
    }
    if (resp.status === 204) return null;
    return resp.json();
  }

  async function fetchProducts() {
    products = await apiFetch('/products/');
    return products;
  }

  async function createProduct(data) {
    const created = await apiFetch('/products/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    products.push(created);
    return created;
  }

  async function deleteProduct(id) {
    await apiFetch('/products/' + id, { method: 'DELETE' });
    products = products.filter(function (p) { return p.id !== id; });
  }

  // --- Rendering ---
  function buildHTML() {
    var html = '';
    html += '<div class="app-container">';
    html += '<h1 class="app-title">&#129722; Grocery Store</h1>';
    html += '<p class="app-subtitle">Manage your products with flair!</p>';

    // Error message area
    html += '<div id="error-msg" class="error-message"></div>';

    // Create product form
    html += '<form id="product-form" class="product-form" autocomplete="off">';
    html += '<input type="text" id="input-name" placeholder="Product name *" required maxlength="100">';
    html += '<input type="text" id="input-desc" placeholder="Description" maxlength="500">';
    html += '<input type="number" id="input-price" placeholder="Price *" required min="0.01" step="0.01">';
    html += '<input type="text" id="input-category" placeholder="Category" maxlength="50">';
    html += '<input type="text" id="input-unit" placeholder="Unit (e.g. kg)" maxlength="20">';
    html += '<input type="number" id="input-stock" placeholder="Stock" min="0" step="1">';
    html += '<button type="submit">&#x2795; Add Product</button>';
    html += '</form>';

    // Products table
    html += '<div class="product-table-wrapper">';
    html += '<table class="product-table">';
    html += '<thead><tr>';
    html += '<th>Name</th><th>Category</th><th>Price</th><th>Unit</th><th>Stock</th><th>Status</th><th></th>';
    html += '</tr></thead>';
    html += '<tbody id="product-tbody"></tbody>';
    html += '</table>';
    html += '</div>';

    html += '</div>';

    return html;
  }

  function renderProductRow(product, animateIn) {
    var row = document.createElement('tr');
    row.setAttribute('data-id', product.id);
    if (animateIn) {
      row.classList.add('bounce-in');
    }

    var priceFormatted = '$' + product.price.toFixed(2);
    var statusBadge = product.is_available
      ? '<span class="badge badge-available">Available</span>'
      : '<span class="badge badge-unavailable">Out of stock</span>';

    row.innerHTML =
      '<td data-label="Name">' + escapeHTML(product.name) + '</td>' +
      '<td data-label="Category">' + escapeHTML(product.category || 'Other') + '</td>' +
      '<td data-label="Price">' + priceFormatted + '</td>' +
      '<td data-label="Unit">' + escapeHTML(product.unit || 'piece') + '</td>' +
      '<td data-label="Stock">' + (product.stock_quantity || 0) + '</td>' +
      '<td data-label="Status">' + statusBadge + '</td>' +
      '<td data-label=""><button class="btn-delete" data-delete="' + product.id + '">&#128165; Delete</button></td>';

    return row;
  }

  function escapeHTML(str) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function renderProductList() {
    var tbody = document.getElementById('product-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (products.length === 0) {
      var row = document.createElement('tr');
      row.innerHTML = '<td colspan="7" class="empty-state">No products yet. Add one above! &#127822;</td>';
      tbody.appendChild(row);
      return;
    }

    products.forEach(function (product) {
      tbody.appendChild(renderProductRow(product, false));
    });
  }

  function showError(message) {
    var el = document.getElementById('error-msg');
    if (!el) return;
    el.textContent = message;
    el.classList.add('visible', 'shake');
    setTimeout(function () {
      el.classList.remove('visible', 'shake');
    }, 3000);
  }

  // --- Event Handling ---
  function handleFormSubmit(e) {
    e.preventDefault();

    var nameInput = document.getElementById('input-name');
    var priceInput = document.getElementById('input-price');

    var name = nameInput.value.trim();
    var price = parseFloat(priceInput.value);

    if (!name) {
      showError('Product name is required.');
      nameInput.classList.add('shake');
      setTimeout(function () { nameInput.classList.remove('shake'); }, 400);
      return;
    }

    if (isNaN(price) || price <= 0) {
      showError('Please enter a valid positive price.');
      priceInput.classList.add('shake');
      setTimeout(function () { priceInput.classList.remove('shake'); }, 400);
      return;
    }

    var data = {
      name: name,
      price: price,
      description: (document.getElementById('input-desc').value || '').trim(),
      category: (document.getElementById('input-category').value || '').trim() || 'Other',
      unit: (document.getElementById('input-unit').value || '').trim() || 'piece',
      stock_quantity: parseInt(document.getElementById('input-stock').value, 10) || 0,
      is_available: true,
    };

    createProduct(data)
      .then(function (created) {
        // Clear form
        document.getElementById('product-form').reset();

        // Remove empty state row if present
        var tbody = document.getElementById('product-tbody');
        var emptyRow = tbody.querySelector('.empty-state');
        if (emptyRow) {
          var parentRow = emptyRow.closest('tr');
          if (parentRow) parentRow.remove();
        }

        // Append new row with bounce animation
        var newRow = renderProductRow(created, true);
        tbody.appendChild(newRow);
      })
      .catch(function (err) {
        showError('Failed to create product: ' + err.message);
      });
  }

  function handleDeleteClick(e) {
    var target = e.target;
    if (!target.matches('.btn-delete')) return;

    var productId = parseInt(target.getAttribute('data-delete'), 10);
    if (isNaN(productId)) return;

    var row = target.closest('tr');
    if (!row) return;

    // Play the poof sound
    playPoofSound();

    // Add poof-out animation class
    row.classList.add('poof-out');

    // After animation completes, remove the row from DOM and call API
    setTimeout(function () {
      deleteProduct(productId)
        .then(function () {
          // If no products left, show empty state
          if (products.length === 0) {
            var tbody = document.getElementById('product-tbody');
            var emptyRow = document.createElement('tr');
            emptyRow.innerHTML = '<td colspan="7" class="empty-state">No products yet. Add one above! &#127822;</td>';
            tbody.appendChild(emptyRow);
          }
        })
        .catch(function (err) {
          showError('Failed to delete product: ' + err.message);
          // Re-render list if delete failed
          fetchProducts().then(renderProductList);
        });
    }, 400);
  }

  function setupEventDelegation() {
    var container = document.getElementById('app');
    if (!container) return;

    // Form submit
    container.addEventListener('submit', function (e) {
      if (e.target.id === 'product-form') {
        handleFormSubmit(e);
      }
    });

    // Delete button clicks (event delegation on tbody)
    container.addEventListener('click', function (e) {
      if (e.target.matches('.btn-delete') || e.target.closest('.btn-delete')) {
        handleDeleteClick(e);
      }
    });
  }

  // --- Initialization ---
  function init() {
    if (!appContainer) {
      console.error('App container #app not found.');
      return;
    }

    appContainer.innerHTML = buildHTML();
    setupEventDelegation();

    // Load initial product list
    fetchProducts()
      .then(renderProductList)
      .catch(function (err) {
        showError('Failed to load products: ' + err.message);
      });
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
