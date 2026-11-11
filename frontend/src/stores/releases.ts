import{reactive}from 'vue';import{listReleases}from '../api/releases';import type{Release}from '../types/domain';
export const releaseStore=reactive({items:[]as Release[]});export async function loadReleases(){releaseStore.items=await listReleases();}
