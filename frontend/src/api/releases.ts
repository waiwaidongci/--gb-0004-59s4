import {request}from './client';import type{Release}from '../types/domain';
export const listReleases=()=>request<Release[]>('/releases');export const publish=(run_id:number,note:string)=>request<Release>('/releases',{method:'POST',body:JSON.stringify({run_id,note})});
