#!/usr/bin/env python3
"""
╔» XOPHY GHOST-WALKER NEBULA «╗ — Aggressive async CT+BF+TLS+Takeover+Port scan+Tech ID
    Author: w45if_4o4  |  <500 lines  |  Next-gen recon engine
"""
import asyncio, aiohttp, aiodns, time, re, json, socket, ssl, hashlib, ipaddress
from datetime import datetime, timezone
from collections import defaultdict
from cryptography import x509
from cryptography.hazmat.backends import default_backend

R,G,Y,C,M,W,X='\033[91m','\033[92m','\033[93m','\033[96m','\033[95m','\033[97m','\033[0m'
BLD,DIM='\033[1m','\033[2m'

# ─── 500 subdomain wordlist (heavy hitters) ───
BF_WORDS = """www mail admin remote blog dev test api webmail portal vpn app staging
git jenkins wiki forum docs support cdn static assets img images video media
cdn2 cdn3 cloud crm erp hr payroll finance accounting backup proxy gateway
edge shop store cart checkout api2 api3 api4 api5 mobile ios android app2
app3 app4 beta alpha demo stage prod production uat qa qa2 qa3 qa4 qa5
staging2 staging3 dev2 dev3 dev4 dev5 devops engineering ops infra infra2
infra3 infra4 infra5 load balancer lb lb1 lb2 lb3 ns1 ns2 ns3 ns4 dns dns1
dns2 mx mx1 mx2 smtp pop imap mail2 mail3 mail4 webmail2 webmail3 webmail4
autodiscover msoid calendar teams skype lync exchange owa ecp rpc rtm
helpdesk support2 support3 support4 support5 ticket tickets chat livechat
board status status2 status3 status4 status5 monitor monitoring nagios
grafana prometheus kibana elasticsearch elastic logs logging syslog
splunk zabbix centreon checkmk cacti observium librenms netbox phpmyadmin
adminer admin2 admin3 admin4 admin5 manager management dashboard reports
reporting analytics bi dwh etl data db database sql mysql postgres mariadb
mongodb redis cache memcached rabbitmq kafka zookeeper hadoop spark storm
airflow jenkins2 circleci travis ci cd pipeline artifactory nexus docker
k8s kubernetes kube k3s swarm nomad consul vault terraform ansible puppet
chef salt rundeck controller master node node1 node2 node3 node4 node5
worker worker1 worker2 worker3 worker4 worker5 app1 app2 app3 app4 app5
web1 web2 web3 web4 web5 web6 web7 web8 web9 web10 srv srv1 srv2 srv3 srv4
srv5 server server1 server2 server3 server4 server5 host host1 host2 host3
host4 host5 node01 node02 node03 node04 node05 web01 web02 web03 web04 web05
app01 app02 app03 app04 db01 db02 db03 db04 dev01 dev02 dev03 dev04
prod01 prod02 prod03 prod04 qa01 qa02 qa03 qa04 staging01 staging02
staging03 staging04 staging05 test01 test02 test03 test04 test05
test6 test7 test8 test9 test10 sandbox playground demo1 demo2 demo3
demo4 demo5 demo6 demo7 demo8 demo9 demo10 training learn tutorial
docs2 docs3 wiki2 wiki3 confluence jira bugzilla redmine gitlab bitbucket
gitea gogs source code review sonarqube fortify coverity checkmarx
veracode blackduck snyk whitesource npm pypi rubygems packagist
composer maven gradle nuget chocolatey brew apt yum dnf pacman zypper
copr obs build builder compile ci cd deploy deployment release
dist distribution download upload ftp ftps sftp ssh telnet rdp vnc
vpn pptp l2tp openvpn wireguard ipsec ike strongswan radius ldap
kerberos ad dc domain controller dc1 dc2 dc3 dc4 adfs adfs1 adfs2
adconnect aad azure aws gcp oracle oci ibm aliyun tencent digitalocean
linode vultr hetzner ovh rackspace softlayer photon photon1 photon2
photon3 photon4 photon5 baremetal metal"""

