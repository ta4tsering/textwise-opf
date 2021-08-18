import os
import yaml
import re
import logging
import uuid
from pathlib import Path
from openpecha import github_utils
from note_postprocessing import post_process
from opf_formatter import create_openpecha
from transfer_note_ref import transfer_ref


logging.basicConfig(
    filename="namsel_pedurma_text_id_and_uid_pipe_line.log",
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)

def notifier(msg):
    logging.info(msg)

def get_pecha_name(type_name, file_path):
    curr_file = {}
    file_info = {}
    pecha_names = []
    for file in os.listdir(f"{file_path}"):
        if file.endswith(".txt"):
            file_name = file[:-4]
            pecha_names.append(file_name)
    pecha_names.sort()
    for pecha_name in pecha_names: 
        map = re.match(r"(D[0-9]+[a-z]?)\_(v[0-9]+)", pecha_name)
        text_id = map.group(1)
        vol_num = map.group(2)
        curr_file[text_id] ={
            'vol': vol_num
            }
        file_info.update(curr_file)
        curr_file = {}
    file_info_yml = yaml.safe_dump(file_info, default_flow_style=False, sort_keys=True, allow_unicode=True)
    Path(f"./{type_name}_text_id_and_volnum_pipeline.yml").write_text(file_info_yml, encoding='utf-8')
    return pecha_names

def read_yaml_files(type_name, file_type):
    file_info_yml = Path(f"./{type_name}{file_type}.yml").read_text(encoding='utf-8')
    file_infos = yaml.safe_load(file_info_yml)
    return file_infos


def post_process_and_create_opf(pedurma_type, pecha_names, opfs_path):
    file_info = {}
    curr_file = {}
    for pecha_name in pecha_names:
        post_process(input_path, pecha_name, "dergoogle", hfml_path)
        pecha_id = uuid.uuid4().hex
        create_openpecha(hfml_path, pecha_name, opfs_path)
        map = re.match(r"(D[0-9]+[a-z]?)\_(v[0-9]+)",pecha_name)
        text_id = map.group(1)
        curr_file[text_id] ={'uid': pecha_id}
        file_info.update(curr_file)
        curr_file = {}
        notifier(f"text_id: {text_id}   uid: {pecha_id}")
    file_info_yml = yaml.safe_dump(file_info, default_flow_style=False, sort_keys=True, allow_unicode=True)
    Path(f"./{pedurma_type}_text_and_uid_pipeline.yml").write_text(file_info_yml, encoding='utf-8')

if __name__ =="__main__":
    pedurma_type = "derge_google_pedurma"
    hfml_path = f"./pipeline/post_process/{pedurma_type}"
    input_path = f".//test/hfmls/{pedurma_type}"
    opfs_path = f"./pipeline/opfs/{pedurma_type}"
    pecha_names = get_pecha_name(input_path)
    post_process_and_create_opf(pedurma_type, pecha_names, opfs_path)
    file_infos = read_yaml_files(pedurma_type, "text_id_and_uid")
    vol_info = read_yaml_files(pedurma_type, "text_id_and_volnum")
    for text_id in file_infos:
        transfer_ref(text_id, file_infos, vol_info, opfs_path)
        pecha_id = file_infos[text_id]['uid']
        pecha_path = Path(f"./pipeline/opfs/{pedurma_type}/{pecha_id}")
        github_utils.github_publish(
            pecha_path,
            message="initial commit",
            not_includes=[],
            layers=[],
            org="ta4tsering",
            token="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"
        )
    



