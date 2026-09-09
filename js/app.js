/**
 * Double Face : Le Père Lucien & Mère Martine
 * Interactions, Panier partagé, Devise & Expérience Clean Luxury
 */

(function() {
  'use strict';

  // 1. Initialisation du Panier partagé & Devise (LocalStorage)
  const CART_KEY = 'pl_mm_shared_cart';
  const CURRENCY_KEY = 'pl_mm_currency';
  
  let cart = [];
  let currency = 'EUR'; // 'EUR' ou 'USD'
  const EUR_TO_USD = 1.10;

  try {
    const saved = localStorage.getItem(CART_KEY);
    if (saved) cart = JSON.parse(saved);
    const savedCur = localStorage.getItem(CURRENCY_KEY);
    if (savedCur) currency = savedCur;
  } catch (e) {
    cart = [];
    currency = 'EUR';
  }

  function formatPrice(amountEUR) {
    if (currency === 'USD') {
      return '$' + (amountEUR * EUR_TO_USD).toFixed(2);
    }
    return amountEUR.toFixed(2).replace('.', ',') + ' €';
  }

  function saveCart() {
    try {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
    } catch (e) {}
    updateCartUI();
  }

  window.toggleCurrency = function() {
    currency = currency === 'EUR' ? 'USD' : 'EUR';
    try {
      localStorage.setItem(CURRENCY_KEY, currency);
    } catch (e) {}
    
    // Update currency toggle button labels
    document.querySelectorAll('.currency-toggle-btn').forEach(btn => {
      btn.textContent = currency === 'EUR' ? '€ EUR' : '$ USD';
    });

    // Update prices on the active page
    document.querySelectorAll('[data-price-eur]').forEach(el => {
      const priceEUR = parseFloat(el.getAttribute('data-price-eur'));
      if (!isNaN(priceEUR)) {
        if (el.classList.contains('product-card')) {
          const priceElem = el.querySelector('.product-price');
          if (priceElem) priceElem.textContent = formatPrice(priceEUR);
        } else {
          el.textContent = formatPrice(priceEUR);
        }
      }
    });

    updateCartUI();
  };

  function updateCartUI() {
    const badges = document.querySelectorAll('.cart-badge');
    const totalItems = cart.reduce((acc, item) => acc + item.qty, 0);
    badges.forEach(b => {
      b.textContent = totalItems;
      b.style.display = totalItems > 0 ? 'flex' : 'none';
    });

    const cartBody = document.querySelector('.cart-body');
    const cartSubtotal = document.querySelector('.cart-subtotal-val');
    const shippingBar = document.querySelector('.shipping-bar-fill');
    const shippingText = document.querySelector('.shipping-status-text');

    if (!cartBody) return;

    if (cart.length === 0) {
      cartBody.innerHTML = `
        <div class="cart-empty-message">
          <div style="font-size:24px;margin-bottom:8px;">🌿</div>
          Votre rituel d'apothicaire est vide.<br>
          <span style="font-size:12px;opacity:0.7;">Micro-lots artisanaux • Fait main en France</span>
        </div>
      `;
      if (cartSubtotal) cartSubtotal.textContent = formatPrice(0);
      if (shippingBar) shippingBar.style.width = '0%';
      if (shippingText) shippingText.textContent = `Plus que ${formatPrice(80)} pour la livraison offerte (Neutral Carbon) !`;
      return;
    }

    let subtotalEUR = 0;
    let html = '';

    cart.forEach((item, index) => {
      const itemTotalEUR = item.price * item.qty;
      subtotalEUR += itemTotalEUR;
      html += `
        <div class="cart-item">
          <img src="${item.image}" alt="${item.name}" class="cart-item-img">
          <div class="cart-item-info">
            <span class="cart-item-brand">${item.brand} • MICRO-LOT</span>
            <h4 class="cart-item-title">${item.name}</h4>
            <div class="cart-item-price">${formatPrice(item.price)}</div>
            <div class="cart-item-qty">
              <button class="qty-btn" onclick="window.updateQty(${index}, -1)" aria-label="Moins">-</button>
              <span>${item.qty}</span>
              <button class="qty-btn" onclick="window.updateQty(${index}, 1)" aria-label="Plus">+</button>
              <button style="margin-left:auto;color:#8a4d5b;font-size:11px;text-transform:uppercase;letter-spacing:1px;" onclick="window.removeCartItem(${index})">Retirer</button>
            </div>
          </div>
        </div>
      `;
    });

    cartBody.innerHTML = html;
    if (cartSubtotal) cartSubtotal.textContent = formatPrice(subtotalEUR);

    // Shipping calculation (80€ threshold)
    const thresholdEUR = 80.0;
    if (shippingBar && shippingText) {
      const percent = Math.min(100, (subtotalEUR / thresholdEUR) * 100);
      shippingBar.style.width = percent + '%';
      if (subtotalEUR >= thresholdEUR) {
        shippingText.innerHTML = '✨ <strong>Félicitations !</strong> Livraison neutre en carbone offerte.';
      } else {
        const remainingEUR = thresholdEUR - subtotalEUR;
        shippingText.innerHTML = `Plus que <strong>${formatPrice(remainingEUR)}</strong> pour la livraison offerte !`;
      }
    }
  }

  window.addToCart = function(product) {
    const existing = cart.find(item => item.id === product.id);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ ...product, qty: 1 });
    }
    saveCart();
    showToast(`"${product.name}" ajouté à votre rituel`);
    openCart();
  };

  window.updateQty = function(index, delta) {
    if (!cart[index]) return;
    cart[index].qty += delta;
    if (cart[index].qty <= 0) {
      cart.splice(index, 1);
    }
    saveCart();
  };

  window.removeCartItem = function(index) {
    if (!cart[index]) return;
    cart.splice(index, 1);
    saveCart();
  };

  // 2. Gestion du tiroir panier
  function openCart() {
    const overlay = document.querySelector('.cart-drawer-overlay');
    const drawer = document.querySelector('.cart-drawer');
    if (overlay && drawer) {
      overlay.classList.add('active');
      drawer.classList.add('active');
    }
  }

  function closeCart() {
    const overlay = document.querySelector('.cart-drawer-overlay');
    const drawer = document.querySelector('.cart-drawer');
    if (overlay && drawer) {
      overlay.classList.remove('active');
      drawer.classList.remove('active');
    }
  }

  // 3. Toasts de confirmation
  function showToast(message) {
    let toast = document.querySelector('.toast-notice');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'toast-notice';
      document.body.appendChild(toast);
    }
    toast.innerHTML = `<span>✓</span> <span>${message}</span>`;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  }

  // 4. Initialisation des événements au chargement
  document.addEventListener('DOMContentLoaded', () => {
    // Initialise currency toggle button labels
    document.querySelectorAll('.currency-toggle-btn').forEach(btn => {
      btn.textContent = currency === 'EUR' ? '€ EUR' : '$ USD';
    });

    // Format all product prices on page
    document.querySelectorAll('.product-card').forEach(card => {
      const priceElem = card.querySelector('.product-price');
      if (priceElem) {
        // extract raw number
        const match = priceElem.textContent.match(/([0-9]+[.,][0-9]{2})/);
        if (match) {
          const raw = parseFloat(match[1].replace(',', '.'));
          card.setAttribute('data-price-eur', raw);
          priceElem.textContent = formatPrice(raw);
        }
      }
    });

    updateCartUI();

    // Trigger cart open/close
    document.querySelectorAll('.btn-cart-toggle').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        openCart();
      });
    });

    const closeBtn = document.querySelector('.close-cart-btn');
    if (closeBtn) closeBtn.addEventListener('click', closeCart);

    const overlay = document.querySelector('.cart-drawer-overlay');
    if (overlay) overlay.addEventListener('click', closeCart);

    // Boutons de filtres catalogue
    const filterBtns = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.product-card');

    // Init prices with stored currency
    if (currency === 'USD') {
      document.querySelectorAll('.currency-toggle-btn').forEach(btn => {
        btn.textContent = '$ USD';
      });
      document.querySelectorAll('[data-price-eur]').forEach(el => {
        const priceEUR = parseFloat(el.getAttribute('data-price-eur'));
        if (!isNaN(priceEUR)) {
          if (el.classList.contains('product-card')) {
            const priceElem = el.querySelector('.product-price');
            if (priceElem) priceElem.textContent = formatPrice(priceEUR);
          } else {
            el.textContent = formatPrice(priceEUR);
          }
        }
      });
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.getAttribute('data-filter');

        productCards.forEach(card => {
          if (filter === 'all' || card.getAttribute('data-category') === filter) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });

    // Express Apple Pay simulation
    const applePayBtn = document.querySelector('.btn-apple-pay');
    if (applePayBtn) {
      applePayBtn.addEventListener('click', () => {
        if (cart.length === 0) {
          alert('Votre rituel est vide.');
          return;
        }
        alert('Pay : Commande validée en un clic ! Emballage 100% sans plastique expédié depuis notre atelier français.');
        cart = [];
        saveCart();
        closeCart();
      });
    }

    // Checkout standard simulation
    const checkoutBtn = document.querySelector('.btn-checkout');
    if (checkoutBtn) {
      checkoutBtn.addEventListener('click', () => {
        if (cart.length === 0) {
          alert('Votre rituel est vide.');
          return;
        }
        alert('Commande validée ! Vos micro-lots artisanaux sont préparés avec amour par la Maison Lelégard.');
        cart = [];
        saveCart();
        closeCart();
      });
    }
  });

})();
