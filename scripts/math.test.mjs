import test from 'node:test';
import assert from 'node:assert/strict';
import {motion,holeValue,compose,inverseInputs,waveStats,choose,binomialTerm,targetTerm,circleValues,restrictedRootValue,powerDifferenceExtension,equalIncrementStudy} from '../dist/math.js';
test('A simplified expression never restores the quotient input',()=>{
 assert.equal(holeValue(1),null);assert.equal(holeValue(1,{extended:true,c:-1}),-1);
 assert.equal(holeValue(0),1);assert.equal(holeValue(2),3);
 assert.equal(motion(0).quotient,null);assert.equal(motion(0).extension,4);
 assert.equal(motion(-3).valid,false);assert.equal(motion(-.5).quotient,3.5);
});
test('Composition follows both operations, including boundaries',()=>{
 assert.equal(compose(-1,'fg').value,0);assert.equal(compose(1,'fg').value,0);
 assert.equal(compose(1.01,'fg').valid,false);assert.equal(compose(-.01,'gf').valid,false);
 assert.equal(compose(0,'gf').value,1);assert.equal(compose(4,'gf').value,-3);
});
test('Inverse branches recover only permitted inputs',()=>{
 assert.deepEqual(inverseInputs(4),[-2,2]);assert.deepEqual(inverseInputs(4,'negative'),[-2]);
 assert.deepEqual(inverseInputs(0),[0]);assert.deepEqual(inverseInputs(-1),[]);
});
test('Period and range handle both a wave and the constant exception',()=>{
 const w=waveStats(12,3);assert.ok(Math.abs(w.period-12)<1e-12);assert.deepEqual(w.range,[9,15]);
 assert.ok(Math.abs(w.fn(3)-15)<1e-12);assert.ok(Math.abs(w.fn(9)-9)<1e-12);
 assert.equal(waveStats(12,0).period,null);assert.deepEqual(waveStats(12,0).range,[12,12]);
 assert.ok(Math.abs(waveStats(12,-3,2).period-6)<1e-12);
});
test('Source coefficient and absent powers agree with the full finite expansion',()=>{
 assert.equal(choose(8,4),70);assert.equal(binomialTerm(4).coefficient,5670);
 assert.equal(targetTerm(-4).exists,true);assert.equal(targetTerm(-3).reason,'fractional');
 assert.equal(targetTerm(-29).reason,'range');assert.equal(targetTerm(.5).reason,'integer');
 for(const x of [.5,1,2,-1]){
  let sum=0;for(let k=0;k<=8;k++){const t=binomialTerm(k);sum+=t.coefficient*x**t.exponent;}
  const actual=(3*x*x-x**-3)**8;
  assert.ok(Math.abs(sum-actual)<=Math.max(1e-7,Math.abs(actual)*1e-10));
 }
});
test('Exact excluded tangent angles remain undefined',()=>{
 for(const n of [-90,-30,30,90])assert.equal(circleValues(n).tan,null);
 assert.equal(circleValues(0).sin,0);assert.equal(circleValues(60).cos,-1);
 assert.ok(Number.isFinite(circleValues(29).tan));
});

test('The root quotient includes its real root endpoint but excludes the pole',()=>{
 assert.ok(restrictedRootValue(-1)===0);assert.equal(restrictedRootValue(-1.001),null);
 assert.equal(restrictedRootValue(2),null);assert.equal(restrictedRootValue(3),2);
 assert.ok(restrictedRootValue(1.99)<0);assert.ok(restrictedRootValue(2.01)>0);
});
test('The extension agrees with the quotient off zero without cancellation near zero',()=>{
 for(let n=1;n<=5;n++){
  for(const x of [-2,0,2]){
   assert.equal(powerDifferenceExtension(n,x,0),n*x**(n-1));
   for(const h of [-.5,.25,1]){
    const actual=((x+h)**n-x**n)/h;
    assert.ok(Math.abs(powerDifferenceExtension(n,x,h)-actual)<1e-9);
   }
  }
 }
 assert.ok(Math.abs(powerDifferenceExtension(4,2,1e-12)-32)<1e-9);
 assert.throws(()=>powerDifferenceExtension(0,2,0),RangeError);
});

test('Equal increments distinguish fixed differences, fixed ratios, and undefined ratios', () => {
  const step = 1.5;
  for (const x of [0, 0.75, 2, 3]) {
    const affine = equalIncrementStudy('affine', x, step);
    assert.equal(affine.difference, 4.5);
    assert.equal(affine.second - affine.first, 4.5);

    const quadratic = equalIncrementStudy('power', x, step);
    assert.equal(quadratic.difference, quadratic.second - quadratic.first);
    if (x === 0) assert.equal(quadratic.ratio, null);

    const exponential = equalIncrementStudy('exponential', x, step);
    assert.ok(Math.abs(exponential.ratio - exponential.second / exponential.first) < 1e-12);
    assert.equal(exponential.ratio, 2 ** step);
  }
  assert.equal(equalIncrementStudy('power', 0, 0).ratio, null);
  assert.equal(equalIncrementStudy('exponential', 2, 0).difference, 0);
  assert.equal(equalIncrementStudy('exponential', 2, -1).ratio, 0.5);
  assert.equal(equalIncrementStudy('power', 1, -1).difference, -1);
});

test('The negative square branch returns the unique zero without a negative sign', () => {
  assert.deepEqual(inverseInputs(0, 'negative'), [0]);
});
