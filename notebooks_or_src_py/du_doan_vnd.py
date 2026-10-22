"""Suy luận CSV/JSON bằng model gốc; điền defaults đúng như service hiện có.

python notebooks_or_src_py/du_doan_vnd.py dau_vao.csv --output du_doan.csv
JSON nhận một object hoặc danh sách object, không cần đủ mọi cột.
"""
import argparse
import json
from pathlib import Path
import joblib
import pandas as pd
from tien_te import sang_vnd

ROOT=Path(__file__).resolve().parents[1]


def predict_file(input_path, output_path):
    source=Path(input_path);target=Path(output_path)
    if source.resolve()==target.resolve():raise ValueError('Tệp đầu ra phải khác tệp đầu vào.')
    if source.suffix.lower()=='.csv':records=pd.read_csv(source).to_dict(orient='records')
    elif source.suffix.lower()=='.json':
        records=json.loads(source.read_text(encoding='utf-8-sig'))
        if isinstance(records,dict):records=[records]
    else:raise ValueError('Chỉ nhận .csv hoặc .json.')
    if not isinstance(records,list) or not records or not all(isinstance(r,dict) for r in records):
        raise ValueError('Cần ít nhất một bản ghi object.')
    defaults=json.loads((ROOT/'models/feature_defaults.json').read_text(encoding='utf-8'))
    rows=[]
    for record in records:
        full=dict(defaults)
        full.update({k:v for k,v in record.items() if k in full})
        rows.append(full)
    model=joblib.load(ROOT/'models/best_model.pkl')
    prediction=model.predict(pd.DataFrame(rows))
    out=pd.DataFrame({'Du_doan_USD_goc':prediction.astype(float),'Du_doan_VND':sang_vnd(prediction.astype(float)),
                      'Du_doan_trieu_VND':sang_vnd(prediction.astype(float))/1_000_000})
    target.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(target,index=False,encoding='utf-8-sig')
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='CSV/JSON chứa các cột đặc trưng có trong defaults')
    parser.add_argument('--output',default=str(ROOT/'results/chuan_hoa/du_doan_VND.csv'))
    args=parser.parse_args()
    print(predict_file(args.input,args.output).to_string(index=False))


if __name__=='__main__':main()
