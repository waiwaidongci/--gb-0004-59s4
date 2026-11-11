import {reactive,computed} from 'vue';import{login}from '../api/auth';import type{User}from '../types/domain';
let saved:User|null=null;try{saved=JSON.parse(localStorage.getItem('tide_user')||'null')}catch{}
export const auth=reactive({user:saved});export const canEdit=computed(()=>auth.user?.role==='admin'||auth.user?.role==='analyst');export const isAdmin=computed(()=>auth.user?.role==='admin');
export async function signIn(email:string,password:string){const data=await login(email,password);localStorage.setItem('tide_token',data.access_token);localStorage.setItem('tide_user',JSON.stringify(data.user));auth.user=data.user;}
export function signOut(){localStorage.removeItem('tide_token');localStorage.removeItem('tide_user');auth.user=null;}
