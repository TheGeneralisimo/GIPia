const BACKEND = (location.hostname === 'localhost') ? 'http://localhost:8000' : 'https://gipia.onrender.com';
document.getElementById('btnUpload').onclick = async () => {
  const f = document.getElementById('file').files[0];
  if (!f) { alert('Selecciona un archivo'); return; }
  const fd = new FormData();
  fd.append('file', f);
  const res = await fetch(`${BACKEND}/upload`, { method: 'POST', body: fd });
  const jd = await res.json();
  alert('Documento procesado: ' + JSON.stringify(jd));
};

document.getElementById('btnSend').onclick = async () => {
  const p = document.getElementById('prompt').value;
  if (!p) return;
  addChat('Tú', p);
  const res = await fetch(`${BACKEND}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: p })
  });
  const jd = await res.json();
  addChat('Bot', jd.response);
};

function addChat(who, msg) {
  const win = document.getElementById('chat');
  const el = document.createElement('div');
  el.innerHTML = `<b>${who}:</b> <div>${msg.replace(/\n/g,'<br>')}</div><hr/>`;
  win.appendChild(el);
  win.scrollTop = win.scrollHeight;
}
