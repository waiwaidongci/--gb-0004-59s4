export interface User {id:number;name:string;email:string;role:string}
export interface Series {id:number;code:string;name:string;city:string;product:string;unit:string;source_file:string;observation_count:number;total_demand:number}
export interface Observation {id:number;series_id:number;day:string;value:number}
export interface ForecastPoint {day:string;predicted:number;lower:number;upper:number}
export interface Comparison {model:string;alpha:number|null;mae:number;wape:number|null}
export interface Run {id:number;name:string;series_id:number;horizon:number;season:number;status:string;error:string|null;created_at:string;result?:{selected:Comparison;comparisons:Comparison[];validation_days:number;training_days:number;interval_note:string};points?:ForecastPoint[];series?:Series}
export interface Release {id:number;run_id:number;note:string;published_at:string}
export interface Audit {id:number;actor:string;action:string;target:string;created_at:string}
