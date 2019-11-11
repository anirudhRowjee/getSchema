import configparser, mysql.connector, tabulate

def getConfig():
    config = configparser.ConfigParser()
    config.read('data.ini')
    data = {
        'username': config['database']['username'],
        'password': config['database']['password'],
        'host': config['database']['host'],
        'database': config['database']['database'],
    }

    return data

def connect_to_database(config):
    try:
        connection = mysql.connector.connect(
                    user= config['username'],
                    passwd= config['password'],
                    database= config['database'],
                    host= config['host']
        )
        print("Connection successful")
        return connection
    except mysql.connector.Error as err:
        print("Error ->  {error}".format(error=err))

def getDESCS(connection):
    # all tables from the database and DESC each of them
    cursor = connection.cursor()
    cursor.execute('show tables;')
    tables = [ x[0] for x in cursor.fetchall()]
    desc_dump = ''' '''
    template = '''
    << {table_name} >>

    {dump}

    '''
    for table in tables:
        cursor.execute("desc {current};".format(current=table))
        formatted_dump = tabulate.tabulate(cursor.fetchall(), tablefmt='grid')
        desc_dump += template.format(table_name=table, dump=formatted_dump)

    return desc_dump

def writedump(dump, filename):
    with open(filename, 'w+') as temp:
        temp.writelines(dump)
    print("Written successfully to {filename}".format(filename=filename))


if __name__ == '__main__':
    filename = input("enter full name of text file to write to >> ")
    conf = getConfig()
    cursor = connect_to_database(conf)
    dump = getDESCS(cursor)
    writedump(dump, filename)


