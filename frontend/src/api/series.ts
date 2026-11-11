import {request} from './client';import type{Series,Observation}from '../types/domain';
export const listSeries=()=>request<Series[]>('/series');
export const listObservations=(id:number)=>request<Observation[]>(`/series/${id}/observations`);
export const createSeries=(data:unknown)=>request<Series>('/series',{method:'POST',body:JSON.stringify(data)});
export const addObservation=(id:number,data:unknown)=>request<Observation>(`/series/${id}/observations`,{method:'POST',body:JSON.stringify(data)});
