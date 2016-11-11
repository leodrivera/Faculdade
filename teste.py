f1 = open("clientes.txt")
texto=f1.readlines()
print texto

usuario="Leo"

for i in range(len(texto)):
    if usuario+"\n" == texto[i]:
        print "linha",i