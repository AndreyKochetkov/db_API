# -*- coding: utf-8 -*-
class Query:
    __sentence = ""

    def get(self):
        """return the sentence of query"""
        return self.__sentence

    def clear(self):
        """clear the sentence of query"""
        self.__sentence = ""

    def parse_args(self, data):
        columns = ""
        values = ""
        length = len(data)
        for i in xrange(0, length):
            columns += data[i][0]
            if isinstance(data[i][1], int):
                values += str(data[i][1])
            else:
                values += "\"" + str(data[i][1]) + "\""
            print (values)
            if i != length - 1:
                columns += ", "
                values += ", "
        return columns, values

    def add_insert(self, table, data):
        """Add INSERT section in query

        table - name of table
        data - list of tuples(!) of names of columns and their values

        """

        columns, values = self.parse_args(data)

        self.__sentence += "INSERT INTO {} ({}) VALUES ({});".format(
            table, columns, values
        )

    def add_select(self, table, columns):
        """Add SELECT section in query

                table - name of table
                columns - tuple of names of columns

        """
        columns_str = ""
        for column in columns:
            columns_str += column
        self.__sentence = "SELECT {} FROM {};".format(
            columns_str, table
        )

    def add_update(self, table, data):
        """
        :param table: таблица которую изменяем
        :param data: список со столбцами и значениями
        :return : none
        """
        columns, values = self.parse_args(data)

        self.__sentence = "UPDATE {} SET {} = {}".format(
            table, columns, values
        )

    def select_last_insert_id(self):
        """select last insert id"""
        self.clear()
        self.__sentence = "SELECT LAST_INSERT_ID();"

    def add_where_condition(self, condition):
        """Add SELECT section in query

            condition - string with the condition of WHERE part

        """
        if self.__sentence.endswith(';'):
            self.__sentence = self.__sentence[:-1]
        self.__sentence += " WHERE {};".format(condition)

    INSERT = 'INSERT {} ({}) VALUES ({});'
    DELETE = 'DELETE FROM {table} WHERE {clause};'
    SELECT = 'SELECT {columns} FROM {table} '
    JOIN = 'JOIN {table} ON {clause} '
    LEFT_JOIN = 'LEFT JOIN {table} ON {clause} '
    WHERE = 'WHERE {clause} '
    AND_CLAUSE = 'AND {clause} '
    ORDER_BY = 'ORDER BY {column} {type} '
    GROUP_BY = 'GROUP BY {column} '
    HAVING = 'HAVING {clause} '
    LIMIT = 'LIMIT {count} '
