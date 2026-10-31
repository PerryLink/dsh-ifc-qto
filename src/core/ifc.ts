export type IfcErrorCode='E_IFC_UNREADABLE'|'E_IFC_EMPTY'|'E_IFC_EXPORT_FAILED'
export class IfcError extends Error{readonly code:IfcErrorCode;constructor(code:IfcErrorCode,message:string){super(`${code}: ${message}`);this.name='IfcError';this.code=code}}
export interface IfcElement{guid:string;type:string;name:string}
export interface IfcQuantity{kind:'length'|'area'|'volume';name:string;value:number}
export interface IfcModel{elements:IfcElement[];quantities:IfcQuantity[];types:Record<string,number>}
export function parseIfc(text:string):IfcModel{
 if(!text.trim())throw new IfcError('E_IFC_EMPTY','empty IFC'); if(!/ISO-10303-21|FILE_SCHEMA/i.test(text))throw new IfcError('E_IFC_UNREADABLE','not an ISO-10303-21 IFC file')
 const elements:IfcElement[]=[]; const types:Record<string,number>={}
 for(const m of text.matchAll(/#\d+\s*=\s*IFC(WALL|SLAB|DOOR|WINDOW|COLUMN|BEAM|FOOTING|STAIR|RAILING|RAMP|PILE|MEMBER|PLATE|COVERING)\s*\(([^;]*)\);/gi)){
  const type=m[1]!.toUpperCase(); const args=m[2]!; const quoted=[...args.matchAll(/'([^']*)'/g)].map(x=>x[1]!); const guid=quoted[0]??''; const name=quoted[2]??quoted[1]??''; elements.push({guid,type,name}); types[type]=(types[type]??0)+1
 }
 const quantities:IfcQuantity[]=[]
 for(const m of text.matchAll(/IFCQUANTITY(LENGTH|AREA|VOLUME)\s*\(\s*'([^']*)'([^)]*)\)/gi)){const numbers=[...m[3]!.matchAll(/([0-9]+(?:\.[0-9]+)?)/g)];const last=numbers.at(-1)?.[1];if(last!==undefined)quantities.push({kind:m[1]!.toLowerCase() as IfcQuantity['kind'],name:m[2]!,value:Number(last)})}
 if(elements.length===0&&quantities.length===0)throw new IfcError('E_IFC_UNREADABLE','no supported IFC elements/quantities')
 return{elements,quantities,types}
}
