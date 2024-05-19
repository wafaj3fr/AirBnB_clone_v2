#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import models
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete-orphan", backref="state")

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        name = ''
        cities = []
        @property
        def cities(self):
            """ cities getter attribute """
            cities_list = []
            all_cities = models.storage.all(City)
            for city in all_cities:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
