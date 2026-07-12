import pypdf
src = r"C:\Users\Admin\.claude\projects\D--Master-Thesis\742d2b06-429d-4330-877c-51bbee0a5b3f\tool-results\webfetch-1783077723585-q0rmpt.pdf"
r = pypdf.PdfReader(src)
print("pages:", len(r.pages))
out = r"D:\Master\Thesis\_tmp_acl2023_report.txt"
with open(out, "w", encoding="utf-8") as f:
    for i, p in enumerate(r.pages):
        f.write(f"\n===== PAGE {i+1} =====\n")
        f.write(p.extract_text() or "")
print("done")
