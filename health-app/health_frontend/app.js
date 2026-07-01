document.addEventListener('DOMContentLoaded', () => {

  /* ─────────────────────────────────────
     State
  ───────────────────────────────────── */
  let userName     = '';
  let userLocation = '';
  let userSymptoms = '';

  /* ─────────────────────────────────────
     DOM helpers
  ───────────────────────────────────── */
  const popup   = id => document.getElementById(id);
  const input   = id => document.getElementById(id);
  const errEl   = id => document.getElementById(id);

  function openPopup(id) {
    // Close all first
    ['popup-name','popup-location','popup-symptoms','popup-loading','popup-result']
      .forEach(p => { popup(p).classList.remove('open'); });
    // Open target with tiny delay so animation fires
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        popup(id).classList.add('open');
      });
    });
  }

  function closeAll() {
    ['popup-name','popup-location','popup-symptoms','popup-loading','popup-result']
      .forEach(p => popup(p).classList.remove('open'));
  }

  function showErr(errId, inputId) {
    const e = errEl(errId);
    const i = input(inputId);
    e.style.display = 'flex';
    i.classList.add('has-error');
    i.focus();
  }

  function clearErr(errId, inputId) {
    errEl(errId).style.display = 'none';
    input(inputId).classList.remove('has-error');
  }

  /* ─────────────────────────────────────
     Open wizard from landing button
  ───────────────────────────────────── */
  document.getElementById('btn-open-wizard').addEventListener('click', () => {
    openPopup('popup-name');
    setTimeout(() => input('input-name').focus(), 400);
  });

  /* ─────────────────────────────────────
     STEP 1 — Name
  ───────────────────────────────────── */
  input('input-name').addEventListener('input', () => clearErr('err-name', 'input-name'));
  input('input-name').addEventListener('keydown', e => { if (e.key === 'Enter') advanceName(); });

  function advanceName() {
    const val = input('input-name').value.trim();
    if (!val) { showErr('err-name', 'input-name'); return; }
    userName = val;
    openPopup('popup-location');
    setTimeout(() => input('input-location').focus(), 400);
  }

  document.getElementById('btn-name-next').addEventListener('click', advanceName);

  /* ─────────────────────────────────────
     STEP 2 — Location
  ───────────────────────────────────── */
  input('input-location').addEventListener('input', () => clearErr('err-location', 'input-location'));
  input('input-location').addEventListener('keydown', e => { if (e.key === 'Enter') advanceLocation(); });

  document.getElementById('btn-loc-back').addEventListener('click', () => {
    openPopup('popup-name');
    setTimeout(() => input('input-name').focus(), 400);
  });

  function advanceLocation() {
    const val = input('input-location').value.trim();
    const errElement = errEl('err-location');
    if (!val) {
      errElement.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> Please enter your location.';
      showErr('err-location', 'input-location');
      return;
    }
    if (!val.toLowerCase().includes('lagos')) {
      errElement.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> We only support locations within Lagos at the moment.';
      showErr('err-location', 'input-location');
      return;
    }
    userLocation = val;
    openPopup('popup-symptoms');
    setTimeout(() => input('input-symptoms').focus(), 400);
  }

  document.getElementById('btn-loc-next').addEventListener('click', advanceLocation);

  /* ─────────────────────────────────────
     STEP 3 — Symptoms
  ───────────────────────────────────── */
  input('input-symptoms').addEventListener('input', () => clearErr('err-symptoms', 'input-symptoms'));

  document.getElementById('btn-sym-back').addEventListener('click', () => {
    openPopup('popup-location');
    setTimeout(() => input('input-location').focus(), 400);
  });

  function advanceSymptoms() {
    const val = input('input-symptoms').value.trim();
    if (!val) { showErr('err-symptoms', 'input-symptoms'); return; }
    userSymptoms = val;
    runAnalysis();
  }

  document.getElementById('btn-sym-next').addEventListener('click', advanceSymptoms);

  /* ─────────────────────────────────────
     Loading animation
  ───────────────────────────────────── */
  function resetLoader() {
    ['lpi-1','lpi-2','lpi-3','lpi-4'].forEach((id, i) => {
      const el = document.getElementById(id);
      el.classList.remove('active','done');
      if (i === 0) el.classList.add('active');
    });
  }

  function animateLoader() {
    const ids = ['lpi-1','lpi-2','lpi-3','lpi-4'];
    let i = 0;
    const iv = setInterval(() => {
      if (i > 0) {
        document.getElementById(ids[i-1]).classList.remove('active');
        document.getElementById(ids[i-1]).classList.add('done');
      }
      if (i < ids.length) {
        document.getElementById(ids[i]).classList.add('active');
        i++;
      } else {
        clearInterval(iv);
      }
    }, 900);
    return iv;
  }

  /* ─────────────────────────────────────
     STEP 4 — Analyze
  ───────────────────────────────────── */
  function runAnalysis() {
    document.getElementById('lp-name').textContent = userName;
    resetLoader();
    openPopup('popup-loading');

    const loaderIv = animateLoader();

    fetch('http://localhost:8000/api/detect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symptoms: userSymptoms, location: userLocation })
    })
    .then(res => {
      if (!res.ok) return res.json().then(e => { throw new Error(e.detail || 'Failed to analyze.'); });
      return res.json();
    })
    .then(data => {
      clearInterval(loaderIv);
      // Small pause so last loader step visually completes
      setTimeout(() => {
        populateResults(data);
        openPopup('popup-result');
      }, 700);
    })
    .catch(err => {
      clearInterval(loaderIv);
      console.error(err);
      closeAll();
      alert(err.message || 'An error occurred. Make sure the backend is running.');
    });
  }

  /* ─────────────────────────────────────
     STEP 5 — Results
  ───────────────────────────────────── */
  function populateResults(data) {
    document.getElementById('result-name').textContent    = userName;
    document.getElementById('disease-name').textContent   = data.disease_name    || 'Unknown Condition';
    document.getElementById('hospital-name').textContent  = data.hospital_name   || 'Unknown Hospital';
    document.getElementById('hospital-address').textContent = data.hospital_address || 'Unknown Address';
    document.getElementById('hospital-contact').textContent = data.hospital_contact || 'Unknown Contact';

    // Map
    const mapIframe = document.getElementById('hospital-map');
    if (mapIframe) {
      const isMock = !data.hospital_name ||
        data.hospital_name === 'Unknown Hospital' ||
        data.hospital_name === 'City General Health Center';

      let mapQuery;
      if (!isMock) {
        mapQuery = data.hospital_name;
        if (data.hospital_address && !data.hospital_address.includes('Unknown')) {
          mapQuery += `, ${data.hospital_address}`;
        } else {
          mapQuery += `, ${userLocation}`;
        }
      } else {
        const terms = ['Hospital','General Hospital','Medical Center','Health Clinic','Memorial Hospital'];
        mapQuery = `${terms[Math.floor(Math.random() * terms.length)]}, ${userLocation}`;
      }
      mapIframe.src = `https://maps.google.com/maps?q=${encodeURIComponent(mapQuery)}&t=&z=14&ie=UTF8&output=embed`;
    }

    // Lists
    const drugsList = document.getElementById('recommended-drugs');
    const solsList  = document.getElementById('solutions');
    const docsList  = document.getElementById('doctors');

    drugsList.innerHTML = '';
    (data.recommended_drugs || []).forEach(d => {
      const li = document.createElement('li'); li.textContent = d; drugsList.appendChild(li);
    });

    solsList.innerHTML = '';
    (data.solutions || []).forEach(s => {
      const li = document.createElement('li'); li.textContent = s; solsList.appendChild(li);
    });

    docsList.innerHTML = '';
    (data.doctors_to_talk_to || []).forEach(doc => {
      const li = document.createElement('li'); li.textContent = doc; docsList.appendChild(li);
    });
  }

  /* ─────────────────────────────────────
     Restart
  ───────────────────────────────────── */
  document.getElementById('btn-restart').addEventListener('click', () => {
    closeAll();
    // Reset
    input('input-name').value = '';
    input('input-location').value = '';
    input('input-symptoms').value = '';
    userName = userLocation = userSymptoms = '';
    // Re-open step 1 after a beat
    setTimeout(() => {
      openPopup('popup-name');
      setTimeout(() => input('input-name').focus(), 400);
    }, 300);
  });

  /* ─────────────────────────────────────
     Close on backdrop click (not loading/result)
  ───────────────────────────────────── */
  ['popup-name','popup-location','popup-symptoms'].forEach(id => {
    popup(id).addEventListener('click', e => {
      if (e.target === popup(id)) closeAll();
    });
  });

});
