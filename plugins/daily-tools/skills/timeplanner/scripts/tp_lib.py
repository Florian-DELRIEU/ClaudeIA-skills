"""
tp_lib.py — Lecture et édition des sauvegardes Time Planner (Android).

Format : SQLite 3, user_version=13, schéma stable (déc. 2024 → juil. 2026+).
Toujours travailler sur une COPIE : la classe ouvre le fichier en écriture,
donc passer un chemin de travail, jamais l'upload d'origine.

Concepts clés du modèle :
- `entry` = table d'identité partagée. Tout objet planifiable (task, note,
  scheduled_activity, logged_activity, *_reminder) a un _id qui EST une ligne
  de `entry`, laquelle porte `pid` (catégorie parente).
  => Créer un objet impose de créer d'abord une `entry`.
  => Supprimer l'`entry` déclenche ON DELETE CASCADE sur tout le reste.
- Dates = timestamp Unix en MILLISECONDES.
- Couleurs = entier ARGB signé (style Android Color).
- category.archive_date_time = 0 → active ; sinon = date d'archivage (ms).
- note = texte enveloppé "<![CDATA[...]]>texte réel" (le CDATA porte le
  formatage rich-text ; le texte utile suit "]]>").
- logged_activity.value : measure 0/1 = durée en ms ; measure 2 = comptage entier.
- days_of_week = bitmask 7 bits (127 = tous les jours).
"""
import sqlite3
import shutil
import time
import datetime
import re

# ---------------------------------------------------------------- helpers date
def ms_to_dt(ms):
    """Timestamp ms -> datetime local. 0/None -> None."""
    if not ms or ms <= 0:
        return None
    return datetime.datetime.fromtimestamp(ms / 1000)

def ms_to_str(ms, fmt="%Y-%m-%d %H:%M"):
    dt = ms_to_dt(ms)
    return dt.strftime(fmt) if dt else "-"

def now_ms():
    return int(time.time() * 1000)

def day_start_ms(dt=None):
    """Minuit (local) du jour donné, en ms — format des task_accomplishment."""
    dt = dt or datetime.datetime.now()
    d = datetime.datetime(dt.year, dt.month, dt.day)
    return int(d.timestamp() * 1000)

# --------------------------------------------------------------- helpers divers
def argb_to_hex(n):
    """Entier ARGB signé -> '#RRGGBB'."""
    v = n & 0xFFFFFFFF
    r = (v >> 16) & 0xFF; g = (v >> 8) & 0xFF; b = v & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"

def hex_to_argb(hexstr, alpha=255):
    """'#RRGGBB' -> entier ARGB signé (comme stocké par l'appli)."""
    s = hexstr.lstrip("#")
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    v = (alpha << 24) | (r << 16) | (g << 8) | b
    return v - 0x100000000 if v >= 0x80000000 else v

_CDATA_RE = re.compile(r"^<!\[CDATA\[.*?\]\]>", re.DOTALL)

def note_text(raw):
    """Extrait le texte utile d'une note (retire le préfixe CDATA de formatage)."""
    if raw is None:
        return None
    return _CDATA_RE.sub("", raw)

def note_wrap(text):
    """Enveloppe un texte en note compatible appli (préfixe CDATA vide)."""
    if text is None:
        return None
    return "<![CDATA[\n\n\n\n\n\n]]>" + text

DAYS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

def days_of_week_str(mask):
    if mask == 127:
        return "tous les jours"
    return ",".join(d for i, d in enumerate(DAYS) if mask & (1 << i)) or "-"

PRIORITY_LABEL = {0: "aucune", 1: "basse", 2: "moyenne", 3: "haute"}


