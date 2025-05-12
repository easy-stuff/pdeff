import io
import zipfile
from PyPDF2 import PdfReader, PdfWriter


def split_pdf(files: list, stepping: int) -> io.BytesIO:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for index, file in enumerate(files):
            # Important: reset file pointer
            file.seek(0)

            try:
                reader = PdfReader(file)
            except Exception as e:
                print(f"Error reading PDF {file.filename}: {e}")
                continue  # Skip unreadable files

            total_pages = len(reader.pages)
            if total_pages == 0:
                print(f"Skipping empty PDF: {file.filename}")
                continue

            base_name = getattr(
                file, 'filename', f'file_{index}').rsplit('.', 1)[0]

            for i in range(0, total_pages, stepping):
                writer = PdfWriter()

                for j in range(i, min(i + stepping, total_pages)):
                    writer.add_page(reader.pages[j])

                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)

                part_name = f"{base_name}_p{i+1}_to_p{min(i+stepping, total_pages)}.pdf"

                # Add to zip
                zip_file.writestr(part_name, output_pdf.read())

    zip_buffer.seek(0)
    return zip_buffer
