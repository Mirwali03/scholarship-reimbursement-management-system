* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Inter, Arial, sans-serif;
  background: #f5f7fb;
  color: #1f2937;
}

a { color: inherit; text-decoration: none; }
button, input, select {
  font: inherit;
}

.app-shell {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: #0f172a;
  color: #e2e8f0;
  padding: 24px 18px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.brand {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar nav a {
  padding: 10px 12px;
  border-radius: 8px;
  background: rgba(255,255,255,0.04);
}

.user-box {
  margin-top: auto;
  background: rgba(255,255,255,0.04);
  padding: 12px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-box button {
  margin-top: 8px;
  border: 0;
  border-radius: 8px;
  padding: 8px 10px;
  cursor: pointer;
  background: #2563eb;
  color: white;
}

.main-panel {
  padding: 32px;
}

.auth-page {
  max-width: 420px;
  margin: 100px auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  padding: 28px;
}

.auth-page h2 {
  margin-top: 0;
}

.form-grid {
  display: grid;
  gap: 16px;
}

.form-grid input, .form-grid select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
}

.form-grid button {
  border: 0;
  background: #2563eb;
  color: white;
  border-radius: 10px;
  padding: 11px 14px;
  cursor: pointer;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.metric-card, .panel {
  background: white;
  border-radius: 14px;
  padding: 18px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.metric-card h3 {
  margin: 0 0 10px;
  color: #64748b;
  font-size: 0.85rem;
}

.metric-card strong {
  font-size: 1.8rem;
}

.panel table {
  width: 100%;
  border-collapse: collapse;
}

.panel th, .panel td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 0.72rem;
  background: #dbeafe;
  color: #1d4ed8;
}

.error-box {
  margin-top: 12px;
  color: #b91c1c;
  background: #fee2e2;
  padding: 8px 10px;
  border-radius: 8px;
}
