from typing import List

from ..models import Farm
from ....utils import DatabaseUtils


class FarmHandler:
    @staticmethod
    @DatabaseUtils.db_transaction
    def get_all(session) -> List[Farm] | None:
        return session.query(Farm).all()

    @staticmethod
    @DatabaseUtils.db_transaction
    def get(session, farm_id: int) -> Farm | None:
        return session.query(Farm).filter(Farm.id == farm_id).one_or_none()

    @staticmethod
    @DatabaseUtils.db_transaction
    def create(session, coconut_id: int = 1, technology_id: int = 1) -> Farm:
        farm = Farm(coconut=coconut_id, technology=technology_id)
        session.add(farm)
        session.commit()
        session.refresh(farm)
        return farm

    @staticmethod
    @DatabaseUtils.db_transaction
    def update(session, farm_id: int, data: dict) -> Farm | None:
        farm = session.query(Farm).filter(Farm.id == farm_id).one_or_none()
        if farm:
            for key, value in data.items():
                if key == 'coconut' and isinstance(value, dict):
                    if 'id' in value:
                        setattr(farm, 'coconut', value['id'])
                elif key == 'technology' and isinstance(value, dict):
                    if 'id' in value:
                        setattr(farm, 'technology', value['id'])
                else:
                    setattr(farm, key, value)
            session.commit()
            session.refresh(farm)
        return farm

    @staticmethod
    @DatabaseUtils.db_transaction
    def update_all_farms(session) -> int:
        farms = session.query(Farm).all()
        updated_farms = 0

        for farm in farms:
            if farm.coconuts_count > 0:
                coconut = farm.coconut_relation
                technology = farm.technology_relation

                new_coconuts = technology.multiplier * farm.coconuts_count * coconut.amount_per_hour
                if new_coconuts + farm.uncollected <= coconut.amount_per_hour * farm.coconuts_count * technology.multiplier * 8:
                    farm.uncollected += new_coconuts
                    updated_farms += 1

        session.commit()
        return updated_farms
