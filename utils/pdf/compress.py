import typing as t
import io
import os
import zipfile
import tempfile
import subprocess


def compress_pdf(files: list, compression_level: t.Literal['low', 'medium', 'high']) -> io.BytesIO:
    zip_buffer = io.BytesIO()

    level_to_gs = {
        'low': '/screen',
        'medium': '/ebook',
        'high': '/prepress'
    }

    gs_quality = level_to_gs.get(compression_level, '/ebook')

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file, tempfile.TemporaryDirectory() as tmpdir:
        for index, file in enumerate(files):
            file.seek(0)
            original_path = os.path.join(tmpdir, f"original_{index}.pdf")
            compressed_path = os.path.join(tmpdir, f"compressed_{index}.pdf")

            with open(original_path, 'wb') as f:
                f.write(file.read())

            cmd = [
                'gswin64',
                '-sDEVICE=pdfwrite',
                '-dCompatibilityLevel=1.4',
                f'-dPDFSETTINGS={gs_quality}',
                '-dNOPAUSE',
                '-dQUIET',
                '-dBATCH',
                f'-sOutputFile={compressed_path}',
                original_path
            ]

            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Ghostscript failed on {file.filename}: {e}")
                continue

            with open(compressed_path, 'rb') as f:
                content = f.read()

            base_name = getattr(
                file, 'filename', f'file_{index}').rsplit('.', 1)[0]
            zip_name = f"{base_name}_{compression_level}_compressed.pdf"
            zip_file.writestr(zip_name, content)

            # Optional explicit cleanup
            try:
                os.remove(original_path)
                os.remove(compressed_path)
            except Exception as e:
                print(f"Cleanup failed: {e}")

    zip_buffer.seek(0)
    return zip_buffer
