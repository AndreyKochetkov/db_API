username = "ff"
about = "fs"
name = "fa"
email = "gf"
strdd = 'INSERT {} ({}) VALUES ({});'.format('user', 'name, email, username, about',
                                             '{}, {}, {}, {}'.format(name, email, username, about))
print (strdd)