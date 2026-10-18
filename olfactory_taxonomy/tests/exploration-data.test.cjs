const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {buildExploration}=require('../scripts/exploration-data.cjs');
const root=path.resolve(__dirname,'..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const cells=read('data/cells.json'),editorial=['fresh','floral-amber','earthy'].map(n=>read('data/hierarchy-review-'+n+'.json'));
const {nodes}=buildExploration(cells,editorial),byId=new Map(nodes.map(n=>[n.id,n]));
function route(node){const out=[];for(let n=node;n;n=byId.get(n.parent))out.unshift(n);return out;}
test('every final scent has a complete four-tier route and local reference metadata',()=>{
 const leaves=nodes.filter(n=>n.level===3);
 assert.equal(leaves.length,82);
 for(const leaf of leaves){const chain=route(leaf);assert.deepEqual(chain.map(n=>n.level),[0,1,2,3]);assert.equal(leaf.outer,2880);assert.equal(leaf.cells.length,3);assert.ok(leaf.reference);assert.ok(leaf.sources.length);assert.ok(chain.every(n=>n.from<=leaf.from+1e-6&&n.to>=leaf.to-1e-6));}
 const covered=leaves.flatMap(n=>n.cells);
 assert.equal(new Set(covered).size,246);
});
test('the two Tobacco families retain distinct realm identities',()=>{
 const branches=nodes.filter(n=>n.level===1&&n.text==='TOBACCO');assert.equal(branches.length,2);assert.notEqual(branches[0].parent,branches[1].parent);
 for(const branch of branches)for(const node of nodes.filter(n=>route(n).some(x=>x.id===branch.id)))assert.equal(route(node)[0].id,branch.parent);
});
test('guided wording comes from final editorial choices rather than SVG wrapping',()=>{
 const leaf=nodes.find(n=>n.id==='descriptors-a5288a8824364d70');assert.equal(leaf.text,'Peppermint, chewing gum');assert.equal(leaf.feel,'cool, crisp');assert.equal(leaf.reference,'Peppermint oil');
 const dry=nodes.find(n=>n.level===2&&n.text==='Dry Wood');assert.equal(nodes.filter(n=>n.parent===dry.id).length,3);
});
