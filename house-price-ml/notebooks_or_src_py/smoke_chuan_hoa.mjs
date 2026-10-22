/** Node có sẵn trong dự án. Kiểm tra HTTP và logic hiển thị, không giả là test trình duyệt. */
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import vm from 'node:vm';
const root=new URL('../',import.meta.url);
const log=[];
function pass(name,detail){log.push({name,detail});}
const home=await fetch('http://localhost:3000/');assert.equal(home.status,200);const html=await home.text();
const before=await fs.readFile(new URL('public/index.html.bak',root),'utf8');
assert.equal(html.match(/<form[\s\S]*?<\/form>/)[0],before.match(/<form[\s\S]*?<\/form>/)[0]);pass('Form gốc nguyên trạng','Sáu trường và cách submit giữ nguyên');
const payload={LotArea:8500,GrLivArea:1500,OverallQual:6,YearBuilt:2005,Neighborhood:'CollgCr',GarageType:'Attchd'};
const res=await fetch('http://localhost:3000/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
assert.equal(res.status,200);const data=await res.json();assert.equal(data.predicted_price_vnd,data.predicted_price_usd*data.usd_to_vnd);assert.equal(data.predicted_price,Number(data.predicted_price_usd.toFixed(2)));pass('Express chuyển đầy đủ các trường tiền',JSON.stringify(data));
const bad=await fetch('http://localhost:3000/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({GrLivArea:'abc'})});assert.equal(bad.status,400);pass('Validation gốc không thay đổi',await bad.text());
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];let handler;let request;
const note={textContent:'Ứng dụng minh họa. Giá hiển thị bằng USD.'};const currency={textContent:''};const result={className:'',style:{removeProperty(){}},textContent:''};const form={addEventListener(event,fn){assert.equal(event,'submit');handler=fn;}};
const context={document:{getElementById(id){return {'predict-form':form,result,'currency-note':currency}[id];},querySelector(){return note;}},FormData:class{entries(){return Object.entries(payload);}},fetch:async(url,options)=>{request={url,options};return {ok:true,json:async()=>data};}};
vm.runInNewContext(script,context);assert.ok(handler);assert.ok(!note.textContent.includes('bằng USD'));await handler({preventDefault(){}});
assert.equal(request.url,'/predict');assert.deepEqual(JSON.parse(request.options.body),payload);assert.ok(result.textContent.includes('₫'));assert.ok(!result.textContent.includes('$'));assert.ok(currency.textContent.includes('không phản ánh giá thị trường Việt Nam'));pass('JavaScript kết quả VND và request giữ nguyên',result.textContent);
const fixedNote=`Giá quy đổi theo tỷ giá cố định 1 USD = ${data.usd_to_vnd.toLocaleString('vi-VN')} ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.`;
let report=`# Kiểm tra HTTP và logic hiển thị VND\n\n${fixedNote}\n\nUTC: ${new Date().toISOString()}\n\n${log.length} PASS; 0 FAIL.\n\n`;
report+=log.map(r=>`- PASS — ${r.name}: ${r.detail}`).join('\n');report+='\n\nĐã chạy HTTP thật qua Express và Flask, kiểm tra handler JavaScript bằng Node vm. Chưa chạy trình duyệt Chromium vì máy kiểm thử chưa có browser binary; không gọi đây là kiểm tra giao diện bằng trình duyệt.\n';
await fs.writeFile(new URL('results/chuan_hoa/KIEM_CHUNG_HTTP.md',root),report,'utf8');console.log(`${log.length} PASS; 0 FAIL`);
