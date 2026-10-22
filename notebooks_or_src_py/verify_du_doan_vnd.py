"""So sánh API mới với service .bak, CLI CSV/JSON với model gốc."""
import json
from pathlib import Path
import runpy
import sys
import tempfile
from datetime import datetime, timezone
import joblib
import numpy as np
import pandas as pd
from du_doan_vnd import predict_file
from tien_te import TY_GIA_USD_VND, sang_vnd, dinh_dang_vnd, dinh_dang_trieu, dinh_dang_ty, ghi_chu_quy_doi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/chuan_hoa'


def main():
    checks=[]
    def check(name,ok,detail):checks.append(('PASS' if bool(ok) else 'FAIL',name,str(detail)))
    old=runpy.run_path(str(ROOT/'service/predict_service.py.bak'))['app'].test_client()
    new=runpy.run_path(str(ROOT/'service/predict_service.py'))['app'].test_client()
    cases=[{}, {'LotArea':8500,'GrLivArea':1500,'OverallQual':6,'YearBuilt':2005,'Neighborhood':'CollgCr','GarageType':'Attchd'}, {'Id':1},{'Id':1460},{'not_a_feature':123},{'GrLivArea':'abc'}]
    for index,record in enumerate(cases,1):
        a=old.post('/predict',json=record);b=new.post('/predict',json=record);ar=a.get_json();br=b.get_json()
        check(f'API {index} giữ nguyên kết quả cũ',a.status_code==b.status_code and all(br.get(k)==v for k,v in ar.items()),f'HTTP cũ/mới={a.status_code}/{b.status_code}; USD cũ={ar.get("predicted_price")}; USD mới={br.get("predicted_price")}')
        if a.status_code==200:
            check(f'API {index} trường tiền mới',br['usd_to_vnd']==TY_GIA_USD_VND and round(br['predicted_price_usd'],2)==br['predicted_price'] and br['predicted_price_vnd']==sang_vnd(br['predicted_price_usd']),f'USD đầy đủ={br["predicted_price_usd"]}; VND={br["predicted_price_vnd"]}; rate={br["usd_to_vnd"]}')
    defaults=json.loads((ROOT/'models/feature_defaults.json').read_text())
    model=joblib.load(ROOT/'models/best_model.pkl')
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp)
        records=[{},cases[1],{'not_a_feature':123},{'Id':1}]
        file=temp/'input.json';file.write_text(json.dumps(records));cli=predict_file(file,temp/'out.csv')
        direct=[]
        for record in records:
            row=dict(defaults);row.update({k:v for k,v in record.items() if k in row});direct.append(row)
        expected=np.asarray(model.predict(pd.DataFrame(direct)),float)
        check('CLI JSON thiếu cột và cột lạ',np.array_equal(cli.Du_doan_USD_goc,expected) and np.array_equal(cli.Du_doan_VND,sang_vnd(expected)),f'n={len(records)}; max USD delta={float(np.max(abs(cli.Du_doan_USD_goc-expected)))}')
        source=pd.read_csv(ROOT/'data/train.csv');idx=json.loads((OUT/'so_lieu_goc_va_doi_chieu.json').read_text())['_meta']['test_indices'];frame=source.loc[idx].drop(columns='SalePrice')
        frame.to_csv(temp/'test.csv',index=False);cli=predict_file(temp/'test.csv',temp/'out.csv');expected=np.asarray(model.predict(frame),float)
        check('CLI CSV toàn bộ TEST so với artifact gốc',len(cli)==len(frame) and np.array_equal(cli.Du_doan_USD_goc,expected) and np.array_equal(cli.Du_doan_VND,sang_vnd(expected)),f'n={len(frame)}; max USD delta={float(np.max(abs(cli.Du_doan_USD_goc-expected)))}')
        no_overwrite=False
        try:predict_file(file,file)
        except ValueError:no_overwrite=True
        check('CLI không ghi đè file input',no_overwrite,'Từ chối output trùng input')
    for name in ['service/predict_service.py','public/index.html']:
        current=(ROOT/name).read_text().splitlines();original=(ROOT/(name+'.bak')).read_text().splitlines();pos=0;ok=True
        for line in original:
            while pos<len(current) and current[pos]!=line:pos+=1
            if pos==len(current):ok=False;break
            pos+=1
        check('Chỉ thêm dòng '+name,ok,f'{len(original)} dòng gốc giữ nguyên thứ tự trong {len(current)} dòng mới')
    check('Định dạng VND nguyên đồng',dinh_dang_vnd(sang_vnd(1))=='25.000 ₫',dinh_dang_vnd(sang_vnd(1)))
    check('Định dạng triệu và tỷ',dinh_dang_trieu(7_800_000)=='7,8 triệu ₫' and dinh_dang_ty(3_690_000_000)=='3,69 tỷ ₫',dinh_dang_trieu(7_800_000)+'; '+dinh_dang_ty(3_690_000_000))
    n=sum(s=='PASS' for s,_,_ in checks);f=len(checks)-n
    text=f'# Kiểm chứng dự đoán VND so với bản gốc\n\n{ghi_chu_quy_doi()}\n\nUTC: {datetime.now(timezone.utc).isoformat()}\n\n{n} PASS; {f} FAIL.\n\n'
    text+='\n'.join(f'- {status} — {name}: {detail}' for status,name,detail in checks)+'\n'
    (OUT/'KIEM_CHUNG_DU_DOAN.md').write_text(text,encoding='utf-8')
    print(f'{n} PASS; {f} FAIL')
    for status,name,detail in checks:
        if status=='FAIL':print(f'{status}: {name}: {detail}')
    return 1 if f else 0


if __name__=='__main__':sys.exit(main())
