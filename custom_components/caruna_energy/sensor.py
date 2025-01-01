from datetime import date, datetime, timedelta
import logging
import math
from typing import Any, Dict, Optional

from dateutil.relativedelta import relativedelta
from carunaservice.api_response import MeasurementResponse
from carunaservice.api_exceptions import InvalidApiResponseException
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SCAN_INTERVAL,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
    STATE_UNAVAILABLE,
    UnitOfEnergy,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
)
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from .const import (
    CONF_DEFAULT_BASE_PRICE,
    CONF_DEFAULT_UNIT_PRICE,
    CONF_DELIVERY_SITE_ID,
    CONF_VAT,
    CONF_CONTRACT_TYPE,
    CONF_INCLUDE_TRANSFER_COSTS,
)
from carunaservice.price_client import CarunaPriceClient
from carunaservice.api_client import CarunaApiClient
from carunaservice.utils import get_month_date_range_by_date

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=3)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_VAT): cv.positive_float,
        vol.Required(CONF_CONTRACT_TYPE): cv.string,
        vol.Optional(CONF_DEFAULT_UNIT_PRICE): cv.positive_float,
        vol.Optional(CONF_DEFAULT_BASE_PRICE): cv.positive_float,
        vol.Optional(CONF_INCLUDE_TRANSFER_COSTS): cv.boolean,
        vol.Optional(CONF_DELIVERY_SITE_ID): cv.string,
    }
)