# PDeff

> NOTE: This tool is sitll UNDER DEVELOPMENT. Feel free to contribute.

The ultimate no BS PDF tool to get stuff done.

![img](./static/images/logo-text.png)

**A tool to handle common PDF tasks with ease.**

This tool allows you to easily handle common PDF related tasks in an intuitive manner. It works entirely locally, without requiring an internet connection - ensuring your private data stays secure and never leaves your computer or reaches any third-party services.

You will soon be able to run this tool easily using Docker or directly from the source. For development purposes, install the requirements listed in `./requirements.txt` and run `app.py`.

This project was inspired by [ilovepdf.com](https://ilovepdf.com/). However, not all features work exactly the same. Some offer better performance and more customization options, while others may be more limited. Parts of the code were reused from the now-archived [easy-stuff/easy-pdf](https://github.com/easy-stuff/easy-pdf).

**Note:** This tool requires Ghostscript to be installed on your system. Make sure it is added to your system’s PATH.

Currently, this project does not focus on user-friendliness during setup. I’m not skilled at developing proper desktop applications with frameworks like Qt or GTK, and I’ve been too lazy to set up an Electron app. This tool was built in a rather janky way, with the goal of creating a _barely functional_ minimum viable product (MVP) - I don't care as long as its functional. It lacks proper input validation and security measures.

**This tool is NOT meant to be exposed online.** It is intended to be run locally at `127.0.0.1` by default. Do not change it as this is a nightmare from a security prespective.

Features:

- **Merge PDFs** :- Works! Based on PyPdf2
- **Split PDFs** :- Works! Based on PyPdf2
- **Compress PDFs** :- BROKEN! might even increase the file size a little bit. Built using ghostscript.

To-do:

- PDF to Word
- Word to PDF
- PDF to JPG
- JPG to PDF
- Watermark (already done)
- Rotate PDF
- Unlock PDF
- Lock/Protect PDF
- Sort PDF
- PDF to PDF/A ??? (not sure about this)
- OCR PDF
- Make the web libraries work completely offiline