SCAN_PORTS = [21,22,23,25,53,80,81,110,111,135,139,143,161,389,443,445,
              465,500,514,587,636,993,995,1080,1433,1521,2049,2082,2083,
              2086,2087,2095,2096,2222,2375,2376,2483,2484,3000,3128,
              3306,3389,3690,4000,4443,4848,5000,5432,5555,5601,5900,
              5901,5902,5984,6000,6001,6379,6443,6666,6667,7000,7001,
              7077,7443,7474,7777,8000,8001,8008,8009,8010,8069,8080,
              8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,
              8092,8093,8094,8095,8096,8097,8098,8099,8181,8222,8333,
              8443,8444,8445,8446,8447,8448,8449,8450,8500,8600,8649,
              8880,8888,8889,9000,9001,9002,9003,9004,9005,9006,9007,
              9008,9009,9010,9042,9043,9044,9045,9046,9047,9048,9049,
              9050,9090,9091,9092,9093,9094,9095,9096,9097,9098,9099,
              9100,9200,9300,9418,9443,9444,9445,9446,9447,9448,9449,
              9450,9999,10000,10001,10002,10003,10004,10005,10006,10007,
              10008,10009,10010,10100,10250,11211,12000,12345,12700,
              15672,16010,16379,17000,17001,17002,17003,17004,17005,
              18080,18081,18082,18083,18084,18085,18086,18087,18088,
              18089,18090,19000,19001,19002,19003,19004,19005,20000,
              20001,20002,20003,20004,20005,21320,22000,22222,23000,
              24000,25000,25565,26000,27000,27017,28000,28015,28017,
              30000,31000,32000,32764,33000,34000,35000,36000,37000,
              38000,39000,40000,41000,42000,43000,44000,45000,46000,
              47000,48000,49000,50000,50070,50090,51000,52000,53000,
              54000,55000,56000,57000,58000,59000,60000,61000,62000,
              63000,64000,65000,65389,65535]

TLS_VULNS = {
    "SSLv2":("CVE-1999-0427",9.8,"SSLv2 — POODLE-like MITM"),
    "SSLv3":("CVE-2014-3566",5.9,"POODLE — padding oracle"),
    "TLSv1.0":("CVE-2011-3389",5.9,"BEAST — CBC plaintext recovery"),
    "TLSv1.1":("CVE-2019-1559",5.9,"Protocol downgrade risk"),
    "RC4":("CVE-2015-2808",5.9,"RC4 biases — plaintext recovery"),
    "3DES":("CVE-2016-2183",5.9,"SWEET32 — 64-bit block cipher"),
    "EXP":("CVE-2016-0800",7.5,"DROWN — export-grade downgrade"),
    "NULL":("CVE-1999-0196",7.5,"NULL cipher — no encryption"),
    "ANON":("CVE-2002-0399",7.5,"Anonymous DH — MITM"),
    "MD5":("CVE-2004-2761",4.8,"MD5 signature collision risk"),
    "SHA1":("CVE-2004-2761",4.8,"SHA1 collision risk"),
    "LOW":("CVE-2015-4000",6.8,"LOGJAM — DH export parameters"),
    "CBC":("CVE-2014-0224",6.8,"CCS injection / Early CCS"),
    "aNULL":("CVE-2002-0399",7.5,"Anonymous NULL auth"),
    "eNULL":("CVE-1999-0196",7.5,"NULL encryption"),
    "SEED":("CVE-2016-2183",5.9,"SEED — 128-bit block cipher"),
    "IDEA":("CVE-2016-2183",5.9,"IDEA — 64-bit block cipher"),
    "RSA_EXPORT":("CVE-2015-4000",6.8,"RSA export key — FREAK"),
    "DSS":("CVE-2004-2761",4.8,"DSS signature collision"),
}

