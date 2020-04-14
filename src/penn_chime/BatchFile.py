"""BarchFile

Create a BatchFile object.
"""

from collections import namedtuple
from datetime import date
from typing import Optional
import json

from .validators import (
    Positive, OptionalStrictlyPositive, StrictlyPositive, Rate, Date, OptionalDate
    )



Disposition = namedtuple("Disposition", ("rate", "days"))

class BatchFile:
    """Parameters."""

    def __init__(
        self,
        *,
        columnList:List = data.keys(),
        data : Dictionary = data,
        # icu: Disposition,
        # relative_contact_rate: float,
        # ventilated: Disposition,
        # current_date: date = date.today(),
        # date_first_hospitalized: Optional[date] = None,
        # doubling_time: Optional[float] = None,
        # infectious_days: int = 14,
        # market_share: float = 1.0,
        # max_y_axis: Optional[int] = None,
        # n_days: int = 100,
        # population: Optional[int] = None,
        # recovered: int = 0,
        # region: Optional[Regions] = None,
    ):

    def typeCheckInputs:
    for key in self.data.keys():
        try:
            if(data[key]=="int"):
                int(data[key])
            elif (data[key]=="Date"):
                datetime(data[key])
        except Exception as e:
            
        else:
            pass
        finally:
            pass
        if(data[key]=="int"):



        self.current_hospitalized = Positive(value=current_hospitalized)
        self.relative_contact_rate = Rate(value=relative_contact_rate)

        Rate(value=hospitalized.rate), Rate(value=icu.rate), Rate(value=ventilated.rate)
        StrictlyPositive(value=hospitalized.days), StrictlyPositive(value=icu.days),
        StrictlyPositive(value=ventilated.days)

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        if region is not None and population is None:
            self.region = region
            self.population = StrictlyPositive(value=region.population)
        elif population is not None:
            self.region = None
            self.population = StrictlyPositive(value=population)
        else:
            raise AssertionError('population or regions must be provided.')

        self.current_date = Date(value=current_date)
       
        self.date_first_hospitalized = OptionalDate(value=date_first_hospitalized)
        self.doubling_time = OptionalStrictlyPositive(value=doubling_time)

        self.infectious_days = StrictlyPositive(value=infectious_days)
        self.market_share = Rate(value=market_share)
        self.max_y_axis = OptionalStrictlyPositive(value=max_y_axis)
        self.n_days = StrictlyPositive(value=n_days)
        self.recovered = Positive(value=recovered)

        self.labels = {
            "hospitalized": "Hospitalized",
            "icu": "ICU",
            "ventilated": "Ventilated",
            "day": "Day",
            "date": "Date",
            "susceptible": "Susceptible",
            "infected": "Infected",
            "recovered": "Recovered",
        }

        self.dispositions = {
            "hospitalized": hospitalized,
            "icu": icu,
            "ventilated": ventilated,
        }
        with open('columnMapping.json') as f:
             data = json.load(f)
