# Copyright (c) 2011 X.commerce, a business unit of eBay Inc.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Defines interface for DB access.

Functions in this module are imported into the ec2api.novadb namespace.
Call these functions from c2api.novadb namespace, not the c2api.novadb.api
namespace.

All functions in this module return objects that implement a dictionary-like
interface. Currently, many of these objects are sqlalchemy objects that
implement a dictionary interface. However, a future goal is to have all of
these objects be simple dictionaries.

"""

from eventlet import tpool
from oslo.config import cfg

from ec2api.openstack.common.db import api as db_api
from ec2api.openstack.common import log as logging


CONF = cfg.CONF
CONF.import_opt('use_tpool', 'ec2api.db.api',
                group='database')
CONF.import_opt('backend', 'ec2api.openstack.common.db.options',
                group='database')

_BACKEND_MAPPING = {'sqlalchemy': 'ec2api.novadb.sqlalchemy.api'}


class NovaDBAPI(object):
    """Nova's DB API wrapper class.

    This wraps the oslo DB API with an option to be able to use eventlet's
    thread pooling. Since the CONF variable may not be loaded at the time
    this class is instantiated, we must look at it on the first DB API call.
    """

    def __init__(self):
        self.__db_api = None

    @property
    def _db_api(self):
        if not self.__db_api:
            nova_db_api = db_api.DBAPI(CONF.database.backend,
                                       backend_mapping=_BACKEND_MAPPING)
            if CONF.database.use_tpool:
                self.__db_api = tpool.Proxy(nova_db_api)
            else:
                self.__db_api = nova_db_api
        return self.__db_api

    def __getattr__(self, key):
        return getattr(self._db_api, key)


IMPL = NovaDBAPI()

LOG = logging.getLogger(__name__)

# The maximum value a signed INT type may have
MAX_INT = 0x7FFFFFFF

####################


def s3_image_get(context, image_id):
    """Find local s3 image represented by the provided id."""
    return IMPL.s3_image_get(context, image_id)


def s3_image_get_by_uuid(context, image_uuid):
    """Find local s3 image represented by the provided uuid."""
    return IMPL.s3_image_get_by_uuid(context, image_uuid)


def s3_image_create(context, image_uuid):
    """Create local s3 image represented by provided uuid."""
    return IMPL.s3_image_create(context, image_uuid)


###################


def get_ec2_volume_id_by_uuid(context, volume_id):
    return IMPL.get_ec2_volume_id_by_uuid(context, volume_id)


def get_volume_uuid_by_ec2_id(context, ec2_id):
    return IMPL.get_volume_uuid_by_ec2_id(context, ec2_id)


def ec2_volume_create(context, volume_id, forced_id=None):
    return IMPL.ec2_volume_create(context, volume_id, forced_id)


def get_snapshot_uuid_by_ec2_id(context, ec2_id):
    return IMPL.get_snapshot_uuid_by_ec2_id(context, ec2_id)


def get_ec2_snapshot_id_by_uuid(context, snapshot_id):
    return IMPL.get_ec2_snapshot_id_by_uuid(context, snapshot_id)


def ec2_snapshot_create(context, snapshot_id, forced_id=None):
    return IMPL.ec2_snapshot_create(context, snapshot_id, forced_id)


###################


def get_ec2_instance_id_by_uuid(context, instance_id):
    """Get ec2 id through uuid from instance_id_mappings table."""
    return IMPL.get_ec2_instance_id_by_uuid(context, instance_id)


def get_instance_uuid_by_ec2_id(context, ec2_id):
    """Get uuid through ec2 id from instance_id_mappings table."""
    return IMPL.get_instance_uuid_by_ec2_id(context, ec2_id)


def ec2_instance_create(context, instance_uuid, id=None):
    """Create the ec2 id to instance uuid mapping on demand."""
    return IMPL.ec2_instance_create(context, instance_uuid, id)


def ec2_instance_get_by_uuid(context, instance_uuid):
    return IMPL.ec2_instance_get_by_uuid(context, instance_uuid)


def ec2_instance_get_by_id(context, instance_id):
    return IMPL.ec2_instance_get_by_id(context, instance_id)


def instance_get_by_uuid(context, uuid, columns_to_join=None, use_slave=False):
    """Get an instance or raise if it does not exist."""
    return IMPL.instance_get_by_uuid(context, uuid,
                                     columns_to_join, use_slave=use_slave)


def block_device_mapping_get_all_by_instance(context, instance_uuid,
                                             use_slave=False):
    """Get all block device mapping belonging to an instance."""
    return IMPL.block_device_mapping_get_all_by_instance(context,
                                                         instance_uuid,
                                                         use_slave)