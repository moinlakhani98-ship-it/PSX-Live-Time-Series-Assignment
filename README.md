# PSX Stocks Dashboard — Streamlit Community Cloud Deploy

Yeh files Streamlit Community Cloud (free, official) ke liye ready hain.
Koi extra config nahi chahiye — bas GitHub par push karke platform par
connect karna hai.

## Deploy Steps

1. **GitHub repo banayein**
   Is folder ki 3 files (`app.py`, `requirements.txt`, `runtime.txt`) ko
   ek naye GitHub repo mein push karein. Repo public ya private dono
   chalega (private ke liye GitHub permission deni hogi).

2. **share.streamlit.io par jayein**
   "Continue with GitHub" se login karein — pehli baar apne repos ki
   access deni hogi.

3. **"Create app" dabayein**
   - Repository: apna repo select karein
   - Branch: `main`
   - Main file path: `app.py`

4. **Deploy dabayein**
   Pehli baar dependencies install hone mein 2-5 minute lagenge
   (`psxdata`, `plotly`, `pandas`, waghera).

5. **Live URL mil jayega**
   Kuch aisa: `https://your-app-name.streamlit.app`

## Zaroori Notes

- **Python version**: `runtime.txt` mein `3.11` pin kiya hai, kyunki
  `psxdata` library ko Python 3.11+ chahiye. Isko delete na karein.
- **Sleep mode**: Free tier par app inactivity ke baad "sleep" ho jata
  hai — agli visit par wake hone mein thoda time (~30 sec) lagega.
- **App settings**: Deploy hone ke baad, agar app crash ho ya error aaye,
  Streamlit Cloud dashboard mein "Manage app" → "Logs" se turant pata
  chal jayega ke kya masla hai.

## Files
- `app.py` — Streamlit dashboard (original code)
- `requirements.txt` — Python dependencies
- `runtime.txt` — Python version pin (3.11, psxdata ki requirement)
