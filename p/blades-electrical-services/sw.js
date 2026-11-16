/* Blades Electrical Services: keeps this one page available with no signal. */
var C='blades-v1', BASE='/p/blades-electrical-services/';
var CORE=[BASE,BASE+'archivo-var.woff',BASE+'icon-192.png',BASE+'manifest.webmanifest',BASE+'blades-electrical-services.vcf'];
self.addEventListener('install',function(e){
  e.waitUntil(caches.open(C).then(function(c){return c.addAll(CORE)}).then(function(){return self.skipWaiting()}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){if(k.indexOf('blades-')===0&&k!==C)return caches.delete(k)}))}).then(function(){return self.clients.claim()}));
});
self.addEventListener('fetch',function(e){
  var r=e.request; if(r.method!=='GET')return;
  var u=new URL(r.url); if(u.origin!==self.location.origin||u.pathname.indexOf(BASE)!==0)return;
  if(r.mode==='navigate'){
    e.respondWith(new Promise(function(done){
      var settled=false;
      function fromCache(){return caches.match(BASE).then(function(m){return m||Response.error()})}
      var t=setTimeout(function(){if(!settled){settled=true;done(fromCache())}},4000);
      fetch(r).then(function(res){
        if(res&&res.ok){var cp=res.clone();caches.open(C).then(function(c){c.put(BASE,cp)})}
        if(!settled){settled=true;clearTimeout(t);done(res)}
      },function(){if(!settled){settled=true;clearTimeout(t);done(fromCache())}});
    }));
    return;
  }
  e.respondWith(caches.match(r).then(function(m){
    if(m)return m;
    return fetch(r).then(function(res){
      if(res&&res.ok){var cp=res.clone();caches.open(C).then(function(c){c.put(r,cp)})}
      return res;
    });
  }));
});
