import io,csv
from fastapi import HTTPException
from .run_service import detail

def export_csv(db,run_id):
    run=detail(db,run_id)
    if run['status']!='completed': raise HTTPException(409,'预测尚未完成')
    stream=io.StringIO(); stream.write('\ufeff')
    writer=csv.writer(stream)
    writer.writerow(['序列','日期','点预测','经验下界','经验上界','模型','口径说明'])
    for p in run['points']:
        writer.writerow([run['series']['name'],p['day'],p['predicted'],p['lower'],p['upper'],run['result']['selected']['model'],run['result']['interval_note']])
    return stream.getvalue()
