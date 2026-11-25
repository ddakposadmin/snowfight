import os,sys
from PIL import Image
res=sys.argv[1]
src=Image.open('icon-512.png').convert('RGBA')
bg=src.getpixel((8,8))[:3]
dens={'mdpi':1,'hdpi':1.5,'xhdpi':2,'xxhdpi':3,'xxxhdpi':4}
for d,m in dens.items():
    for sub in (d+'-v4',d):
        p=os.path.join(res,'mipmap-'+sub)
        if os.path.isdir(p): break
    else:
        p=os.path.join(res,'mipmap-'+d); os.makedirs(p,exist_ok=True)
    s=int(48*m)
    ic=src.resize((s,s),Image.LANCZOS)
    ic.save(os.path.join(p,'ic_launcher.png'))
    # round
    mask=Image.new('L',(s*4,s*4),0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0,0,s*4-1,s*4-1),fill=255)
    mask=mask.resize((s,s),Image.LANCZOS)
    r=Image.new('RGBA',(s,s),(0,0,0,0)); r.paste(ic,(0,0),mask)
    r.save(os.path.join(p,'ic_launcher_round.png'))
    # adaptive foreground (108dp canvas, icon 80% centered)
    c=int(108*m); i=int(c*0.80)
    fg=Image.new('RGBA',(c,c),(0,0,0,0))
    fg.paste(src.resize((i,i),Image.LANCZOS),((c-i)//2,(c-i)//2))
    fg.save(os.path.join(p,'ic_launcher_foreground.png'))
vals=os.path.join(res,'values'); os.makedirs(vals,exist_ok=True)
open(os.path.join(vals,'ic_launcher_background.xml'),'w').write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#%02X%02X%02X</color>\n</resources>\n'%bg)
print('icons ok',bg)
