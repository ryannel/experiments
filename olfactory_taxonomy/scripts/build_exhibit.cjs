#!/usr/bin/env node
// Rebuild the public exhibit without any historical experiments.
const fs=require('node:fs/promises'),path=require('node:path'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFile(path.join(root,p),'utf8');
async function main(){
 const args=new Set(process.argv.slice(2));
 const config=JSON.parse(await read('data/explorer.json'));
 await fs.mkdir(path.join(root,'build'),{recursive:true});
 if(args.has('--prepare')){
  const manifest=JSON.parse(await read('source/artwork.json'));
  let svg=await read('source/master.svg');
  for(const asset of manifest.assets){
   const bytes=await fs.readFile(path.join(root,'source',asset.path));
   const hash=crypto.createHash('sha256').update(bytes).digest('hex');
   if(hash!==asset.sha256)throw Error(`Source checksum mismatch: ${asset.path}. Update the manifest for intentional edits.`);
   svg=svg.split(`href="${asset.path}"`).join(`href="data:image/png;base64,${bytes.toString('base64')}"`);
  }
  await fs.writeFile(path.join(root,'build/embedded.svg'),svg);
  await fs.writeFile(path.join(root,'build/embedded-image.svg'),svg.replace(/id="(labels|label-backs|central-title)"/g,'id="$1" visibility="hidden"'));
  await fs.writeFile(path.join(root,'build/render.html'),(await read('templates/explorer-render.html')).replaceAll('6144',String(config.size)));
  console.log('Open /build/render.html through the local server. Export both PNGs with Baskerville and Avenir installed. Put labels.png and image.png in build/, then run npm run build:tiles.');
  return;
 }
 if(args.has('--tiles')){
  const sharp=require('sharp');sharp.cache({memory:128});sharp.concurrency(2);
  for(const mode of ['labels','image']){
   const file=path.join(root,'build',mode+'.png'),meta=await sharp(file).metadata();
   if(meta.width!==config.size||meta.height!==config.size)throw Error(`Expected ${config.size} × ${config.size} ${mode}.png`);
   await sharp(file).webp({quality:94}).tile({size:512,overlap:1,layout:'dz',container:'fs'}).toFile(path.join(root,'exhibit',mode+'.dz'));
  }
  await sharp(path.join(root,'build/labels.png')).avif({quality:65,effort:4,chromaSubsampling:'4:4:4'}).toFile(path.join(root,'exports/olfactory-atlas.avif'));
  await sharp(path.join(root,'build/labels.png')).resize(1600).webp({quality:86,effort:6}).toFile(path.join(root,'exhibit/preview.webp'));
  config.revision=crypto.createHash('sha256').update(await fs.readFile(path.join(root,'exports/olfactory-atlas.avif'))).digest('hex').slice(0,12);
  await fs.writeFile(path.join(root,'data/explorer.json'),JSON.stringify(config,null,2)+'\n');
 }
 await fs.writeFile(path.join(root,'exhibit/index.html'),(await read('templates/explorer.html')).replace('/* CONFIG */','const config='+JSON.stringify(config)+';'));
 console.log('Exhibit viewer built. No dependencies are needed to view the checked-in exhibit.');
}
main().catch(e=>{console.error(e.message);process.exitCode=1});
