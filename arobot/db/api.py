import uuid

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from arobot.common import states
from arobot.common.config import CONF
from arobot.db import models


class API():

    def __init__(self):
        super(API, self).__init__()
        self._init_db_connect()

    def _init_db_connect(self):
        url = CONF.get('DEFAULT', 'db_connection')
        self.engine = sqlalchemy.create_engine(url)

    def get_ipmi_conf_by_sn(self, sn):
        session = sessionmaker(bind=self.engine)()
        ipmi_conf = session.query(models.IPMIConf).filter_by(
            sn=sn).one()
        session.close()
        return ipmi_conf

    def ipmi_conf_create(self, ipmi_conf):
        session = sessionmaker(bind=self.engine)()
        ipmi_id = str(uuid.uuid4())
        session.add(
            models.IPMIConf(
                id=ipmi_id,
                sn=ipmi_conf.get('sn'),
                state=states.IPMI_CONF_RAW
            )
        )
        session.commit()
        session.close()
        return ipmi_id

    def get_all_ipmi_raw(self):
        session = sessionmaker(bind=self.engine)()
        all_raws = session.query(models.IPMIConf).filter_by(
            state=states.IPMI_CONF_RAW).all()
        session.close()
        return all_raws

    def update_ipmi_conf_by_sn(self, sn, values):
        session = sessionmaker(bind=self.engine)()
        session.query(models.IPMIConf).filter_by(
            sn=sn).update(values)
        session.commit()
        session.close()

