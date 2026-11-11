import{reactive}from 'vue';import{listRuns,getRun}from '../api/runs';import type{Run}from '../types/domain';
export const runStore=reactive({items:[]as Run[],selected:null as Run|null});
export async function loadRuns(){runStore.items=await listRuns();}
export async function loadRun(id:number){runStore.selected=await getRun(id);}
