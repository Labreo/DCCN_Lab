#!/usr/bin/env python3
"""
Master Orchestration Script to build:
1. Individual .docx documents for Experiments 10, 11, 12, 13, 14, 15
2. Master unified .docx document containing Experiments 10 to 15 in continuous sequence
3. Copy all files to /Users/sanjaywaradkar/Downloads/
"""

import os
import shutil
import docx
from builder_helpers import setup_header_footer
from build_exp10 import build_exp10_content
from build_exp11 import build_exp11_content
from build_exp12 import build_exp12_content
from build_exp13 import build_exp13_content
from build_exp14 import build_exp14_content
from build_exp15 import build_exp15_content

WORKSPACE_DIR = "/Users/sanjaywaradkar/DCCN_Lab"
DOWNLOADS_DIR = "/Users/sanjaywaradkar/Downloads"

EXPERIMENTS = [
    ("10", "Kanak_DCCN_EXPT_10.docx", "exp10", build_exp10_content, 95),
    ("11", "Kanak_DCCN_EXPT_11.docx", "exp11", build_exp11_content, 100),
    ("12", "Kanak_DCCN_EXPT_12.docx", "exp12", build_exp12_content, 106),
    ("13", "Kanak_DCCN_EXPT_13.docx", "exp13", build_exp13_content, 112),
    ("14", "Kanak_DCCN_EXPT_14.docx", "exp14", build_exp14_content, 118),
    ("15", "Kanak_DCCN_EXPT_15.docx", "exp15", build_exp15_content, 124),
]

def generate_individual_documents():
    print("Generating individual documents...")
    for exp_num, filename, folder, builder_func, start_page in EXPERIMENTS:
        doc = docx.Document()
        setup_header_footer(doc.sections[0], start_page=start_page)
        builder_func(doc)
        
        target_path = os.path.join(WORKSPACE_DIR, folder, filename)
        doc.save(target_path)
        print(f"  [SAVED] {target_path} (Starting page: {start_page})")
        
        # Copy to Downloads
        dl_path = os.path.join(DOWNLOADS_DIR, filename)
        shutil.copy2(target_path, dl_path)
        print(f"  [COPIED] {dl_path}")

def generate_master_document():
    print("\nGenerating master unified document (Exp 10 to 15)...")
    master_doc = docx.Document()
    setup_header_footer(master_doc.sections[0], start_page=95)
    
    for i, (exp_num, filename, folder, builder_func, _) in enumerate(EXPERIMENTS):
        if i > 0:
            master_doc.add_page_break()
        print(f"  Adding Experiment {exp_num} to master document...")
        builder_func(master_doc)
        
    master_path = os.path.join(WORKSPACE_DIR, "Kanak_DCCN_EXPT_10_to_15.docx")
    master_doc.save(master_path)
    print(f"  [SAVED MASTER] {master_path}")
    
    master_dl_path = os.path.join(DOWNLOADS_DIR, "Kanak_DCCN_EXPT_10_to_15.docx")
    shutil.copy2(master_path, master_dl_path)
    print(f"  [COPIED MASTER] {master_dl_path}")

if __name__ == "__main__":
    generate_individual_documents()
    generate_master_document()
    print("\nALL LAB EXPERIMENTS GENERATED SUCCESSFULLY!")
