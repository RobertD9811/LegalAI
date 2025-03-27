import streamlit as st
import pytesseract
import fitz  # PyMuPDF pentru PDF
from PIL import Image
import re
from docx import Document
import os
import language_tool_python

# Inițializare corector gramatical
tool = language_tool_python.LanguageTool('ro')

# Setare Tesseract OCR (dacă rulezi local, schimbă calea)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_pdf(pdf_file):
    """Extrage text dintr-un fișier PDF."""
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_text_from_docx(docx_file):
    """Extrage text dintr-un fișier Word (DOCX)."""
    doc = Document(docx_file)
    return "\n".join([p.text for p in doc.paragraphs])

def identify_variable_fields(text_samples):
    """Identifică câmpurile fixe și variabile din modelele de cereri."""
    common_words = set(text_samples[0].split())
    for text in text_samples[1:]:
        common_words.intersection_update(text.split())
    return common_words

def extract_data(text, fixed_fields):
    """Extrage datele variabile dintr-un document comparativ cu câmpurile fixe."""
    words = text.split()
    variable_data = [word for word in words if word not in fixed_fields]
    return variable_data

def correct_grammar(text):
    """Corectează greșelile gramaticale folosind LanguageTool."""
    return tool.correct(text)

def generate_word_doc(variable_data, fixed_text, output_name):
    """Generează un fișier
