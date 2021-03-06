#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
import status_params

# server configurations
config = Script.get_config()

hive_metastore_user_name = config['configurations']['hive-site']['javax.jdo.option.ConnectionUserName']
hive_server_conf_dir = "/etc/hive/conf.server"
hive_jdbc_connection_url = config['configurations']['hive-site']['javax.jdo.option.ConnectionURL']

hive_metastore_user_passwd = config['configurations']['hive-site']['javax.jdo.option.ConnectionPassword']
hive_metastore_db_type = config['configurations']['global']['hive_database_type']

#users
hive_user = config['configurations']['global']['hive_user']
hive_lib = '/usr/lib/hive/lib/'
#JDBC driver jar name
hive_jdbc_driver = config['configurations']['hive-site']['javax.jdo.option.ConnectionDriverName']
if hive_jdbc_driver == "com.mysql.jdbc.Driver":
  jdbc_jar_name = "mysql-connector-java.jar"
elif hive_jdbc_driver == "org.postgresql.Driver":
  jdbc_jar_name = "postgresql-jdbc.jar"
elif hive_jdbc_driver == "oracle.jdbc.driver.OracleDriver":
  jdbc_jar_name = "ojdbc6.jar"

check_db_connection_jar_name = "DBConnectionVerification.jar"
check_db_connection_jar = format("/usr/lib/ambari-agent/{check_db_connection_jar_name}")

#common
hdp_stack_version = config['hostLevelParams']['stack_version']
hive_metastore_port = config['configurations']['global']['hive_metastore_port']
hive_var_lib = '/var/lib/hive'
hive_bin = '/usr/lib/hive/bin'
hive_server_host = config['clusterHostInfo']['hive_server_host'][0]
hive_server_port = 10000
hive_url = format("jdbc:hive2://{hive_server_host}:{hive_server_port}")

smokeuser = config['configurations']['global']['smokeuser']
smoke_test_sql = "/tmp/hiveserver2.sql"
smoke_test_path = "/tmp/hiveserver2Smoke.sh"
smoke_user_keytab = config['configurations']['global']['smokeuser_keytab']

_authentication = config['configurations']['core-site']['hadoop.security.authentication']
security_enabled = ( not is_empty(_authentication) and _authentication == 'kerberos')

kinit_path_local = functions.get_kinit_path([default("kinit_path_local",None), "/usr/bin", "/usr/kerberos/bin", "/usr/sbin"])
hive_metastore_keytab_path =  config['configurations']['hive-site']['hive.metastore.kerberos.keytab.file']

#hive_env
hive_conf_dir = "/etc/hive/conf"
hive_dbroot = config['configurations']['global']['hive_dbroot']
hive_log_dir = config['configurations']['global']['hive_log_dir']
hive_pid_dir = status_params.hive_pid_dir
hive_pid = status_params.hive_pid

#hive-site
hive_database_name = config['configurations']['global']['hive_database_name']

#Starting hiveserver2
start_hiveserver2_script = 'startHiveserver2.sh.j2'

hadoop_home = '/usr'

##Starting metastore
start_metastore_script = 'startMetastore.sh'
hive_metastore_pid = status_params.hive_metastore_pid
java_share_dir = '/usr/share/java'
driver_curl_target = format("{java_share_dir}/{jdbc_jar_name}")

hdfs_user =  config['configurations']['global']['hdfs_user']
user_group = config['configurations']['global']['user_group']
artifact_dir = "/tmp/HDP-artifacts/"

target = format("{hive_lib}/{jdbc_jar_name}")

jdk_location = config['hostLevelParams']['jdk_location']
driver_curl_source = format("{jdk_location}/{jdbc_jar_name}")

start_hiveserver2_path = "/tmp/start_hiveserver2_script"
start_metastore_path = "/tmp/start_metastore_script"

hive_aux_jars_path = config['configurations']['global']['hive_aux_jars_path']
hadoop_heapsize = config['configurations']['global']['hadoop_heapsize']
java64_home = config['hostLevelParams']['java_home']

##### MYSQL

db_name = config['configurations']['global']['hive_database_name']
mysql_user = "mysql"
mysql_group = 'mysql'
mysql_host = config['clusterHostInfo']['hive_mysql_host']

mysql_adduser_path = "/tmp/addMysqlUser.sh"

######## Metastore Schema
if str(hdp_stack_version).startswith('2.1') and \
    config['configurations']['global']['hive_database'] == 'New MySQL Database':
  init_metastore_schema = True
else:
  init_metastore_schema = False

########## HCAT

if str(hdp_stack_version).startswith('2.0'):
  hcat_conf_dir = '/etc/hcatalog/conf'
  hcat_lib = '/usr/lib/hcatalog/share/hcatalog'
# for newer versions
else:
  hcat_conf_dir = '/etc/hive-hcatalog/conf'
  hcat_lib = '/usr/lib/hive-hcatalog/share/hcatalog'


metastore_port = 9933

hcat_dbroot = hcat_lib

hcat_user = config['configurations']['global']['hcat_user']
webhcat_user = config['configurations']['global']['webhcat_user']

hcat_pid_dir = status_params.hcat_pid_dir
hcat_log_dir = config['configurations']['global']['hcat_log_dir']

hadoop_conf_dir = '/etc/hadoop/conf'

#hive-log4j.properties.template
if (('hive-log4j' in config['configurations']) and ('content' in config['configurations']['hive-log4j'])):
  log4j_props = config['configurations']['hive-log4j']['content']
else:
  log4j_props = None

#hive-exec-log4j.properties.template
if (('hive-exec-log4j' in config['configurations']) and ('content' in config['configurations']['hive-exec-log4j'])):
  log4j_exec_props = config['configurations']['hive-exec-log4j']['content']
else:
  log4j_exec_props = None

daemon_name = status_params.daemon_name

hive_hdfs_user_dir = format("/user/{hive_user}")
hive_hdfs_user_mode = 0700
hive_apps_whs_dir = config['configurations']['hive-site']["hive.metastore.warehouse.dir"]
#for create_hdfs_directory
hostname = config["hostname"]
hadoop_conf_dir = "/etc/hadoop/conf"
hdfs_user_keytab = config['configurations']['global']['hdfs_user_keytab']
hdfs_user = config['configurations']['global']['hdfs_user']
kinit_path_local = functions.get_kinit_path([default("kinit_path_local",None), "/usr/bin", "/usr/kerberos/bin", "/usr/sbin"])

# Tez libraries
tez_lib_uris = default("/configurations/tez-site/tez.lib.uris", None)
tez_local_api_jars = '/usr/lib/tez/tez*.jar'
tez_local_lib_jars = '/usr/lib/tez/lib/*.jar'
tez_user = config['configurations']['global']['tez_user']

# Hive security
hive_authorization_enabled = config['configurations']['hive-site']['hive.security.authorization.enabled']

import functools
#create partial functions with common arguments for every HdfsDirectory call
#to create hdfs directory we need to call params.HdfsDirectory in code
#create partial functions with common arguments for every HdfsDirectory call
#to create hdfs directory we need to call params.HdfsDirectory in code
HdfsDirectory = functools.partial(
  HdfsDirectory,
  conf_dir=hadoop_conf_dir,
  hdfs_user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local
)
