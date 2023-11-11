from db_Illustrator_master import db_session_master
from db_Illustrator_master.main_db import Main_master


def add_main_master(drawing):
    master = Main_master()
    master.drawing = drawing
    db_sess = db_session_master.create_session()
    db_sess.add(master)
    db_sess.commit()
    db_sess.close()
