# import os
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# from io import BytesIO
# from PIL import Image, ImageChops

# # Fungsi untuk crop otomatis background putih
# def trim(im):
#     bg = Image.new(im.mode, im.size, (255, 255, 255))
#     diff = ImageChops.difference(im, bg)
#     bbox = diff.getbbox()
#     if bbox:
#         return im.crop(bbox)
#     return im

# # Baca file CSV
# df = pd.read_csv("data.csv")

# st.title("🔍 Cari BPKB Kendaraan")

# # Input pencarian
# search_input = st.text_input("Masukkan Nomor TNKB / Mesin / Rangka:")

# if search_input:
#     # Filter data
#     data = df[
#         df["NOMOR MESIN"].astype(str).str.contains(search_input, case=False, na=False) |
#         df["NOMOR RANGKA"].astype(str).str.contains(search_input, case=False, na=False) |
#         df["NO. TNKB"].astype(str).str.contains(search_input, case=False, na=False)
#     ]

#     if not data.empty:
#         st.success(f"Ditemukan {len(data)} data")
#         st.dataframe(data)

#         # --- Persiapan untuk menampilkan gambar dalam tabel ---
#         img_col_name = "GAMBAR"
#         has_img_col = img_col_name in data.columns

#         if has_img_col:
#             img_paths = data[img_col_name].astype(str).fillna("").tolist()
#             display_df = data.copy()
#             display_df[img_col_name] = ""  # kosongkan path supaya hanya thumbnail yang tampil
#         else:
#             display_df = data.copy()

#         # --- Buat figure dan table ---
#         fig, ax = plt.subplots(figsize=(14, len(display_df) * 0.8 + 2))
#         ax.axis("off")

#         table = ax.table(
#             cellText=display_df.values.tolist(),
#             colLabels=display_df.columns.tolist(),
#             cellLoc="center",
#             loc="center"
#         )

#         # Atur font & ukuran
#         table.auto_set_font_size(False)
#         table.set_fontsize(10)
#         table.scale(1.2, 1.3)

#         # Styling header & isi tabel
#         for (row, col), cell in table.get_celld().items():
#             if row == 0:  # header
#                 cell.set_text_props(weight="bold", color="white")
#                 cell.set_facecolor("#2f6fb2")
#             else:
#                 cell.set_facecolor("#ffffff")
#                 cell.set_edgecolor("black")

#         # --- Atur lebar kolom tertentu ---
#         col_widths = {
#             "NO": 0.03,
#             # "NO. MESIN": 0.03,          # kecil
#             "KETERANGAN": 0.4    # lebih besar
#         }
#         cols = display_df.columns.tolist()
#         for cname, w in col_widths.items():
#             if cname in cols:
#                 idx = cols.index(cname)
#                 for r in range(len(display_df) + 1):
#                     try:
#                         table[(r, idx)].set_width(w)
#                     except Exception:
#                         pass

#         # Pastikan layout rapat
#         plt.tight_layout(pad=0)
#         plt.subplots_adjust(top=1, bottom=0, left=0, right=1)
#         plt.draw()
#         renderer = fig.canvas.get_renderer()

#         # --- Tambahkan gambar (jika ada kolom GAMBAR) ---
#         if has_img_col:
#             img_col_idx = cols.index(img_col_name)
#             for row_idx in range(len(display_df)):
#                 cell = table.get_celld().get((row_idx + 1, img_col_idx))
#                 if cell is None:
#                     continue
#                 bbox = cell.get_window_extent(renderer)
#                 fig_bbox = fig.transFigure.inverted().transform_bbox(bbox)
#                 ax_img = fig.add_axes([fig_bbox.x0, fig_bbox.y0, fig_bbox.width, fig_bbox.height])
#                 ax_img.axis("off")

#                 img_path = img_paths[row_idx]
#                 if isinstance(img_path, str) and img_path.strip() and os.path.exists(img_path):
#                     try:
#                         img = Image.open(img_path)
#                         ax_img.imshow(img)
#                     except Exception:
#                         ax_img.text(0.5, 0.5, "Gagal\ngambar", ha="center", va="center", fontsize=8)
#                 else:
#                     ax_img.text(0.5, 0.5, "No Image", ha="center", va="center", fontsize=8)

#         # --- Simpan ke buffer ---
#         buf = BytesIO()
#         fig.savefig(buf, format="png", dpi=250, bbox_inches="tight", pad_inches=0)
#         buf.seek(0)

#         # --- Crop otomatis hapus space putih ---
#         img = Image.open(buf).convert("RGB")
#         img_cropped = trim(img)

#         buf2 = BytesIO()
#         img_cropped.save(buf2, format="PNG", dpi=(250, 250))
#         buf2.seek(0)
#         img_bytes = buf2.getvalue()

#         # Tampilkan di Streamlit
#         st.image(img_bytes, caption="Hasil Pencarian", use_container_width=True)

#         # Tombol download
#         st.download_button(
#             label="Download Gambar",
#             data=img_bytes,
#             file_name="data_bpkb.png",
#             mime="image/png"
#         )
#     else:
#         st.warning("Tidak ada data yang cocok dengan pencarian")



# =================================================

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image, ImageChops

