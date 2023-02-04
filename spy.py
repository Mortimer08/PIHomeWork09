def log(data):
    file = open('db.csv', 'a')
    file.write(f'{" | ".join(data)}\n')
    file.close()

