from pathlib import Path
from openpecha import github_utils as gu


if __name__=="__main__":
    pecha_path = Path(f"./test/opfs/namsel_pedurma/4e3c12ff85b6429dbd0d3e05949d4165")
    gu.github_publish(
        pecha_path,
        message="initial commit",
        not_includes=[],
        layers=[],
        org="OpenPecha",
        token="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"
    )
    print(f"done with the release")




    # "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"