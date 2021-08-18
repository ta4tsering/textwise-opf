from pathlib import Path
import yaml


def get_meta_data():
    meta_yml = Path(f"./sample/1123232422/1123232422.opf/meta.yml").read_text(encoding='utf-8')
    meta_data = yaml.safe_load(meta_yml)
    return meta_data

def add_original_meta(text_id, file_infos, pedurma_type):
    original_meta_data = get_meta_data()
    pecha_id = file_infos[text_id]['uid']
    original_meta_data['id'] = f"{pecha_id}"
    curr_pecha_meta_yml  = Path(f"./opfs/derge_google_pedurma/{pecha_id}/{pecha_id}.opf/meta.yml").read_text(encoding='utf-8')
    curr_pecha_meta_data = yaml.safe_load(curr_pecha_meta_yml)
    del original_meta_data['vol2fn']
    original_meta_data['vol2fn'] = curr_pecha_meta_data['vol2fn']
    original_meta_yml = yaml.safe_dump(original_meta_data)
    Path(f"./opfs/{pedurma_type}/{pecha_id}/{pecha_id}.opf/meta.yml").write_text(original_meta_yml, encoding='utf-8')
    
if __name__=='__main__':
    add_original_meta(text_id, file_infos, pedurma_type)
        
