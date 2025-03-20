
DBT-spark (Local):
------------------

Requirement:
------------

    - Python
    - Java
    - Spark installation
    - dbt

Setup:
------

    -	Install python 
            >> sudo apt install python[version number]
            >> sudo apt install python3-pip
    -   Install Java 
            >> sudo apt install default-jdk
            >> sudo apt-get install libkrb5-dev krb5-user
    -   Install Spark
        . https://www.apache.org/dyn/closer.lua/spark/spark-3.4.4/spark-3.4.4-bin-hadoop3.tgz
        . vi $HOME/.bashrc 
            >  Set SPARK_HOME, JAVA_HOME, SCALA_HOME, PATH
            . Ex:
                export SPARK_HOME="/usr/lib/spark/spark-3.5.3-bin-hadoop3"
                export PATH=$PATH:/usr/lib/spark/spark-3.5.3-bin-hadoop3/bin
        . source $HOME/.bashrc
    -	Python/python3 -m venv <env_name>
    -	touch $HOME/.dbt/profiles.yml (or) touch ~/.dbt/profile.yml
    -	source ./<venv path>/bin/activate
    -	pip install dbt-core dbt-spark 'dbt-spark[PyHive]'
    -	mkdir <folder-name>
    -	cd <folder-name>
    -	dbt init
    -	> app_name
        > Choose Spark
        > Choose thrift 
        > host : localhost 
        > port : 10000

        Commands:
            - dbt debug (in console)
            - dbt compile (to see the actual model code)
            - dbt show (to see the sample result)
            - dbt run (to execute the model)
            - dbt run --select <model-name>


Start local spark Thrift server:
--------------------------------

    blog : - https://medium.com/@omidvd/how-to-connect-via-jdbc-to-spark-sql-emr-on-aws-517f5a039e7d

    Note: 
        - Change the below as per the version of spark and location
            change > spark.sql.warehouse.dir
            change version > org.apache.spark, spark-hive

    spark-submit \
    --master 'local[*]' \
    --conf spark.executor.extraJavaOptions=-Duser.timezone=Etc/UTC \
    --conf spark.eventLog.enabled=false \
    --conf spark.sql.warehouse.dir=/usr/lib/spark/spark-3.5.3-bin-hadoop3/sparkwarehouse \
    --packages 'org.apache.spark:spark-sql_2.12:3.5.3,org.apache.spark:spark-hive_2.12:3.4.0' \
    --class org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 \
    --name "Thrift JDBC/ODBC Server" \
    --executor-memory 512m

    beeline -u jdbc:hive2://localhost:10000/default

    CREATE EXTERNAL TABLE IF NOT EXISTS example_s3_table (session STRING, aid STRING, type STRING)
    COMMENT 'My S3 table'
    STORED AS PARQUET
    LOCATION '/usr/lib/spark/spark-3.5.3-bin-hadoop3/sparkwarehouse/sesion/data/';


Emr-spark-thrift server config Setup:
-------------------------------------

