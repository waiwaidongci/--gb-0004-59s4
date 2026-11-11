import{request}from './client';import type{Audit}from '../types/domain';export const listAudits=()=>request<Audit[]>('/audits');
