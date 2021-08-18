
import yaml
import os
from pathlib import Path

def from_yaml(yml_path):
    return yaml.load(yml_path.read_text(encoding="utf-8"), Loader=yaml.CLoader)

def to_yaml(dict_):
    return yaml.dump(dict_, sort_keys=False, allow_unicode=True, Dumper=yaml.CDumper)

def parse_nam_pg(pg_ann):
    return pg_ann['note_ref'], pg_ann['page_index']

def get_note_ref_id(note_ref_idx, dg_pagination):
    for uuid, pg_ann in dg_pagination['annotations'].items():
        if pg_ann['page_index'] == note_ref_idx:
            return uuid
    return ''

def transfer_note_ref(dg_pagination, note_ref_idx, pg_idx):
    for uuid, pg_ann in dg_pagination['annotations'].items():
        note_ref_id = get_note_ref_id(note_ref_idx, dg_pagination)
        if pg_ann['page_index'] == pg_idx:
            dg_pagination['annotations'][uuid]['note_ref'] = note_ref_id
            return dg_pagination
    return dg_pagination

def update_note_ref(nam_pagination, dg_pagination):
    for uuid, pg_ann in nam_pagination['annotations'].items():
        if pg_ann.get('note_ref', ''):
            note_ref_id, pg_idx = parse_nam_pg(pg_ann)
            note_ref_idx = nam_pagination['annotations'][note_ref_id]['page_index']
            dg_pagination = transfer_note_ref(dg_pagination, note_ref_idx, pg_idx)
    return dg_pagination

def transfer_text_note_ref(pecha_id, vol_num):
    text_pg_layer = from_yaml(Path(f'./opfs/namsel_pedurma/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    src_pagination = from_yaml(Path(f'./opfs/P000792/P000792.opf/layers/v{int(vol_num):03}/Pagination.yml'))
    new_text_pg_layer = update_note_ref(src_pagination, text_pg_layer)
    new_text_pg_layer = to_yaml(new_text_pg_layer)
    return new_text_pg_layer

def change_vol_num(pecha_id, vol):
    source = f"./opfs/namsel_pedurma/{pecha_id}/{pecha_id}.opf/layers/v001"
    dest = f"./opfs/namsel_pedurma/{pecha_id}/{pecha_id}.opf/layers/v{vol:03}"
    os.rename(source, dest)
    print(f"volumes changed from v001 to v{vol:03}")

def transfer_ref(text_id, file_infos, vol_info, opfs_path):
    pecha_id = file_infos[text_id]['uid']
    vol_num = vol_info[text_id]['vol'][1:]
    change_vol_num(pecha_id, int(vol_num))
    new_text_pg_layer = transfer_text_note_ref(pecha_id, vol_num)
    Path(f"{opfs_path}/{pecha_id}/{pecha_id}.opf/layers/v{int(vol_num):03}/Pagination.yml").write_text(new_text_pg_layer, encoding='utf-8')

if __name__ == "__main__":
    transfer_ref(text_id, file_infos, vol_info, opfs_path)
   
