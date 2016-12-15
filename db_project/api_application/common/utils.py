def reset_increment(table):
    return "ALTER TABLE {} AUTO_INCREMENT = 1;".format(table)
