"""Deterministic one-step rolling validation; each fit sees only earlier observations."""
import math
from statistics import mean

def quantile(values,p):
    values=sorted(values)
    pos=(len(values)-1)*p
    lo=int(pos); hi=min(lo+1,len(values)-1)
    return values[lo]+(values[hi]-values[lo])*(pos-lo)

def predict(history,model,season,alpha=.5):
    if model=='seasonal_naive': return history[-season]
    level=history[0]
    for value in history[1:]: level=alpha*value+(1-alpha)*level
    return level

def forecast(values,horizon,season):
    if not 1<=horizon<=30 or not 2<=season<=30: raise ValueError('预测期1–30天，季节周期2–30天')
    if len(values)<max(42,season*3): raise ValueError('观测不足：至少42天且不少于3个季节周期')
    if any(not math.isfinite(x) or x<0 for x in values): raise ValueError('需求必须为非负有限数')
    holdout=min(28,len(values)//3)
    start=len(values)-holdout
    candidates=[('seasonal_naive',None),('exponential_smoothing',.2),('exponential_smoothing',.5),('exponential_smoothing',.8)]
    comparisons=[]
    residual_sets=[]
    for model,alpha in candidates:
        predictions=[predict(values[:i],model,season,alpha) for i in range(start,len(values))]
        residuals=[y-p for y,p in zip(values[start:],predictions)]
        mae=mean(abs(e) for e in residuals)
        denom=sum(values[start:])
        comparisons.append({'model':model,'alpha':alpha,'mae':round(mae,4),'wape':round(sum(abs(e) for e in residuals)/denom,6) if denom else None})
        residual_sets.append(residuals)
    best=min(range(len(comparisons)),key=lambda i:comparisons[i]['mae'])
    selected=comparisons[best]
    residuals=residual_sets[best]
    low,high=quantile(residuals,.1),quantile(residuals,.9)
    history=list(values)
    points=[]
    for _ in range(horizon):
        point=predict(history,selected['model'],season,selected['alpha'])
        history.append(point)
        points.append({'predicted':round(point,2),'lower':round(max(0,point+low),2),'upper':round(max(0,point+high),2)})
    return {'selected':selected,'comparisons':comparisons,'validation_days':holdout,'training_days':len(values),'interval_note':'滚动回测残差的10%/90%经验分位带；未来覆盖率没有保证，未建模节假日冲击。','points':points,'checksum':round(sum(values),4)}
