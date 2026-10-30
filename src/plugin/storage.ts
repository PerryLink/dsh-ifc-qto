import { defineDomain, domainTable } from '@deepseek-ai/dsh-storage-domain'; import type { Context } from '@deepseek-ai/cordis'; import { z } from 'zod'
const model=z.object({model_id:z.string(),source_name:z.string(),sha256:z.string(),elements:z.array(z.object({guid:z.string(),type:z.string(),name:z.string()})),quantities:z.array(z.object({kind:z.enum(['length','area','volume']),name:z.string(),value:z.number()})),types:z.record(z.string(),z.number()),created_at:z.string()})
export type ModelRecord=z.infer<typeof model>; export type Table<T>={get(k:string):T|undefined;entries():IterableIterator<[string,T]>;size:number;put(k:string,v:T):Promise<void>}
export const ifcSpec=defineDomain({name:'ifc',version:1,tables:{models:domainTable<string,ModelRecord>(model)}})
export async function openIfc(ctx:Context){const d=await ctx.storageDomain.open(ifcSpec);ctx.effect(()=>()=>d.close(),'dsh-ifc-qto.domainClose');return d.table('models') as Table<ModelRecord>}
