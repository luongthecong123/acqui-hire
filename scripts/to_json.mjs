import fs from 'fs';
const m = await import(process.argv[2]);
fs.writeFileSync(process.argv[3], JSON.stringify(m.acquisitionDataset, null, 1));