class TimePlanner:
    """Ouvre une base Time Planner. Utiliser open_copy() pour éditer sans risque."""

    def __init__(self, path):
        self.path = path
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row
        self.con.execute("PRAGMA foreign_keys=ON")

    @classmethod
    def open_copy(cls, src, dst):
        """Copie src->dst puis ouvre dst en écriture (ne touche jamais src)."""
        shutil.copy(src, dst)
        return cls(dst)

    def close(self):
        self.con.close()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

    # ---------------------------------------------------------------- LECTURE
    def q(self, sql, params=()):
        return [dict(r) for r in self.con.execute(sql, params).fetchall()]

    def summary(self):
        """Vue d'ensemble : compte par table + plage temporelle."""
        out = {}
        for t in ["category", "task", "task_accomplishment", "note",
                  "scheduled_activity", "logged_activity", "tag", "attachment",
                  "entry", "activity_reminder", "category_reminder"]:
            out[t] = self.con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        out["categories_actives"] = self.con.execute(
            "SELECT COUNT(*) FROM category WHERE archive_date_time=0").fetchone()[0]
        out["categories_archivees"] = self.con.execute(
            "SELECT COUNT(*) FROM category WHERE archive_date_time>0").fetchone()[0]
        out["taches_completees"] = self.con.execute(
            "SELECT COUNT(*) FROM task WHERE completed=1").fetchone()[0]
        out["taches_actives"] = self.con.execute(
            "SELECT COUNT(*) FROM task WHERE completed=0").fetchone()[0]
        mn, mx = self.con.execute(
            "SELECT MIN(creation_date_time),MAX(creation_date_time) "
            "FROM task WHERE creation_date_time>0").fetchone()
        out["premiere_tache"] = ms_to_str(mn)
        out["derniere_tache"] = ms_to_str(mx)
        return out

    def categories(self, include_archived=True):
        sql = ("SELECT _id,pos,name,color,icon_res,archive_date_time,note,"
               "creation_date_time FROM category")
        if not include_archived:
            sql += " WHERE archive_date_time=0"
        sql += " ORDER BY archive_date_time>0, pos, _id"
        rows = self.q(sql)
        for r in rows:
            r["color_hex"] = argb_to_hex(r["color"]) if r["color"] is not None else None
            r["archived"] = r["archive_date_time"] > 0
            r["note_text"] = note_text(r["note"])
        return rows

    def category_by_name(self, name):
        return self.q("SELECT * FROM category WHERE name=? COLLATE NOCASE", (name,))

    def tasks(self, pid=None, completed=None):
        sql = "SELECT _id,pid,pos,name,priority,completed,note,creation_date_time FROM task"
        cond, params = [], []
        if pid is not None:
            cond.append("pid=?"); params.append(pid)
        if completed is not None:
            cond.append("completed=?"); params.append(int(completed))
        if cond:
            sql += " WHERE " + " AND ".join(cond)
        sql += " ORDER BY pos, _id"
        rows = self.q(sql, params)
        for r in rows:
            r["priority_label"] = PRIORITY_LABEL.get(r["priority"], r["priority"])
            r["note_text"] = note_text(r["note"])
        return rows

    def scheduled(self, pid=None):
        sql = ("SELECT _id,pid,name,measure,type,start_date,start_time_or_part_of_day,"
               "end_date,repeat_unit,days_of_week,every_num,note FROM scheduled_activity")
        params = ()
        if pid is not None:
            sql += " WHERE pid=?"; params = (pid,)
        sql += " ORDER BY start_date"
        rows = self.q(sql, params)
        for r in rows:
            r["start"] = ms_to_str(r["start_date"], "%Y-%m-%d")
            r["days"] = days_of_week_str(r["days_of_week"])
        return rows

    def integrity(self):
        ic = self.con.execute("PRAGMA integrity_check").fetchone()[0]
        fk = self.con.execute("PRAGMA foreign_key_check").fetchall()
        uv = self.con.execute("PRAGMA user_version").fetchone()[0]
        return {"integrity_check": ic,
                "foreign_key_violations": [tuple(r) for r in fk],
                "user_version": uv}

    # ---------------------------------------------------------------- ÉDITION
    def _new_entry(self, pid):
        """Crée une ligne entry et renvoie son _id (obligatoire avant tout objet)."""
        cur = self.con.execute("INSERT INTO entry(pid) VALUES(?)", (pid,))
        return cur.lastrowid

    def add_task(self, pid, name, priority=0, note=None, pos=None):
        """Crée une tâche (entry + task). Renvoie l'_id.

        IMPORTANT : dans une catégorie, l'app range les tâches par bloc contigu
        de `pos` — actives d'abord (pos bas), terminées ensuite (pos haut). Une
        tâche active insérée après la fin de ce bloc s'affiche à tort dans la
        section « Terminé » même avec completed=0. Par défaut (pos=None), on
        insère donc juste après la dernière tâche ACTIVE et on décale de +1 le
        pos de toutes les tâches déjà à cette position ou après (donc les
        terminées) pour préserver l'invariant."""
        if pos is None:
            active_count = self.con.execute(
                "SELECT COUNT(*) FROM task WHERE pid=? AND completed=0",
                (pid,)).fetchone()[0]
            pos = active_count
            self.con.execute(
                "UPDATE task SET pos = pos + 1 WHERE pid=? AND pos >= ?",
                (pid, pos))
        _id = self._new_entry(pid)
        self.con.execute(
            "INSERT INTO task(_id,pid,pos,name,priority,completed,_offset,expanded,"
            "note,creation_date_time) VALUES(?,?,?,?,?,0,0,1,?,?)",
            (_id, pid, pos, name, priority, note_wrap(note) if note else None, now_ms()))
        return _id

    def complete_task(self, tid, done=True, when=None):
        """Marque une tâche complétée/non. Si complétée, insère un accomplishment
        daté (minuit du jour) comme le fait l'appli.

        Repositionne aussi `pos` pour respecter l'invariant de la catégorie
        (actives en bloc bas, terminées en bloc haut) — sinon la tâche reste
        affichée dans la mauvaise section malgré le bon statut `completed`."""
        row = self.con.execute("SELECT pid,completed FROM task WHERE _id=?",
                               (tid,)).fetchone()
        if row is None:
            return
        pid, was_done = row["pid"], row["completed"]
        self.con.execute("UPDATE task SET completed=? WHERE _id=?",
                         (1 if done else 0, tid))
        if done and not was_done:
            # déplacer en fin de bloc "terminé" (fin de catégorie)
            max_pos = self.con.execute(
                "SELECT COALESCE(MAX(pos),-1) FROM task WHERE pid=?",
                (pid,)).fetchone()[0]
            self.con.execute("UPDATE task SET pos=? WHERE _id=?", (max_pos + 1, tid))
        elif not done and was_done:
            # déplacer en fin de bloc "actif" (juste avant le premier terminé)
            active_count = self.con.execute(
                "SELECT COUNT(*) FROM task WHERE pid=? AND completed=0 AND _id!=?",
                (pid, tid)).fetchone()[0]
            self.con.execute(
                "UPDATE task SET pos = pos + 1 WHERE pid=? AND pos >= ? AND _id!=?",
                (pid, active_count, tid))
            self.con.execute("UPDATE task SET pos=? WHERE _id=?", (active_count, tid))
        if done:
            d = day_start_ms(when)
            exists = self.con.execute(
                "SELECT 1 FROM task_accomplishment WHERE tid=? AND date=?",
                (tid, d)).fetchone()
            if not exists:
                self.con.execute(
                    "INSERT INTO task_accomplishment(tid,date) VALUES(?,?)", (tid, d))

    def rename_task(self, tid, name):
        self.con.execute("UPDATE task SET name=? WHERE _id=?", (name, tid))

    def set_priority(self, tid, priority):
        self.con.execute("UPDATE task SET priority=? WHERE _id=?", (priority, tid))

    def set_task_note(self, tid, text):
        self.con.execute("UPDATE task SET note=? WHERE _id=?",
                         (note_wrap(text) if text else None, tid))

    def add_category(self, name, color_hex="#808080", icon_res="icl_tag", pos=None):
        """Crée une catégorie active. Renvoie l'_id."""
        if pos is None:
            pos = (self.con.execute(
                "SELECT COALESCE(MAX(pos),-1)+1 FROM category").fetchone()[0])
        cur = self.con.execute(
            "INSERT INTO category(pos,name,color,icon_res,_offset,expanded,"
            "creation_date_time,archive_date_time,task_list_expanded,merge_bubbles) "
            "VALUES(?,?,?,?,0,1,?,0,1,0)",
            (pos, name, hex_to_argb(color_hex), icon_res, now_ms()))
        return cur.lastrowid

    def archive_category(self, cid, archived=True, when=None):
        val = day_start_ms(when) if archived else 0
        self.con.execute("UPDATE category SET archive_date_time=? WHERE _id=?",
                         (val, cid))

    def delete_entry(self, _id):
        """Supprime un objet par son _id. Le CASCADE nettoie task/note/reminders/
        accomplishments/pins liés. Fonctionne pour task, note, scheduled, etc."""
        self.con.execute("DELETE FROM entry WHERE _id=?", (_id,))

    def delete_category(self, cid):
        """Supprime une catégorie ET tout son contenu (CASCADE via pid)."""
        self.con.execute("DELETE FROM category WHERE _id=?", (cid,))

    def commit(self):
        self.con.commit()

    def save_and_check(self):
        """Commit + rapport d'intégrité. À appeler avant de livrer le fichier."""
        self.commit()
        return self.integrity()
