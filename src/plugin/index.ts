import path from'node:path';import type{Context}from'@deepseek-ai/cordis';import{createTools}from'./tools.js';import{openIfc}from'./storage.js'
export const name='dsh-ifc-qto';export const inject=['tools','storageDomain']
export async function apply(ctx:Context):Promise<void>{const baseDir=process.env.DSH_IFC_HOME??path.join(process.env.DSH_HOME??process.cwd(),'storages','dsh-ifc-qto');const models=await openIfc(ctx);for(const t of createTools({models,baseDir}))ctx.tools.register(t)}