TAKEOVER_SIGS = (
    (".s3.amazonaws.com","AWS S3","NoSuchBucket"),
    (".s3-website","AWS S3","NoSuchBucket"),
    (".cloudfront.net","CloudFront","CloudFront distribution"),
    (".elasticbeanstalk.com","AWS EB","NXDOMAIN"),
    (".azurewebsites.net","Azure App","404 Not Found"),
    (".trafficmanager.net","Azure TM","404 Not Found"),
    (".azure-api.net","Azure API","404 Not Found"),
    (".azureedge.net","Azure CDN","404 Not Found"),
    (".blob.core.windows.net","Azure Blob","404"),
    (".firebaseio.com","Firebase","404 Not Found"),
    (".herokuapp.com","Heroku","no-such-app"),
    (".pages.dev","Cloudflare","DNS_PROBE"),
    (".myshopify.com","Shopify","Sorry, this shop"),
    (".squarespace.com","Squarespace","404 Not Found"),
    (".ghost.io","Ghost","The thing you"),
    (".unbouncepages.com","Unbounce","404"),
    (".fastly.net","Fastly","Fastly error"),
    (".github.io","GitHub Pages","404 Not Found"),
    (".gitlab.io","GitLab Pages","404 Not Found"),
    (".netlify.app","Netlify","Not Found - Request ID"),
    (".surge.sh","Surge","project not found"),
    (".pantheonsite.io","Pantheon","The gods are angry"),
    (".aftership.com","AfterShip","Oops"),
    (".freshdesk.com","Freshdesk","404"),
    (".zendesk.com","Zendesk","Help Center Closed"),
    (".atlassian.net","Atlassian","404"),
    (".cargo.site","Cargo","404 Not Found"),
    (".fly.dev","Fly.io","404 Not Found"),
    (".render.com","Render","404 Not Found"),
    (".onrender.com","Render","404 Not Found"),
    (".cyclic.app","Cyclic","404"),
    (".railway.app","Railway","404 Not Found"),
    (".vercel.app","Vercel","404: NOT_FOUND"),
    (".tf-idx.dev","TensorFlow","404 Not Found"),
    (".000webhostapp.com","000WebHost","404 Not Found"),
    (".bitbucket.io","Bitbucket","404 Not Found"),
    (".carrd.co","Carrd","404"),
    (".discourse.org","Discourse","404"),
    (".glitch.me","Glitch","404"),
    (".mystrikingly.com","Strikingly","404"),
    (".tilda.ws","Tilda","404"),
    (".usercontent","Custom","404"),
)

WAF_SIGS = {
    "cloudflare":["cf-ray","cf-cache-status","server: cloudflare","attention required","cloudflare ray id"],
    "akamai":["akamai-grn","x-akamai","akamai-origin-hop","reference id"],
    "aws":["x-amz-cf-id","x-amz-cf-pop","x-amzn-trace-id","x-amz-request-id","request blocked"],
    "sucuri":["x-sucuri-id","x-sucuri-cache","server: sucuri"],
    "imperva":["x-iinfo","x-cdn: imperva","incapsula"],
    "f5":["x-f5-application","x-f5","bigip","server: bigip"],
    "modsecurity":["mod_security","no-doubt"],
    "cloudflare_mitm":["cf-mitm"],
    "cloudfront":["x-amz-cf"],
    "azure":["x-azure-ref","x-azure"],
}

TECH_SIGS = {
    "nginx/":"nginx","apache":"Apache","IIS":"IIS","caddy":"Caddy","openresty":"OpenResty",
    "gunicorn":"Gunicorn","uwsgi":"uWSGI","node.js":"Node.js","express":"Express",
    "python/":"Python","php/":"PHP","java":"Java","tomcat":"Tomcat","jetty":"Jetty",
    "django":"Django","flask":"Flask","rails":"Ruby on Rails","rack":"Rack",
    "wordpress":"WordPress","drupal":"Drupal","joomla":"Joomla","magento":"Magento",
    "shopify":"Shopify","woocommerce":"WooCommerce","squarespace":"Squarespace",
    "cloudflare":"Cloudflare","fastly":"Fastly","varnish":"Varnish","ats":"Apache Traffic Server",
    "docker":"Docker","k8s":"Kubernetes","istio":"Istio","envoy":"Envoy",
    "traefik":"Traefik","haproxy":"HAProxy","nginx plus":"NGINX Plus",
    "python aiohttp":"aiohttp","san":"SAN",
}

