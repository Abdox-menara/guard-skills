import sqlite3, time, hashlib, json
from collections import OrderedDict

class TwoTierCache:
    def __init__(s, db="cache.db"):
        s.l1 = OrderedDict()
        s.stats = {"l1": 0, "l2": 0, "miss": 0}
        s.db = db
        s.conn = sqlite3.connect(db, check_same_thread=False)
        s.conn.execute("CREATE TABLE IF NOT EXISTS cache (k TEXT PRIMARY KEY, v TEXT, ts REAL, ttl REAL)")
        s.conn.commit()
    
    def get(s, k):
        if k in s.l1:
            e = s.l1[k]
            if time.time()-e[1] < e[2]:
                s.stats["l1"] += 1
                return e[0]
            del s.l1[k]
        r = s.conn.execute("SELECT v,ts,ttl FROM cache WHERE k=?", (k,)).fetchone()
        if r and time.time()-r[1] < r[2]:
            v = json.loads(r[0])
            s.stats["l2"] += 1
            return v
        s.stats["miss"] += 1
        return None
    
    def put(s, k, v, ttl=3600):
        if len(s.l1) >= 1000: s.l1.popitem(last=False)
        s.l1[k] = (v, time.time(), ttl)
        s.conn.execute("INSERT OR REPLACE INTO cache VALUES (?,?,?,?)", (k, json.dumps(v), time.time(), ttl))
        s.conn.commit()
    
    def clear(s):
        s.l1.clear()
        s.conn.execute("DELETE FROM cache")
        s.conn.commit()
    
    def size(s):
        return len(s.l1) + s.conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
