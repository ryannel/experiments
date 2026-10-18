// Build the interactive hierarchy from this repository's final cell/editorial data.
const levels=['realm','family','note','descriptors'];
const norm=s=>String(s||'').replace(/\s+/g,'').toLowerCase();
const readable=s=>String(s||'').replace(/([,:])(?=\S)/g,'$1 ');
const hints={
 'FRESH & LIFTED':'Citrus peel, cut grass, mint and herbs, clean laundry, sea air',
 'FLORAL & FRUITY':'Orange blossom, jasmine and rose, powdery violet, berries, peach and coconut',
 'AMBER, SPICE & SWEET':'Vanilla and caramel, coffee and rum, warm spices, sweet tobacco, incense',
 'EARTHY, WOODY & DEEP':'Wood and smoke, leather, warm skin, damp earth and moss, rain on stone'
};
function buildExploration(cells,editorial){
 const choices=editorial.flatMap(doc=>(Array.isArray(doc)?doc:doc.reviews).flatMap(row=>row.choices.map(choice=>({source:JSON.stringify(row.source_path),...choice}))));
 const nodes=cells.filter(c=>levels.includes(c.field)).map(c=>{
  const level=levels.indexOf(c.field);
  const parents=level?cells.filter(p=>p.field===levels[level-1]&&p.realm===c.realm&&p.start<=c.start+1e-6&&p.end>=c.end-1e-6):[];
  if(level&&parents.length!==1)throw Error('Ambiguous parent for '+c.id);
  const node={id:c.id,parent:parents[0]?.id||null,level,text:readable(c.text),from:c.start,to:c.end,inner:c.inner,outer:c.outer};
  if(!level)node.hint=hints[c.text];
  if(level===3){
   const choice=choices.find(x=>x.source===JSON.stringify(c.source_path)&&norm(x.print_text)===norm(c.text));
   if(!choice)throw Error('Missing editorial wording for '+c.id);
   const related=field=>cells.find(x=>x.field===field&&Math.abs(x.start-c.start)<1e-6&&Math.abs(x.end-c.end)<1e-6);
   const feel=related('texture_tactile'),reference=related('reference_material');
   if(!feel||!reference)throw Error('Incomplete route '+c.id);
   node.text=choice.print_text;
   node.outer=reference.outer;
   node.feel=Array.isArray(choice.feel)?choice.feel.join(', '):readable(feel.text);
   node.reference=norm(choice.reference)===norm(reference.text)?choice.reference:readable(reference.text);
   node.referenceNote=choice.reference_note||'';
   node.sources=choice.reference_sources||[];
   node.cells=[c.id,feel.id,reference.id];
  }
  return node;
 });
 const ids=new Set(nodes.map(n=>n.id));
 for(const node of nodes)if(node.parent&&!ids.has(node.parent))throw Error('Missing parent '+node.parent);
 return {units:6144,nodes};
}
module.exports={buildExploration};
