import {request,download}from './client';import type{Run}from '../types/domain';
export const listRuns=()=>request<Run[]>('/runs');export const getRun=(id:number)=>request<Run>(`/runs/${id}`);
export const createRun=(data:unknown)=>request<Run>('/runs',{method:'POST',body:JSON.stringify(data)});
export const exportRun=(id:number)=>download(`/runs/${id}/export`,`tide-forecast-${id}.csv`);
