from PyPDF2 import PdfFileWriter, PdfFileReader


def combine_pdfs(pages, output_filename):
    pdf_writer = PdfFileWriter()
    for idx, pdf_file in enumerate(pages):
        with open(pdf_file, 'rb') as pdf:
            pdf_reader = PdfFileReader(pdf)
            start_page, end_page = (0, pdf_reader.getNumPages())

            for page_num in range(start_page, end_page):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

    output_pdf = "combined.pdf"
    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)
