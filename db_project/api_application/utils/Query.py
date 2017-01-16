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
                values += "\"" + data[i][1] + "\""
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
        self.__sentence = u"INSERT INTO {} ({}) VALUES ({})".format(
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
        self.__sentence = "SELECT {} FROM {}".format(
            columns_str, table
        )

    def add_update(self, table, data):
        """
        :param table: таблица которую изменяем
        :param data: список со столбцами и значениями
        :return : none
        """
        self.__sentence = "UPDATE {} SET {}".format(
            table, data
        )

    def add_delete(self, table):
        self.__sentence = "delete from {} ".format(table)

    def select_last_insert_id(self):
        self.clear()
        self.__sentence = "SELECT LAST_INSERT_ID()"

    def add_where_condition(self, condition):
        self.__sentence += " WHERE {}".format(condition)

    def add_more_where_condition(self, condition):
        self.__sentence += " and {}".format(condition)

    def add_left_join(self, table, condition):
        self.__sentence += " LEFT JOIN {} ON {} ".format(table, condition)

    def add_group_by(self, column):
        self.__sentence += " group by {}".format(column)

    def add_order_by(self, column, type):
        self.__sentence += " order by {} {}".format(column, type)

    def add_limit(self, limit):
        self.__sentence += " limit {}".format(limit)
