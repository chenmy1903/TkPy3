import pycodestyle

fchecker = pycodestyle.Checker(__file__)
file_errors = fchecker.check_all()

print('File name: {}\n'.format(fchecker.filename))
print("Found %s errors (and warnings)" % file_errors)

if file_errors:
    print('Errors:\n')
    for key, value in fchecker.counters.items():
        print(key, value, sep=": ")