Access EMR using SSH:
---------------------
    https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-connect-master-node-ssh.html

    - Create EMR service in AWS
    - While creating the EMR add the step below to start thrift server

        <!-- 
        Add step in EMR cluster:
        Jar : common-runner.jar
        command : sudo /usr/lib/spark/sbin/start-thriftserver.sh --master yarn-client 
        -->

    - Copy pem into ~/.ssh/secret_key.pem
    - chmod 400 ~/.ssh/secret_key.pem
    - Need to enable Inbound network traffic with port 22
        . https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-connect-ssh-prereqs.html
    
    - GET EC2 public DNS : <EC2-ip>.compute-1.amazonaws.com
    - Run ubuntu cli > ssh -i "~/.ssh/secret_key.pem" ec2-user@<EC2-ip>.compute-1.amazonaws.com
    - vi ~/.bashrc
        . insert button
        . Add the below two
            export SPARK_HOME="/usr/lib/spark"
            export PATH=$PATH:/usr/lib/spark/bin
        . esc button > :wq

    - start thrift server:

        <!-- 
            Change the package version as per the installation

            to check > cd /usr/lib/spark/jars > ls

            spark-sql_2.12:3.5.4 
            spark-hive_2.12:3.5.4
        !-->

        spark-submit \
        --master 'local[*]' \
        --conf spark.executor.extraJavaOptions=-Duser.timezone=Etc/UTC \
        --conf spark.eventLog.enabled=false \
        --conf spark.sql.warehouse.dir=/usr/lib/spark/data \
        --packages 'org.apache.spark:spark-sql_2.12:3.5.4,org.apache.spark:spark-hive_2.12:3.5.4' \
        --class org.apache.spark.sql.hive.thriftserver.HiveThriftServer2 \
        --name "Thrift JDBC/ODBC Server" \
        --executor-memory 512m

        beeline -u jdbc:hive2://localhost:10001/default
    
    - Port forwarding in order to use EMR-spark-thrift server locally so that DBT-core can be work with s3.
        > ssh -i ~/.ssh/secret_key.pem -N -L 10000:<EC2-ip>.compute-1.amazonaws.com:10000 hadoop@<EC2-ip>.compute-1.amazonaws.com

        > Syntax: beeline -n username -p password -u jdbc:hive2://hs2.local:10012
            > beeline -n hadoop -u  jdbc:hive2://localhost:10000/vehicle_poc

    
        In Beeline >> 
            CREATE DATABASE s3_database LOCATION 's3://aws-logs-537124954106-us-east-1/elasticmapreduce/j-3A8MYQIDHTLMW/sample_data/';

            CREATE EXTERNAL TABLE IF NOT EXISTS example_s3_table (session STRING, aid STRING, type STRING)
            COMMENT 'My S3 table'
            STORED AS PARQUET
            LOCATION 's3://aws-logs-537124954106-us-east-1/elasticmapreduce/j-3A8MYQIDHTLMW/sample_data/';

            INSERT OVERWRITE DIRECTORY 's3://'
            ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            SELECT * FROM <table-name>;

    DBT Execution:
    --------------
    Create Macro for DDL and DML statement 
    >> factory.sql

        {% macro <macro-name> %}

            {% set <var-name> %}
                -- query
            {% endset %}

            {% if execute %}
                {% do run_query(<var-name>) %}
            {% endif %}

        {% endmacro%}

    >> dbt run-operation <macro-name> --args '{<arg-name : value, arg-name : value>}'


Create external table from s3 and write back to s3:
---------------------------------------------------

    Read data from CSV file and store it as CSV:
    ---------------------------------------------

        CREATE external TABLE if not exists s3_dbt.bronze (
            VIN string, County string, City string, State string, Postal_Code integer, 
            Model_Year integer, Make string, Model string, Electric_Vehicle_Type string, 
            Clean_Alternative_Fuel_Vehicle string, Electric_Range integer, Base_MSRP integer, 
            Legislative_District integer, DOL_Vehicle_ID integer, Vehicle_Location string, 
            Electric_Utility string, Census_Tract float
        )
            ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
            WITH SERDEPROPERTIES (
            'separatorChar' = ','
        )
        STORED AS TEXTFILE
        LOCATION 's3://dev-mdf-data-lake/dbt-spark-emr-poc/data/bronze/'
        TBLPROPERTIES (
        'serialization.null.format' = '',
        'skip.header.line.count' = '1');


        insert overwrite directory 's3://dev-mdf-data-lake/dbt-spark-emr-poc/data/silver/'
        row format delimited
        fields terminated by ','
        select * from s3_dbt.bronze where make not in ("LEXUS", "MITSUBISHI", "RAM");

    Read data from Parquet file and store it as Parquet:
    ----------------------------------------------------

        INSERT OVERWRITE DIRECTORY 's3://dev-mdf-data-lake/dbt-spark-emr-poc/data/parquet_test/'
        select *, 
            sum(cnt) over(partition by model_year order by model_year rows unbounded preceding) as cons_sum
        from (select make, model_year, count(make) as cnt from s3_dbt.silver group by model_year, make order by make
        ) as tb1;


        CREATE EXTERNAL TABLE if not exists s3_dbt.parquet_test (
            make string,
            model_year int,
            cnt int, 
            cons_sum int
        )
        LOCATION 's3://dev-mdf-data-lake/dbt-spark-emr-poc/data/parquet_test/';