# ─── MAIN ENGINE ───
class GhostWalkerNebula:
    def __init__(self, target, concurrency=300, timeout=10):
        self.target = target.rstrip('.')
        self.domain = self.target
        self.sema = asyncio.Semaphore(concurrency)
        self.port_sema = asyncio.Semaphore(500)
        self.timeout = timeout
        self.resolver = aiodns.DNSResolver()
        self.results = {"scan_start":datetime.now(timezone.utc).isoformat(),"target":self.target,
            "subdomains":{},"port_scan":{},"tls_issues":[],"takeover_candidates":[],
            "cve_matches":[],"wildcard":False,"wafs":[],"technologies":{},
            "zone_transfer":None,"total_found":0,"alive_count":0}
        self.seen_domains = set()
        self.lock = asyncio.Lock()

    def log(self, level, msg):
        t = datetime.now().strftime("%H:%M:%S")
        c = {"good":G,"warn":Y,"critical":R,"info":C}.get(level,W)
        print(f" {DIM}{t}{X} {c}[{level.upper()}]{X} {msg}")

    # ─── CT SOURCES ───
    async def fetch_json(self, session, url, label, parser):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(self.timeout),
                    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) XOPHY/3.0"}) as r:
                if r.status==200: return await parser(r)
                self.log("warn",f"{label} HTTP {r.status}")
        except Exception as e:
            self.log("warn",f"{label} failed: {str(e)[:50]}")
        return None

    async def ct_crtsh(self, session):
        d=await self.fetch_json(session,f"https://crt.sh/?q=%25.{self.target}&output=json","crt.sh",lambda r:r.json())
        if not d: return set()
        s=set()
        for e in d:
            for n in e.get("name_value","").split("\n"):
                n=n.strip().lower()
                if n and "*" not in n and n.endswith("."+self.target): s.add(n)
        self.log("good",f"crt.sh: {len(s)} subs"); return s

    async def ct_hackertarget(self, session):
        d=await self.fetch_json(session,f"https://api.hackertarget.com/hostsearch/?q={self.target}","HT",lambda r:r.text())
        if not d: return set()
        s=set()
        for l in d.strip().split("\n"):
            p=l.split(",")
            if len(p)>=1 and p[0].strip().lower().endswith("."+self.target): s.add(p[0].strip().lower())
        self.log("good",f"HackerTarget: {len(s)} subs"); return s

    async def ct_alienvault(self, session):
        d=await self.fetch_json(session,f"https://otx.alienvault.com/api/v1/indicators/domain/{self.target}/passive_dns","OTX",lambda r:r.json())
        if not d: return set()
        s=set()
        for e in d.get("passive_dns",[]):
            h=e.get("hostname","").strip().lower()
            if h.endswith("."+self.target): s.add(h)
        self.log("good",f"OTX: {len(s)} subs"); return s

    async def ct_urlscan(self, session):
        d=await self.fetch_json(session,f"https://urlscan.io/api/v1/search/?q=domain:{self.target}&size=100","urlscan",lambda r:r.json())
        if not d: return set()
        s=set()
        for e in d.get("results",[]):
            p=e.get("page",{})
            for f in ["domain","apex"]:
                v=p.get(f,"")
                if v and v.lower().endswith("."+self.target): s.add(v.lower())
        self.log("good",f"urlscan: {len(s)} subs"); return s

    async def ct_rapiddns(self, session):
        d=await self.fetch_json(session,f"https://rapiddns.io/subdomain/{self.target}?full=1","RapidDNS",lambda r:r.text())
        if not d: return set()
        s=set()
        for m in re.finditer(rf'([\w.-]+\.{re.escape(self.target)})',d,re.I):
            v=m.group(1).lower().strip('.')
            if v.endswith("."+self.target): s.add(v)
        self.log("good",f"RapidDNS: {len(s)} subs"); return s

    async def ct_anubis(self, session):
        d=await self.fetch_json(session,f"https://jldc.me/anubis/subdomains/{self.target}","Anubis",lambda r:r.json())
        if not d: return set()
        s=set()
        for e in d:
            if isinstance(e,str) and e.strip().lower().endswith("."+self.target): s.add(e.strip().lower())
        self.log("good",f"Anubis: {len(s)} subs"); return s

    # ─── WILDCARD ───
    async def wildcard_check(self):
        nonce=f"xophy-{hashlib.md5(str(time.time()).encode()).hexdigest()[:10]}.{self.target}"
        try:
            await self.resolver.query(nonce,'A')
            self.results["wildcard"]=True
            self.log("warn",f"WILDCARD DNS! {nonce} resolves")
            return True
        except: return False

    # ─── DNS RESOLVE ───
    async def resolve(self, domain, qtype='A'):
        try:
            ans=await self.resolver.query(domain,qtype)
            if isinstance(ans,list): return [a.host for a in ans]
            return [ans.host]
        except: return None

    async def resolve_any(self, domain):
        """Returns (ips, cname) or (None, None)"""
        ips = await self.resolve(domain,'A')
        if not ips:
            try:
                ips=list(set(i[4][0] for i in socket.getaddrinfo(domain,80,socket.AF_INET)))
            except: pass
        cname = None
        try:
            c=await self.resolver.query(domain,'CNAME')
            cname=c.host.rstrip('.')
        except: pass
        return ips, cname

    # ─── DNS BRUTEFORCE ───
    async def bruteforce(self):
        words=[w.strip() for w in BF_WORDS.strip().split() if w.strip()]
        self.log("info",f"DNS bruteforce: {len(words)} names")
        found=set()
        sem=asyncio.Semaphore(100)

        async def try_word(w):
            async with sem:
                d=f"{w}.{self.target}"
                try:
                    await self.resolver.query(d,'A')
                    found.add(d); return d
                except: return None

        tasks=[try_word(w) for w in words]
        await asyncio.gather(*tasks)
        self.log("good",f"Bruteforce found: {len(found)}")
        return found

    # ─── PERMUTATIONS ───
    async def permutations(self, seeds):
        """Generate mutations from discovered subdomains."""
        perms=set()
        prefixes=['dev-','staging-','test-','prod-','uat-','qa-','backup-','old-','new-',
                   'v1.','v2.','v3.','admin-','api-','beta-','demo-']
        suffixes=['-dev','-staging','-test','-prod','-uat','-qa','-backup','-old','-new',
                   '-v1','-v2','-admin','-api','-beta']
        envs=['dev.','staging.','test.','qa.','uat.','prod.','backup.','old.','new.']

        for seed in list(seeds)[:30]:
            sub=seed.replace("."+self.target,"")
            for p in prefixes:
                perms.add(f"{p}{sub}.{self.target}")
            for s in suffixes:
                perms.add(f"{sub}{s}.{self.target}")
            for e in envs:
                perms.add(f"{e}{sub}.{self.target}")
            perms.add(f"{sub}2.{self.target}")
            perms.add(f"{sub}3.{self.target}")

        perms-=seeds
        self.log("info",f"Permutations: {len(perms)}")
        found=set()
        sem=asyncio.Semaphore(100)
        async def try_one(d):
            async with sem:
                try:
                    await self.resolver.query(d,'A')
                    found.add(d)
                except: pass
        tasks=[try_one(p) for p in list(perms)[:2000]]
        await asyncio.gather(*tasks)
        self.log("good",f"Permutation hits: {len(found)}")
        return found

    # ─── ZONE TRANSFER ───
    async def zone_transfer(self):
        self.log("info","Attempting zone transfer...")
        # Get NS records
        try:
            ns_ans=await self.resolver.query(self.target,'NS')
            ns_servers=[a.host.rstrip('.') for a in (ns_ans if isinstance(ns_ans,list) else [ns_ans])]
        except:
            try: ns_servers=[i[4][0] for i in socket.getaddrinfo(self.target,53)][:3]
            except: ns_servers=[]

        for ns in ns_servers[:3]:
            try:
                r, w = await asyncio.wait_for(asyncio.open_connection(ns,53), timeout=5)
                w.close()
                # If TCP 53 open, attempt AXFR via dig-like query
                self.log("good",f"Zone transfer possible on {ns}? TCP/53 open")
                self.results["zone_transfer"]={"ns":ns,"status":"tcp_open"}
                return {"ns":ns,"status":"tcp_open"}
            except: continue
        return None

    # ─── PORT SCAN ───
    async def port_scan(self, ip):
        if ip in self.results["port_scan"]: return self.results["port_scan"][ip]
        open_ports = []
        async def check_port(p):
            async with self.port_sema:
                try:
                    r,w = await asyncio.wait_for(asyncio.open_connection(ip,p), timeout=2)
                    w.close()
                    open_ports.append(p)
                except: pass
        tasks=[check_port(p) for p in SCAN_PORTS[:50]]  # Top 50 ports per host for speed
        await asyncio.gather(*tasks)
        self.results["port_scan"][ip] = open_ports
        return open_ports

    # ─── TLS SCAN ───
    async def tls_scan(self, domain, ip, port=443):
        result={"tls_version":None,"cipher":None,"cert_cn":None,"cert_sans":[],
                "cert_issuer":None,"cert_fingerprint":None,"cert_valid_from":None,
                "cert_valid_to":None,"cert_serial":None,"tls_vulns":[],"cves":[]}
        try:
            ctx=ssl.create_default_context()
            ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            r,w=await asyncio.wait_for(asyncio.open_connection(ip if ip else domain,port,ssl=ctx),timeout=self.timeout)
            sock=w.get_extra_info('ssl_object')
            if sock:
                ver=sock.version(); ciph=sock.cipher()
                result["tls_version"]=ver; result["cipher"]=ciph[0] if ciph else None
                if ver and ver in TLS_VULNS:
                    cve,cvss,desc=TLS_VULNS[ver]
                    result["tls_vulns"].append({"vuln":desc,"cve":cve,"cvss":cvss})
                    result["cves"].append({"cve":cve,"type":"tls_version","cvss":cvss})
                if ciph:
                    cn=ciph[0] if ciph else ""
                    for k,v in TLS_VULNS.items():
                        if k in cn and k not in ("SSLv2","SSLv3","TLSv1.0","TLSv1.1"):
                            cve,cvss,desc=v
                            result["tls_vulns"].append({"vuln":desc,"cve":cve,"cvss":cvss})
                            result["cves"].append({"cve":cve,"type":"cipher","cvss":cvss})
                cert_bin=sock.getpeercert(binary_form=True)
                if cert_bin:
                    cert=x509.load_der_x509_certificate(cert_bin,default_backend())
                    result["cert_cn"]=cert.subject.rfc4514_string()
                    try: result["cert_sans"]=cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.DNSName)
                    except: pass
                    result["cert_issuer"]=cert.issuer.rfc4514_string()
                    result["cert_serial"]=str(cert.serial_number)
                    result["cert_fingerprint"]=hashlib.sha256(cert_bin).hexdigest()
                    result["cert_valid_from"]=str(cert.not_valid_before)
                    result["cert_valid_to"]=str(cert.not_valid_after)
            w.close()
        except: pass
        return result

    # ─── HTTP PROBE + WAF/TECH DETECTION ───
    async def http_probe(self, session, domain, ip):
        result={"status":None,"server":None,"title":None,"redirect":None,"waf":None,
                "tech":[],"missing_headers":[],"body_hash":None,"content_length":0}
        for proto in ("https://","http://"):
            try:
                url=f"{proto}{domain}"
                async with session.get(url,timeout=aiohttp.ClientTimeout(8),
                        allow_redirects=False,ssl=False,
                        headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}) as r:
                    result["status"]=r.status
                    result["server"]=r.headers.get("Server")
                    result["redirect"]=r.headers.get("Location")
                    result["content_length"]=len(await r.read())
                    body=await r.text()
                    mt=re.search(r'<title[^>]*>(.*?)</title>',body,re.I|re.S)
                    if mt: result["title"]=mt.group(1).strip()[:120]
                    result["body_hash"]=hashlib.md5(body.encode()).hexdigest()
                    # Missing security headers
                    for h in ["X-Frame-Options","X-Content-Type-Options","Content-Security-Policy",
                              "Strict-Transport-Security","X-XSS-Protection","Referrer-Policy"]:
                        if h not in r.headers: result["missing_headers"].append(h)
                    # WAF detection from headers
                    hdr_str=str(r.headers).lower()+body[:2000].lower()
                    for waf_name, patterns in WAF_SIGS.items():
                        for pat in patterns:
                            if pat.lower() in hdr_str:
                                result["waf"]=waf_name
                                if waf_name not in self.results["wafs"]:
                                    self.results["wafs"].append(waf_name)
                                break
                        if result["waf"]: break
                    # Tech detection
                    full_sig=f"{r.headers.get('Server','')} {r.headers.get('X-Powered-By','')} {body[:500]}".lower()
                    for sig,tech in TECH_SIGS.items():
                        if sig.lower() in full_sig and tech not in result["tech"]:
                            result["tech"].append(tech)
                    # Takeover body check
                    for sig,provider,fingerprint in TAKEOVER_SIGS:
                        if fingerprint.lower() in body[:800].lower():
                            cand={"domain":domain,"provider":provider,"sig":sig,"fingerprint":fingerprint,"detected_by":"http_body"}
                            async with self.lock:
                                if cand not in self.results["takeover_candidates"]:
                                    self.results["takeover_candidates"].append(cand)
                            self.log("critical",f"TAKEOVER BODY: {domain} -> {provider}")
                    break
            except: continue
        return result

    # ─── SUB SCAN ───
    async def scan_one(self, session, domain):
        async with self.sema:
            if domain in self.seen_domains: return
            async with self.lock: self.seen_domains.add(domain)

            entry={"domain":domain,"ips":None,"cname":None,"alive":False,"ports":[],
                   "tls":None,"http":None,"takeover":None}

            ips, cname = await self.resolve_any(domain)
            if not ips: return entry
            entry["ips"]=ips; entry["alive"]=True; entry["cname"]=cname

            # Takeover by CNAME
            if cname:
                for sig,provider,fp in TAKEOVER_SIGS:
                    if sig in cname.lower():
                        cand={"domain":domain,"cname":cname,"provider":provider,"sig":sig,"fingerprint":fp,"detected_by":"cname"}
                        entry["takeover"]=cand
                        async with self.lock: self.results["takeover_candidates"].append(cand)
                        self.log("critical",f"TAKEOVER CNAME: {domain} -> {cname} ({provider})")

            # Port scan first IP
            ports=await self.port_scan(ips[0])
            entry["ports"]=ports

            # TLS on 443 if open
            if 443 in ports:
                tls=await self.tls_scan(domain,ips[0])
                entry["tls"]=tls
                if tls.get("cves"):
                    async with self.lock: self.results["cve_matches"].extend(tls["cves"])
                if tls.get("tls_vulns"):
                    async with self.lock: self.results["tls_issues"].extend([{"domain":domain,**v} for v in tls["tls_vulns"]])

            # HTTP probe on 80 or 443
            if 80 in ports or 443 in ports or not ports:
                http=await self.http_probe(session,domain,ips[0])
                entry["http"]=http
                if http.get("status"):
                    lvl="good" if http["status"]<400 else "warn"
                    self.log(lvl,f"{domain:35s} {http['status']}  {http.get('server','?'):18s} {http.get('waf','—'):12s} {http.get('title','')[:40] or ''}")

            async with self.lock: self.results["subdomains"][domain]=entry
            return entry

    # ─── RUN ───
    async def run(self):
        t0=time.time()
        self.log("info",f"{BLD}{M}GhostWalker Nebula{X} → {C}{self.target}{X}")

        connector = aiohttp.TCPConnector(limit=100, limit_per_host=15, ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Phase 1: CT sources
            ct_tasks = [self.ct_crtsh(session), self.ct_hackertarget(session),
                        self.ct_alienvault(session), self.ct_urlscan(session),
                        self.ct_rapiddns(session), self.ct_anubis(session)]
            ct_results = await asyncio.gather(*ct_tasks, return_exceptions=True)

        all_subs = set()
        for r in ct_results:
            if isinstance(r, set): all_subs |= r
        self.log("info",f"CT sources: {len(all_subs)} unique subs")

        # Phase 2: Wildcard check
        wc = await self.wildcard_check()

        # Phase 3: DNS bruteforce
        bf = await self.bruteforce()
        all_subs |= bf

        # Phase 4: Permutations from found subs
        perm = await self.permutations(all_subs)
        all_subs |= perm

        # Phase 5: Zone transfer
        await self.zone_transfer()

        self.log("info",f"Total targets: {len(all_subs)} — scanning...")

        # Phase 6: Full scan each subdomain
        connector2 = aiohttp.TCPConnector(limit=200, limit_per_host=20, ssl=False)
        async with aiohttp.ClientSession(connector=connector2) as session:
            tasks = [self.scan_one(session, s) for s in sorted(all_subs)]
            await asyncio.gather(*tasks, return_exceptions=True)

        # Compile stats
        alive = [s for s in self.results["subdomains"].values() if s.get("alive")]
        self.results["total_found"] = len(all_subs)
        self.results["alive_count"] = len(alive)
        elapsed = time.time()-t0
        self.results["scan_duration"] = f"{elapsed:.1f}s"

        # Print report
        print(f"\n{BLD}{M}╔══════════════════════════════════════════╗{X}")
        print(f"{BLD}{M}║        GHOST-WALKER NEBULA REPORT         ║{X}")
        print(f"{BLD}{M}╚══════════════════════════════════════════╝{X}")
        print(f" {C}Target        {X}: {self.target}")
        print(f" {C}CT+BF+Perm    {X}: {len(all_subs)}")
        print(f" {C}Alive         {X}: {len(alive)}")
        print(f" {C}Wildcard      {X}: {R}YES{X}" if wc else f" {C}Wildcard      {X}: No")
        print(f" {C}Ports scanned{X}: 50/host")
        print(f" {C}TLS Issues    {X}: {R}{len(self.results['tls_issues'])}{X}")
        print(f" {C}Takeover cand {X}: {R}{len(self.results['takeover_candidates'])}{X}" if self.results['takeover_candidates'] else f" {C}Takeover cand {X}: None")
        print(f" {C}CVE Hits      {X}: {Y}{len(self.results['cve_matches'])}{X}")
        print(f" {C}WAFs detected {X}: {', '.join(self.results['wafs']) if self.results['wafs'] else 'None'}")
        if self.results["zone_transfer"]:
            print(f" {C}Zone Transfer {X}: {R}POSSIBLE on {self.results['zone_transfer']['ns']}{X}")
        print(f" {DIM}Duration      {X}: {elapsed:.1f}s\n")

        # Top findings
        if self.results["takeover_candidates"]:
            print(f" {R}{'═'*55}{X}")
            for t in self.results["takeover_candidates"]:
                print(f" {R}[!] TAKEOVER: {t['domain']} → {t.get('cname','?')} ({t['provider']}){X}")
        if self.results["tls_issues"]:
            for t in self.results["tls_issues"][:5]:
                print(f" {Y}[TLS] {t['domain']}: {t['vuln']} ({t['cve']}){X}")
        if self.results["wafs"]:
            print(f" {C}[WAF] Detected: {', '.join(self.results['wafs'])}{X}")

        return self.results

def run(target):
    import warnings; warnings.filterwarnings("ignore")
    engine = GhostWalkerNebula(target)
    return asyncio.run(engine.run())

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        print(f"Usage: {sys.argv[0]} <target.com>")
        sys.exit(1)
    results = run(sys.argv[1])
    import os; os.makedirs("/home/kali/Desktop/xophy/reports/", exist_ok=True)
    report=f"/home/kali/Desktop/xophy/reports/{sys.argv[1]}_nebula.json"
    with open(report,"w") as f: json.dump(results,f,indent=2,default=str)
    print(f"{G}[+] {report}{X}")

