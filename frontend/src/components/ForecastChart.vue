<script setup lang="ts">
import{computed}from 'vue';import type{ForecastPoint,Observation}from '../types/domain';
const props=defineProps<{points?:ForecastPoint[];observations?:Observation[]}>();
const values=computed(()=>props.observations?.slice(-42).map(x=>({value:x.value,day:x.day}))||props.points?.map(x=>({value:x.predicted,day:x.day}))||[]);
const max=computed(()=>Math.max(1,...values.value.map(x=>x.value),...(props.points?.map(x=>x.upper)||[]))*1.15);
const xy=(v:number,i:number)=>`${35+i*730/Math.max(1,values.value.length-1)},${240-v/max.value*210}`;
const line=computed(()=>values.value.map((x,i)=>xy(x.value,i)).join(' '));
const area=computed(()=>props.points?[...props.points.map((x,i)=>xy(x.upper,i)),...props.points.map((x,i)=>xy(x.lower,i)).reverse()].join(' '):'');
</script><template><div class="chart"><svg viewBox="0 0 800 280" role="img" aria-label="需求随日期变化折线图"><g stroke="currentColor" opacity=".16"><line v-for="y in [30,100,170,240]" :x1="35" :x2="765" :y1="y" :y2="y"/></g><text x="3" y="26">{{Math.round(max)}}</text><text x="14" y="245">0</text><polygon v-if="area" :points="area" class="interval"/><polyline :points="line" fill="none" stroke="currentColor" stroke-width="3"/><text x="35" y="270">{{values[0]?.day}}</text><text x="645" y="270">{{values[values.length-1]?.day}}</text></svg></div></template>
