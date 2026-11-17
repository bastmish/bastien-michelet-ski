"""Deterministic route CSS compilation, with a bounded legacy compatibility bridge.
No browser is required for the build. Legacy source assets are never edited/deleted.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass,field
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,json,re
import tinycss2
from cssselect2.parser import parse as parse_selector
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]

@dataclass
class Rule:
    selector: str
    declarations: list
    context: tuple
    source: str
    line: int
    raw: str=''

def family(path):
    if path=='index.html':return 'home'
    if path=='manifesto.html':return 'collective'
    if path=='stations.html':return 'catalogue'
    if path=='destinations.html':return 'directory'
    if path=='404.html':return 'error'
    if path.startswith('stations/'):return 'destination'
    if path.startswith('legal/'):return 'legal'
    if path=='offres/index.html':return 'offer-index'
    if path in ['offres/ski-prive.html','offres/performance-technique.html','offres/freeride-decouverte.html','offres/snowboard.html']:return 'offer'
    return None

def color_key(value):
    value=value.lower()
    if value.startswith('#') and len(value) in [4,5]:value='#'+''.join(c*2 for c in value[1:])
    return value

def variable(name):return 'var(--ss-'+name+')'

def token_value(tokens,prop,registry):
    result=[]
    for t in tokens:
        text=tinycss2.serialize([t])
        if t.type=='hash':text=variable('color-'+registry['color_aliases'][color_key('#'+t.value)])
        elif t.type=='ident' and t.value.lower() in ['white','black','transparent']:
            key={'white':'#ffffff','black':'#000000','transparent':'transparent'}[t.value.lower()]
            text=variable('color-'+registry['color_aliases'][key])
        elif t.type=='function':
            if t.lower_name in ['rgb','rgba','hsl','hsla']:text=variable('color-'+registry['color_aliases'][color_key(text)])
            elif t.lower_name!='url':text=t.name+'('+token_value(t.arguments,prop,registry)+')'
        elif t.type=='dimension' and t.lower_unit=='px':
            val=t.representation+'px'
            if prop.startswith(('margin','padding')) or prop in ['gap','row-gap','column-gap','outline-offset']:
                text=variable(registry['space_aliases'][val])
            elif prop in ['font','font-size']:text=variable(registry['type_aliases'][val])
            elif prop in ['width','max-width','--width'] and t.value in [1320,1340]:text=variable('container-'+('content' if t.value==1320 else 'legacy'))
        result.append(text)
    text=''.join(result)
    if prop in ['font','font-family'] or prop in ['--font','--display','--ss-accent-type']:
        for literal,name in sorted(registry['font_aliases'].items(),key=lambda x:-len(x[0])):
            text=text.replace(literal,variable('font-'+name))
    if prop=='font-weight':
        key={'400':'regular','500':'medium','600':'semibold','700':'bold','800':'heavy'}.get(text.strip())
        if key:text=variable('weight-'+key)
    return text

def selectors(tokens):
    result=[];current=[]
    for t in tokens:
        if t.type=='literal' and t.value==',':
            result.append(tinycss2.serialize(current).strip());current=[]
        else:current.append(t)
    result.append(tinycss2.serialize(current).strip())
    return result

def parse_rules(text,source,registry,context=()):
    for name,query in registry['media'].items():text=text.replace('(--'+name+')',query)
    rules=[];imports=[]
    def walk(nodes,ctx):
        for n in nodes:
            if n.type=='error':raise ValueError(f'{source}:{n.source_line}: {n.message}')
            if n.type=='qualified-rule':
                ds=[d for d in tinycss2.parse_declaration_list(n.content,skip_comments=True,skip_whitespace=True) if d.type!='whitespace']
                if any(d.type!='declaration' for d in ds):raise ValueError(f'Unsupported declaration in {source}:{n.source_line}')
                for s in selectors(n.prelude):rules.append(Rule(s,[{'name':d.lower_name,'value':d.value,'important':d.important} for d in ds],ctx,source,n.source_line))
            elif n.type=='at-rule':
                prelude=tinycss2.serialize(n.prelude).strip()
                if n.lower_at_keyword=='import':imports.append('@import '+prelude+';')
                elif n.lower_at_keyword in ['media','supports','container'] and n.content:
                    if n.lower_at_keyword=='media' and prelude in registry['media_aliases']:prelude=registry['media'][registry['media_aliases'][prelude]]
                    walk(tinycss2.parse_rule_list(n.content,skip_comments=True,skip_whitespace=True),ctx+((n.lower_at_keyword,prelude),))
                else:rules.append(Rule('',[],ctx,source,n.source_line,tinycss2.serialize([n])))
    walk(tinycss2.parse_stylesheet(text,skip_comments=True,skip_whitespace=True),context)
    return rules,imports

def required_classes(tree):
    """Only necessary positive classes; deliberately do not infer :not/:is/:has states."""
    if hasattr(tree,'left'):return required_classes(tree.left)|required_classes(tree.right)
    out=set()
    for s in getattr(tree,'simple_selectors',[]):
        if type(s).__name__=='ClassSelector':out.add(s.class_name)
    return out

def impossible(selector,classes):
    try:
        parsed=list(parse_selector(selector))
        return bool(parsed) and all(required_classes(p.parsed_tree)-classes for p in parsed)
    except Exception:return False  # Unknown/vendor selectors are retained, never guessed away.

def property_group(name):
    if name.startswith('--'):return name
    for prefix in ['background','margin','padding','border','font','animation','transition','grid','flex','outline','text-decoration','list-style','columns','column-rule','inset']:
        if name==prefix or name.startswith(prefix+'-'):return prefix
    return name

def wrap(text,context):
    for name,query in reversed(context):text='@'+name+' '+query+'{'+text+'}'
    return text

def render(rules,registry,optimize,inline_groups):
    base=[];priority=[];retained=0;converted=0
    for r in rules:
        if r.raw:base.append(wrap(r.raw,r.context));continue
        normal=[];compat=[]
        for d in r.declarations:
            text=d['name']+':'+token_value(d['value'],d['name'],registry)
            if d['important']:
                if not optimize:normal.append(text+'!important');retained+=1
                elif property_group(d['name']) in inline_groups:compat.append(text+'!important');retained+=1
                else:compat.append(text);converted+=1
            else:normal.append(text)
        if normal:base.append(wrap(r.selector+'{'+ ';'.join(normal)+'}',r.context))
        if compat:priority.append(wrap(r.selector+'{'+ ';'.join(compat)+'}',r.context))
    if optimize:
        # This reproduces author importance without new !important. Inline-sensitive
        # property groups retain their original importance; no new priorities are added.
        text='@layer ss-legacy-base,ss-legacy-priority;\n@layer ss-legacy-base{\n'+'\n'.join(base)+'\n}\n@layer ss-legacy-priority{\n'+'\n'.join(priority)+'\n}\n'
    else:text='\n'.join(base)+'\n'
    return text,retained,converted

def tokens_css(registry):
    out=[]
    for category,prefix in [('colors','color'),('space',''),('type_size',''),('fonts','font'),('font_weights','weight'),('containers','container'),('aliases','')]:
        for name,value in registry[category].items():
            key=(prefix+'-' if prefix else '')+name;out.append('--ss-'+key+':'+value)
    return '/* Generated from styles/design-tokens.json; do not edit. */\n:root{'+ ';'.join(out)+'}\n'

def compile_css(public=ROOT/'public'):
    registry=json.loads((ROOT/'styles/design-tokens.json').read_text())
    config=json.loads((ROOT/'styles/entries.json').read_text());optimize=config['optimize']
    routes=defaultdict(list)
    for file in sorted(public.rglob('*.html')):
        group=family(str(file.relative_to(public)))
        if group:routes[group].append(file)
    output=public/'assets/css';output.mkdir(parents=True,exist_ok=True)
    previous=output/'manifest.json'
    if previous.exists():
        for name in json.loads(previous.read_text()).get('generated',[]):
            p=output/name
            if p.is_file():p.unlink()
    common=tokens_css(registry);common_name='tokens.'+hashlib.sha256(common.encode()).hexdigest()[:12]+'.css';(output/common_name).write_text(common)
    result={'schema':1,'optimized':optimize,'generated':[common_name],'routes':{},'entries':{}}
    for group,files in sorted(routes.items()):
        classes=set(config['runtime_classes']);inline_groups=set()
        for file in files:
            soup=BeautifulSoup(file.read_text(),'html.parser')
            for n in soup.select('[class]'):classes.update(n.get('class',[]))
            for n in soup.select('[style]'):
                for d in tinycss2.parse_declaration_list(n['style'],skip_comments=True,skip_whitespace=True):
                    if d.type=='declaration':inline_groups.add(property_group(d.lower_name))
        rules=[];imports=[]
        for source in config['entries'][group]:
            rr,ii=parse_rules((ROOT/source).read_text(),source,registry);rules+=rr;imports+=ii
        before={'rules':len(rules),'declarations':sum(len(r.declarations) for r in rules),'important':sum(d['important'] for r in rules for d in r.declarations)}
        removed=[];duplicates=[]
        if optimize:
            retained=[]
            for r in rules:
                if not r.raw and impossible(r.selector,classes):removed.append({'source':r.source,'line':r.line,'selector':r.selector})
                else:retained.append(r)
            rules=retained
            # Last declaration of the same selector/property/condition wins if its
            # importance is at least as high. Shorthands are never guessed equivalent.
            seen={}
            for r in reversed(rules):
                ds=[]
                for d in reversed(r.declarations):
                    key=(r.selector,r.context,d['name']);later=seen.get(key)
                    if later is not None and (later or not d['important']):duplicates.append({'source':r.source,'line':r.line,'selector':r.selector,'property':d['name']})
                    else:ds.append(d);seen[key]=d['important']
                r.declarations=list(reversed(ds))
        text,important,converted=render(rules,registry,optimize,inline_groups)
        text='/* Generated: '+group+'; sources: styles/entries.json. */\n'+'\n'.join(dict.fromkeys(imports))+'\n'+text
        name=group+'.'+hashlib.sha256(text.encode()).hexdigest()[:12]+'.css';(output/name).write_text(text);result['generated'].append(name)
        result['entries'][group]={'sources':config['entries'][group],'before':before,'after':{'declarations':sum(len(r.declarations) for r in rules),'important':important,'priority_bridge_declarations':converted},'removed_unreachable':removed,'removed_superseded':duplicates,'inline_sensitive_groups':sorted(inline_groups),'css':name}
        for file in files:
            path=str(file.relative_to(public));raw=file.read_text();inserted=False
            def replace(match):
                nonlocal inserted
                tag=match.group(0);soup=BeautifulSoup(tag,'html.parser');n=soup.find('link')
                if not n or 'stylesheet' not in n.get('rel',[]):return tag
                href=n.get('href','')
                if urlsplit(href).netloc:return tag
                if not inserted:
                    inserted=True
                    return '<link rel="stylesheet" href="/assets/css/'+common_name+'"><link rel="stylesheet" href="/assets/css/'+name+'">'
                return ''
            raw=re.sub(r'<link\b[^>]*>',replace,raw)
            if not inserted:raise ValueError('No CSS entry in '+path)
            file.write_text(raw);result['routes'][path]={'family':group,'stylesheets':[common_name,name]}
    previous.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result

if __name__=='__main__':
    report=compile_css();print('CSS:',len(report['routes']),'routes,',len(report['entries']),'isolated family entries; optimized=',report['optimized'])
