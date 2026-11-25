"""Read records from a Fallout 4 plugin (.esm/.esp/.esl) directly, without xEdit.

    from esp import records, edid
    for sig, formid, subrecords in records(path, {'WEAP', 'OMOD'}):   # second argument: record types, or None
        print(sig, '%08X' % formid, edid(subrecords))

subrecords is a list of (signature, bytes). FormIDs are file-local. Localized names (FULL) are string-table indices.
Handles compressed records and XXXX oversize fields. Use `python3 -B`.
"""
import struct, zlib, mmap
def records(path, want=None):
    f=open(path,'rb'); m=mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    def walk(pos,end):
        while pos+24<=end:
            sig=m[pos:pos+4]; size=struct.unpack_from('<I',m,pos+4)[0]
            if sig==b'GRUP':
                label=m[pos+8:pos+12]; gtype=struct.unpack_from('<I',m,pos+12)[0]
                if not(want and gtype==0 and label.decode('latin1') not in want):
                    yield from walk(pos+24,pos+size)
                pos+=size; continue
            flags,fid=struct.unpack_from('<II',m,pos+8)
            data=m[pos+24:pos+24+size]
            if flags&0x40000: data=zlib.decompress(data[4:])
            yield sig.decode('latin1'),fid,subs(data)
            pos+=24+size
    yield from walk(0,len(m))
def subs(d):
    p=0;out=[];big=None
    while p+6<=len(d):
        s=d[p:p+4].decode('latin1'); n=struct.unpack_from('<H',d,p+4)[0]; p+=6
        if s=='XXXX': big=struct.unpack_from('<I',d,p)[0]; p+=n; continue
        if big is not None: n=big; big=None
        out.append((s,d[p:p+n])); p+=n
    return out
def edid(s):
    for k,v in s:
        if k=='EDID': return v.rstrip(b'\0').decode('latin1')
    return ''
