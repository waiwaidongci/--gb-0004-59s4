import{reactive}from 'vue';import{listSeries,listObservations}from '../api/series';import type{Series,Observation}from '../types/domain';
export const seriesStore=reactive({items:[]as Series[],observations:[]as Observation[]});
export async function loadSeries(){seriesStore.items=await listSeries();}
export async function loadObservations(id:number){seriesStore.observations=await listObservations(id);}