# Fungsi untuk crop otomatis background putih
def trim(im):
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

# Atur tampilan halaman
st.set_page_config(
    page_title="Cari BPKB",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS untuk ubah warna tombol download
st.markdown(
    """
    <style>
    div.stDownloadButton > button {
        background-color: #0c9507ff;  /* biru gelap */
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 16px;
        border: none;
    }
    div.stDownloadButton > button:hover {
        background-color: #054b02ff;  /* biru lebih gelap saat hover */
        color: white;
    }
    </style>
    <style>
        .main {
        padding-bottom: 50px; /* ruang supaya tidak ketiban footer */
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #2f6fb2;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 13px;
        border-top: 1px solid #1e4d80;
        z-index: 1000;
    }
    </style>
    <div class="footer">
        Powered by © SkinnyXypz
    </div>
    </style>
    """,
    unsafe_allow_html=True
)

# Baca file CSV
df = pd.read_csv("data.csv")

st.title("Cari BPKB 🔎")

# Input pencarian
search_input = st.text_input("Masukkan Nomor TNKB / Mesin / Rangka:")

if search_input:
    # Filter data
    data = df[
        df["NOMOR MESIN"].astype(str).str.contains(search_input, case=False, na=False) |
        df["NOMOR RANGKA"].astype(str).str.contains(search_input, case=False, na=False) |
        df["NO. TNKB"].astype(str).str.contains(search_input, case=False, na=False)
    ]

    if not data.empty:
        st.success(f"Ditemukan {len(data)} data")
        st.dataframe(data)

        # --- Persiapan untuk menampilkan gambar dalam tabel ---
        img_col_name = "GAMBAR"
        has_img_col = img_col_name in data.columns

        if has_img_col:
            img_paths = data[img_col_name].astype(str).fillna("").tolist()
            display_df = data.copy()
            display_df[img_col_name] = ""  # kosongkan path supaya hanya thumbnail yang tampil
        else:
            display_df = data.copy()

        # --- Buat figure dan table ---
        fig, ax = plt.subplots(figsize=(14, len(display_df) * 0.8 + 2))
        ax.axis("off")

        table = ax.table(
            cellText=display_df.values.tolist(),
            colLabels=display_df.columns.tolist(),
            cellLoc="center",
            loc="center"
        )

        # Atur font & ukuran
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.3)

        # Styling header & isi tabel
        for (row, col), cell in table.get_celld().items():
            if row == 0:  # header
                cell.set_text_props(weight="bold", color="white")
                cell.set_facecolor("#2f6fb2")
            else:
                cell.set_facecolor("#ffffff")
                cell.set_edgecolor("black")

        # --- Atur lebar kolom tertentu ---
        col_widths = {
            "NO": 0.03,          # kecil
            "KETERANGAN": 0.4    # lebih besar
        }
        cols = display_df.columns.tolist()
        for cname, w in col_widths.items():
            if cname in cols:
                idx = cols.index(cname)
                for r in range(len(display_df) + 1):
                    try:
                        table[(r, idx)].set_width(w)
                    except Exception:
                        pass

        # Pastikan layout rapat
        plt.tight_layout(pad=0)
        plt.subplots_adjust(top=1, bottom=0, left=0, right=1)
        plt.draw()
        renderer = fig.canvas.get_renderer()

        # --- Tambahkan gambar (jika ada kolom GAMBAR) ---
        if has_img_col:
            img_col_idx = cols.index(img_col_name)
            for row_idx in range(len(display_df)):
                cell = table.get_celld().get((row_idx + 1, img_col_idx))
                if cell is None:
                    continue
                bbox = cell.get_window_extent(renderer)
                fig_bbox = fig.transFigure.inverted().transform_bbox(bbox)
                ax_img = fig.add_axes([fig_bbox.x0, fig_bbox.y0, fig_bbox.width, fig_bbox.height])
                ax_img.axis("off")

                img_path = img_paths[row_idx]
                if isinstance(img_path, str) and img_path.strip() and os.path.exists(img_path):
                    try:
                        img = Image.open(img_path)
                        ax_img.imshow(img)
                    except Exception:
                        ax_img.text(0.5, 0.5, "Gagal\ngambar", ha="center", va="center", fontsize=8)
                else:
                    ax_img.text(0.5, 0.5, "No Image", ha="center", va="center", fontsize=8)

        # --- Simpan ke buffer ---
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=250, bbox_inches="tight", pad_inches=0)
        buf.seek(0)

        # --- Crop otomatis hapus space putih ---
        img = Image.open(buf).convert("RGB")
        img_cropped = trim(img)

        buf2 = BytesIO()
        img_cropped.save(buf2, format="PNG", dpi=(250, 250))
        buf2.seek(0)
        img_bytes = buf2.getvalue()

        # Tampilkan di Streamlit
        st.image(img_bytes, caption="Hasil Pencarian", use_container_width=True)

        # Tombol download (warna sudah diubah lewat CSS di atas)
        st.download_button(
            label="Download Gambar",
            data=img_bytes,
            file_name="hasil_pencarian.png",
            mime="image/png"
        )
    else:
        st.warning("Tidak ada data yang cocok dengan pencarian")
