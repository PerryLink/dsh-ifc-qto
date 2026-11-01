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

export interface IfcUnitInfo { prefix: string; unit: string }
export interface IfcUnitsResult {
  assignment: boolean
  length: IfcUnitInfo | null
  area: IfcUnitInfo | null
  volume: IfcUnitInfo | null
  issues: string[]
}
/**
 * Unit-assignment check for a QTO model: a take-off is meaningless without a declared length,
 * area and volume unit (IFC 4.3 IfcUnitAssignment / IfcSIUnit). Read-only and text-based.
 */
export function checkUnits(text: string): IfcUnitsResult {
  const assignment = /IFCUNITASSIGNMENT\s*\(/i.test(text)
  const find = (kind: string): IfcUnitInfo | null => {
    const re = new RegExp('IFCSIUNIT\\s*\\(\\s*\\*\\s*,\\s*\\.' + kind + '\\.\\s*,\\s*(\\.[A-Z]+\\.|\\$)\\s*,\\s*\\.([A-Z_]+)\\.', 'i')
    const m = re.exec(text)
    if (!m) return null
    return { prefix: m[1]!.replaceAll('.', ''), unit: m[2]!.toUpperCase() }
  }
  const length = find('LENGTHUNIT')
  const area = find('AREAUNIT')
  const volume = find('VOLUMEUNIT')
  const issues: string[] = []
  if (!assignment) issues.push('E_IFC_UNITASSIGNMENT_MISSING')
  if (!length) issues.push('E_IFC_LENGTHUNIT_MISSING')
  if (!area) issues.push('E_IFC_AREAUNIT_MISSING')
  if (!volume) issues.push('E_IFC_VOLUMEUNIT_MISSING')
  return { assignment, length, area, volume, issues }
}
