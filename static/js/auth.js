let token = localStorage.getItem('authToken') || '';

function setMessage(id, text, type = '') {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = text;
    el.className = `message ${type}`.trim();
  }
}

function togglePasswordVisibility(inputId, toggleEl) {
  const input = document.getElementById(inputId);
  if (input.type === 'password') {
    input.type = 'text';
    toggleEl.textContent = 'Ẩn';
  } else {
    input.type = 'password';
    toggleEl.textContent = 'Hiện';
  }
}

async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(path, { ...options, headers });
  const data = await response.json();
  return { response, data };
}

// Cập nhật thanh điều hướng thông minh dựa trên trạng thái Token
function updateNavbar() {
  const guestLinks = document.getElementById('guestLinks');
  const userLinks = document.getElementById('userLinks');
  const navUsername = document.getElementById('navUsername');
  const navIntro = document.getElementById('navIntro'); // Lấy thẻ Giới thiệu

  // Khai báo đầy đủ token và username từ localStorage
  const token = localStorage.getItem('authToken'); 
  const username = localStorage.getItem('username');

  if (token && username) {
    // === TRẠNG THÁI ĐÃ ĐĂNG NHẬP ===
    if (navIntro) navIntro.style.display = 'none'; // Ẩn chữ Giới thiệu
    if (guestLinks) guestLinks.style.display = 'none';
    if (userLinks) userLinks.style.display = 'flex';
    if (navUsername) navUsername.textContent = username;
  } else {
    // === TRẠNG THÁI CHƯA ĐĂNG NHẬP ===
    if (navIntro) navIntro.style.display = ''; // Hiện lại chữ Giới thiệu (để trống để nhận CSS mặc định)
    if (guestLinks) guestLinks.style.display = 'flex';
    if (userLinks) userLinks.style.display = 'none';
  }
}

// Khởi chạy khi tải trang
document.addEventListener('DOMContentLoaded', updateNavbar);