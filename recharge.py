charge = None
with open("/var/www/html/wordpress/nowp/python/charge.txt", "r") as f:
    charge = int(f.read())
charge = charge + 2
with open("/var/www/html/wordpress/nowp/python/charge.txt", "w") as f:
    f.write(str(charge))
