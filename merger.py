import PyPDF2
import os

# Crear un merger de PyPDF2
merger = PyPDF2.PdfMerger()

# Buscar todos los archivos PDF en el directorio actual
pdfs = sorted([f for f in os.listdir() if f.lower().endswith(".pdf")])

# Agregar cada PDF al merger
for pdf in pdfs:
    print(f"Agregando: {pdf}")
    merger.append(pdf)

# Guardar el PDF combinado
output_name = "merged_books.pdf"
merger.write(output_name)
merger.close()

print(f"\n✅ all  PDFs merged here: {output_name}")
