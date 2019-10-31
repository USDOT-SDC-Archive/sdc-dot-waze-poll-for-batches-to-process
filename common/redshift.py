import psycopg2

from common.logger_utility import *


class RedshiftConnection:

    def __init__(self, user, password, redshift_jdbc_url):
        endpoint_and_rest = redshift_jdbc_url.split('://')[1].split(':')
        endpoint = endpoint_and_rest[0]
        port_and_dbname = endpoint_and_rest[1].split('/')
        port = port_and_dbname[0]
        dbname = port_and_dbname[1]
        self.connection = psycopg2.connect(
            database=dbname,
            port=port,
            host=endpoint,
            password=password,
            user=user
        )
        self.connection.set_session(autocommit=True)
        self.cursor = self.connection.cursor()
        LoggerUtility.log_info("Established connection successfully")

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor


class RedshiftManager:

    def __init__(self, region_name, redshift_role_arn, redshift_connection, query_loader):
        self.region_name = region_name
        self.redshift_role_arn = redshift_role_arn
        self.redshift_connection = redshift_connection
        self.query_loader = query_loader

    def execute_from_file(self, file_name, **query_kwargs):
        LoggerUtility.log_info("Filename - {}, Role - {}".format(file_name, self.redshift_role_arn))
        query = self.query_loader.load_from_file(
            file_name,
            region_name=self.region_name,
            redshift_role_arn=self.redshift_role_arn,
            **query_kwargs
        )
        LoggerUtility.log_info("Query details - {}".format(query))
        LoggerUtility.log_info("Executing redshift copy command")
        return self.redshift_connection.execute(query)
