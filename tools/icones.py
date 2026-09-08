"""Icones de BOUK : un B en laiton sur tapis de jeu, un coeur et un pique.
   Les enseignes sont dessinees (pas des caracteres) pour rendre partout.
   Usage : python3 tools/icones.py web <dossier>
           python3 tools/icones.py android <dossier res>
   (c) 2026 Hacen AHMED BENANE. Tous droits reserves."""
import os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SERIF='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FELT2=(15,66,56); BRASS=(201,155,74); CREAM=(241,232,214); RED=(200,90,74)

def font(p,s):
    for q in (p,SANS):
        if os.path.exists(q): return ImageFont.truetype(q,s)
    return ImageFont.load_default()

def fond(w,h=None):
    h = h or w
    img=Image.new('RGB',(w,h),FELT2); d=ImageDraw.Draw(img)
    cx,cy=w//2,int(h*0.42); r=int(max(w,h)*0.62)
    for i in range(r,0,-max(1,r//90)):
        t=i/r
        c=(int(FELT2[0]+(44-FELT2[0])*(1-t)),int(FELT2[1]+(115-FELT2[1])*(1-t)),int(FELT2[2]+(100-FELT2[2])*(1-t)))
        d.ellipse([cx-i,cy-i,cx+i,cy+i],fill=c)
    return img.filter(ImageFilter.GaussianBlur(max(1,w//60)))

def coeur(d,cx,cy,s,col):
    r=s*0.29
    d.ellipse([cx-s*0.50,cy-s*0.50,cx-s*0.50+2*r,cy-s*0.50+2*r],fill=col)
    d.ellipse([cx+s*0.50-2*r,cy-s*0.50,cx+s*0.50,cy-s*0.50+2*r],fill=col)
    d.polygon([(cx-s*0.50,cy-s*0.30),(cx+s*0.50,cy-s*0.30),(cx,cy+s*0.52)],fill=col)

def pique(d,cx,cy,s,col):
    d.polygon([(cx,cy-s*0.58),(cx-s*0.52,cy+s*0.18),(cx+s*0.52,cy+s*0.18)],fill=col)
    r=s*0.24
    for sg in (-1,1):
        ox=cx+sg*s*0.30; oy=cy+s*0.14
        d.ellipse([ox-r,oy-r,ox+r,oy+r],fill=col)
    d.polygon([(cx-s*0.09,cy+s*0.26),(cx+s*0.09,cy+s*0.26),(cx+s*0.21,cy+s*0.58),(cx-s*0.21,cy+s*0.58)],fill=col)

def marque(img,n,scale=1.0):
    d=ImageDraw.Draw(img)
    f=font(SERIF,int(n*0.58*scale))
    bb=d.textbbox((0,0),'B',font=f); tw,th=bb[2]-bb[0],bb[3]-bb[1]
    d.text((n/2-tw/2-bb[0], n*0.42-th/2-bb[1]),'B',font=f,fill=BRASS)
    s=n*0.175*scale; ec=n*0.145*scale; y=n*0.795
    coeur(d, n/2-ec, y, s, RED)
    pique(d, n/2+ec, y, s, CREAM)

def arrondi(n,r):
    m=Image.new('L',(n,n),0); ImageDraw.Draw(m).rounded_rectangle([0,0,n-1,n-1],radius=r,fill=255); return m
def cercle(n):
    m=Image.new('L',(n,n),0); ImageDraw.Draw(m).ellipse([0,0,n-1,n-1],fill=255); return m

def icone(n, scale=0.92, masque='arrondi'):
    img=fond(n).convert('RGBA'); marque(img,n,scale)
    if masque is None: return img.convert('RGB')
    m = arrondi(n,int(n*0.22)) if masque=='arrondi' else cercle(n)
    out=Image.new('RGBA',(n,n),(0,0,0,0)); out.paste(img,(0,0),m)
    return out

def pour_le_web(dest):
    for n in (180,192,512):
        icone(n).save(os.path.join(dest,'icon-%d.png'%n))
    icone(512, scale=0.66, masque=None).save(os.path.join(dest,'icon-maskable-512.png'))
    print('icones web ecrites dans', dest)

def pour_android(res):
    for f in sorted(glob.glob(res+'/mipmap-*/ic_launcher.png')):
        n=Image.open(f).size[0]
        icone(n).save(f)
        icone(n, masque='cercle').save(f.replace('ic_launcher.png','ic_launcher_round.png'))
    for f in sorted(glob.glob(res+'/mipmap-*/ic_launcher_foreground.png')):
        n=Image.open(f).size[0]
        img=Image.new('RGBA',(n,n),(0,0,0,0)); marque(img,n,0.62); img.save(f)
    for f in sorted(glob.glob(res+'/drawable*/splash.png')):
        w,h=Image.open(f).size
        img=fond(w,h).convert('RGB'); d=ImageDraw.Draw(img)
        taille=int(min(w,h)*0.20); fw=font(SERIF,taille)
        bb=d.textbbox((0,0),'BOUK',font=fw); tw,th=bb[2]-bb[0],bb[3]-bb[1]
        d.text((w/2-tw/2-bb[0], h/2-th/2-bb[1]-h*0.04),'BOUK',font=fw,fill=CREAM)
        s=taille*0.30; y=h/2+th*0.85
        coeur(d, w/2-taille*0.42, y, s, RED)
        pique(d, w/2+taille*0.42, y, s, CREAM)
        img.save(f)
    bgx=res+'/values/ic_launcher_background.xml'
    if os.path.exists(bgx):
        open(bgx,'w').write('<?xml version="1.0" encoding="utf-8"?>' + chr(10) + '<resources>' + chr(10) +
                            '    <color name="ic_launcher_background">#17564A</color>' + chr(10) + '</resources>' + chr(10))
    print('icones android ecrites dans', res)

if __name__=='__main__':
    quoi = sys.argv[1] if len(sys.argv)>1 else 'web'
    dest = sys.argv[2] if len(sys.argv)>2 else '.'
    (pour_le_web if quoi=='web' else pour_android)(dest)
