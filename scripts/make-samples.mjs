/**
 * Build the PS1 quickstart sample.
 *
 * The IFC text below is hand-written for this repository. It is a synthetic
 * take-off model: fictional project/site names, no customer model, no real
 * building data, no derived geometry. Numbers are chosen to be obviously
 * illustrative (4200 mm wall, 86.4 m2 slab, one 0 m2 side area that exists to
 * exercise the data-quality check).
 *
 *   node scripts/make-samples.mjs
 */
import { createHash } from 'node:crypto'
import { mkdirSync, writeFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

const IFC = `ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [QuantityTakeoff]'),'2;1');
FILE_NAME('sample-building.ifc','2026-11-02T00:00:00',('synthetic sample'),('PerryLink'),'manual','manual','');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
/* Project + units. All names/ids are invented for this sample. */
#1=IFCPROJECT('0SAMPLEPROJECT000001',#20,'合成样例项目',$,$,$,$,$,#10);
#10=IFCUNITASSIGNMENT((#11,#12,#13));
#11=IFCSIUNIT(*,.LENGTHUNIT.,.MILLI.,.METRE.);
#12=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#13=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#20=IFCOWNERHISTORY(#21,#22,$,.ADDED.,$,$,$,0);
#21=IFCPERSONANDORGANIZATION(#23,#24,$);
#22=IFCAPPLICATION('synthetic-sample','1.0',$);
#23=IFCPERSON($,'Synthetic','Sample',$,$,$,$,$);
#24=IFCORGANIZATION($,'Synthetic Sample Co',$,$,$);
/* Elements: 2 walls, 1 slab, 1 door, 1 window, 1 column. */
#101=IFCWALL('0SAMPLEWALL0000000001',#20,'外墙-W1',$,$,$,$,$,.STANDARD.);
#102=IFCWALL('0SAMPLEWALL0000000002',#20,'内墙-W2',$,$,$,$,$,.STANDARD.);
#103=IFCSLAB('0SAMPLESLAB0000000001',#20,'楼板-S1',$,$,$,$,$,.FLOOR.);
#104=IFCDOOR('0SAMPLEDOOR0000000001',#20,'门-D1',$,$,$,$,$,900.,2100.,.DOOR.,.SINGLE_SWING_LEFT.,$);
#105=IFCWINDOW('0SAMPLEWINDOW00000001',#20,'窗-C1',$,$,$,$,$,1200.,1500.,.WINDOW.,.SINGLE_PANEL.,$);
#106=IFCCOLUMN('0SAMPLECOLUMN00000001',#20,'柱-K1',$,$,$,$,$,.COLUMN.);
/* Quantity entities in millimetres / square metres / cubic metres. */
#201=IFCQUANTITYLENGTH('Length',$,4200.,$);
#202=IFCQUANTITYLENGTH('Length',$,3000.,$);
#203=IFCQUANTITYLENGTH('Length',$,900.,$);
#204=IFCQUANTITYAREA('NetArea',$,86.4,$);
#205=IFCQUANTITYVOLUME('NetVolume',$,25.92,$);
#206=IFCQUANTITYAREA('NetSideArea',$,0.,$);
ENDSEC;
END-ISO-10303-21;
`

const target = path.join(root, 'samples', 'quickstart', 'input', 'sample-building.ifc')
mkdirSync(path.dirname(target), { recursive: true })
writeFileSync(target, IFC, 'utf8')
const sha256 = createHash('sha256').update(IFC).digest('hex')
console.log(`wrote ${path.relative(root, target)} (${Buffer.byteLength(IFC)} B, sha256 ${sha256})`)
console.log('synthetic only: fictional names/ids, no customer model')
