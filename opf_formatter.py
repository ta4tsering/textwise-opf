import os
import uuid
import yaml
import re
import uuid
import logging
from pathlib import Path
from openpecha.formatters import HFMLFormatter


def create_openpecha(hfml_path, pecha_name, opfs_path, pecha_id):
    hfml_text = f"{hfml_path}/{pecha_name}/"
    formatter = HFMLFormatter(output_path=opfs_path)
    formatter.create_opf(hfml_text, pecha_id)

if __name__ == "__main__":
   create_openpecha(hfml_path, pecha_name, opfs_path, pecha_id)