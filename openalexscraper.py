import requests
import os
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

# === CONFIG ===
OUTPUT_DIR = "openalex_papers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_URL = "https://api.openalex.org/works"
QUERY = "title_and_abstract.search:gold+forecast,primary_topic.id:t11326,open_access.is_oa:true"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


# === FUNCTION: DOWNLOAD FILE ===
def save_pdf(pdf_url, title):
    """Descarga un PDF directo"""
    title_clean = re.sub(r'[\\/*?:"<>|]', "_", title)[:100]
    pdf_path = os.path.join(OUTPUT_DIR, f"{title_clean}.pdf")

    if os.path.exists(pdf_path):
        print(f"⏩ Ya descargado: {title_clean}")
        return True

    try:
        with requests.get(pdf_url, stream=True, headers=HEADERS, timeout=30) as r:
            if r.status_code == 200 and "pdf" in r.headers.get("Content-Type", "").lower():
                total = int(r.headers.get("content-length", 0))
                with open(pdf_path, "wb") as f, tqdm(
                    desc=title_clean[:80],
                    total=total,
                    unit="iB",
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            bar.update(len(chunk))
                print(f"✅ Guardado: {pdf_path}")
                return True
            else:
                print(f"⚠️ El link no apunta a PDF directo: {pdf_url}")
                return False
    except Exception as e:
        print(f"❌ Error en descarga {pdf_url}: {e}")
        return False


# === FUNCTION: HANDLE HTML LANDING PAGE ===
def extract_pdf_from_html(url, title):
    """Intenta encontrar un enlace .pdf dentro de una página HTML"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if "pdf" in resp.headers.get("Content-Type", "").lower():
            return save_pdf(url, title)

        soup = BeautifulSoup(resp.text, "html.parser")
        pdf_links = [a.get("href") for a in soup.find_all("a", href=True) if ".pdf" in a["href"].lower()]
        if pdf_links:
            pdf_link = pdf_links[0]
            if pdf_link.startswith("/"):
                # convertir a URL completa si es relativa
                base = "/".join(url.split("/")[:3])
                pdf_link = base + pdf_link
            print(f"🔗 PDF encontrado en página: {pdf_link}")
            return save_pdf(pdf_link, title)
        else:
            print(f"❌ No se encontró PDF en página: {url}")
            return False
    except Exception as e:
        print(f"❌ Error procesando página {url}: {e}")
        return False


# === MAIN LOOP ===
for page in range(1, 11):  # páginas 1–10
    print(f"\n🔎 Página {page}")
    url = f"{BASE_URL}?page={page}&filter={QUERY}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print(f"❌ Error al obtener página {page}: {r.status_code}")
        continue

    data = r.json()
    for item in data.get("results", []):
        title = item.get("title", "sin_titulo")
        oa = item.get("open_access", {})
        pdf_url = oa.get("oa_url")

        if not pdf_url:
            print(f"⚠️ Sin link OA para: {title[:80]}")
            continue

        print(f"⬇️ Intentando descargar: {title[:80]}")

        # 1️⃣ Primero intenta descarga directa
        success = save_pdf(pdf_url, title)
        if success:
            continue

        # 2️⃣ Si no es PDF directo, abre la página y busca un enlace PDF interno
        extract_pdf_from_html(pdf_url, title)
